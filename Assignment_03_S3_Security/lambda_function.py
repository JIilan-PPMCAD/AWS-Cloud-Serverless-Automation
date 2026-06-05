import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    non_compliant_buckets = []
    response = s3.list_buckets()
    
    for bucket in response['Buckets']:
        name = bucket['Name']
        try:
            enc = s3.get_bucket_encryption(Bucket=name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            
            # Check if it uses SSE-KMS (Strict Corporate Standard)
            algo = rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
            if algo != 'aws:kms':
                print(f"Bucket {name} uses {algo} instead of aws:kms!")
                non_compliant_buckets.append(name)
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                # Legacy unencrypted bucket (created before 2023)
                non_compliant_buckets.append(name)
                
    return {
        'statusCode': 200,
        'unencrypted_or_non_compliant_buckets': non_compliant_buckets
    }
