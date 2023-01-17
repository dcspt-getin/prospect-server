
docker rmi -f nmsilva90s/housepref-api
docker build . -f compose/django/Dockerfile --no-cache -t nmsilva90s/housepref-api

docker login --username nmsilva90s -p 30ffa2f6-f7e8-4b64-a08a-386e82709ef2
docker push nmsilva90s/housepref-api:latest

# https://193.137.172.44:9443/
# sh -c python\ manage.py\ collectstatic\ --no-input\;\ python\ manage.py\ migrate\;\ gunicorn\ mydjango.wsgi\ -b\ 0.0.0.0:\$PORT