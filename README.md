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


### 5. Run migration
```commandline
$ python manage.py migrate
```

### 6. Create Superuser
```commandline
$ python manage.py createsuperuser
```

### 7. Run development server
```commandline
$ python manage.py runserver 0.0.0.0:8000
```

### 8. Create wallet using django admin
### 9. Deposit to user's account using django admin
### 10. Create stock using django admin

# Coding Test
- Please see __/api/v1/order__ for creation of Order
- Please see __api/v1/order/upload/(filename)__ for bulk creation of orders. Note: Use postman to upload file
- Please see __tasks.py__ file in orders app.
- Please see __/api/v1/wallet/balance/(ticker)__ for retrieving total value invested in a single stock.

## Additional

- __/api/v1/wallet/balance/__ for list stock balances
- __/api/v1/wallet__ for wallet information

# Improvements (Due to time constraint)
- Use storage backend like AWS S3
- Create API for wallet creation and wallet transaction i.e Deposit and Withdrawal
- Create API for stock creation
- Create unittest