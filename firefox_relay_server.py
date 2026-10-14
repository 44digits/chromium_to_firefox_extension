"""Firefox Relay Server.

Date: 2026-10-13
User: 44digits

This module runs a small local HTTP server that accepts a JSON payload
containing a URL and launches that URL in Firefox. It is intended to act as
an internal relay between a browser extension and Firefox, allowing the
extension to request that a link be opened externally.
"""

import http.server
import json
import subprocess

PORT = 18080

class LinkHandler(http.server.BaseHTTPRequestHandler):
    """Handle incoming HTTP requests from the browser extension."""

    def do_OPTIONS(self):
        """Respond to CORS preflight requests from the extension.

        This allows the browser to send POST requests from the extension
        origin without being blocked by the same-origin policy.
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Process JSON requests to open a URL in Firefox.

        Expected payload:
            {"url": "https://example.com"}

        If a valid URL is provided, the server launches Firefox with that
        page. Otherwise, it returns a 400 error response.
        """
        if self.path == '/open':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                url = data.get('url')

                if url:
                    print(f"[+] Opening URL in Firefox: {url}")
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
    """Start the local relay server and keep it running until interrupted."""
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
