from fastapi import FastAPI
from os import getenv
from re import match
import datetime

# import the database handler
import db_handler as db_handler

# import the email handler
import email_handler as email_handler

app = FastAPI()

# Get the environment variable from docker-compose
ALLOW_REGISTRATION: str = getenv("ALLOW_REGISTRATION")


@app.get("/register")
def register(email: str):
    if ALLOW_REGISTRATION == "false":
        return {"message": "Registration is disabled"}
    if not match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return {"message": "Invalid email"}
    if db_handler.email_exists(email):
        return {"message": "Email already exists"}
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
    return {"message": "a token has been sent to your email"}


@app.get("/confirm")
def confirm(token: str):
    # Check if the token exists
    temp_token = db_handler.get_temp_token(token)
    if temp_token is None:
        return {"message": "Invalid token"}
    # Check if the token is expired
    if (
        temp_token.generated_at + datetime.timedelta(minutes=5)
        < datetime.datetime.now()
    ):
        return {"message": "Token expired"}
    # If all the conditions are met, create a user
    db_handler.create_user(temp_token.email)
    return {"message": "Your email has been confirmed"}
