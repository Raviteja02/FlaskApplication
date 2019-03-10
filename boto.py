import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Student_Details')
def lambda_handler():
    table.put_item(
        Item={
        "Admission_number":"6011663076",
        "Name":"jaggu",

    })
    return {"message":"Details Successfully Saved"}
'''lambda_handler()


TtSBAd72COarOPLgOomY62ryITJk2Keg3mOK2QBW 


var apigClient = apigClientFactory.newClient({
  accessKey: 'AKIAJ5ZEK4WM2SEOTNZQ',
  secretKey: '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',
});'''

