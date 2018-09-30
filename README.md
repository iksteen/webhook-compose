# webhook-compose

Small flask web application that can run in docker to trigger
```
docker-compose pull && \
	docker-compose up -d --build
```
in response to a HTTP request.

Example docker-compose.yml:

```
version: "2"

services:
  updater:
    build: .
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./webhook-compose.conf:/webhook-compose.conf
      - ../web:/projects/web
```

Example webhook-compose.conf (based on drone webhook):
```
{
  "projects/web:web": {
    "body": {
      "repo": {
        "owner": "iksteen",
        "name": "blurringexistence.net"
      },
      "build": {
         "ref": "refs/heads/master"
      }
    }
  }
}
```
