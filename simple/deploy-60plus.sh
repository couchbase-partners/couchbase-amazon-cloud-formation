#!/usr/bin/env bash

STACK_NAME=$1

TEMPLATE_BODY="file://couchbase-ee.60plus.template"
REGION=`aws configure get region`

#Universal Settings
Username="couchbase" #For the Couchbase Web Console
Password="foo123!" #For the Couchbase Web Console
KeyName="couchbase-${REGION}" #The ssh key that will be used to connect to the nodes
License=BYOL #Couchbase Server license use: BYOL or HourlyPricing

#Couchbase Server Settings
InstanceType="m5.xlarge" #Couchbase Server Instance Type
ServerInstanceCount="3"
ServerDiskSize="100"
ServerVersion="6.6.0"
Services="data" #separate each service with \\, e.g data\\,index\\,query\\,fts\\,eventing\\,analytics


#Couchbase Sync Gateway Settings
SyncGatewayVersion="2.7.3"
SyncGatewayInstanceCount="0"
SyncGatewayInstanceType="m5.large"

aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--template-body ${TEMPLATE_BODY} \
--stack-name ${STACK_NAME} \
--region ${REGION} \
--parameters \
ParameterKey=ServerInstanceCount,ParameterValue=${ServerInstanceCount} \
ParameterKey=ServerDiskSize,ParameterValue=${ServerDiskSize} \
ParameterKey=SyncGatewayInstanceCount,ParameterValue=${SyncGatewayInstanceCount} \
ParameterKey=InstanceType,ParameterValue=${InstanceType} \
ParameterKey=Username,ParameterValue=${Username} \
ParameterKey=Password,ParameterValue=${Password} \
ParameterKey=KeyName,ParameterValue=${KeyName} \
ParameterKey=Services,ParameterValue=${Services} \
ParameterKey=ServerVersion,ParameterValue=${ServerVersion} \
ParameterKey=SyncGatewayVersion,ParameterValue=${SyncGatewayVersion} \
ParameterKey=License,ParameterValue=${License}
