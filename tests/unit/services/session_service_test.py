from unittest.mock import patch

from api.init import init
from api.services.session_service import SessionService

session_service: SessionService = init()["session_service"] 
def test_session_service():
    mock_get_item_return = {
        "Item": {
            "doc_html": {
                "S": "<p>this is a test doc</p>"
            },
            "id": {
                "S": "test"
            },
            "messages": {
                "L": [
                    {"S": "{\"message\": \"Hi\", \"isUser\": false}"},
                    {"S": "{\"message\": \"Yo\", \"isUser\": true}"}
                ]
            }
        },
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "166",
                "content-type": "application/x-amz-json-1.0",
                "date": "Fri, 26 Jul 2024 10:22:24 GMT",
                "server": "Server",
                "x-amz-crc32": "4238721578",
                "x-amzn-requestid": "M48B6NKO16JFTSJ4A51RKQ0UDVVV4KQNSO5AEMVJF66Q9ASUAAJG"
            },
            "HTTPStatusCode": 200,
            "RequestId": "M48B6NKO16JFTSJ4A51RKQ0UDVVV4KQNSO5AEMVJF66Q9ASUAAJG",
            "RetryAttempts": 0
        }
    }

    test_response = {
        "doc_html": "<p>this is a test doc</p>",
        "id": "test",
        "messages": [
            "{\"message\": \"Hi\", \"isUser\": false}", 
            "{\"message\": \"Yo\", \"isUser\": true}"
        ]
    }

    with patch("api.clients.aws.dynamodb.DynamoDBClient.get_item", return_value=mock_get_item_return):
        print(session_service.get_session(session_id="test"))
        assert(session_service.get_session(session_id="test")) == test_response

    mock_put_item_return = {
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "2",
                "content-type": "application/x-amz-json-1.0",
                "date": "Sat, 27 Jul 2024 04:23:58 GMT",
                "server": "Server",
                "x-amz-crc32": "2745614147",
                "x-amzn-requestid": "MJAF0PN5G5D3TQFP5VCRF0IMAJVV4KQNSO5AEMVJF66Q9ASUAAJG"
            },
            "HTTPStatusCode": 200,
            "RequestId": "MJAF0PN5G5D3TQFP5VCRF0IMAJVV4KQNSO5AEMVJF66Q9ASUAAJG",
            "RetryAttempts": 0
        }
    }
    with patch("api.clients.aws.dynamodb.DynamoDBClient.put_item", return_value=mock_put_item_return):
        assert(session_service.put_session(session={            
            "id": "test",
            "messages": [
                "{'message': 'Hi', 'isUser': false}",
                "{'message': 'Yo', 'isUser': true}"
            ],
            "doc_html": "<p>this is a test doc</p>"
        })) == mock_put_item_return
