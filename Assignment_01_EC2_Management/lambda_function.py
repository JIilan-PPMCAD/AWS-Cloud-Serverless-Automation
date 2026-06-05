import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # 1. Find all instances with 'Auto-Stop' tag (regardless of current state)
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    
    stop_ids = [i['InstanceId'] for r in stop_response['Reservations'] for i in r['Instances']]
    
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Issued STOP command for: {', '.join(stop_ids)}")
    else:
        print("No instances found with 'Auto-Stop' tag.")

    # 2. Find all instances with 'Auto-Start' tag (regardless of current state)
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    
    start_ids = [i['InstanceId'] for r in start_response['Reservations'] for i in r['Instances']]
    
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Issued START command for: {', '.join(start_ids)}")
    else:
        print("No instances found with 'Auto-Start' tag.")

    return {'statusCode': 200, 'body': 'Process Complete'}