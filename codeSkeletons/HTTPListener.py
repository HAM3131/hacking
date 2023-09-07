from http.server import SimpleHTTPRequestHandler, HTTPServer
import requests

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Received GET request")
        print(f"Received GET request on path: {self.path}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Received POST request")
        print(f"Received POST request with data: {post_data.decode('utf-8')}")

def get_public_ip():
    try:
        # Using a third-party service to get the public IP
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
        return ip
    except Exception as e:
        print(f"Error getting public IP: {e}")
        return "Unknown"

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, port=7788):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

   # Get the public IP address of the current machine
    public_ip = get_public_ip()

    print(f"Server Address: {public_ip}:{port}")
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()