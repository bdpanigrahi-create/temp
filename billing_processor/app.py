import http.server
import socketserver
import urllib.parse
import json
import sys
import os

# Add the current directory to path so we can import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import processor

PORT = 8080

class BillingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == '/process':
            query = urllib.parse.parse_qs(parsed_url.query)
            tx_id = query.get('tx_id', [None])[0]
            if not tx_id:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing tx_id')
                return
            
            # Simulate large payload to speed up OOM
            data = "X" * 1024 * 1024 # 1MB
            
            processor.process_transaction(tx_id, data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Processed {tx_id}. Cache size: {processor.get_cache_size()}'.encode())
            
        elif parsed_url.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                'cache_size': processor.get_cache_size()
            }
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run():
    # Allow reuse of address to avoid "Address already in use" errors on restart
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BillingHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down")
            httpd.server_close()

if __name__ == '__main__':
    run()
