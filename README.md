# Project: Distributed Social Networking

This is blogging/social network platform that allows the importing of other sources of posts (github, twitter, etc.) as well as the distribution and sharing of posts and content.

## Team Members
1. Steven Heung
2. Sandy Huang
3. Ashwin Mahesh
4. Mehrshad Sahebsara
5. Nishtha Pant

## Frameworks Used
  * Frontend - Redux
  * Backend - Django
  * Database - SQLite3

## Project Structure
The prject code is divided into multiple Django applications each associated with an important component of the project.
  * accounts
  * author
  * post
  * comment
  * followers
  * frontend

## Installation
NOTE: It is recommended to use a virtual environment.

1. Clone the repository.
2. Install required packages.
   In the root directory which has requirements.txt, run the following command:
   ```bash
   $ pip install -r requirements.txt 
   ```
3. While in the root directory, run the following commands:
   ```bash
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```

##  Running Locally
1. After successful migration, run the project:
   ```bash
   $ python manage.py runserver 
   ```
2. Hit the following endpoint to view the running project:
   ```bash
   http://localhost:8000/
   ```

## API Documentaion
##### Package Used: [drf-yasg ](https://drf-yasg.readthedocs.io/en/stable/)

To view documentation for APIs, hit the following endpoint:
   ```bash
   http://localhost:8000/docs/
   ```