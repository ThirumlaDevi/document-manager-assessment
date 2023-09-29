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
    - This project was tested with 10.1 npm version.

### How to run application in local
1. Run `direnv allow` to approve the local `.envrc` variables.
2. `$ pipenv install -r requirements/local.txt`.  If Python 3.11 is not the default Python version on your system you may need to explicitly create the virtual environment (`$ python3.11 -m venv .venv`) prior to running the install command. 
3. `$ pipenv run python manage.py migrate` to create the database.
4. `$ pipenv run python manage.py load_file_fixtures` to create the fixture file versions.
5. `$ pipenv run python manage.py runserver 0.0.0.0:8001` to start the development server on port 8001.
6. Navigate to the client/doc-manager directory.
7. `$ npm install` to install the dependencies.
8. `$ npm start` to start the React development server.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

_Note: check the [BRAIN-DUMP.md](./BRAIN-DUMP.md) file to learn more about the architectural and logical decisions being made for this application_

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

### Type checks

Running type checks with mypy:

    $ mypy propylon_document_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

## Todo
- Change debug as not true in local.py
- Stores files of any type and name
Uniqueness of name is specific to a user 
- Stores files at any URL
A user may submit the file "review.pdf" to the application, specifying "/documents/reviews/review.pdf" as the desired URL. The user later submits a new version of the file at the same URL.
The user can now retrieve the latest version of the file by accessing the document URL ("/documents/reviews/review.pdf"). The original version of the file can be accessed at the URL ("/documents/reviews/review.pdf?revision=0").
- Does not allow interaction by non-authenticated users
- Does not allow a user to access files submitted by another user
- Allows users to store multiple revisions of the same file at the same URL
- Allows users to fetch any revision of any file
- Demonstrate functionality that allows a client to retrieve any given version of documentusing a endpoint that implements a Content Addressable Storage mechanism.
