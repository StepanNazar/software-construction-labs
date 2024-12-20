from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    if path == '':
        template = env.get_template('index.html')
        response = template.render()
    elif path == 'info':
        template = env.get_template('info.html')
        response = template.render()
    else:
        status = '404 Not Found'
        response = '404 Not Found'
    response = response.encode('utf-8')
    start_response(status, headers)
    return [response]

if __name__ == '__main__':
    port = 8000
    with make_server('', 8000, application) as httpd:
        print(f'Server started on localhost:{port}')
        httpd.serve_forever()