import os
import boto3
import botocore.config
from dotenv import load_dotenv
import requests

load_dotenv()
session = boto3.Session()

client = session.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='sgp1',
                        endpoint_url=os.getenv('ENDPOINTURL'),
                        aws_access_key_id=os.getenv('SPACES_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET'))

def checkUrl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("URL request succeeded!")
            return True
        else:
            print(f"URL request failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print("URL request failed:", e)


def uploadFileToS3(fileContents, email, fileName):
    pathName = 'AGM/'+email+'/'+fileName    
    try:
        client.put_object(Body=fileContents, Bucket='agm-match', Key=pathName, ACL='public-read-write')
        print("Image uploaded successfully.")
    except Exception as e:
        print("Error uploading image:", str(e))

def deleteFolderS3(email):
    bucket_name = 'agm-match'
    folder_path = 'AGM/' + email + '/'

    # List objects within the folder
    objects = client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)['Contents']

    # Delete objects within the folder
    delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects]}
    client.delete_objects(Bucket=bucket_name, Delete=delete_keys)

    # Delete the folder itself
    client.delete_object(Bucket=bucket_name, Key=folder_path)
    print("Delete folder successfully")
    return True

def listFile():    
    response = client.list_objects(Bucket='agm-match')
    for obj in response['Contents']:
        print(obj['Key'])