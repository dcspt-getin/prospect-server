# Prospect API

## Run Locally

Requires Docker and Docker Compose. To run, execute:

To run execute:

```bash
docker-compose up
```

To enter inside of container execute:

```bash
docker exec -ti protc-server_web_1 bash
```

## Deployment

Define environment variables:

```bash
DB_HOST=postgres
DB_PORT=5432
DB_PASSWORD=password
DB_USER=prospect
DB_NAME=prospect
CLIENT_BASE_URL=https://dcspt-getin.ua.pt/prospect/
ADMIN_URL_PREFIX=prospect/
STATIC_URL_PREFIX=/prospect
MEDIA_URL_PREFIX=https://dcspt-getin.ua.pt/prospect
SENDGRID_API_KEY=sdsdsad
EMAIL_FROM=dcspt-getin@ua.pt
DEBUG=1
ALLOWED_HOSTS=dcspt-drivitup.ua.pt,dcspt-getin.ua.pt
```

`DB_HOST` This variable specifies the hostname or IP address of the PostgreSQL database server. In this case, it's set to "postgres."

`DB_PORT` This variable defines the port number on which the PostgreSQL database server is running. The default port for PostgreSQL is 5432.

`DB_PASSWORD` This variable holds the password required to authenticate and access the PostgreSQL database.

`DB_USER` The username used to connect to the PostgreSQL database.

`DB_NAME` This variable specifies the name of the PostgreSQL database to be used, which is "prospect" in this case.

`CLIENT_BASE_URL` This variable represents the base URL for the client application. It seems to be pointing to "https://dcspt-getin.ua.pt/prospect/."

`ADMIN_URL_PREFIX` This variable is likely used as a prefix for the admin URL. It's set to "prospect/" in this case.

`STATIC_URL_PREFIX` This variable might be defining the prefix for static files' URLs. It's set to "/prospect."

`MEDIA_URL_PREFIX` Similar to the CLIENT_BASE_URL, this variable defines the base URL for media files, such as images or uploads.

`SENDGRID_API_KEY` This variable holds the API key for SendGrid, a service that can be used for sending emails.

`EMAIL_FROM` The email address used as the sender when sending emails.

`DEBUG` This variable is likely used to enable debugging. When set to 1, it indicates that the application is in debug mode, which is useful for identifying and fixing issues during development.

`ALLOWED_HOSTS` A list of host/domain names splitted by comma that this Django site can serve. As example could be `dcspt-drivitup.ua.pt,dcspt-getin.ua.pt`

_Note_: `DEBUG=1` for incomplete production server deployment.

### Build

First remove the last image built before if exists

```bash
docker rmi -f nmsilva90s/housepref-api
```

Build the image locally

```bash
docker build . -f compose/django/Dockerfile --no-cache -t nmsilva90s/housepref-api
```

Publish the image to Docker registry

```bash
docker login --username nmsilva90s -p <auth-login-key>

docker push nmsilva90s/housepref-api:latest
```

Go to Portainer and pull the latest image and restart the container to run witth most recent container

### Nginx Configuration

```
server {
  ...

  location /prospect/api/ {
		proxy_pass http://193.137.172.44:8001/api/;
    proxy_redirect off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  location /prospect/static-backend/ {
    proxy_pass http://193.137.172.44:8001/prospect/static-backend/;
    proxy_redirect off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  location /prospect/media/ {
    proxy_pass http://193.137.172.44:8001/prospect/media/;
    proxy_redirect off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  location /prospect/admin/ {
    proxy_pass http://193.137.172.44:8001/prospect/admin/;
    proxy_redirect off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  ...
}
```

### Caddy Configuration

```
example.com {
    ...

    handle /prospect/api/* {
        uri strip_prefix /prospect
        reverse_proxy 127.0.0.1:8001
    }

    handle /prospect/static-backend/* {
        reverse_proxy 127.0.0.1:8001
    }

    handle /prospect/media/* {
        reverse_proxy 127.0.0.1:8001
    }

    handle /prospect/admin/* {
        reverse_proxy 127.0.0.1:8001
    }

    ...
}

```

## Setup

### Enter on the docker container

Execute this command inside the server:

```bash
docker exec -it <container-name> /bin/bash
```

Or, use Portainer to connect.

### Create a new super user to enter on admin

Execute this command:

```bash
python manage.py createsuperuser
```

Insert the requested credentials on command line
After try to login on admin with credentials created for super admin user

## Database

### Enter on the docker container

Execute this command inside the server:

```bash
docker exec -it <container-name> /bin/bash
```

Or, use Portainer to connect.

## Backup database

Execute this command:

```bash
bash backup.sh
```

## Restore database

Execute this command:

```bash
bash restore.sh
```

_Note: Not recommended for prod instances; do it manually or create a new instance._

### Dump with Docker command

```bash
docker exec -i protc-server_db_1 /bin/bash -c "PGPASSWORD=password pg_dump --username user django_db" > ./dump.sql
```
