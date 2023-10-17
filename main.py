from fastapi import FastAPI, Request, Response
import httpx
import logging
import yaml
import os

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(name)s - %(asctime)s - %(message)s')

# Load the configuration from the YAML file
config_path = os.getenv("CONFIG_PATH", "config.yaml")
with open(config_path, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

target_server_url = config.get("target_server_url")
excluded_headers = config.get("response_excluded_headers", [])
included_headers = config.get("request_included_headers", [])

@app.get("/{path:path}")
@app.post("/{path:path}")
@app.put("/{path:path}")
@app.patch("/{path:path}")
@app.delete("/{path:path}")
async def proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f"{target_server_url}/{path}"

        headers = {}
        for header, value in request.headers.items():
            if header in included_headers:
                headers[header] = value
        
        logger.info(f"Target request: {request.method} {target_url} {headers}")
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=request.stream(),
        )
        logger.info(response)

        proxy_response = Response(content=response.content, status_code=response.status_code)
        for header, value in response.headers.items():
            if not header in excluded_headers:
                proxy_response.headers[header] = value

        return proxy_response


@app.middleware("http")
async def proxy_handler(request, call_next):
    logger.info(f"Request received: {request.method} {request.url}")
    
    response = await call_next(request)
    return response
