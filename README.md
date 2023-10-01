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
  - SQL

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
"password": "password"
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
  - 400: Missing Body Parameters, Username not found

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
  "password": "password"
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
  "username": "username"
}
```
  - Responses:
```
[
  {
    "eventid": 1,
    "name": "skiing",
    "host": "stephen",
    "dates": ["4/12/23", "4/14/23"],
    "participants": [
      "joseph",
      "brandon"
    ]
  },
  {
    "eventid": 2,
    "name": "movies",
    "dates": ["4/01/23", "4/08/23"],
    "participants": [
      "joseph",
      "brandon"
    ]
  }
]
```
Error Handling:
  - 400: Missing Body Parameters, Username not found


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
  "username": "username"
}
```
  - Responses:
```
{
   "Vote on Date",
   "Invited to Camping :)"
}
```
* Error Handling:
  - 400: Missing Body Parameters, Username not found
 
### Create Event
* Endpoint Name: Create Event
* Description: Creates and hosts an event, sends invites to participants' notifications
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
   "host": "stephen",
   "dates": [
    "4/12/23",
    "4/14/23",
   ],
   "participants": [
    "joseph",
    "brandon",
   ]
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
  - 400: Missing Body Parameters, Username not found, Participant Username not found

* Sequence Diagram
![Sequence Diagram](./Sequence%20Diagram/Create%20Event%20SD.png)

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
[
  {
    "eventid": 1,
    "name": "skiing",
    "host": "stephen",
    "dates": ["4/12/23", "4/14/23"],
    "participants": [
      "joseph",
      "brandon"
    ]
  },
  {
    "eventid": 2,
    "name": "movies",
    "host": "jason",
    "dates": ["4/01/23", "4/08/23"],
    "participants": [
      "joseph",
      "brandon"
    ]
  }
]
```
* Error Handling:
  - 400: Missing Body Parameters, Username not found

### Push Voting
* Endpoint Name: Push Votes
* Description: Hosted User can PUSH vote objectives onto participating users
* Endpoint Type: POST
* Endpoint: \push
* Parameters: Event ID (Integer), Category (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "event_id": 123,
  "category": "date"
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
  - 400: Missing Body Parameters, Username not found

### Voting
* Endpoint Name: Vote
* Description: Participants of an event can vote on preferred date
* Endpoint Type: POST
* Endpoint: \vote
* Parameters: Username (String), Event ID (Integer), Votes (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
  "event_id": 123,
  "date":[
    "4/01/23",
    "4/08/23",
   ]
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
  - 400: Missing Body Parameters, Username not found

### Update
* Endpoint Name: Update
* Description: User can join and leave event
* Endpoint Type: POST
* Endpoint: event\update
* Parameters: Username (String), Event ID (Integer), Operation (String)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
  "event_id": 123,
  "operation": "join"
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
  - 400: Missing Body Parameters, Username not found, Event ID not found, Cannot join/leave
  
### Remove
* Endpoint Name: Remove
* Description: Host removes user from event, removes any votes from user
* Endpoint Type: POST
* Endpoint: event\remove
* Parameters: Username (String), Event ID (Integer)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
  "event_id": 123
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
  - 400: Missing Body Parameters, Username not found, Event ID not found
 

### Delete
* Endpoint Name: Delete
* Description: Checks if user is host, then deletes event
* Endpoint Type: POST
* Endpoint: event\delete
* Parameters: Username (String), Event ID (Int)
* Return Type: JSON
* Example Case:
  - Request:
```
{
  "username": "username",
  "event_id": 123
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
  - 400: Missing Body Parameters, Username not found, Event ID not found




      
  


