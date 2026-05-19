import http.server
import socketserver
import json
import base64

PORT = 8080

class AlertingHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            envelope = json.loads(post_data.decode('utf-8'))
            payload = base64.b64decode(envelope['message']['data']).decode('utf-8')
            data = json.loads(payload)
            
            print(f"Received log event: {data}")
            
            # Check for alert condition (e.g., cache size too large)
            if data.get('cache_size', 0) > 1000: # Arbitrary threshold
                print(f"ALERT: Cache size is large: {data['cache_size']}")
                # In a real app, we would send an email, slack message, or trigger an incident.
                
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            print(f"Error processing message: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Error')

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AlertingHandler) as httpd:
        print(f"Alerting server serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down")
            httpd.server_close()

if __name__ == '__main__':
    run()
