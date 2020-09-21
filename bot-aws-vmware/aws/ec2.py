import boto3


count_instaces = 0

ec2 = boto3.client('ec2',region_name='sa-east-1')

def ec2_all_instances():
    instances = []
    response = ec2.describe_instances()
    for reservation in response['Reservations']:  
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = instance['Tags'][0]['Value']
            instance_type = instance['InstanceType']
            instance_key_name = instance['KeyName']
            instance_state_code = instance['State']['Code']
            instance_state_name = instance['State']['Name']
            instance_privateip = instance['PrivateIpAddress']
            instance_subnetid_= instance['SubnetId']
            instance_vpcid = instance['VpcId']
            temp_dict = {}
            temp_dict['instance_id'] = instance_id
            temp_dict['instance_name'] = instance_name 
            temp_dict['instance_type'] = instance_type 
            temp_dict['instance_key_name'] = instance_key_name 
            temp_dict['instance_state_code'] = instance_state_code
            temp_dict['instance_state_name'] =  instance_state_name 
            temp_dict['instance_privateip'] = instance_privateip 
            temp_dict['instance_subnetid'] = instance_subnetid_
            temp_dict['instance_vpcid'] =  instance_vpcid 
            instances.append(temp_dict)
    return instances

def ec2_filter_by_id(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in response['Reservations']:  
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = instance['Tags'][0]['Value']
            return instance_name

# all_ec2 = ec2_all_instances()
# print("Total instance:", len(all_ec2))


def ec2_stop(instance_id):
    response = ec2.stop_instances(
        InstanceIds=[instance_id]
    )

    current_state = response['StoppingInstances'][0]['CurrentState']['Name']
    previous_state = response['StoppingInstances'][0]['PreviousState']['Name']

    message = f'Instance id :{instance_id} current state is {current_state} and previous state was {previous_state}'
    return message

def ec2_start(instance_id):
    response = ec2.start_instances(
    InstanceIds=[instance_id]
    )
    current_state = response['StartingInstances'][0]['CurrentState']['Name']
    previous_state = response['StartingInstances'][0]['PreviousState']['Name']

    message = f'Instance id :{instance_id} current state is {current_state} and previous state was {previous_state}'
    return message

