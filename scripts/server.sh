#!/usr/bin/env bash
#TODO: remove or make tag false when terminating -- optional
#TODO: possibly do not need to pass the stackName
#TODO: think about the need to pass the autoscaling group
#TODO: Handle alternate address especially if the public IP is not available.  Right now only using private ips.
echo "Running server.sh"

adminUsername=$1
adminPassword=$2
services=$3
stackName=$4
version=$5

echo "Got the parameters:"
echo adminUsername \'"$adminUsername"\'
echo adminPassword \'"$adminPassword"\'
echo services \'"$services"\'
echo stackName \'"$stackName"\'
echo version \'"$version"\'

#######################################################"
############## Install Couchbase Server ###############"
#######################################################"
echo "Installing Couchbase Server..."

wget https://packages.couchbase.com/releases/"${version}"/couchbase-server-enterprise-"${version}"-amzn2.x86_64.rpm
rpm --install couchbase-server-enterprise-"${version}"-amzn2.x86_64.rpm

source util.sh

echo "Turning off transparent huge pages"
turnOffTransparentHugepages

echo "Setting swappiness to 0..."
setSwappinessToZero

echo "Formatting disk"
formatDataDisk
sudo yum -y update
#yum -y install jq #TODO: May need jq later
#All servers that join the cluster successfully can allow others to be added the cluster using server-add.
#Initially there is one pre-defined rally server when the cluster is being initialized which is chosen based on the earliest LaunchTime node.

region=$(getRegion)
instanceId=$(getInstanceId)
nodePrivateDNS=$(curl http://169.254.169.254/latest/meta-data/local-hostname)
rallyPrivateDNS="$nodePrivateDNS" #Defaulting to this node but it will be overwritten (possibly with the same value) later 
nodePublicDNS=$(curl http://169.254.169.254/latest/meta-data/public-hostname) 
rallyPublicDNS="$nodePublicDNS" #Defaulting to this node but it will be overwritten (possibly with the same value) later
rallyInstanceId=$(getRallyInstanceId)
rallyFlag=$?
if [[ $rallyFlag -eq 0 ]] #exit 0 means it is the rally server (i.e. cluster initializing node)
then
  if [[ "$rallyInstanceId" == "$instanceId" ]] #If true this server is the cluster creator
  then
    echo "This node is the cluster creator"
    rallyPrivateDNS="$nodePrivateDNS" 
    rallyPublicDNS="$nodePublicDNS"
  else
    #Found a rally but this node is not the rally
    rallyFlag=1
    DNSResult=$(getDNS "$rallyInstanceId") 
    DNSFlag=$?
    if [[ $? -eq 0 ]]
    then
      read -a DNSarr <<< "$DNSResult"  # privateDNS [0] publicDNS [1]
    else
      echo "Can't continue because DNS can't be retrieved."
      exit 1
    fi
    rallyPrivateDNS=${DNSarr[0]}
    rallyPublicDNS=${DNSarr[1]}
  fi
else
  rallyInstanceId=$(getClusterInstance) #Any cluster with the $CB_RALLY_TAG tag
  DNSResult=$(getDNS "$rallyInstanceId") 
  DNSFlag=$?
  if [[ "$DNSFlag" -eq 0 ]]
  then
    read -a DNSarr <<< "$DNSResult"  # privateDNS [0] publicDNS [1]
  else
    echo "Can't continue because DNS can't be retrieved."
    exit 1
  fi
  rallyPrivateDNS=${DNSarr[0]}
  rallyPublicDNS=${DNSarr[1]} 
fi

echo "Using the settings:"
echo adminUsername \'"$adminUsername"\'
echo adminPassword \'"$adminPassword"\'
echo services \'"$services"\'
echo stackName \'"$stackName"\'
echo rallyPrivateDNS \'"$rallyPrivateDNS"\'
echo rallyPublicDNS \'"$rallyPublicDNS"\'
echo region \'"$region"\'
echo instanceId \'"$instanceId"\'
echo nodePublicDNS \'"$nodePublicDNS"\'
echo nodePrivateDNS \'"$nodePrivateDNS"\'
echo rallyFlag \'$rallyFlag\'
echo rallyInstanceId \'"$rallyInstanceId"\'

echo "Switching to couchbase installation directory"
cd /opt/couchbase/bin/ || exit

echo "Running couchbase-cli node-init"
output=""
while [[ ! $output =~ "SUCCESS" ]]
do
  #TODO: Handle different services and their folders based on the running services
  output=$(./couchbase-cli node-init \
    --cluster="$nodePublicDNS" \
    --node-init-hostname="$nodePublicDNS" \
    --node-init-data-path=/mnt/datadisk/data \
    --node-init-index-path=/mnt/datadisk/index \
    -u="$adminUsername" \
    -p="$adminPassword")
  echo node-init output \'"$output"\'
  sleep 10
done

if [[ $rallyFlag -eq 0 ]] #Rally
then
  echo "Creating node tag for Rally (cluster initialization) Node Name"
  aws ec2 create-tags \
  --region "${region}" \
  --resources "${rallyInstanceId}" \
  --tags Key=Name,Value="${stackName}"-ServerRally

  totalRAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  dataRAM=$((40 * $totalRAM / 100000))
  indexRAM=$((8 * $totalRAM / 100000))

  ./couchbase-cli cluster-init \
    --cluster="$rallyPublicDNS" \
    --cluster-username="$adminUsername" \
    --cluster-password="$adminPassword" \
    --cluster-ramsize=$dataRAM \
    --cluster-index-ramsize=$indexRAM \
    --cluster-analytics-ramsize=$indexRAM \
    --cluster-fts-ramsize=$indexRAM \
    --cluster-eventing-ramsize=$indexRAM \
    --index-storage-setting=memopt \
    --services="${services}"

  setCBRallyTag
  setCBClusterTag
else
  echo "Creating node tag for Node Name"
  aws ec2 create-tags \
    --region "${region}" \
    --resources "${instanceId}" \
    --tags Key=Name,Value="${stackName}"-Server
  echo "Running couchbase-cli server-add"
  output=""
  while [[ $output != "Server $nodePublicDNS:8091 added" && ! $output =~ 'Node is already part of cluster' ]]
  do
    output=$(./couchbase-cli server-add \
      --cluster="$rallyPublicDNS" \
      -u="$adminUsername" \
      -p="$adminPassword" \
      --server-add="$nodePublicDNS" \
      --server-add-username="$adminUsername" \
      --server-add-password="$adminPassword" \
      --services="${services}")
    echo server-add output \'"$output"\'
    sleep 10
  done

  echo "Running couchbase-cli rebalance"
  output=""
  while [[ ! $output =~ "SUCCESS" ]]
  do
    output=$(./couchbase-cli rebalance \
    --cluster="$rallyPublicDNS" \
    -u="$adminUsername" \
    -p="$adminPassword")
    echo rebalance output \'"$output"\'
    sleep 10
  done
  setCBClusterTag
fi
