The backend was made with [Django](https://www.djangoproject.com/)

# Setting up the backend
- Ensure you have python3 installed on your machine
    - Run pip3 install -r requirements.txt
    - Run python3 manage.py makemigrations 
    - Run python3 manage.py migrate

# Running the backend
- Run python3 manage.py runserver

The backend must be running in order to access it through the API endpoints

## Authorization Flow 
(Guidelines for how the front end should authorize users using the backend)<br>
Hit a dedicated auth endpoint (such as /auth/token) which will give back a Mentorq specific token.<br>
Note: this introduces management of two separate tokens. It can be a JWT token to allow front-end and back-end to generate and verify them easily using standard libraries)<br>

User is logged in through HackRU:
- Mentorq front-end has the email and auth token at their disposal (need to verify with HackRU front-end)
- Menorq front-end sends the email and auth token it has over to the back-end with each request to any of the Mentorq back-end endpoints (using the Auth Scheme defined above)
- Mentorq back-end checks with LCS to authenticate the email and auth token and then sends back the data relevant to those credentials

User is not logged in through HackRU:
- Mentorq front-end prompts them/redirects them to login
- Mentorq front-end takes in their username and password and hits the LCS back-end (NOT the Mentorq back-end) 
- Mentorq front-end either receives a token (successful login) or receive an error (in which case the flow stops here)
- Mentorq front-end takes the auth token received and the email they already have to continue with the first flow



# API Endpoints

<h3>
/api
</h3>

<h4>
/auth/token/
</h4>
[POST]<br>
obtain a JWT token for Mentorq by passing in a request with the following body<br>
{<br>
    “email”: “< user email >”,<br>
    “lcs_token”: < user lcs auth token ><br>
}<br>
    returns a JSON object with an access token, a refresh token and booleans that state if a user is a mentor or director. Access tokens are short lived so refresh endpoint will be used to renew the access token

<h4>
/auth/refresh/
</h4>
[POST]<br>
obtain an access token from a valid refresh token by making a request with the following body<br>
{<br>
“refresh”: “< mentorq refresh token >”<br>
}<br>
returns a JSON object with a new unexpired access token<br>
<br>
<br>
<b><em>The following are secured endpoints, i.e. they require the access token obtained earlier to be put into the Authorization header with token type as “Bearer” </em> </b>

<h4>
/tickets/
</h4>
[GET]<br>
obtain the list of all tokens visible to the user (mentors, organizers and directors can view all the tickets and everyone else can only view tickets that they made)<br>

\[POST]<br>
create a ticket with the following minimum request body<br>
{<br>
    “owner_email”: “...”,<br>
    “status”: “\[one of OPEN, CLOSED, CLAIMED,CANCELLED]”,<br>
    “title”: “...”,<br>
    “comment”: “...”,<br>
    “contact”: “...”,<br>
    “location”: “..."<br>
}<br>
returns JSON with relevant extra fields added such as “id” and “created” as well as optional fields of “mentor” and “mentor_email”

<h4>
/tickets/< id >
</h4>
[GET]<br>
use the id of ticket to get all the details about the ticket<br>
[PATCH]<br>
update the ticket identified by id to change either “mentor”, “mentor_email” or “status” fields within the request body<br>

<h4>
/tickets/< id >/slack-dm
</h4>
[GET]<br>
use the id of ticket to get slack DM link<br>

<h4>
/tickets/stats/
</h4>
[GET]<br>
(Requires director permissions in LCS)<br>
Obtain the statistics of all of the tickets in the database<br>
Returns a JSON with:

{<br>
   "average_claimed_datetime_seconds": average_claimed_datetime,<br>
   "average_closed_datetime_seconds": average_closed_datetime<br>
}<br>

#### /feedback
Fields:  
id = id of the ticket associated with feedback  
ticket_url = the direct url to the referenced ticket  
rating = the numerical rating of the feedback  
comments = any additional comments part of the feedback  

**\[GET]**  
**REQUIRED: director permissions in LCS**  
Obtain the list of all the feedbacks submitted  
Returns a list of JSON objects, each representing a feedback.  
Example feedback JSON schema -
```
{
    "ticket": ...,
    "ticket_url": ...,
    "rating": ...,
    "comments": ...
}
```


**\[POST]**  
**REQUIRED: creator of ticket and feedback must be same**  
Creates a feedback  
Expects a JSON with following schema:
```
{
    "ticket": ...,
    "rating": ...,
    "comments": ...
}
```


#### /feedback/\<ticket_id>
**\[GET]**  
**REQUIRED: director permissions in LCS**  
Obtains the details about a specific feedback, identified by the closed ticket's id  
Returns the JSON for a feedback
Example feedback JSON schema - 
```
{
    "ticket": ...,
    "ticket_url": ...,
    "rating": ...,
    "comments": ...
}
```


#### /feedback/leaderboard?limit=\<number>
**\[GET]**  
Obtains a list of mentors with the highest average ratings (number of mentors must be specified)
Expects a JSON with following schema:
```
[
    {
        "mentor": ...,
        "average_rating": ...
    }
    ...
]
```

