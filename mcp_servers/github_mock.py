import http.server
import json
import os
import sys

PORT = 8105

class MCPMockHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        print(f"Received request: {post_data.decode('utf-8')}")
        
        try:
            request_json = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return
        
        # Simple mock response
        response = {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": "Mock success: Branch pushed successfully (simulated)."
                    }
                ]
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        # Handle discovery or health check
        response = {
            "tools": [
                {
                    "name": "git_push_branch",
                    "description": "Push a local branch to remote GitHub repository.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "branch": {"type": "string"},
                            "repo": {"type": "string"}
                        },
                        "required": ["branch"]
                    }
                }
            ]
        }
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run():
    server_address = ('', PORT)
    try:
        httpd = http.server.HTTPServer(server_address, MCPMockHandler)
        print(f"Starting mock MCP server on port {PORT}...")
        httpd.serve_forever()
    except OSError as e:
        print(f"Could not bind to port {PORT}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
