# Analytix - Overview
Welcome to Analytix! Analytix is an up and coming cross-industrial AI-powered search engine for connecting users with the products and services they care about. The Analytix platform provides support for end users and organizations seeking a means to find the items they need at a detailed degree of specificity.

# Structure of the Cloud
This is a FastAPI application that is broken up by domains and services. Each domain hosts a router, a controller,
and a service. Functions for each controller can be found by their corresponding domain in domains -> controllers. These controllers generally connect with services which manage the interaction with the database. 

There are 3 services, that make up the FTM-Cloud prod environment - 2 hosted on Linux VMs, one Atlas instance. The services are:

ftm-cloud-prod
ftm-services-prod
ftm-cloud-mongo-prod

# Development Environment
A development environment can easily be setup for non-production or prod-like environments at any time by running
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
