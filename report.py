import os
import sys
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
STORJ_IMAGENAME=os.environ.get("STORJ_IMAGENAME", "storjlabs/storagenode:beta")

if STORJ_DASHBOARD_URLS:
    dashboard_urls = STORJ_DASHBOARD_URLS.split(",")
else:
    # Storage nodes Auto-discovery
    dashboard_urls = []
    with requests_unixsocket.monkeypatch():
        try:
            containers = requests.get('http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/json')
        except:
            print("No endpoints found, aborting ...")
            sys.exit(1)

        if containers.status_code != 200:
            print("No endpoints found, aborting ...")
            sys.exit(1)

        for container in containers.json():
            image = container.get("Image")
            if image not in STORJ_IMAGENAME:
                continue

            public_port = 14002
            for entry in container.get("Ports", []):
                if entry.get("PrivatePort") != 14002:
                    continue
                # else storj node
                public_port = entry.get("PublicPort")
                dashboard_urls.append("127.0.0.1:{}".format(public_port))

    print(json.dumps(dashboard_urls, indent=4))

time.sleep(10)