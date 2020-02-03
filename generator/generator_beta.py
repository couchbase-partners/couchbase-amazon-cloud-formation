import sys
import yaml
import json


def main():
    filename = sys.argv[1]


    print('Using parameter file: ' + filename)
    with open(filename, 'r')as stream:
        parameters = yaml.load(stream)
    print('Parameters: ' + str(parameters))

    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "AWS Deployment for Couchbase Enterprise",
        "Parameters": {
            "Username": {
                "Description": "Username for Couchbase administrator",
                "Type": "String"
            },
            "Password": {
                "Description": "Password for Couchbase administrator",
                "Type": "String",
                "NoEcho": True
            },
            "KeyName": {
                "Description": "Name of an existing EC2 KeyPair",
                "Type": "AWS::EC2::KeyPair::KeyName"
            }
        },
        "Mappings": {},
        "Resources": {}
    }

    serverVersion = parameters['serverVersion']
    syncGatewayVersion = parameters['syncGatewayVersion']
    cluster = parameters['cluster']

    template['Mappings'] = dict(list(template['Mappings'].items()) + list(generateMappings().items()))
    template['Resources'] = dict(list(template['Resources'].items()) + list(generateMiscResources().items()))
    template['Resources'] = dict(
        list(template['Resources'].items()) + list(generateCluster(serverVersion, syncGatewayVersion, cluster).items()))

    file = open('generated_beta.template', 'w')
    file.write(json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    file.close()


def generateMappings():
    mappings = {
        "CouchbaseServer": {
            "ap-northeast-1": {
                "BYOL": "ami-0167ba3c266acfd63",
                "HourlyPricing": "ami-0b40b05ad9d54cbc3"
            },
            "ap-northeast-2": {
                "BYOL": "ami-048f48645e2fc112a",
                "HourlyPricing": "ami-03a3705fdda4b9436"
            },
            "ap-south-1": {
                "BYOL": "ami-06fe2c3f72b82a4a3",
                "HourlyPricing": "ami-065d1a1771bb3a897",
            },
            "ap-southeast-1": {
                "BYOL": "ami-04a3f9837dc9bae0d",
                "HourlyPricing": "ami-07c8a5c9daa5d378b",
            },
            "ap-southeast-2": {
                "BYOL": "ami-08a684bfacbeb32cd",
                "HourlyPricing": "ami-0ed38d65d72290bce",
            },
            "ca-central-1": {
                "BYOL": "ami-0cf562b37f8aba1a3",
                "HourlyPricing": "ami-01134c53172e1e6ff",
            },
            "eu-central-1": {
                "BYOL": "ami-06bdd2efe3aa977f9",
                "HourlyPricing": "ami-06bdd2efe3aa977f9",
            },
            "eu-west-1": {
                "BYOL": "ami-09214027564070c45",
                "HourlyPricing": "ami-06937b6ae4710e42f",
            },
            "eu-west-2": {
                "BYOL": "ami-0ba9accab1515252c",
                "HourlyPricing": "ami-0516a8ccb788e0542",
            },
            "eu-west-3": {
                "BYOL": "ami-03bb90cb881172c51",
                "HourlyPricing": "ami-0b7026377a8881250"
            },
            "sa-east-1": {
                "BYOL": "ami-07726ffcc71bbac59",
                "HourlyPricing": "ami-00dc52838b61f577f",
            },
            "us-east-1": {
                "BYOL": "ami-0875b7c9f9efaafbd",
                "HourlyPricing": "ami-027e465eec366030a",
            },
            "us-east-2": {
                "BYOL": "ami-01c42180217e37eb1",
                "HourlyPricing": "ami-04afd1f6579a29e1d",
            },
            "us-west-1": {
                "BYOL": "ami-0794b581b4a10c0d1",
                "HourlyPricing": "ami-0a80456c26588e950",
            },
            "us-west-2": {
                "BYOL": "ami-027781b130e8252ff",
                "HourlyPricing": "ami-0e408a9a88a43609f",
            }
        },
    "CouchbaseSyncGateway":{  
        "ap-northeast-1":{  
        "BYOL":"ami-0b0174e6",
        "HourlyPricing":"ami-410b7eac"
        },
        "ap-northeast-2":{  
        "BYOL":"ami-ca8631a4",
        "HourlyPricing":"ami-37823559"
        },
        "ap-south-1":{  
        "BYOL":"ami-628bb80d",
        "HourlyPricing":"ami-4174462e"
        },
        "ap-southeast-1":{  
        "BYOL":"ami-be7a3d54",
        "HourlyPricing":"ami-0a783fe0"
        },
        "ap-southeast-2":{  
        "BYOL":"ami-5833943a",
        "HourlyPricing":"ami-49288f2b"
        },
        "ca-central-1":{  
        "BYOL":"ami-13aa2777",
        "HourlyPricing":"ami-adaa27c9"
        },
        "eu-central-1":{  
        "BYOL":"ami-7e070495",
        "HourlyPricing":"ami-3e7f7cd5"
        },
        "eu-west-1":{  
        "BYOL":"ami-836a7169",
        "HourlyPricing":"ami-8a170c60"
        },
        "eu-west-2":{  
        "BYOL":"ami-49ea002e",
        "HourlyPricing":"ami-d3eb01b4"
        },
        "eu-west-3":{  
        "BYOL":"ami-9e8d3de3",
        "HourlyPricing":"ami-9f8d3de2"
        },
        "sa-east-1":{  
        "BYOL":"ami-14577678",
        "HourlyPricing":"ami-457a5b29"
        },
        "us-east-1":{  
        "BYOL":"ami-f6e3e089",
        "HourlyPricing":"ami-2ce5e653"
        },
        "us-east-2":{  
        "BYOL":"ami-10271d75",
        "HourlyPricing":"ami-bf251fda"
        },
        "us-west-1":{  
        "BYOL":"ami-f4d13c97",
        "HourlyPricing":"ami-cbd13ca8"
        },
        "us-west-2":{  
        "BYOL":"ami-dfcc92a7",
        "HourlyPricing":"ami-ddcc92a5"
            }
        }
    }
    return mappings


def generateMiscResources():
    resources = {
        "CouchbaseInstanceProfile": {
            "Type": "AWS::IAM::InstanceProfile",
            "Properties": {"Roles": [{"Ref": "CouchbaseRole"}]}
        },
        "CouchbaseRole": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole"]
                    }]
                },
                "Policies": [{
                    "PolicyName": "CouchbasePolicy",
                    "PolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Effect": "Allow",
                            "Action": [
                                "ec2:CreateTags",
                                "ec2:DescribeTags",
                                "ec2:DescribeInstances",
                                "autoscaling:DescribeAutoScalingGroups"
                            ],
                            "Resource": "*"
                        }]
                    }
                }]
            }
        },
        "CouchbaseSecurityGroup": {
            "Type": "AWS::EC2::SecurityGroup",
            "Properties": {
                "GroupDescription": "Enable SSH and Couchbase Ports",
                "SecurityGroupIngress": [{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 4369, "ToPort": 4369, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 4984, "ToPort": 4985, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 8091, "ToPort": 8096, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9100, "ToPort": 9105, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9110, "ToPort": 9122, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 9998, "ToPort": 9999, "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 11207, "ToPort": 11215,
                                          "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 18091, "ToPort": 18096,
                                          "CidrIp": "0.0.0.0/0"},
                                         {"IpProtocol": "tcp", "FromPort": 21100, "ToPort": 21299,
                                          "CidrIp": "0.0.0.0/0"}
                                         ]
            }
        }
    }


    return resources


