import boto3
from datetime import datetime, timezone

RETENTION_DAYS = 30

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    now = datetime.now(timezone.utc)
    now_str = now.isoformat()
    
    # 1. Dynamically find all currently unattached volumes
    print("Scanning region for unattached (available) EBS volumes...")
    try:
        vol_response = ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        volumes = vol_response.get('Volumes', [])
    except Exception as e:
        print(f"ERROR fetching volumes from EC2: {str(e)}")
        return {'statusCode': 500, 'body': 'Failed to scan volumes.'}

    if not volumes:
        print("No unattached volumes found in this region.")
        return {'statusCode': 200, 'body': 'No unattached volumes found.'}
        
    print(f"Found {len(volumes)} unattached volumes. Checking detachment age...")
    
    for vol in volumes:
        vol_id = vol['VolumeId']
        detach_time_str = None
        
        # Check if the volume already has our tracking timestamp tag
        for tag in vol.get('Tags', []):
            if tag['Key'] == 'DetachedAt':
                detach_time_str = tag['Value']
                break
                
        # Case A: First time seeing this unattached volume -> Tag it with current time
        if not detach_time_str:
            print(f"Volume {vol_id} is unattached but has no tracking tag. Stamping with current time.")
            try:
                ec2.create_tags(
                    Resources=[vol_id],
                    Tags=[{'Key': 'DetachedAt', 'Value': now_str}]
                )
            except Exception as e:
                print(f"Failed to apply tag to {vol_id}: {str(e)}")
            continue
            
        # Case B: Volume was already tagged -> Calculate how long it has been sitting idle
        detach_time = datetime.fromisoformat(detach_time_str)
        idle_time = now - detach_time
        
        print(f"Volume {vol_id} has been unattached for {idle_time.days} days.")
        
        # Check if it has crossed the 30-day deletion threshold
        if idle_time.days >= RETENTION_DAYS:
            print(f"MATCHED CRITERIA: Volume {vol_id} has been idle for >= {RETENTION_DAYS} days. Purging...")
            
            # 2. Clean up snapshots associated with this specific volume first
            try:
                snap_response = ec2.describe_snapshots(
                    Filters=[{'Name': 'volume-id', 'Values': [vol_id]}]
                )
                for snap in snap_response.get('Snapshots', []):
                    snap_id = snap['SnapshotId']
                    print(f"-> Deleting snapshot backup {snap_id}")
                    ec2.delete_snapshot(SnapshotId=snap_id)
            except Exception as e:
                print(f"Warning: Snapshot cleanup failed for {vol_id}: {str(e)}")
                
            # 3. Delete the unattached volume itself
            try:
                ec2.delete_volume(VolumeId=vol_id)
                print(f"SUCCESS: Deleted volume {vol_id}")
            except Exception as e:
                print(f"ERROR deleting volume {vol_id}: {str(e)}")
        else:
            days_left = RETENTION_DAYS - idle_time.days
            print(f"KEEPING: Volume {vol_id} is safe. Deletion in {days_left} days.")
            
    return {'statusCode': 200, 'body': 'Unattached volume cleanup check complete.'}
