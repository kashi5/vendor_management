# Vendor Management

This module is used to manage vendors, there purchase orders and vendor performance metrics.

### Stack
- Language - Python 3.10
- Backend Framework - Django rest framework
- Database - PostgreSQL

## Pre-requisites
-  Install docker on you system if it is not installed.
- https://docs.docker.com/get-docker/
- https://docs.docker.com/compose/install/

# Installation 💿
- To run the docker, build the image for any changes
    ```bash
    docker-compose build
    ```
- To start the app
    ```bash
    docker-compose up 
    ```
- Run migrations
    ```bash
    docker-compose run --rm vendor_management python manage.py migrate
    ```
- Run Test suite
    ```bash
    docker-compose run --rm vendor_management python manage.py test
    ```
- To stop the conatiner
    ```bash
    docker-compose down 
    ```
- To check the API swagger documnetation
    ```bash
    http://localhost:8000/api/docs
    ```
