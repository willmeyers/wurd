# Wurd
*A CLI password manager.*

## Purpose

This project was done by a student trying to solve his password problems. I have no real intention
of doing anything else with this other than putting it on Github as it most likey has countless
security loopholes that people smarter than me would point out if I were to actual distribute this.

## Install

1. Install dependences using `pip install -r requirements.txt`

2. Run `python setup.py install`

## Usage

__Creating a new instance__

`wurd -i MyPasswords`

Creates a new Wurd database and other files necessary to store passwords on your machine. All
you have to do is follow a simple CLI setup wizard.

__Creating a new password__

`wurd -n PasswdName`

Passwords are easy to create with the built-in password generator. The generated password is automatically
saved and then copied on your clipboard for copy-paste use.

__Getting a password__

`wurd -g PasswdName`

A password is fetched by name and then put on the clipboard for copy-paste use.

__Deleting a password__

`wurd -d PasswdName`

Deletes the password from the database.
