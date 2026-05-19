import json
import urllib.request
import urllib.error

DEFAULT_URL = "https://log-reader-server-b4k8d-naesxhheza-uc.a.run.app/logs"

def read_logs(url=DEFAULT_URL, token=None):
    """
    Reads logs from the specified URL.
    
    Args:
        url: The URL to fetch logs from.
        token: Optional bearer token for authentication.
        
    Returns:
        A list of log entries (dictionaries) or an error message.
    """
    req = urllib.request.Request(url)
    
    if token:
        req.add_header('Authorization', f'Bearer {token}')
        
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                content = response.read().decode('utf-8')
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return f"Error: Failed to decode JSON response. Content: {content}"
            else:
                return f"Error: Received status code {response.status}"
    except urllib.error.HTTPError as e:
        return f"HTTP Error: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"Error: {str(e)}"

def read_logs_with_auth(url=DEFAULT_URL):
    """
    Reads logs after automatically obtaining an identity token from gcloud.
    """
    import subprocess
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-identity-token"], text=True).strip()
        return read_logs(url=url, token=token)
    except Exception as e:
        return f"Error getting token or logs: {e}"

if __name__ == "__main__":
    # Quick manual test if run directly
    import sys
    
    print(f"Fetching logs from {DEFAULT_URL} using gcloud identity token...")
    result = read_logs_with_auth()
    print(json.dumps(result, indent=2))
