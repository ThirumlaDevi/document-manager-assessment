# Propylon Document Manager Assessment

The Propylon Document Management Technical Assessment is a simple (and incomplete) web application consisting of a basic API backend and a React based client.  This API/client can be used as a bootstrap to implement the specific features requested in the assessment description. 

## Getting Started
### Pre-requisites
1. [Install Direnv](https://direnv.net/docs/installation.html)
   - Make sure to hook the package into you shell to directly take set environment variables from .envrc file ([reference](https://shivamarora.medium.com/a-guide-to-manage-your-environment-variables-in-a-better-way-using-direnv-2c1cd475c8e))
2. [Install Pipenv](https://pipenv.pypa.io/en/latest/installation/)
3. This project requires Python 3.11 so you will need to ensure that this version of Python is installed on your OS before building the virtual environment.
    - Instructions on how to hook the python version from pipenv over local version (if not 3.11) can be referred [here](https://stackoverflow.com/a/34156303)
4. [Install npm](https://nodejs.org/en/download/package-manager)
    - This project was tested with npm version 10.1 .
5. [Install plsql](https://www.postgresql.org/download/) version 12.15

### How to run application in local
1. Run `direnv allow` to approve the local `.envrc` variables.
2. `$ pipenv install -r requirements/local.txt`.  
   - If Python 3.11 is not the default Python version on your system you may need to explicitly create the virtual environment (`$ python3.11 -m venv .venv`) prior to running the install command. 
3. `$ pipenv run python manage.py makemigrations file_version` to create separate migration files for any model changes
4. Create the database and respective tables in the default sqlite3 database using following commands:
`$ pipenv run python manage.py migrate file_versions` 

5. Django doesn't create plsql database automatically, hence follow the following commands in psql command line for local development
```
CREATE DATABASE chunk_data;
CREATE USER dev WITH PASSWORD 'localDevPassword';
GRANT ALL PRIVILEGES ON DATABASE chunk_data TO dev;
GRANT insert on chunks to dev;
GRANT select on chunks to dev;
ALTER ROLE dev SET timezone TO 'UTC';
```
_Note: Grant permission reference https://stackoverflow.com/q/9325017_
Applying migrations on different databases from the same app is also not supported in django, hence run the following commands too
```
CREATE TABLE chunks ( 
    orgId INTEGER, 
    userId INTEGER, 
    chunkId char(34), 
    created_at_epoc INTEGER,
    data BYTEA,
    PRIMARY KEY(orgId, userId, chunkId) );
```
6. `$ pipenv run python manage.py load_file_fixtures` to create the fixture file versions.
7. `$ pipenv run python manage.py runserver 0.0.0.0:8001` to start the development server on port 8001.
8. Navigate to the client/doc-manager directory.
9. `$ npm install` to install the dependencies.
10. `$ npm start` to start the React development server.

_Note: Run step 7,8,10 alone if other setup have been done otherwise and no change has been made to the models/requirement packages for the django and react projects_


[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


_Note: check the [BRAIN-DUMP.md](./BRAIN-DUMP.md) file to learn more about the architectural and logical decisions being made for this application_

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ pipenv run python manage.py createsuperuser --email <email-id>

### Curl request to upload file chunks

```
curl -v POST http://0.0.0.0:8001/api/v1/docs -F chunk=@<file-chunk> \
-H 'details:{"userId":<user-id>,"orgId":<orgid>,"chunkId":<chunk-id>}' 
```

For example
```shell
# command to get chunk id
md5sum cookie.txt
# sample upload that will currently work
curl -v POST http://0.0.0.0:8001/api/v1/docs -F chunk=@cookie.txt \
-H 'details:{"userId":1,"orgId":1,"chunkId":"9d9121966c738889a7624a8e1954a9c7"}' 
```

### Curl request to upload file chunk details

### Type checks

Running type checks with mypy:

    $ mypy propylon_document_manager

### List all the endpoint in the django service
reference taken from [this link](https://stackoverflow.com/a/8844834). Run the following command: 

    $ pipenv run python manage.py show_urls

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
 
## Todo
- ~~Change debug as not true in local.py~~
- ~~Fix errors when running project in local~~
- ~~File currently uses base settings and not local settings passing config.settings.local didn't even host up the file (noob) DJANGO_SETTINGS_MODULE=myapp.production_settings~~
- Stores files of any type and name Uniqueness of name is specific to a user 
Make file upload work in both backend post and frontend
reference https://dev.to/shubhamkshatriya25/ajax-file-upload-in-chunks-using-django-with-a-progress-bar-4nhi
https://github.com/shubhamkshatriya25/AJAX-File-Uploader/tree/master
- Stores files at any URL
A user may submit the file "review.pdf" to the application, specifying "/documents/reviews/review.pdf" as the desired URL. The user later submits a new version of the file at the same URL.
The user can now retrieve the latest version of the file by accessing the document URL ("/documents/reviews/review.pdf"). The original version of the file can be accessed at the URL ("/documents/reviews/review.pdf?revision=0").
- Does not allow interaction by non-authenticated users
- Does not allow a user to access files submitted by another user
- Allows users to store multiple revisions of the same file at the same URL
- Allows users to fetch any revision of any file
- Demonstrate functionality that allows a client to retrieve any given version of documentusing a endpoint that implements a Content Addressable Storage mechanism.
- swagger docs
- restrict file upload path to not be authentication paths
- Make sure all endpoints use django rest auth methods
- check base.py environment file read function ( that might have to be altered)
- Handling common errors like [this](https://stackoverflow.com/questions/73097147/following-error-raised-templatedoesnotexisttemplate-name-chain-chain-django)
- Replace harcoded postgres data information with something else

## Existing errors fixed
- Fix TemplateDoesNotExist due to debug_toolbar
- the auth part of propylon_document_manager is overwritten for the current uploader endpoint
- No DjangoTemplates backend is configured
- Unique constraint failure on Migration when new columns are added. 
    - Reference -> https://stackoverflow.com/a/50456186


