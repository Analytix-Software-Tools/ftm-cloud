# Analytix - Overview
Welcome to Analytix! Analytix is an up and coming cross-industrial AI-powered search engine for connecting users with the products and services they care about. The Analytix platform provides support for end users and organizations seeking a means to find the items they need at a detailed degree of specificity.

# Structure of the Cloud
This is a FastAPI application that is broken up by domains and services. Each domain hosts a router, a controller,
and a service. Functions for each controller can be found by their corresponding domain in domains -> controllers. These controllers generally connect with services which manage the interaction with the database. 

There are a total of 5 resources (accounting for dev and prod environments) within the FTMCloud:

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
which users can view the application and additionally provides quality-of-life features such as SSO, password reset, and
email.

## Task Queues
The service exposes functionality to trigger batch processing and migration to internal users when specific changes are
made that impact other datasets. There is a Celery-based worker node which interfaces with a Redis backend and a RabbitMQ
message broker.

## Search Engine
The application serves data to end users via searching methods backed by an ElasticSearch search engine. Queries to the
engine

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


## TODO
* Implement Celery task queue services/controller/system
* Implement endpoints that would trigger batch jobs
* Integrate with Keycloak authentication system and support SSO in React app
* Separation of the data layer could be better... as of now, services are largely responsible to sanitize before defined
  even though they are inherited in most cases, probably want to isolate the logic
=======
