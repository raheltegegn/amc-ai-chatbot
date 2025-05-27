from app import app

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 5000, app)
    server.serve_forever()