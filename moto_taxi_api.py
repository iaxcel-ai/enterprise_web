import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64

rides_db = {
    "1": {"id": "1", "driver": "Alice", "passenger": "Bob", "status": "pending", "fare": 1500},
    "2": {"id": "2", "driver": "James", "passenger": "Chloe", "status": "in_progress", "fare": 2000},
}

users = {
    "wilson": "wilson123",
    "axcel":  "axcel456",
}

def check_auth(header):
    if not header or not header.startswith('Basic '):
        return False
    encoded_credentials = header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    input_username, input_password = decoded_credentials.split(':', 1)
    return users.get(input_username) == input_password

class MotoTaxiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        header = self.headers.get('Authorization', None)
        if not check_auth(header):
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.send_header('WWW-Authenticate', 'Basic realm="Access to /rides"')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid username or password"}).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"rides": list(rides_db.values())}).encode('utf-8'))

    def do_DELETE(self):
        header = self.headers.get('Authorization', None)
        if not check_auth(header):
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.send_header('WWW-Authenticate', 'Basic realm="Access to /rides"')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid username or password"}).encode('utf-8'))
            return

        path_parts = self.path.strip('/').split('/')

        if len(path_parts) != 2 or path_parts[0] != 'rides':
            self.send_response(404)
            self.end_headers()
            return

        ride_id = path_parts[1]

        if ride_id not in rides_db:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Ride '{ride_id}' not found."}).encode('utf-8'))
            return

        deleted = rides_db.pop(ride_id)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Ride deleted.", "ride": deleted}).encode('utf-8'))

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MotoTaxiHandler)
    print(f'Starting server on port {server_address[1]}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()