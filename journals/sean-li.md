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

  - Implemented AUTH on all microservice endpoints that need it

## Nov 28, 2022
  - Minor bug fix relating to updated user accounts having unhashed passwords
  - Pair programmed with Lindsey to get started on emailer and email formatters

## Nov 29, 2022
  - Successfully completed emailer with SMTPlib and the formatter
  - Merged emailer and formatter with scheduler and compilers
  - Tested functionality and confirmed success!

## Nov 30, 2022
  - Began React frontend work, starting with reminder form component
  - Stylized reminder form

## Dec 1, 2022
  - Added front end authentication. Login and logout functionality working as intended
  - Connected reminder form with backend. Reminders can now be created from front end

## Dec 2, 2022
  - Pair programmed with Alex on reminders and contacts dashboard
  - Reminder dashboard now shows list of reminders, but needs refactoring so that list refreshes when a new reminder is created
  - Initial start on contact creation form
  - Need styling for reminder dashboard page

## Dec 3, 2022
  - Alex & I completed a contacts dashboard with a list view and create contact functionality. Each contact has a link that redirects to creating a new reminder and auto populates the recipient field with contact info. Still needs styling
  - Reminder hook refactored. When a new reminder is created, reminder dashboard will auto update to reflect
  - Reminder dashboard styled with css, accounting for scaling
  - Added route protection (currently just for dashboard pages but easy enough to add to any route). If there is no token, the user will automatically be bounced back to landing page when trying to access an authorized only page

## Dec 4, 2022
  - Updated css for navigation menu and login widget
  - Updated contacts book with book component and corresponding css

## Dec 5, 2022
  - Bug fixed on contacts book
  - Added ability to add contacts within contact book
  - Polished contact creation form
  - Added delete functionality on contact book for contacts
  - Added active styling to NavLinks in menu
