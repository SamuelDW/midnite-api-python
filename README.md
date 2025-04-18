# Midnite API Task Python

Im adding this in to show that I can use python, even if it is not the most well layed out code.

To add, this is the first time I have used python, I kept to best practises that I usually follow in PHP. Functions should do one thing only, return early.

I've used FastAPI as I've been interested in this one for a while, and thought it would be nice to take a crack at it. It was really enjoyable learning this one, I love the syntax and seems a lot nicer than PHP at times. 

## Setup 
1. I've used Python 3.10, FastAPI
2. I think you need to run pip install to install, there is a `requirements.txt` and `pyproject.toml` in the folder so think that should cover it.
2. There is a test.db database for this project, so shouldn't need to fiddle around setting up databases.
3. Create a user using the `/user` endpoint 


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

### Issues and Challenges
1. Setting up SQLite seemed a bit off, would prefer a fully fletched database but I think that as I'm handing in two solutions, the one I'm less experienced in gets a simpler set up
2. Writing the setup instructions, I'm used to composer which tends to write all the files needed automatically, I see that python is ever so slightly more complex than this, which isn't a problem, it's one more thing to learn!
3. Slightly different syntax, took a moment to get and or rather than && and || but its nice at the same time.


## Improvements
1. Use BackgroundTasks from FastAPI, I could say transaction recieved, and then process the checks and then return a full response. 