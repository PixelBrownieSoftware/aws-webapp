import json
import re
import boto3

from time import gmtime, strftime

dynamodb = boto3.resource('dynamodb')
client = boto3.client('cloudtrail')

table = dynamodb.Table('ArtscapyDB')

now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def validateFeild(event, indexName, reqType):
    if indexName in event:
        if type(event[indexName]) == reqType:
            return event[indexName]
        else:
            return 'Incorrect type'
    else :
        return 'No data'
        
def validateColourFeild(event, indexName):
    if indexName in event:
        colour = event[indexName]
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colour)
        if match:
            return event[indexName]
        else:
            return 'Incorrect type'
    else :
        return 'No data'

def lambda_handler(event, context):
    
    if(event['requestCom'] == "post"):
        name = event['firstName'] +' '+ event['lastName']
        colour = validateColourFeild(event, 'fColour')
        fruit = validateFeild(event, 'fFruit', str)
        number = validateFeild(event, 'fNumber', int)
        
        response = table.put_item(
        Item={
            'ID': name,
            'fName': event['firstName'],
            'lName':event['lastName'],
            'fColour':colour,
            'fFruit' : fruit,
            'fNumber' : number
            }) 
        return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda, ' + name)
        }
            
    if(event['requestCom'] == "scan"):
        response = table.scan()
        return {
        'statusCode': 200,
        'body': response["Items"]
        }
    if(event['requestCom'] == "getLogs"):
        response = client.lookup_events()
        return {
        'statusCode': 200,
        'body': response
        }
           