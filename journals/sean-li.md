## Nov 15, 2022

- Worked as a team of 4 on the following:
  - Built a working boilerplate yaml file for database and services to test fast API endpoints
  - Created working endpoints with fast API for creating a new user account and retrieving a single user account
- Looking forwards:
  - Finish user endpoints by adding in an endpoint for updating
  - Divide into initial pairs and assign tasks for completing out backend

## Nov 16, 2022

- Continued to work as a team of 4 on the following:
  - Adjusted docker compose file to allow for multiple databases
  - Added in update endpoint for users
  - Created microservices for remaining aggregates: reminders, contacts, and templates
- Looking forwards:
  - Settle on git branch conventions
  - Divide into pairs and tackle building out endpoints for assigned microservices
  - Merge request #1

## Nov 17, 2022

- Ron/Sean - Pair programming
  - Created a ron/seng contacts_api branch to work off of for contacts API
  - Completed Create ContactIn, ContactOut, Create SpecialDayIn, SpecialDayOut
  - Implemented back end where users can create multiple special days when creating one contact

## Nov 18, 2022

- Ron/Sean - Pair programming
  - Completed get_all contacts endpoint (list of contacts)
  - Completed get_contact endpoint (single contact)
  - Started Update contact endpoint

## Nov 21, 2022

- Ron/Seng - Pair programming
- Implement actual data crossing to grab recipient data from reminders db into contacts microservice

## Nov 22, 2022

- Group programming

  - Update recipient mapping table to be functional

  - Router for create recipient functional

  - Updated recipient table to include user_id

  - Added get_message method

  - Added message out parameter to all recipient

  - Updated mapping table repo

  - Created get all recipients by user endpoint

  - Created delete mapping table associated with reminder ID endpoint

  - Completed merge of all microservices

## Nov 23, 2022

    -Implemented AUTH on all microservice endpoints that need it
