docker-compose down 
docker-compose build
docker-compose up -d
docker-compose exec web chmod -R 777 .
docker-compose exec web python3 manage.py makemigrations 
docker-compose exec web python3 manage.py migrate 
docker-compose exec web python3 manage.py createsuperuser
docker-compose exec web sh -c crond
