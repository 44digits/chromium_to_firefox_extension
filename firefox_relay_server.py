import http.server
import json
import subprocess
import urllib.parse

PORT = 18080

class LinkHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight requests from the extension
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/open':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                url = data.get('url')
                
                if url:
                    print(f"[+] Opening URL in Firefox: {url}")
                    # Launch firefox using subprocess
                    subprocess.Popen(['firefox', url])
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                    return
            except Exception as e:
                print(f"[-] Error: {e}")
                
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "failed"}).encode('utf-8'))

def run():
    server_address = ('127.0.0.1', PORT)
    httpd = http.server.HTTPServer(server_address, LinkHandler)
    print(f"[ * ] Python Link-Relay Server running on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[ * ] Shutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
