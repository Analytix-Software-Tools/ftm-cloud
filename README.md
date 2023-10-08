# Analytix - Overview
Welcome to Analytix! Analytix is an up and coming cross-industrial AI-powered search engine for connecting users with the products and services they care about. The Analytix platform provides support for end users and organizations seeking a means to find the items they need at a detailed degree of specificity.

# Structure of the Cloud
This is a FastAPI application that is broken up by domains and services. Each domain hosts a router, a controller,
and a service. Functions for each controller can be found by their corresponding domain in domains -> controllers. These controllers generally connect with services which manage the interaction with the database. 

The following resources exist within the FTMCloud:

ftmcloud-prod
ftmcloud-dev
ftmcloud-mongo-prod (Atlas)
ftmcloud-mongo-dev (Atlas)
ftmcloud-auth-server (Keycloak)
ftmcloud-rabbitmq (RabbitMQ)
ftmcloud-es-cluster (ElasticSearch)
ftmcloud-kibana (Kibana)

All resources are hosted and backed on an AWS Elastic Kubernetes Service cluster (with the exception of ftmcloud-mongo-dev 
and ftmcloud-mongo-prod, which are hosted on MongoDB Atlas).

# FTMCloud Overview
The FTMCloud is a group of services designed to serve and ingest large amounts of data that back the Analytix
application. 

## Keycloak
This service integrates directly with Keycloak's identity management framework. This provides fine-grained control over
which users can view the application and additionally provides quality-of-life and advanced account management features such as SSO, 
password reset, and email login.

In order to enable keycloak authentication, specify the following environment variables:

'KEYCLOAK_URI_ENCODED': base64 encoded keycloak URI
'KEYCLOAK_AUTH_TOKEN_ENCODED': base64 encoded auth token to communicate with keycloak

## Background Processing
The service exposes functionality to trigger batch processing and migration to internal users when specific changes are
made that impact other datasets. There is a Celery-based worker node which interfaces with a Redis backend and a RabbitMQ
message broker. This API contains connectors to interface with the RabbitMQ broker. See documentation under the tasks cross-cutting domain
for more information.

## Search Engine
The application serves data to end users via searching methods backed by an ElasticSearch search engine. There is a connector class
which allows you to easily query against different indexes that are defined. 

## Database
The database is a dedicated AWS-backed MongoDB Atlas instance with autoscaling configured. 

# Development Environment
A development environment can easily be setup for local development and testing at any time by running
the command

```commandline
docker compose up -d
```

This will build images for the ftm-cloud, the ftm-cloud-mongo, and the ftm-services application and run a containerized
version of the micro services environment.

# Generating Client
Generation of client files is supported through the use of OpenAPI generator, which analyzes the resulting spec as defined
from your endpoints and spawns a client for use with any frontend application.

If you need to generate a client, you can do so by running the following commands:

```console
$ cd autogen
$ npm run openapi-server-generate-client
$ cd client/release
$ npm pack
```

This will generate a tarball that can be installed by transferring the tarball to the
target directory and running npm install.

# Unit Testing
Unit test suites are provided for each domain. Be sure to update and run unit tests prior to deployment to
either dev or prod environments. To generate unit test stubs for your domains, you may run the following commands, starting
from the root directory:

```console
$ cd autogen
$ npm run openapi-server-generate-tests
```

This will generate function stubs which contain the logic of analyzing the responses and automatically populate in each
respective domain if one does not exist already. If you need to run all tests, run the command:

```console
$ python3 runtests --all
```

# Exception Handling
Exception handling is standardized using an exception class called FtmException. When you need to raise an exception
at any point,

```console
raise FtmException('errors.ftmcloud.InvalidEmailAddress')
```

This will present an error response that is clean, presentable and easily consumed by any end users.

In ```crosscutting/error```, there is an ```errors.yaml``` file which lists all the possible errors and error codes by 
language identifier. This is used to display the errors and descriptions in the live documentation.

# FastAPI and MongoDB Boilerplate

A simple starter for building RESTful APIs with FastAPI and MongoDB. 

## Features

+ Python FastAPI backend.
+ MongoDB database.
+ Authentication
+ Deployment

## Using the applicaiton

To use the application, follow the outlined steps:

1. Clone this repository and create a virtual environment in it:

```console
$ python3 -m venv venv
```

2. Install the modules listed in the `requirements.txt` file:

```console
(venv)$ pip3 install -r requirements.txt
```
3. You also need to start your mongodb instance either locally or on Docker as well as create a `.env.dev` file. See the `.env.sample` for configurations.

4. Start the application:

```console
python main.py
```


The starter listens on port 8000 on address [0.0.0.0](0.0.0.0:8080). 

![FastAPI-MongoDB starter](https://user-images.githubusercontent.com/31009679/165318867-4a0504d5-1fd0-4adc-8df9-db2ff3c0c3b9.png)

## Deployment

## TODO - READ
This repository is a work in progress. There are several features planned for the near future but not yet implemented to keep in mind
when browsing this public repo:
* Implement Celery task queue services/controller/system (in development)
* Implement endpoints that would trigger batch jobs
* Integrate with Keycloak authentication system and support SSO in React app (testing via docker-compose temporarily)
* Separate CrudService out - too much repeated CRUD code in the app, may want to isolate the logic into a 
  Repository/DAO pattern to decouple from service logic