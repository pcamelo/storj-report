docker build . -t storj-report-dev -f Dockerfile.dev
docker run \
    -v "$(pwd)":/app:ro \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    storj-report-dev