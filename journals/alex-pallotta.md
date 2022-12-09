## Nov 15, 2022

- Worked as a team of 4 on the following:
  - Built a working boilerplate yaml file for database and services to test fast API endpoints
  - Created working endpoints with fast API for creating a new user account and retrieving a single user account
- Looking forwards:
  - Finish user endpoints by adding in an endpoint for updating
  - Divide into initial pairs and assign tasks for completing out backend

## Nov 16, 2022

- Worked as a team of 4 on the following:
  - Structured docker-compose YAML file
  - Finished put request for users microservice
  - Migration files for all APIs

## Nov 21, 2022

- Worked with Linsey on the following:
  - Worked on the update functionality for recipients
  - Worked on the update functionality for reminders

## Nov 22, 2022

Accomplishments
-Update recipient mapping table to be functional
-Router for create recipient functional
-Updated recipient table to include user_id
-Added get_message method
-Added message out parameter to all recipient
-Updated mapping table repo
-Created get all recipients by user endpoint
-Created delete mapping table associated with reminder ID endpoint
-Completed merge of all microservices

## Nov 23, 2022

    -Implemented AUTH on all microservice endpoints that need it

## Nov 28, 2022

    - Started email microservice
    - fixed auth bugs to contain hashed passwords for user updates
    - Finished scheduler microservice
      - Completed reminder compiler ( it allows you to pull a reminder id and then pull the recipients and messages related to that reminder id to be sent out)

## Nov 29, 2022

-Refactored reminder compiler function to use more one SQL table which reduced our code by half

-Refactored reminder’s microservice auth
-Refactored contacts microservice auth
-Refactored templates microservice auth

bump
