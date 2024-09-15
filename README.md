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

### 3. Spin up web, postgres and rabbitmq services.
```commandline
$ docker-compose -f compose/development.yml run --rm --name web --service-ports web /bin/bash
$ su trader
```