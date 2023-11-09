# Prospect API

## Run locally

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
```

_Note_: `DEBUG=1` for incomplete production server deployment.

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
