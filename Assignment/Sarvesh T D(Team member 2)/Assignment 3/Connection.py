import ibm_boto3
from ibm_botocore.client import Config, ClientError

def Connect():
    # Constants for IBM COS values
    COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud/"
    COS_API_KEY_ID = "akwv72aZO4E4lWXVnvWItm4laqjeryVQvmqPsQtMvWCS"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/85d9229314ff4e13adcdee6b467de71f:d369e3db-234b-485a-88ac-93f871d82673::"

    # Create resource
    try:
        cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
        )
        print("Connected Successfully :-)")
        return cos

    except:
        print("Error while connecting !")
        return 0

#List the items in a bucket
def get_bucket_contents(bucket_name,cos):
    res = []
    try:
        files = cos.Bucket(bucket_name).objects.all()
        for file in files:
            File = "https://"+bucket_name+".s3.jp-tok.cloud-object-storage.appdomain.cloud/"+file.key
            if("jpg" in file.key):
                res.append(File)
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return 0
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))
        return 0
    return res

#List the bucket 
# def get_buckets(cos):
#     print("Retrieving list of buckets")
#     try:
#         buckets = cos.buckets.all()
#         for bucket in buckets:
#             print("Bucket Name: {0}".format(bucket.name))
#     except ClientError as be:
#         print("CLIENT ERROR: {0}\n".format(be))
#     except Exception as e:
#         print("Unable to retrieve list buckets: {0}".format(e))