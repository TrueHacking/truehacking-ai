from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        secure = self.path.startswith('/seguro')
        body = ('<!doctype html><html><head><title>Laboratório True Hacking AI</title></head>'
                '<body><h1>Olá, comunidade!</h1><p>Laboratório educacional Docker.</p></body></html>').encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        if secure:
            self.send_header('Content-Security-Policy', "default-src 'none'")
            self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers()
        self.wfile.write(body)

HTTPServer(('0.0.0.0', 3000), Handler).serve_forever()
