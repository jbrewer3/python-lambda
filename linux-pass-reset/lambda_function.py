import boto3
import random
import string
import datetime

ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2')
secrets_manager_client = boto3.client('secretsmanager')

AWS_REGION = "us-east-2"

def lambda_handler(event, context):

    tag_key = 'tag:Linux-Pass-Rotation'
    tag_value= 'True'

    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': tag_key,
                'Values': [
                    tag_value,
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            }
        ]
    )

    instance_ids = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    for instance_id in instance_ids:

        length=14
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        ssm_command = f"sudo sh -c 'echo ec2-user:{password} | chpasswd'"
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [ssm_command]},
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print(f"error executing ssm command on instance {instance_id}")
        
        secret_name = f"{instance_id}-ec2-password-{datetime.datetime.today().strftime('%Y-%m-%d_%H%M')}"
        secret_value = {'password': password}
        secrets_manager_client.create_secret(
            Name=secret_name,
            SecretString=str(secret_value)
        )
    
        

    return {
        'statusCode': 200,
        'body': 'EC2 instance passwords updated successfully'
    }


