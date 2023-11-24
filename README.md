# Social Media

## Swagger screens
![Screenshot 2023-11-24 at 13.08.29.png](Readme_images%2FScreenshot%202023-11-24%20at%2013.08.29.png)
![Screenshot 2023-11-24 at 13.08.51.png](Readme_images%2FScreenshot%202023-11-24%20at%2013.08.51.png)

## Getting Started
```
git clone git@github.com:Polyakiv-Andrey/social_media.git
pip install -r requirements.txt
python manage.py migrate
```
create .env file 
```
python manage.py runserver
celery -A social_network worker --loglevel=info  
 ```