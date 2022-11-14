# ENDPOINTS FOR SOON TM

# Login and logout

### Log in

* Endpoint path: /token
* Endpoint method: POST

* Request shape (form):
  * username: string
  * password: string

* Response: Account information and a token
* Response shape (JSON):
    ```json
    {
      "account": {
        «key»: type»,
      },
      "token": string
    }
    ```

### Log out

* Endpoint path: /token
* Endpoint method: DELETE

* Headers:
  * Authorization: Bearer token

* Response: Always true
* Response shape (JSON):
    ```json
    true
    ```


# Accounts Aggregate

### Create user 

* Endpoint path: /users/
* Endpoint method: POST

* Headers:
  * Authorization: User token

* Response: Create a new user profile
* Response shape:

    ```json
    {
      {
        "username": string,
        "password": string,
        "email": email string,
        "name": string,
      }
    }
    ```


### Specific user

* Endpoint path: /users/:id
* Endpoint method: GET, PUT

* Headers:
  * Authorization: User token

* Response: Retrieve or update information for a user profile
* Response shape:

    ```json
    {
      "user": [
        {
          "user_id": UUID,
          "username": string,
          "email": email string,
          "name": string,
        }
      ]
    }
    ```


# Contacts Aggregate

### All contacts pertaining to a specific user

* Endpoint path: /users/:id/contacts
* Endpoint method: GET, POST

* Headers:
  * Authorization: User token

* Response: Retrieve all contacts associated with a user or create a new contact
* Response shape:

    ```json
    {
        "contacts":
            [
                {
                "contact_id": int,
                "contact_name": string,
                "contact_email": email,
                "contact_phone": string,
                "special_days": [
                    {
                        "name": string,
                        "date": date,
                    }],          
                "notes": string
                }
            ]
    }
    ```

### Specific contact

* Endpoint path: /users/:id/contacts/:id
* Endpoint method: GET, PUT, DELETE

* Headers:
  * Authorization: User token

* Response: Retrieve information regarding a specific contact
* Response shape:

    ```json
    {
      "contact": 
        {
          "contact_id": int,
          "contact_name": string,
          "contact_email": email,
          "contact_phone": string,
          "special_days": {
              [special day object]
              "name": string,
              "date": date,
            }
          "notes": string
        }      
    }
    ```


# Reminders aggregate


### Create a reminder pertaining to an anonymous user

* Endpoint path: /users/:id=None/reminders
* Endpoint method: POST

* Headers:
  * Authorization: No token

* Response: Let anonymous user create a reminder
* Response shape:

    ```json
    {
      {
        "email_target": string,
        "message_recipients": [
          ```List of recipent objects
          ```
            {
              "name": string,
              "email": string,
              "phone": string,
            }
          ],
        "reminder_date": date,        
        "message": {
            "template_id": ,
            "text": string
          }
      }
    }
    ```


### All reminders pertaining to a user

* Endpoint path: /users/:id/reminders
* Endpoint method: GET, POST

* Headers:
  * Authorization: User token

* Response: Retrieve all reminders for a user or create a new reminder
* Response shape:

    ```json
    {
        "reminders":
            [
              {
                "reminder_id": int,
                "message_recipients": [
                  ```List of recipent objects
                  ```
                    {
                      "name": string,
                      "email": string,
                      "phone": string,
                    }
                  ],
                "reminder_date": date,        
                "message": {
                    "template_id": ,
                    "text": string
                  },
                "sent": boolean,
              }
            ]
    }
    ```

### Specific reminder

* Endpoint path: /users/:id/reminders/:id
* Endpoint method: GET, PUT, DELETE

* Headers:
  * Authorization: User token

* Response: Retrieve, edit, or delete a reminder
* Response shape:

    ```json
    {
      "reminder": 
        {
          "reminder_id": int,
          "message_recipients": [
            ```List of recipent objects
            ```
              {
                "name": string,
                "email": string,
                "phone": string,
              }
            ],
          "reminder_date": date,        
          "message": {
              "template_id": ,
              "text": string
            },
          "sent": boolean,
        }    
    }
    ```


# Templates Aggregate

### Get list of themes

* Endpoint path: users/:id/templates/
* Endpoint method: GET, POST

* Headers:
  * Authorization: None or user token

* Response: Retrieve a list of public and user templates (if any) or create a new template
* Response shape:

* GET
    ```json
    {
      "public_templates": [
        {
          ``` template object
          ```
          "theme": {
            "theme_name": string,
            "theme_picture": picture_url,
          },
          "template_name": string,
          "text": string,
        }
      ],
      "user_templates": [
        {
          ``` template object
          ```
          "template_name": string,
          "text": string,
        }
      ]
    }
    ```


* POST
  ```json
      {
        "template_name": string,
        "text": string,
      }
  ```



### Specific template

* Endpoint path: /users/:id/templates/:id
* Endpoint method: GET, PUT, DELETE

* Headers:
  * Authorization: User token

* Response: Retrieve, edit, or delete a template
* Response shape:

    ```json
    {
      "template_name": string,
      "text": string, 
    }
    ```


