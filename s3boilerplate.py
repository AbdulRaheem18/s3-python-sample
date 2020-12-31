import os
import boto3
from boto3.s3.transfer import TransferConfig
from io import BytesIO

session_token = "FwoGZXIvYXdzENH//////////wEaDGgjQLKoXTOwOM9CgiLEAUWqgNAWcvAAWQi5dnt1/bye/ed6e28St1yRhT0OeKIa7gzwXBJ+xwZdgY1oSMp14L8ibQiN5Htm9R6EpystoAv1tAP9+uJ++NaW4MdPxAQv4By3yaUj1qJycQkektbgOZK7048YYliasO1DZrOMBFdhpshbtZIOQHP5jNxFjMkdUjotO+XO/aL3zye+r0yYZcHL2vySgVmgsFnEjRCzzVhw/+ZzDkXZE1hdiksFeoew2fIbLtJW666g/N981cq2Q02yWIoo/8Ky/wUyLb4hO2LFmEsXdvw7LNwKoZNe8Mng3SFQ/BDyfyowlEf6d8G43AqRchk5fyW+tw=="
region = 'us-east-1'
aws_id ="ASIA2H4EW26KNPAMGMMQ"
secret = "6aQY2IdrEvH+1+ciexDgd6EEpROrYVkL+6QDxoc7"

#This function is responsible for creating aws session by providing Secret Id and Key session token is optional 
def aws_session(region_name=region,id=aws_id,secret=secret):
    return boto3.session.Session(aws_access_key_id=id,
                                aws_secret_access_key=secret,
                                region_name=region_name,aws_session_token=session_token)

#if you have large files, this function will upload the file to s3 and it also make the object public if you don't want it remove ACL rule
def upload_to_s3_multipart(s3_client,file,file_name,S3_bucket,content):
     config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
                        multipart_chunksize=1024*25, use_threads=True)
     obj = BytesIO(file)
     obj.seek(0)
     s3_client.upload_fileobj(obj, S3_bucket, file_name,
     ExtraArgs={ 'ACL': 'public-read', 'ContentType': content},
     Config = config
     )


#this function takes the s3 client and bucket name and deletes it 
def delete_bucket(s3_client,bucket_name):
    s3_client.delete_bucket(Bucket=bucket_name)
    #bucket.objects.all().delete()

#this function takes the s3 client and bucket name and create bucket the bucket name should be unique
def create_s3_bucket(s3_client,bucket_name,region):
    s3_client.create_bucket(Bucket=bucket_name)

#this function takes the s3 client and list all the bucket
def list_bucket(s3_client):
    list_of_bucket =  s3_client.list_buckets()
    for bucket in list_of_bucket['Buckets']:
        print(f'  {bucket["Name"]}')

#this function takes the s3 client and bucket name and key and deletes the s3 object
def delete_s3_obj(s3_client,bucket_name,key):
    s3_client.delete_object(Bucket=bucket_name,Key=key)


#if your s3 object is not public and you want someone to access it you can create pre-signed URL with expiration
def create_s3_signed_url(s3_client,method,bucket_name,key,expiration):
    return s3_client.generate_presigned_url(ClientMethod=method,
                                            Params={'Bucket': bucket_name,
                                                    'Key': key},
                                                    ExpiresIn=expiration)

def main():
    session = aws_session()
    bucket_name = "bucketName"
    region = "us-east-1"
    key = "uniqueKey"
    s3_client = session.client('s3')
    file = open("demofile.txt", "rb")
    create_s3_bucket(s3_client,bucket_name,region) 
    list_bucket(s3_client)
   
    #delete_bucket(s3_client,bucket_name)
    upload_to_s3_multipart(s3_client,file.read(),key,bucket_name,'plain/text')
    signed_url = create_s3_signed_url(s3_client,'get_object',bucket_name,key,3600)
    delete_s3_obj(s3_client,bucket_name,key)



main()