# Simple Trading
A simple trading project

## Requirements
Latest Docker Desktop
- [docker-desktop](https://docs.docker.com/desktop/)

or

Latest Docker and Docker Compose for your OS
- [docker-machine](https://docs.docker.com/engine/installation/)
- [docker-compose](https://docs.docker.com/compose/install/)

Postgresql for psql command
- [postgresql](https://www.postgresql.org/download/)


## Setting up development
### 1. Cloning the project.
```commandline
$ git clone <repo-url> simpletrading
$ cd simpletrading
```
### 2. Initialize database and rabbitmq.
This will create user. Please omit this if done previously  
Please see env.template for environment variables to be configured for the project.  
Replace some environment variables for the meantime(we're using __0.0.0.0__ for local setup)
```commandline
$ export POSTGRES_HOST=0.0.0.0
$ export RABBITMQ_HOST=0.0.0.0
```
Run command
```commandline
$ make initialize_database
$ make initialize_rabbitmq
```

### 3. Spin up  the services (web, postgres, rabbitmq, celery and celery-beat).
```commandline
$ docker-compose -f compose/development.yml run -d --rm --name simple-trading-dev --service-ports web
```

### 4. SSH to the web service
```commandline
$ ssh trader_super@0.0.0.0 -p 2326
$ sudo su
$ cd /srv/trader
$ source .env
```
Note:
- Password is *pass@1234* 