def generateCluster(serverVersion, syncGatewayVersion, cluster):
    resources = {}


    rallyAutoScalingGroup = cluster[0]['group']
    for group in cluster:
        groupResources = generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup)
        resources = dict(list(resources.items()) + list(groupResources.items()))
    return resources


def generateGroup(serverVersion, syncGatewayVersion, group, rallyAutoScalingGroup):
    resources = {}


    license = group['license']
    if 'syncGateway' in group['services']:
        resources = dict(
            list(resources.items()) + list(generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup).items()))
    else:
        resources = dict(list(resources.items()) + list(generateServer(license, serverVersion, group, rallyAutoScalingGroup).items()))
    return resources


def generateSyncGateway(license, syncGatewayVersion, group, rallyAutoScalingGroup):
    groupName = group['group']
    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    #TODO: handle this better
    #temp change for version swapping
    if license == 'BYOL6':
        license == 'BYOL'

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": {"Fn::GetAZs": ""},
                "LaunchConfigurationName": {"Ref": groupName + "LaunchConfiguration"},
                "MinSize": 0,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": {"Fn::FindInMap": ["CouchbaseSyncGateway", {"Ref": "AWS::Region"}, license]},
                "InstanceType": nodeType,
                "SecurityGroups": [{"Ref": "CouchbaseSecurityGroup"}],
                "KeyName": {"Ref": "KeyName"},
                "EbsOptimized": True,
                "IamInstanceProfile": {"Ref": "CouchbaseInstanceProfile"},
                "BlockDeviceMappings":
                    [{
                        "DeviceName": "/dev/xvda",
                        "Ebs": {"DeleteOnTermination": True}
                    }
                    ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": ["", [
                            "#!/bin/bash\n",
                            "echo 'Running startup script...'\n",
                            "stackName=", {"Ref": "AWS::StackName"}, "\n",
                            "syncGatewayVersion=" + syncGatewayVersion + "\n",
                            "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/master/scripts/\n",
                            "wget ${baseURL}syncGateway.sh\n",
                            "chmod +x *.sh\n",
                            "./syncGateway.sh ${stackName} ${syncGatewayVersion}\n"
                        ]]
                    }
                }
            }
        }
    }
    return resources


