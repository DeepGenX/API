import re
from fastapi import FastAPI
from os import getenv
from re import match
import datetime
from database_setup import Temp_tokens

# import the database handler
import db_handler as db_handler

# import the email handler
import email_handler as email_handler

app: FastAPI = FastAPI()

# Get the environment variable from docker-compose
ALLOW_REGISTRATION: str = getenv("ALLOW_REGISTRATION")


def message_handler(message: str) -> dict:
    """
    This function is used to handle the messages send to the user.
    It will return a message to the user.
    """
    return {"message": message}


@app.get("/register")
def register(email: str):
    """
    This function is used to register the user.
    It will send an email to the user with a temporary token.
    """
    if ALLOW_REGISTRATION == "false":
        return message_handler("Registration is not allowed")
    if not match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return message_handler("Invalid email")
    if db_handler.email_exists(email):
        return message_handler("Email already exists")
    # If all the conditions are met, create a temp token
    token: str = db_handler.create_temp_token(email)

    # Reading the email template
    f = open("templates/confirm_template.html", "r")
    # Template is return by readlines() as a list
    template: list = f.readlines()
    # We transform the list into a string
    template: str = " ".join(map(str, template))
    # We replace the token in the template
    template: str = template.replace("{url}", f"http://localhost/confirm?token={token}")

    # Send the email with the token
    email_handler.send_html_email(
        email=email, subject="Confirm your email", html=template
    )
    return message_handler("A token has been sent to your email")


@app.get("/confirm")
def confirm(token: str):
    """
    This function is used to confirm the email of the user.
    It will create a user in the database if the token is valid.
    """
    # Check if the token exists
    temp_token: Temp_tokens = db_handler.get_temp_token(token)
    if temp_token is None:
        return message_handler("Invalid token")
    # Check if the token is expired
    if (
        temp_token.generated_at + datetime.timedelta(minutes=5)
        < datetime.datetime.now()
    ):
        return message_handler("Token expired")
    # If all the conditions are met, create a user
    db_handler.create_user(temp_token.email)
    return message_handler("Your email has been confirmed")
