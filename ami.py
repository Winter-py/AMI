import boto3
from datetime import datetime

region = 'eu-west-1'

# 
current_date = datetime.now()
retention = 10


client = boto3.client('ec2', region_name=region)

packer_build_ID = client.describe_images(Owners=['self'])['Images']
Tags = client.describe_tags(Filters=[{'Name': 'tag-key', 'Values': ['Packer-Build-ID']}])['Tags']


for ami in packer_build_ID:
    creation_date = ami['CreationDate']
    ami_id = ami['ImageId']
    ami_location = ami['ImageLocation']
    state = ami['State']
    #print(ami_id, creation_date, ami_location, state)

for tag in Tags:
    tag_key = tag['Key']
    tag_value = tag['Value']
    print(tag_key, tag_value)

if tag_value == '1':
    print("AMI is due for deletion")
else:
    print("AMI is not due for deletion")





