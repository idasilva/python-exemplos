import boto3
from ec2 import ec2_filter_by_id


ebs = boto3.client('ec2',region_name='sa-east-1')

def ebs_get_volumes():
    volumes = []
    response = ebs.describe_volumes()
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        volume_type = volume['VolumeType']
        volume_state = volume['State']
        instance_id = volume['Attachments'][0]['InstanceId']
        instance_name  = ec2_filter_by_id(instance_id)
        temp_dict = {}
        temp_dict['volume_id'] = volume_id 
        temp_dict['volume_type'] = volume_type 
        temp_dict['volume_state '] = volume_state 
        temp_dict['instance_id'] = instance_id 
        volumes.append(temp_dict)

def get_volumes_available():  
    response =  ebs.describe_volumes(
        Filters=[
            {
            'Name':'status',
            'Values':[
                'available',
            ]}
        ]
    )
    count_volumes = response['Volumes']
    return len(count_volumes)


ebs_volumes = get_volumes_available()
print(ebs_volumes)