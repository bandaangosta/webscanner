# Web Scanner

Gives your typical flatbed USB scanner a simple, yet very efficient web interface.

![Screenshot](docs/main.png) ![Screenshot](docs/options.png)

## Quick Start

Run the application:

    make run

And open it in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


## Prerequisites

This is built to be used with Python 3. Update `Makefile` to switch to Python 2 if needed.

Some Flask dependencies are compiled during installation, so `gcc` and Python header files need to be present.
For example, on Ubuntu:

    apt install build-essential python3-dev


## Development environment and release process

 - create virtualenv with Flask and Web Scanner installed into it (latter is installed in
   [develop mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode) which allows
   modifying source code directly without a need to re-install the app): `make venv`

 - run development server in debug mode: `make run`; Flask will restart if source code is modified

 - run tests: `make test` (see also: [Testing Flask Applications](http://flask.pocoo.org/docs/0.12/testing/))

 - create source distribution: `make sdist` (will run tests first)

 - to remove virtualenv and built distributions: `make clean`

 - to add more python dependencies: add to `install_requires` in `setup.py`

 - to modify configuration in development environment: edit file `settings.cfg`; this is a local configuration file
   and it is *ignored* by Git - make sure to put a proper configuration file to a production environment when
   deploying


## Deployment

See [Flask Deployment Options](http://flask.pocoo.org/docs/1.0/deploying/) for a number of ways to deploy your web application. For example, by using Apache and mod_wsgi.

## Deployment with Docker (experimental)

Install Docker (in this example, on a Raspberry Pi) following the [Documentation](https://docs.docker.com/install/linux/docker-ce/debian/#upgrade-docker-after-using-the-convenience-script).
In the same folder as the Dockerfile, run the following to build the image:
    
    docker build -t webscanner .

You can test the web application is working by running the following and visiting the IP address of your device on a browser:
    
    docker run -it --rm -p 80:5000 --name webscanner_container webscanner

Leave it running in the background:
    
    docker run -d --rm -p 80:5000 --name webscanner_container webscanner

Leave it running in the background and restart automatically, particularly on server reboot:
    
    docker run -d -p 80:5000 --restart unless-stopped --name webscanner_container webscanner
