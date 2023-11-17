import json
import boto3

ssm = boto3.client('ssm', region_name="ap-south-1")

def lambda_handler(event, context):
    parameter_name = '/myapp/access-token'
    
    token = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    tokenFromHeader = event['headers']['authorization']
    
    if tokenFromHeader == token['Parameter']['Value']:
        auth_status = 'Allow'
    else:
        auth_status = 'Deny'
    
    authResponse = {
        'principalId': '121',
        'policyDocument': { 
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Resource': [
                        event['routeArn']
                    ], 
                    'Effect': auth_status
                }
            ]
        }
    }

    return authResponse