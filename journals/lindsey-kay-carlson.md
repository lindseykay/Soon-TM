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

## Nov 17, 2022

-Pair programming with Alex
  - started work on Create Reminder routes/endpoints
  - created Messages classes
  - struggling with how to connect reminder to recipiets with no pk.
    - created a mapping table to solve this

## Nov 18, 2022
-Pair programming with Alex
  -Contined worked on reminderes routers

## Nov 21, 2022

- Worked with Ron on the following:
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

  -debugged update user router to include hashped password
  -discovered that account_data object contains user id
  - plan to refactor any code that has "user_id" with "account_data.id" to make it easier on the front end
  - pair programmed wiht Sean on emailer service
    -messed around with Google API for a long time, before finding a simplier python work around


## Nov 29, 2022
  -learned STRING_AGG and GROUPED_BY 1, 2, 3 (destructing) for SQL
  - discovered the CONCATENATE symbol for sql, which will handle updating data (will update if there's data provide, will keep as is if data is blank)
  - pair programmed with Sean:
    - created email formatter to parase through objects returned from the compiler in order to send emails
    - integrated email with schedule/compiler

## Nov 30, 2022
  - Added a change Boolean function to send emails feature
  - Decided again redux as a group, and begin working on Create Reminder Form (all 4 of us)

## Dec 1, 2022
- incorporated front-end authorization
  -useToken must be inside browser router
- created login widget
- created navbar

## Dec 2, 2022
- Solo work -- used Pixel Online to create the photo logo (learned about layered images)


## Dec 3, 2022
- Solo work -- user settings dashboard
  -users can update password and name
  - had to work with Nav Links and useToken, and then use ternary operator to get user info to show up
  - couldn't update without logging out since the user info used on the front end was stored in the current session token
  - sovled this by redireting users to a log in page after an update


## Dec 5, 2022
  - began work on Elephant SQL and merged all progress from the weekend

## Dec 6, 2022
- as a group:
  - worked on deployment
    - added each microservice to elephantSQL and copied those links into render as DATABASE_URL env. variables
    - made adjustments tso docker deployment files (copying files, migrations, etc)
    - refactored microservices to make get class to other databases, instead of accessing them directly
    - blew up one database on elephantSQL and rebuilt to solve the unhealthy server error


## Dec 7, 2022
- as a group:
  - refactored scheduler into fast api service

## Dec 8, 2022
- worked as a group all day on deployment
- wrote unit test
