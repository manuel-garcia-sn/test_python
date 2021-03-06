# INSTALL PROJECT LOCAL
```
virtualenv py_name_project_env
source py_name_project_env/bin/activate
pip install -r requirements.txt
```

### example
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# RUN virtualenv
```
flask run
```

# Commands utils
```
which python
which pip
pip list
pip freeze --local > requirements.txt
rm -rf py_name_project_env
```


## Fresh Virtualenv Project
```
rm -rf py_name_project_env
```

## Desactivate virtualenv
```
which pip
deactivate
which pip
```

# Create Token Twitter APi
Insert .env file
```
TWITTER_KEY
TWITTER_SECRET
```

- https://developer.twitter.com
- Login user
- Create app
    - App Name: sngularRocks
    - Description: Finally it is to perform a proof of concept with Python to popularize a section of a website with the tweets related to the company.
    - Sign in with Twitter: Disabled
    - Callback URL: None
    - Terms of service URL: None
    - Privacy policy URL: None
    - Organization name: None
    - Organization website URL: None

- View and copy Keys and tokens Tab

# Create MongoDb container
```
docker run -p 27017:27017 -d mongo:latest
```
Now you can connect to DB on localhost:27017

# Commands
Get al tweets with certain hastag
```
python3 main.py twitter_service
```

Calculate user count posts
```
python3 main.py count_service
```