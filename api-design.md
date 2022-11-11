### ENDPOINTS FOR SOON TM

### Accounts Aggregate

# Create user 

* Endpoint path: /users/
* Endpoint method: POST

* Headers:
  * Authorization: User token

* Response: Create a new user profile
* Response shape:

    ```json
    {
      "user": [
        {
          "username": string,
          "password": string,
          "email": email string,
          "name": string,
        }
      ]
    }
    ```


# Specific user

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


## Contacts Aggregate

# All contacts pertaining to a specific user

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

# Specific contact

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


## Messages aggregate

# All messages pertaining to a user

* Endpoint path: /users/:id/messages
* Endpoint method: GET, POST

* Headers:
  * Authorization: User token

* Response: Retrieve all messages for a user or create a new message
* Response shape:

    ```json
    {
        "messages":
            [
                {
                  "message_id": int,
                  "message_recipients": [list of emails],
                  "target_date": date,        
                  "message": string
                }
            ]
    }
    ```

# Specific message

* Endpoint path: /users/:id/messages/:id
* Endpoint method: GET, PUT, DELETE

* Headers:
  * Authorization: User token

* Response: Retrieve, edit, or delete a message
* Response shape:

    ```json
    {
      "message": 
        {
            "message_id": int,
            "message_recipients": [list of emails],
            "target_date": date,        
            "message": string
        }    
    }
    ```
