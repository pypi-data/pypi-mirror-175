
# GlitchTip Commandline Tool



* [Glitchtip-cli](https://gitlab.cee.redhat.com/cssre/glitchtipcli)
* [API Documentations](https://app.glitchtip.com/docs/)


# Overview

This document describes the strategy, execution, and results of building a glitchtip cli tool that performs CRUD operations against an instance of the Glitchtip service. Using python click.


## Problem Statements



* The CS-SRE team need a glitchtip commandline tool in order to create and manage Team/projects/organizations on staging (gltichtip.staging.devshift.net) and (glitchtip.devshift.net) Production.
* Glitchtip [API documentation](https://app.glitchtip.com/docs/) is poorly documented, however its aim is for Sentry capability support. I am finding that some of the UI to backend mapping is incorrect.
* Some upstream changes might need to be made, in order for some functionality to work.


## Requirements 



* Perform CRUD operations against Glitchtip API’s.
* Produce glitchtip reporting and integrate with jira.
* Remediate Glitchtip API tokens.
* Host the command line tool on[ https://pypi.io](https://pypi.io)
* Implement a testing suit. (pytest)
* Provide full error tracing in module code blocks.(rich package, poetry used for package management)
* Containerized the command-line application and host images on quay.io cs-sre organizations and docker-hub. (We could automate this using make or a build script)
* End to End to tests 


## Design Flow:

- Example 1.

![List Organization](/images/list_organization.png)


## API Endpoints

| Route                                                  | Verb   | Description                              |   |   |
|--------------------------------------------------------|--------|------------------------------------------|---|---|
| /api/0/users/                                          | GET    | Return list of users                     |   |   |
| /api/0/users/                                          | POST   | Creates a user                           |   |   |
| /api/0/users/{id}/                                     | UPDATE | Updates user                             |   |   |
| /api/0/users/{id}/                                     | DELETE | Deletes User                             |   |   |
| /api/0/user/{id}                                       | PATCH  | Update a team                            |   |   |
| /api/0/teams/                                           | GET    | Get Teams                                |   |   |
| /api/0/teams/                                          | POST   | Creates a team                           |   |   |
| /api/0/teams/{id}/                                     | PUT    | Updates Teams                            |   |   |
| /api/0/teams/{id}/                                     | GET    | Gets team list                           |   |   |
| /api/0/teams/{id}/                                     | DELETE | Deletes a team                           |   |   |
| /api/organizations/<slug>/members/                     | GET    | Get Team members listing                 |   |   |
| /api/organizations/<slug>/members/                     | POST   | Create team members                      |   |   |
| /api/organizations/<slug>/members/                     | GET    | Team member list                         |   |   |
| /api/0/teams/{team_pk}/members/{id}/                   | UPDATE | Update team members list                 |   |   |
| /api/organizations/<slug>/members/                     | DELETE | Delete team members                      |   |   |
| /api/0/organizations/                                  | GET    | Get the list of organizations            |   |   |
| /api/0/organizations/                                  | POST   | Create an organization                   |   |   |
| /api/0/organizations/{organization_slug}/chunk-upload/ | GET    | Get organization chuck upload list       |   |   |
| /api/0/organizations/{organization_slug}/chunk-upload/ | POST   | Create an organization chuck upload list |   |   |
| /api/0/products/                                       | GET    | Get product list                         |   |   |
| /api/0/products/{djstripe_id}/                         | GET    | Get product info                         |   |   |
| /api/0/projects/                                       | GET    | Get Project list                         |   |   |
| /api/0/projects/                                       | POST   | Create a Project                         |   |   |



# Strategy

The main aim of this command-line tool is for CS-SRE to managed API calls to glitchtip backend and established upstream feature not present in glitchtip and to provided a management tool for glitchtip application resources.


# Challenges


* The Glitchtip upstream API is poorly [documented ](https://app.glitchtip.com/docs/)and has some slight compatibility issues as it trying to keep compatibility with Sentry’s API.
* The backend API uses a mixture of refernece for both `puk` and `slug`. 
* This means that some upstreams changes to glitchtip backend may be needed to enable featured flags.A good example of this the Observalability feature flag work committed by our team.
* The Glitchtip community might not except our feature request or change, as it might not fit into their continuous feature release planning.
* The Glitchtip might want theses features as part the Sentry CLI tool instead.


# Limitations

Red Hat does not own the product and therefore SRE have many unknown paths to established as the glitchtip command-line tool as a valid management tool for both the community and SRE.
