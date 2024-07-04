# Club Category Server 

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Basic Settings

### Requirements
   Check `./requirements.txt`


## Basic Commands

### Type checks

Running type checks with mypy:

    $ mypy community

### Create Migration File

Create Migrations files:

    $ python manage.py makemigrations

### Apply Migrate

Apply migration to the entire project:

    $ python manage.py migrate

Apply migration to individual apps:

    $ python manage.py migrate `app-name`

### Live reloading and Sass CSS compilation

Moved
to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Change Environment Settings

Follow this step if you want to set your environment setting in Local.  
1. Install autoenv  
   `$ brew install autoenv`
2. Create to .env file with this text.  
   `DJANGO_SETTINGS_MODULE=config.settings."env-name"`
3. Choose env setting you want.
4. Apply env setting.  
Type `$ cd .` OR Create new Session in Terminal 


## Deployment
This repository uses GitHub Actions and AWS Elastic Beanstalk (EB) to automate the Continuous Integration (CI) and Continuous Deployment (CD) process. The CI/CD pipeline is designed to deploy the application to different environments based on the Git branches: `dev`, `stg`, and `production`.

### Workflow Overview

The CI/CD pipeline is configured as follows:

- Pushing code to the `dev` branch triggers the deployment to the development environment.
- Pushing code to the `stg` branch triggers the deployment to the staging environment.
- Pushing code to the `production` branch triggers the deployment to the production/live environment.

### Prerequisites

Before setting up the CI/CD pipeline, make sure you have the following prerequisites in place:

1. An AWS Elastic Beanstalk (EB) environment set up for each target environment (development, staging, and production).
2. AWS credentials and environment variables configured securely in your GitHub repository settings.
3. AWS Elastic Beanstalk CLI (`eb` command) installed in your CI/CD environment.

### GitHub Secrets

In order to securely store AWS credentials and environment-specific configuration, we use GitHub Secrets. Make sure you have set up the following GitHub Secrets in your repository:

- `AWS_ACCESS_KEY_ID`: The AWS access key for your IAM user.
- `AWS_SECRET_ACCESS_KEY`: The AWS secret key for your IAM user.
- `APPLICATION_NAME`: The AWS region where your Elastic Beanstalk environments are located.
- `ENVIRONMENT_ENV_NAME`: Each name is different for env settings.
  - `ENVIRONMENT_DEV_NAME`: The name of the Elastic Beanstalk environment for the development branch.
  - `ENVIRONMENT_STG_NAME`: The name of the Elastic Beanstalk environment for the staging branch.
  - `ENVIRONMENT_PROD_NAME`: The name of the Elastic Beanstalk environment for the production branch.


### Workflow Configuration

The CI/CD workflow is defined in the `.github/workflows/'ENV_NAME'.yml` file. The workflow consists of the following stages:

1. **Build**: Build the application.
2. **Deploy**: Deploy the application to the appropriate Elastic Beanstalk environment based on the branch.

If you want to see the documentation, Moved
to [docs](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

## Celery Local Setting

https://cscheng.info/2018/01/26/installing-pycurl-on-macos-high-sierra.html

Install openssl and pycurl, and Run Celery worker for this `Project-Name`

### Celery Setting

    $ brew install openssl

    $ pip uninstall pycurl
    $ pip install --install-option="--with-openssl" --install-option="--openssl-dir=/opt/homebrew/opt/openssl@3" pycurl

### Celery Run Command

    $ celery -A community worker --loglevel=INFO

### Celery Beat Run Command

    $ celery beat -A community worker --loglevel=INFO



