import functions_framework
import asyncio
from src.main import app

@functions_framework.http
def star_wars_api(request):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    scope = {
        "type": "http",
        "method": request.method,
        "path": request.path,
        "raw_path": request.path.encode(),
        "query_string": request.query_string,
        "headers": [[k.encode(), v.encode()] for k, v in request.headers],
        "client": [request.remote_addr, 0] if request.remote_addr else None,
        "server": ["localhost", 8080],
        "scheme": "http",
    }
    
    body_received = False
    async def receive():
        nonlocal body_received
        if not body_received:
            body_received = True
            return {"type": "http.request", "body": request.data or b""}
        return {"type": "http.request", "body": b""}
    
    status_code = 200
    headers = []
    body_parts = []
    
    async def send(message):
        nonlocal status_code, headers, body_parts
        if message["type"] == "http.response.start":
            status_code = message["status"]
            headers = message["headers"]
        elif message["type"] == "http.response.body":
            body_parts.append(message.get("body", b""))
    
    loop.run_until_complete(app(scope, receive, send))
    body = b"".join(body_parts)
    response_headers = [(k.decode(), v.decode()) for k, v in headers]
    
    return body, status_code, response_headers
