## Nov 15, 2022

- Worked as a team of 4 on the following:
  - Built a working boilerplate yaml file for database and services to test fast API endpoints
  - Created working endpoints with fast API for creating a new user account and retrieving a single user account
- Looking forwards:
  - Finish user endpoints by adding in an endpoint for updating
  - Divide into initial pairs and assign tasks for completing out backend

## Nov 16, 2022

- Completed .yaml file to include all databases and microservices
- Assigned pair program partners to finish the rest of the back end API endpoints
- Created the accounts, reminders, contacts and templates migration files
- Refactored update to use COALESCE for puts if you don’t want to update a particular field for a user

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

## Nov 30, 2022

- Add code ability to change boolean from false to true for message sent
- Revisit wireframe to outline a plan for front end

## Dec 1, 2022

- Implemented useToken.js
- Implemented code logic for certain website endpoints to be available for logged in users vs anonymous users
- Implemented loginwidget.js to toggle back and forth for users to sign up or sign in

## Dec 4, 2022

- Wrote deleteReminder.js function that allows for deletion of specific reminder based off the reminder id. Exported it into the reminderDashboard to be used with onClick event when "delete" is clicked on the website. Still need to implement a hook to automatically update page to showcase the list of reminders after one is deleted.

- Added hamburger menu bar

## Dec 6, 2022

- Started deployment
- Created render account
- Integration of CI/CD

## Dec 7, 2022

- Created elephantSQL account
- Troubleshooting of getting elephantSQL and render to connect and deploy our microservices
- Created create user account unit test

## Dec 8, 2022

- debug and troubleshoot render
- finished unit testing

## Dec 9, 2022

- Completed ReadME for Project description, MVP, design concepts, and unit testing with Alex Pallota.
