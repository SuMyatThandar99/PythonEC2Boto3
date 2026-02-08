import boto3

ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId='ami-0f65fc8c24ec8d2a1',  # Ubuntu 22.04 (ap-northeast-1)
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName='my-keypair-name',
    #SecurityGroupIds=['sg-xxxxxxxx'],
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 20,
                'VolumeType': 'gp3',
                'DeleteOnTermination': True
            }
        }
    ],
    UserData='''#!/bin/bash
apt update -y
apt install apache2 -y
systemctl start apache2
systemctl enable apache2

echo "<html><body><h1>Welcome to Apache Web Server</h1></body></html>" > /var/www/html/index.html
''',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'Pythontest'},
                {'Key': 'Department', 'Value': 'Technical'},
                {'Key': 'Environment', 'Value': 'Test'}
            ]
        }
    ]
)

for instance in instances:
    print(f"Instance {instance.id} is launching")
