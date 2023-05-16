# python-lambda Password Reset

To deploy this lambda function you must follow the steps below.

## Prerequisites

 1. IAM policy for your lambda function with the following actions
	 `"Action": [
                "ssm:SendCommand",
                "ssm:StartSession",
                "ec2:DescribeInstances",
                "secretsmanager:CreateSecret",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]`
2. IAM policy for your EC2 instance with the following [AmazonSSMManagedInstanceCore] amazon managed policy attached.
3. SSM agent installed and running on each instance you can verify the ssm agent is connected properly in the systems manager > fleet manager user interface in AWS Console
4. EC2 Instances with the tags Key: Pass-Rotation Value: True

## Steps to deploy and test function
1.	Create IAM policy with the above mentioned actions as seen below as well. 
	`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "ssm:SendCommand",
                "ssm:StartSession",
                "ec2:DescribeInstances",
                "ec2:DescribeImages",
                "secretsmanager:CreateSecret",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}`
2.	Create IAM role to attache this policy too. 
3.	Create your Lambda Function with the following code. https://github.com/jbrewer3/python-lambda/blob/main/linux-pass-reset/lambda_function.py Note. Ensure you select the new IAM role that you created earlier so that the function has proper permissions. 
5.	Create your EC2 instances both linux and windows and ensure you have user data script to install ssm. Please see the two post for instructions on this. 
	1 https://repost.aws/knowledge-center/install-ssm-agent-ec2-linux 
	2 https://repost.aws/knowledge-center/ssm-agent-windows-ec2
6.	Make sure that you tag these instances with Key: Password-Rotation Value: True
7.	Once the instances are created you can look at fleet manager in systems manager to ensure the ssm agent is connected. 
8.	We can then go to lambda and test our function https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html
9.	Then check secrets manager to ensure the secrets for each instance are showing up the naming convention will look as so. 
	instanceid-ec2-password-<date yyyy-mm-dd_Hour_Minute>
10.	login via ssh or instance connect to the ec2 instance and run `su ec2-user` put in the password retrieved from secrets manager to ensure it works. 
11.	Start RDP session to windows instances and input the new password to verify this works. 
12.	Last we can configure a trigger for our lambda function to trigger every 30 days to ensure password are rotated. 
