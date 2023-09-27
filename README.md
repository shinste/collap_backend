# Collap Backend

## Introduction

  The idea for this application comes from our own personal experiences planning events. Specifically when involved with a large number of participants, there are a lot of moving parts when it comes to dealing with everybody’s availability, cooperation, and overall changes with the details of the event. Because of this inevitably troubling task, we’ve thought of this project as a way to streamline event planning, automate tedious information gathering, and assist with straightening out tricky details that may arise during planning.

## Scope
Features for our application that we plan to implement are as followed:
* User Authorization
  - Login with username and password
  - Create new user with valid credentials
* Event Handling
  - View an event(s)
  - Create/Host event
  - Leave event
  - Cancel event
  - Vote on event
* Push Objectives
  - Pushing voting objectives on participants of an event
  - Anonymous Voting
* Conflict System
  - Suggest possible dates based on voting
  - Suggest dates that can work for the most people if full participation isn’t possible
* Database
  - SQL vs noSQL?

## API Documentation
### Login
* Endpoint Name: Login
* Description: Authorizing User
* Endpoint Type: GET
* Endpoint: \login
* Parameters: Username (String), Password(String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
"username": "username",
"password": "password",
}
```
  - Response:
```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```
* Error Handling:
  - 400: Missing Body Parameters
  - 401: Invalid authentication
  - 404: Username not found

### Registration
* Endpoint Name: Registration
* Description: Creating a new user profile
* Endpoint Type: POST
* Endpoint: /register
* Parameters: Username (String), Password(String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
  "password": "password",
}
```
  - Response:
```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```
* Error Handling:
  - 400: Missing Body Parameters, Account already registered, Username already in use

### Events
* Endpoint Name: View Events
* Description: Retrieves a list of the user's participating events
* Endpoint Type: GET
* Endpoint: event/view
* Parameters: Username (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
}
```
  - Responses:
```
{
   "eventid": 1,
   "name": "skiing",
   "dates": "4/12/23", "4/14/23",
   "participants": [
    "joseph",
    "brandon",
   ],
   "time": "tbd"
},

{
   "eventid": 2,
   "name": "movies",
   "dates": [
    "4/01/23",
    "4/08/23",
   ]
   "participants": [
    "joseph",
    "brandon",
   ],
   "time": "tbd"
}
```
Error Handling:
  - 400: Missing Body Parameters


### Notifications
* Endpoint Name: Notifications
* Description: Retrieves a list of the user's notifications
* Endpoint Type: GET
* Endpoint: /notification
* Parameters: Username (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
}
```
  - Responses:
```
{
   "Vote on kicking "brandon",
   "Vote on time"
   "Invited to Camping :)"
}
```
* Error Handling:
  - 400: Missing Body Parameters
 
### Create Event
* Endpoint Name: Create Event
* Description: Creates and hosts an event
* Endpoint Type: POST
* Endpoint: event\create
* Parameters: Event (JSON)
* Return Type: JSON
* Example Case:
  - Request:
```
{
   "eventid": 1,
   "name": "skiing",
   "dates": [
    "4/12/23",
    "4/14/23",
   ]
   "participants": [
    "joseph",
    "brandon",
   ],
   "time": "tbd"
}
```
  - Response:


```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```

* Error Handling:
  - 400: Missing Body Parameters
  - 404: Participant Username not found
 

### Hosted Events
* Endpoint Name: Hosted Events
* Description: Displays the events the user is currently hosting
* Endpoint Type: GET
* Endpoint: /hosted
* Parameters: username (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
}
```
  - Response(s):
```
{
   "eventid": 1,
   "name": "skiing",
   "dates": [
    "4/12/23",
    "4/14/23",
   ]
   "participants": [
    "joseph",
    "brandon",
   ],
   "time": "tbd"
},

{
   "eventid": 2,
   "name": "movies",
   "dates": [
    "4/01/23",
    "4/08/23",
   ]
   "participants": [
    "joseph",
    "brandon",
   ],
   "time": "tbd"
}
```
* Error Handling:
  - 400: Missing Body Parameters
  - 404: Participant Username not found

### Push Voting
* Endpoint Name: Push Votes
* Description: Hosted User can PUSH vote objectives onto participating users
* Endpoint Type: POST
* Endpoint: \push
* Parameters: category (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "category": "date",
}
```
  - Response(s):
```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```
* Error Handling:
  - 400: Missing Body Parameters
  - 401: Invalid authentication ???
  - 404: Participant Username not found ???

### Voting
* Endpoint Name: Vote
* Description: Participants of an event can vote on specified categories
* Endpoint Type: POST
* Endpoint: \vote
* Parameters: Votes (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "date":[
    "4/01/23",
    "4/08/23",
   ],
  "jason_add": "no",
}
```
  - Response(s):
```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```
* Error Handling:
  - 400: Missing Body Parameters
  - 401: Invalid authentication ???
  - 404: Participant Username not found ???

### Join
* Endpoint Name: Vote
* Description: Participants of an event can leave an event
* Endpoint Type: POST
* Endpoint: event\leave
* Parameters: Votes (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "date":[
    "4/01/23",
    "4/08/23",
   ],
  "jason_add": "no",
}
```
  - Response(s):
```
{
  "status": "success"
}
```
or 
```
{
  "status": "failure"
}
```
* Error Handling:




      
  


