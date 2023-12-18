import shared  # Importing a shared module (to hold data across the application)

import http.server  # Importing modules for creating an HTTP server
import socketserver  # Importing modules for handling socket connections
import threading  # Importing modules for managing threads
import json  # Importing the JSON module for data serialization

# Create a custom handler by inheriting from BaseHTTPRequestHandler
class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Respond to GET requests with a 200 status code and appropriate headers
        self.send_response(200)
        self.send_header('Content-type', 'text/json')  # Set the content type to JSON
        self.end_headers()

        # Convert shared.clan_data into pretty-printed JSON with indentation
        pretty_json = json.dumps(shared.clan_data, indent=4)
        self.wfile.write(pretty_json.encode('utf-8'))  # Write the JSON response to the client

# Create a server class by mixing ThreadingMixIn with HTTPServer
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

# Create a function to run the server in a separate thread
def run_server_in_thread():
    server_address = ('', 8080)  # Define the server address and port
    httpd = ThreadedHTTPServer(server_address, MyHttpRequestHandler)  # Create a threaded HTTP server
    print("Server running at port 8080")  # Print a message indicating the server is running
    httpd.serve_forever()  # Start serving HTTP requests indefinitely

# Function to start the HTTP server in a separate thread
def start_server():
    server_thread = threading.Thread(target=run_server_in_thread)  # Create a new thread for the server
    server_thread.start()  # Start the server thread
