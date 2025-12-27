"""Ultra-minimal handler for Vercel"""
import json

def handler(request):
    """Test handler"""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Hello from Vercel"})
    }
