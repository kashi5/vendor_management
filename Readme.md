# Vendor Management

This module is used to manage vendors, there purchase orders and vendor performance metrics.

### Stack
- Language - Python 3.10
- Backend Framework - Django rest framework
- Database - PostgreSQL

## Pre-requisites
- clone the git repository

    ```bash
    git clone https://github.com/kashi5/vendor_management.git
    ```

-  Install docker on you system if it is not installed.
- https://docs.docker.com/get-docker/
- https://docs.docker.com/compose/install/


# Installation 💿
- Follow the steps in a chronological order to access the APIs
- Enter the project root folder
    ```bash
    cd vendor_management
    ```

- To run the docker, build the image for any changes
    ```bash
    docker-compose build
    ```

- To start the app
    ```bash
    docker-compose up -d
    ```

- Wait for 3 or 4 minutes after the above command is run. Run database migrations
    ```bash
    docker-compose run --rm vendor python manage.py migrate
    ```

- Run Test suite
    ```bash
    docker-compose run --rm vendor python manage.py test
    ```

- To check the API swagger documnetation
    ```bash
    http://0.0.0.0:8000/api/docs/
    ```

- To access any APIs, register as user check the doumentation
    ```bash
    http://0.0.0.0:8000/api/register/
    ```

- Once registered, access the token. To access any other APIs you need to add the token in the header as Authorization Token <token_value>
    ```bash
    http://0.0.0.0:8000/api/token/
    ```

- To stop the docker container
    ```bash
    docker-compose down 
    ```
#### Note
- Filter based on vendor id on purchase order list endpoint not documented on swagger.
    - http://0.0.0.0:8000/api/purchase_orders/?vendor_id=uuid

-   ```baash
    http://localhost:8000/api/docs/   # we can use localhost too
    ```