import http.server
import socketserver
import json
import os
import urllib.parse
from google.cloud import bigquery

PORT = 8080

class ReaderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == '/logs':
            try:
                client = bigquery.Client()
                
                dataset_id = os.environ.get('billing_logs_dataset_b4k8d_BIGQUERY_DATASET', 'billing_logs_dataset_b4k8d')
                table_id = 'billing_logs_table_b4k8d'
                project_id = client.project
                
                query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}` LIMIT 10"
                
                query_job = client.query(query)
                results = query_job.result()
                
                logs = []
                for row in results:
                    logs.append(row.data)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(logs).encode())
            except Exception as e:
                print(f"Error querying BigQuery: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ReaderHandler) as httpd:
        print(f"Log reader server serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down")
            httpd.server_close()

if __name__ == '__main__':
    run()
