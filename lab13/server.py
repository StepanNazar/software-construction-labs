import re
from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader
import os
from urllib.parse import parse_qs

template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))
db = {}


def process_form(environ: dict) -> str:
    """Process the form data and return the response"""
    content_length = int(environ.get("CONTENT_LENGTH", 0))
    post_data = parse_qs(environ["wsgi.input"].read(content_length).decode("utf-8"))
    name = post_data.get("name", "")[0].strip()
    email = post_data.get("email", "")[0].strip()
    age = post_data.get("age", "")[0].strip()
    errors = []
    if email in db:
        errors.append("Email already exists")
    if not name:
        errors.append("Name is required")
    if not email:
        errors.append("Email is required")
    if not age:
        errors.append("Age is required")
    if not re.match(r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", email):
        errors.append("Invalid email")
    try:
        age = int(age)
        if age < 0:
            errors.append("Age must be a positive number")
        elif age > 150:
            errors.append("You can't be that old!")
    except ValueError:
        errors.append("Age must be a number")
    if not errors:
        template = env.get_template("info.html")
        submitted_data = {"name": name, "email": email, "age": age}
        db[email] = submitted_data
        response = template.render(submitted_data=submitted_data, success=True)
    else:
        template = env.get_template("info.html")
        response = template.render(errors=errors)
    return response


def application(environ: dict, start_response: callable):
    path = environ.get("PATH_INFO", "").lstrip("/")
    method = environ["REQUEST_METHOD"]
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]
    if path == "":
        template = env.get_template("index.html")
        response = template.render()
    elif path == "info":
        if method == "POST":
            response = process_form(environ)
        else:
            template = env.get_template("info.html")
            response = template.render()
    else:
        status = "404 Not Found"
        response = "404 Not Found"
    response = response.encode("utf-8")
    start_response(status, headers)
    return [response]


if __name__ == "__main__":
    port = 8000
    with make_server("", 8000, application) as httpd:
        print(f"Server started on localhost:{port}")
        httpd.serve_forever()