def generateServer(license, serverVersion, group, rallyAutoScalingGroup):
    groupName = group['group']


    nodeCount = group['nodeCount']
    nodeType = group['nodeType']
    dataDiskSize = group['dataDiskSize']
    services = group['services']

    servicesParameter = ''
    for service in services:
        servicesParameter += service + ','
    servicesParameter = servicesParameter[:-1]

    command = [
        "#!/bin/bash\n",
        "echo 'Running startup script...'\n",
        "adminUsername=", {"Ref": "Username"}, "\n",
        "adminPassword=", {"Ref": "Password"}, "\n",
        "services=" + servicesParameter + "\n",
        "stackName=", {"Ref": "AWS::StackName"}, "\n",
        "serverVersion=" + serverVersion + "\n",
        "baseURL=https://raw.githubusercontent.com/couchbase-partners/amazon-cloud-formation-couchbase/6.5Test/scripts/\n",
        "wget ${baseURL}server_beta.sh\n",
        "wget ${baseURL}utilAmzLnx2.sh\n",
        "chmod +x *.sh\n",
    ]
    if groupName == rallyAutoScalingGroup:
        command.append("./server_beta.sh ${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion}\n")
    else:
        command.append("rallyAutoScalingGroup=")
        command.append({"Ref": rallyAutoScalingGroup + "AutoScalingGroup"})
        command.append("\n")
        command.append(
            "./server_beta.sh " +
            "${adminUsername} ${adminPassword} ${services} ${stackName} ${serverVersion} ${rallyAutoScalingGroup}\n")

    resources = {
        groupName + "AutoScalingGroup": {
            "Type": "AWS::AutoScaling::AutoScalingGroup",
            "Properties": {
                "AvailabilityZones": {"Fn::GetAZs": ""},
                "LaunchConfigurationName": {"Ref": groupName + "LaunchConfiguration"},
                "MinSize": 0,
                "MaxSize": 100,
                "DesiredCapacity": nodeCount
            }
        },
        groupName + "LaunchConfiguration": {
            "Type": "AWS::AutoScaling::LaunchConfiguration",
            "Properties": {
                "ImageId": {"Fn::FindInMap": ["CouchbaseServer", {"Ref": "AWS::Region"}, license]},
                "InstanceType": nodeType,
                "SecurityGroups": [{"Ref": "CouchbaseSecurityGroup"}],
                "KeyName": {"Ref": "KeyName"},
                "EbsOptimized": True,
                "IamInstanceProfile": {"Ref": "CouchbaseInstanceProfile"},
                "BlockDeviceMappings":
                    [{
                        "DeviceName": "/dev/xvda",
                        "Ebs": {"DeleteOnTermination": True}
                    }, {
                        "DeviceName": "/dev/sdk",
                        "Ebs": {
                            "VolumeSize": dataDiskSize,
                            "VolumeType": "gp2",
                            "Encrypted": True
                        }
                    }
                    ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": ["", command]
                    }
                }
            }
        }
    }
    return resources

main()