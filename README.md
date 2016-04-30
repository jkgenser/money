# money

### Local Setup

Instructions are for mac only.

Install system requirements using homebrew:

```
brew install python
brew install postgresql
```

This project uses Python2 because it heavily relies on Scrapy, which is not stable for Python3.

Create and activate a virtualenv for this project. From the top of the project:

```
virtualenv venv
source venv/bin/activate
```

Install python dependencies:

```
pip install -r requirements.txt
```

Set local environment variables (which are hooked into Flask through config) using autoenv by following these steps:

```
deactivate
pip install autoenv
touch .env
```

Add the following to the *.env* file:

```
source venv/bin/activate
export APP_SETTINGS="config.DevelopmentConfig"
```

Then run this update and refresh your *.bashrc*:

```
$ echo "source `which activate.sh`" >> ~/.bashrc
$ source ~/.bashrc
```

If you move up a directory and cd back into it, the virtual environment will automatically be started and the APP_SETTINGS variable will be declared. You can add any environment variables to the *.env* file in the future in order for it to be set when you cd to the project. 

Next steps will be to initialize the database. Make sure you have a local postgres server running. 

Create an environment variable `DATABASE_URL="postgresql://localhost/money"` in the *.env* file.

Perform the initial database migration

```
python manage.py db upgrade
```

The project should now be ready for local development.


