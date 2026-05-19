import http.server
import json
import os
import subprocess
import sys
import threading

PORT = 8105
PROCESS = None

class MCPBridgeHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        global PROCESS
        if PROCESS is None or PROCESS.poll() is not None:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"MCP server not running")
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        print(f"Forwarding to MCP: {post_data.decode('utf-8')}")
        
        # Write to subprocess stdin
        PROCESS.stdin.write(post_data + b"\n")
        PROCESS.stdin.flush()
        
        # Read from subprocess stdout
        # This assumes the response is a single line
        response_line = PROCESS.stdout.readline()
        print(f"Received from MCP: {response_line.decode('utf-8')}")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response_line)

    def do_GET(self):
        # Handle health check or discovery if needed
        # For now, just return a static response or proxy it if possible
        # The standard server might not respond to GET on stdio in a way that maps to HTTP
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "running", "note": "This is a bridge to stdio MCP server"}')

def run_mcp_server():
    global PROCESS
    token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
    if not token:
        print("ERROR: GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set.")
        sys.exit(1)
        
    # Run the server using npx
    # We need to make sure it uses the token
    env = os.environ.copy()
    
    print("Starting real GitHub MCP server via npx...")
    PROCESS = subprocess.Popen(
        ['npx', '-y', '@modelcontextprotocol/server-github'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Thread to read stderr and print it to logs
    def log_stderr(pipe):
        for line in iter(pipe.readline, b''):
            print(f"[MCP STDERR] {line.decode('utf-8').strip()}", file=sys.stderr)
            
    threading.Thread(target=log_stderr, args=(PROCESS.stderr,), daemon=True).start()
    
    print(f"Bridge listening on port {PORT}...")
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MCPBridgeHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_mcp_server()
