import boto3
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # 1. Initialize a boto3 S3 client
    s3 = boto3.client('s3')
    
    # Configuration
    BUCKET_NAME = "jilan-s3-cleanup-assignment"
    DAYS_THRESHOLD = 30
    
    # Calculate the cutoff date (Timezone-aware to match S3 timestamps)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_THRESHOLD)
    
    print(f"Starting cleanup for bucket: {BUCKET_NAME}")
    print(f"Deleting files older than {DAYS_THRESHOLD} days (Before: {cutoff_date})")
    
    try:
        # 2. List objects in the specified bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        # Check if the bucket has any files
        if 'Contents' not in response:
            print(f"The bucket '{BUCKET_NAME}' is currently empty.")
            return {'statusCode': 200, 'body': 'No files found to delete.'}

        deleted_count = 0
        
        # 3. Iterate through objects and delete those older than 30 days
        for obj in response['Contents']:
            file_name = obj['Key']
            file_date = obj['LastModified'] # The upload timestamp
            
            if file_date < cutoff_date:
                # 4. Print the names of deleted objects for logging purposes
                print(f"DELETING: {file_name} (Uploaded: {file_date})")
                
                s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
                deleted_count += 1
            else:
                print(f"KEEPING: {file_name} (Uploaded: {file_date})")
        
        print(f"Cleanup complete. Total files deleted: {deleted_count}")
        
        return {
            'statusCode': 200,
            'body': f"Process finished. Deleted {deleted_count} files."
        }

    except Exception as e:
        print(f"Error during execution: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error performing cleanup.'
        }