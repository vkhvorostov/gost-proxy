from fastapi import FastAPI, Request, Response
from cipher.text_cipher import text_cipher
import httpx
import logging
import yaml
import os

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(name)s - %(asctime)s - %(message)s')
logger.setLevel(logging.DEBUG)

# Load the configuration from the YAML file
config_path = os.getenv("CONFIG_PATH", "config.yaml")
with open(config_path, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

target_server_url = config.get("target_server_url")
excluded_headers = config.get("response_excluded_headers", [])
included_headers = config.get("request_included_headers", [])
mode = config.get("mode")
cipher = text_cipher(config.get("key"), config.get("alg"))

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
        
        logger.info(f"Target request: {request.method} {target_url}")
        logger.debug(f"Headers: {headers}")
        body = await request.body()
        if mode == 'client':
            logger.debug(f"Body: {body}")
            converted_body = cipher.encrypt(body)
            logger.debug(f"Cipherbody: {converted_body.hex()}")
        elif mode == 'server':
            logger.debug(f"Cipherbody: {body.hex()}")
            converted_body = cipher.decrypt(body)
            logger.debug(f"Body: {converted_body}")
        else:
            raise ValueError("Wrong mode value")
        

        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=converted_body,
        )
        logger.debug(f"Response: {response.content}")

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
