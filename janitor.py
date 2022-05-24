from datetime import datetime, timedelta, timezone
import boto3
import time
 
client = boto3.client('ec2', region_name='eu-west-1')
 
#Here all images which are older than 5 days from the present date will be filtered
older_days = 5
 
def lambda_handler(event, context):
    get_ami_list(older_days)
 
def get_ami_list(older_days):
    amiNames = client.ec2.describe_images(Owners=['self'])
    print(amiNames)
    today_date = datetime.now().strftime('%d-%m-%Y')
    print("Today's date is " + today_date)
    deldate1 = get_delete_date(older_days)
    print("AMI images which are older than " + str(deldate1) + " will be deregistered")
    for image in amiNames['Images']:
        taginfo = image['Tags']
        for tagName in taginfo:
            #Filter only the images having tag value as Proj1AMI
            if (tagName['Value'] == 'Proj1AMI'):
                ami_creation = image['CreationDate']
                imageID = image['ImageId']
                print("=================================================")
                print("Image id is " + imageID)
                print("Creation date for above image is " + ami_creation)
                if (str(ami_creation) < str(get_delete_date(older_days))):
                    print("This AMI is older than " + str(older_days) + " days")
                    delete_ami(imageID)
 
def get_delete_date(older_days):
    delete_time = datetime.now(tz=timezone.utc) - timedelta(days=older_days)
    return delete_time;
 
def delete_ami(imageID):
    print("Deregistering Image ID: " + imageID)
    #client.ec2.deregister_image(ImageId=imageID)
