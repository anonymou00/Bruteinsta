#!/usr/bin/env python3
"""
Simple test server with vulnerable forms for XSS scanner testing
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Vulnerable form page
            html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test Forms - XSS Scanner Test</title>
</head>
<body>
    <h1>Test Forms for XSS Scanner</h1>
    
    <!-- Vulnerable Login Form -->
    <h2>Login Form (Vulnerable)</h2>
    <form id="login_form" action="/login" method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="Login">
    </form>
    
    <!-- Vulnerable Search Form -->
    <h2>Search Form (Vulnerable)</h2>
    <form id="search_form" action="/search" method="GET">
        <input type="text" name="q" placeholder="Search query">
        <input type="submit" value="Search">
    </form>
    
    <!-- Contact Form -->
    <h2>Contact Form</h2>
    <form id="contact_form" action="/contact" method="POST">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Message" required></textarea>
        <input type="submit" value="Send Message">
    </form>
    
    <!-- Comment Form -->
    <h2>Comment Form (Vulnerable)</h2>
    <form id="comment_form" action="/comment" method="POST">
        <input type="text" name="author" placeholder="Your Name">
        <textarea name="comment" placeholder="Your Comment"></textarea>
        <input type="submit" value="Post Comment">
    </form>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        elif path == '/search':
            # Vulnerable search endpoint - reflects query without escaping
            search_query = query_params.get('q', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
</head>
<body>
    <h1>Search Results</h1>
    <p>You searched for: {search_query}</p>
    <p>No results found.</p>
    <a href="/">Back to forms</a>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        
        path = self.path
        
        if path == '/login':
            # Vulnerable login endpoint
            username = parsed_data.get('username', [''])[0]
            password = parsed_data.get('password', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Login Result</title>
</head>
<body>
    <h1>Login Attempt</h1>
    <p>Username: {username}</p>
    <p>Login failed - invalid credentials</p>
    <a href="/">Back to forms</a>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        elif path == '/contact':
            # Contact form endpoint
            name = parsed_data.get('name', [''])[0]
            email = parsed_data.get('email', [''])[0]
            message = parsed_data.get('message', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Message Sent</title>
</head>
<body>
    <h1>Thank You!</h1>
    <p>Hello {name}, your message has been received.</p>
    <p>We will reply to {email} soon.</p>
    <div>Your message: {message}</div>
    <a href="/">Back to forms</a>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        elif path == '/comment':
            # Vulnerable comment endpoint
            author = parsed_data.get('author', [''])[0]
            comment = parsed_data.get('comment', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Comment Posted</title>
</head>
<body>
    <h1>Comment Posted</h1>
    <div class="comment">
        <strong>{author} says:</strong>
        <p>{comment}</p>
    </div>
    <a href="/">Back to forms</a>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, VulnerableHandler)
    print(f"Test server running on http://localhost:{port}")
    print("This server contains intentionally vulnerable forms for XSS testing")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()