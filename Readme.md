# League Manager

## Requirements

* Python 3.8+
* Django 4.0+

## Specification

## How to run the application

1. Prepare the database by running the following commands

<pre>
python manage.py makemigrations
python manage.py makemigrations restapi
python manage.py migrate
</pre>

2. (**Optional**) If testing, run the following to load initial data

<pre>
python manage.py loaddata test-data
</pre>

3. Run the server

<pre>
python manage.py runserver
</pre>

## How to test the application
The `test-data.yaml` fixture will generate the following users along with related records

<pre>
admin@domain.com    (ADMIN)
coach1@domain.com   (COACH)
coach2@domain.com   (COACH)
player1A@domain.com (PLAYER 1 on Team A)
player2A@domain.com (PLAYER 2 on Team A)
player1B@domain.com (PLAYER 1 on Team B)
player2B@domain.com (PLAYER 2 on Team B)

All users have passwords set as: test123#
</pre>

1. First, generate a token for a selected user as follows:

<pre>
curl -X POST -H "Content-Type: application/json" \
    -d '{"username": "{username}", "password": "{password}"}' \
    http://localhost:8000/token/

{"token":"0b29f4462aa7e617a254bd95413510c3638b8ab4"}
</pre>

2. Include the above token to test any of the endpoints specified in the **Specification** section

<pre>
curl -X GET http://localhost:8000/path/to/api \
    -H "Authorization: Token {token}" 
</pre>
