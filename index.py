import subprocess
import sys
import os

def handler(event, context):
    """Vercel serverless function handler for Streamlit"""
    
    # Set environment variables for Streamlit
    os.environ['STREAMLIT_SERVER_PORT'] = '8000'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run Streamlit app
    try:
        result = subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port=8000',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ], capture_output=True, text=True, timeout=30)
        
        return {
            'statusCode': 200,
            'body': result.stdout,
            'headers': {
                'Content-Type': 'text/html'
            }
        }
    except subprocess.TimeoutExpired:
        return {
            'statusCode': 500,
            'body': 'Request timeout'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }

# For local testing
if __name__ == "__main__":
    print("Starting Streamlit app...")
    os.system("streamlit run app.py")