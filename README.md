# Project: Distributed Social Networking

This is blogging/social network platform that allows the importing of other sources of posts (github, twitter, etc.) as well as the distribution and sharing of posts and content.

## Team Members

1. Steven Heung
2. Sandy Huang
3. Ashwin Mahesh
4. Mehrshad Sahebsara
5. Nishtha Pant

## Frameworks Used

- Frontend - Redux
- Backend - Django
- Database - SQLite3

## Project Structure

The prject code is divided into multiple Django applications each associated with an important component of the project.

- accounts
- author
- post
- comment
- followers
- frontend

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

4. Change directory to "frontend"

   ```bash
   $ cd frontend
   ```

5. Run the following commands to install dependencies:

   ```bash
   $ npm install
   $ npm run dev
   ```

6. If all commands run successfully, you are ready to run the project locally.

## Running Locally

1. While in the root directory, run the project using the following command:
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

## Basic Auth

1. username: socialdistribution_t03
2. password: c404t03

## References

##### [Django Documentation](https://docs.djangoproject.com/en/3.2/)

##### [Django REST framework](https://www.django-rest-framework.org/api-guide/serializers/)

##### [Django-Rest-Knox](https://james1345.github.io/django-rest-knox/)

##### [React](https://reactjs.org/docs/getting-started.html)

##### [Redux](https://redux.js.org/introduction/getting-started)

##### [Stackoverflow - Sort an object by date](https://stackoverflow.com/questions/10123953/how-to-sort-an-object-array-by-date-property)

##### [Mozilla - Array sort documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

##### [Stackoverflow - Array frontend pagination](https://stackoverflow.com/questions/48405643/reactjs-how-to-always-show-only-certain-number-of-array-items)
