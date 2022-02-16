heroku container:login
docker login --username=_ --password=$(heroku auth:token) registry.heroku.com

docker rmi -f registry.heroku.com/thawing-wildwood-49356/web
docker build . -f compose/django/Dockerfile --no-cache -t registry.heroku.com/thawing-wildwood-49356/web

docker push registry.heroku.com/thawing-wildwood-49356/web
heroku container:release web
