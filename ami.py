import boto3
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

region = 'eu-west-1'

# Image older than this will be deleted
current_date = datetime.today()
retention = 10


client = boto3.client('ec2', region_name=region)

ami_id = client.describe_images(Owners=['self'])['Images']
Tags = client.describe_tags(Filters=[{'Name': 'tag-key', 'Values': ['Packer-Build-ID']}])['Tags']


for image in ami_id['Images']:
    taginfo = image['Tags']
    for tag in taginfo:
        if (tag['Value'] == 'Packer-Build-ID'):
            image_date = parse(image['CreationDate'])
            if (current_date - image_date) > timedelta(days=retention):
                print("Deleting AMI: " + image['ImageId'])
                #client.deregister_image(ImageId=image['ImageId'])
            


# for tag in Tags:
#     tag_key = tag['Key']
#     tag_value = tag['Value']
#     #print(tag_key, tag_value)

# for ami in packer_build_ID:
#     creation_date = ami['CreationDate']
#     creation_date = parse(creation_date).replace(tzinfo=None)
#     ami_id = ami['ImageId']
#     ami_location = ami['ImageLocation']
#     state = ami['State']
    
    #print(ami_id, tag_value)
    #print(ami_id, creation_date, ami_location, state)

# for tag in Tags:
#     tag_key = tag['Key']
#     tag_value = tag['Value']
    #print(tag_key, tag_value)

# if tag_value == '1' and current_date - creation_date > retention:
#     print('AMI:', ami_id, 'is older than', retention, 'days and will be deleted')
#     print("AMI is due for deletion") 
# else:
#     print("AMI is not due for deletion")

#print(current_date - creation_date)





