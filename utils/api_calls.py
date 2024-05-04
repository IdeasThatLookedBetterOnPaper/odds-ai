import http.client
import base64
import os
from typing import Mapping


def call_api(method: str, url: str, payload: str, headers: Mapping[str, str]) -> str:
    proxy_host = os.getenv("proxy_host")
    proxy_port = os.getenv("proxy_port")
    proxy_username = os.getenv("proxy_username")
    proxy_password = os.getenv("proxy_password")

    target_host = 'scan-inbf.betfair.com'
    if 'authority' in headers:
        target_host = headers['authority']

    # Set up authentication headers
    auth = base64.b64encode(f"{proxy_username}:{proxy_password}".encode()).decode()
    proxy_headers = {'Proxy-Authorization': 'Basic ' + auth}

    # Connect to the proxy server
    conn = http.client.HTTPSConnection(proxy_host, proxy_port)

    # Send a request to the target server through the proxy
    conn.set_tunnel(target_host, headers=proxy_headers)

    conn.request(method, url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
