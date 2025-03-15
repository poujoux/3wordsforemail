{
  "KeySchema": [
    {
      "AttributeName": "email",
      "KeyType": "HASH"
    },
    {
      "AttributeName": "num",
      "KeyType": "RANGE"
    }
  ],
  "AttributeDefinitions": [
    {
      "AttributeName": "email",
      "AttributeType": "S"
    },
    {
      "AttributeName": "num",
      "AttributeType": "S"
    }
  ],
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 15,
    "WriteCapacityUnits": 15
  }
}



