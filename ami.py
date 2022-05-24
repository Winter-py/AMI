from warnings import filters
import boto3
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

region = 'eu-west-1'

# Image older than this will be deleted
current_date = datetime.today()
retention = 30


client = boto3.client('ec2', region_name=region)

ami_id = client.describe_images(Owners=['self'])['Images']

Tags = client.describe_tags(Filters=[{'Name': 'tag-key', 'Values': ['Packer-Build-ID']}])['Tags']

for tag in Tags:
    tag_key = tag['Key']
    tag_value = tag['Value']
    #print(tag_key, tag_value)

for ami in ami_id:
    creation_date = ami['CreationDate']
    creation_date = parse(creation_date).replace(tzinfo=None)
    ami_id = ami['ImageId']
    ami_location = ami['ImageLocation']
    state = ami['State']

for tag in Tags:
    version = [tag['Value'] for tag in Tags if tag['Key'] == 'Packer-Build-ID'][0]
    version = version[0]
    #print(version)
    #print(tag['Key'], tag['Value'], tag['ResourceId'], tag['ResourceType']
    
if version == '1' and creation_date < current_date - timedelta(days=retention):
    print('AMI:', ami_id, 'is older than', retention, 'days and will be deleted')
else:
    print("AMI is not due for deletion")


# def delete_ami(imageID):
#     print("Deregistering Image ID: " + imageID)
    #client.ec2.deregister_image(ImageId=imageID)



