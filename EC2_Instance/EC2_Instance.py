import boto3
import os
from credentials import config, security_group_config

def create_key_pair(key_pair_input):
    ec2 = boto3.client('ec2')
    try:
        key_pair = ec2.create_key_pair(KeyName=key_pair_input)
        private_key = key_pair['KeyMaterial']

        with os.fdopen(os.open(key_pair_input + '.pem', os.O_WRONLY | os.O_CREAT, 0o400), 'w') as f:
            f.write(private_key)
        return key_pair_input


    except Exception:
        print('Key pair already exists')



def authorize_security_inbound_rule(ec2_client_, instance_id, security_group_name):
    security_group_id = security_group_config.get_security_group_config(security_group_name)
    response = ec2_client_.modify_instance_attribute(
        InstanceId = instance_id,
        Groups=[security_group_id]
    )
    # Check if the modification was successful
    print(f"Security group {security_group_id} attached to instance {instance_id}")

def create_instance_and_store_id(ami_id, instance_type, instance_name, security_group_name, storage_file, key_pair_name):
    # Create an EC2 client
    ec2_client = boto3.client('ec2', region_name='us-east-1',
                              aws_access_key_id=config.get_config('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=config.get_config('AWS_SECRET_ACCESS_KEY'))

    # Launch an EC2 instance
    response = ec2_client.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )

    # Get the instance ID
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance {instance_name} launched with ID: {instance_id}")
    authorize_security_inbound_rule(ec2_client, instance_id, security_group_name)

    # Store the instance ID in a file
    with open(storage_file, 'w') as file:
        file.write(instance_id)

# Example usage for the initial instance creation
ami_id = "ami-0277155c3f0ab2930"
instance_type = "t2.micro"
security_group_name = "CSE546_EC2_Security_Group"
instance_name = "web-instance"
storage_file = "instance_id.txt"



def operate_on_instance(instance_id, operation):
    # Create an EC2 client
    ec2_client = boto3.client('ec2', region_name='us-east-1',
                              aws_access_key_id=config.get_config('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=config.get_config('AWS_SECRET_ACCESS_KEY'))

    # Perform the desired operation (e.g., start, stop, terminate)
    if operation == 'start':
        ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} started.")
    elif operation == 'stop':
        ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} stopped.")
    elif operation == 'terminate':
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} terminated.")
    else:
        print("Invalid operation.")


key_pair_name = create_key_pair('ec2_key_pair')
create_instance_and_store_id(ami_id, instance_type, instance_name, security_group_name, storage_file, 'ec2_key_pair')
# Example usage for subsequent operations
stored_instance_id = open(storage_file, 'r').read()
operate_on_instance(stored_instance_id, 'start')  # Replace 'start' with your desired operation
