# Midnite API Task Python
This is a Python version of the challenge I was sent. 

I am primarily a PHP developer, but I have made this one in addtion to show that I can be and am a very quick learner. 

I've used FastAPI as I've been interested in this one for a while, and thought it would be nice to take a crack at it. It was really enjoyable learning this one, I love the syntax and seems a lot nicer than PHP at times, and of course offers a great range of applications than PHP is able to.

## Setup 
1. I've used Python 3.10, FastAPI, pytest and SQLModel
2. I think you need to run `pip install .` to install, there is a `requirements.txt` and `pyproject.toml` in the folder so think that should cover it.
2. There is a test.db database for this project, so shouldn't need to fiddle around setting up databases.
3. Create a user using the `/user` endpoint 
4. You should be able to run tests with `pytest`


## Assumptions
1. That the user_id may not exist, in which case, this needs to be handled
2. Time is in seconds
3. That for code 123, it does not matter if the deposit amount is not consecutive, if it fits into a 30 second window, it should error. Withdrawals still count towards the time limit
4. Users should not be able to withdraw into a negative balance.
5. Time must be greater than 0, 0 is usually treated as a null value in most languages

## Routes

1. POST `/event`
Expected Payload:
```json
{
    "type": "deposit",
    "amount": "42.00",
    "user_id": 1,
    "time": 10
}
```

Expected Response
```json
{
    "user_id": 1,
    "alerts": true,
    "alert_codes": [1100, 123]
}
```

2. POST `/user`
Expected Payload:
```json
{
    "name": "Samuel Walker",
    "total": 100.00
}
```

Expected Response:
```json
{
    "name": "Sam",
    "total": 100.0,
    "id": 2
}
```

## Database Models
I will create 2 tables, Users, and Transactions

Users should be self explanatory

Transactions for recording user transactions

I actually removed TransactionTypes and AlertCodes for this Python API to keep things simple, it wasn't hugely necessary for this however I developed this one second to
show my understanding of Python 3.10 and FastAPI.


### How I approached this

1. I had already completed the PHP version of this, that is what I have developed for most of my career. This version is to show that I am adaptable to new languages quickly. 
2. Looked into FastAPI and how to use it, how to set it up. What I'd need for a basic API
3. Installed Python into my WSL2 setup.
4. Installed fastapi and a virtual environment, this one was using uvicorn. Absolutely love a environment that auto refreshes.
5. I've used SQLite for this so less hassle setting it up. 
5. Create a /users route so I can just add a user for the purposes of this exercise
6. Recreate the process under /event like in the PHP version
7. Start moving things out into their own files, keeping the route slimmer, and things grouped in a way that seems relevant. 
8. Make sure that things are working as intended, sending through deposits and withdrawals and making sure things throw in the same way
9. Look into some basic tests
10. Optimizations, reducing number of query statements for transactions, could be done with one function with optional params. Added try catch blocks on creating users
11. Creating a better folder structure, creating app to hold the main structure, and to make testing easier, in line with better practices
12. Creating the rest of the tests. 

### Issues and Challenges
1. Setting up SQLite seemed a bit off, would prefer a fully fletched database but I think that as I'm handing in two solutions, the one I'm less experienced in gets a simpler set up
2. Writing the setup instructions, I'm used to composer which tends to write all the files needed automatically, I see that python is ever so slightly more complex than this, which isn't a problem, it's one more thing to learn!
3. Slightly different syntax, took a moment to get and or rather than && and || but its nice at the same time.
4. Understanding imports from tests and app, bit confusing but got there in the end!
5. I wasn't quite able to stop the `/user` endpoint not being able to accept negative amounts, despite the model having the `ge=0` requirement, though from some research should be solved by having a schemas file and using the pydantic model there to create the model from the request data, this should allow errors to be caught properly.

## Improvements
1. Use BackgroundTasks from FastAPI, I could say transaction recieved, and then process the checks and then return a full response, however for such a small API this would be premature optimization. 
2. It's a small API, so I don't need to use async functions, but if I wanted to improve ability to handle heavier loads, I should use async functions in various places, most likely around the database calls which tend to be blocking.
3. Perhaps a slightly improved folder structure, more domain oriented perhaps instead, so perhaps users, transactions, events (might need another name for conflict)
4. Schemas for creating entities, so that errors are caught properly and things can be dealt with properly.