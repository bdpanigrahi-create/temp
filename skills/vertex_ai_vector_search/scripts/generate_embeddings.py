import json
import os
import subprocess
import urllib.request
import urllib.error
import argparse

def get_access_token():
    try:
        result = subprocess.run(['gcloud', 'auth', 'print-access-token'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

def get_embedding(text, token, project_id, region):
    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/text-embedding-004:predict"
    
    payload = {
        "instances": [
            {"content": text}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'))
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['predictions'][0]['embeddings']['values']
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(e.read().decode('utf-8'))
        return None
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for text files.")
    parser.add_argument("--input_dir", required=True, help="Directory containing text files.")
    parser.add_argument("--output_file", required=True, help="Path to save output JSONL file.")
    parser.add_argument("--project_id", default="ide-exp", help="GCP Project ID.")
    parser.add_argument("--region", default="us-central1", help="GCP Region.")
    
    args = parser.parse_args()
    
    token = get_access_token()
    if not token:
        print("Could not obtain access token. Exiting.")
        return
    
    if not os.path.exists(args.input_dir):
        print(f"Directory not found: {args.input_dir}")
        return
    
    files = sorted([f for f in os.listdir(args.input_dir) if f.endswith('.txt')])
    
    with open(args.output_file, 'w') as out_f:
        for filename in files:
            filepath = os.path.join(args.input_dir, filename)
            print(f"Processing {filename}...")
            with open(filepath, 'r') as f:
                content = f.read()
            
            incident_id = os.path.splitext(filename)[0]
            
            embedding = get_embedding(content, token, args.project_id, args.region)
            if embedding:
                data = {
                    "id": incident_id,
                    "embedding": embedding
                }
                out_f.write(json.dumps(data) + "\n")
                print(f"Successfully embedded {incident_id}")
            else:
                print(f"Failed to embed {incident_id}")
                
    print(f"Finished processing. Output saved to {args.output_file}")

if __name__ == "__main__":
    main()
