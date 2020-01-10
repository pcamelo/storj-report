import os
import json
import time
import requests
import requests_unixsocket
from elasticsearch import Elasticsearch

NAME=os.environ.get("NAME", "storj")
SLACK_WEBHOOK_URL=os.environ.get("SLACK_WEBHOOK_URL", "")
ELASTICSEARCH_HOST=os.environ.get("ELASTICSEARCH_HOST", "elasticsearch")
ELASTICSEARCH_HOST=os.environ.get("ELASTICSEARCH_HOST", "9200")
STORJ_DASHBOARD_URLS=os.environ.get("STORJ_DASHBOARD_URLS", "")

# Storage nodes Auto-discovery 
with requests_unixsocket.monkeypatch():
    try:
        containers = requests.get('http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/json')
        if containers.status_code == 200:
            for container in containers.json():
                imagename = container.get("Image")
                ports = container.get("Ports")

                print(json.dumps(container, indent=4))
    except:
        print("Docker socket not found")

time.sleep(10)