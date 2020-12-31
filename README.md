# s3-python-sample
A sample python script that use boto3 and interact with aws s3 storage.

# Introduction
To interact with s3 in python we have boto3 library https://boto3.amazonaws.com/v1/documentation/api/latest/index.html.
s3 is a file storage service that is provided by aws.The s3 has buckets which is similiar to the concept of directory in file system.

# Boto3
The boto3 is library that is used to interact with s3 with python code.
We need aws_access_key_id and aws_secret_access_key to access s3 programmaticaly, we get it at the time of creating new user on aws through IAM or we can re-generate it through aws IAM

# Sample Code
The Code consist of sample function to create/delete/list bucket and upload/delete s3 objects 
