# Project: Distributed Social Networking

This is blogging/social network platform that allows the importing of other sources of posts (github, twitter, etc.) as well as the distribution and sharing of posts and content.

## Team Members

1. Steven Heung
2. Sandy Huang
3. Ashwin Mahesh
4. Mehrshad Sahebsara
5. Nishtha Pant
6. Jingyu Xiang

## Frameworks Used

- Frontend - Redux
- Backend - Django
- Database - Postgres

## Project Structure

The project code is divided into multiple Django applications each associated with an important component of the project.

- accounts
- author
- post
- comment
- followers
- inbox
- likes
- frontend

## Installation

NOTE: Postgres is required

On Linux:

1. Install postgres using:

```bash
 $ sudo apt-get install libpq-dev postgresql postgresql-contrib

```

2. Restart psql service with

```bash
$ sudo service postgresql restart
```

3. To set up the database for postgres:

```bash

   $ sudo su - postgres
   $ psql
   $ CREATE DATABASE c404t03db;
   $ CREATE USER postgres WITH PASSWORD 'c404t03db'
   $ GRANT ALL PRIVILEGES ON DATABASE c404t03db TO postgres
   $ Quit psql with `\q` then `exit';

```

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
https://social-dis.herokuapp.com/docs/
```

## Basic Auth

1. Register
2. Fill out required fields: Username, Displayname, Email, Password
3. Login


## Remote user Login

1. username: socialdistribution_t03
2. password: c404t03




# AJAX Usages
We used Ajax whenever we needed to fetch/send data to our Django server. 
Below is a list of our front-end React code where we used Ajax:

[Registration](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/auth.js#L97)
[Login](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/auth.js#L60)
[Logout](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/auth.js#L136)

[Creating a Post](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L192)
[Deleting a post](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L132)
[Adding a comment to a post](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L221)
[Liking a post](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L255)

[Load Local Posts](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L21)
[Load posts from foreign servers](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L69)
[Load Author Posts for Profiel](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/ed5cc623ab9eda552b61e523d3a062f50863ac81/frontend/src/actions/posts.js#L45)
[Load Github Activity](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/GitHub.js#L19)

[Load list of Authors](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/AuthorSearch.js#L34)
[Load list of possible follows](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/AuthorSearch.js#L72)
[Handle following an Author](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/AuthorSearch.js#L90)

[Send Friend Request](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/Inbox.js#L86)
[Accepting a Friend Request](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/25547598ee98a3546eaca3c2d50fe3c56ed2352b/frontend/src/components/pages/Inbox.js#L137)
[Rejecting a Friend Request](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/25547598ee98a3546eaca3c2d50fe3c56ed2352b/frontend/src/components/pages/Inbox.js#L163)
[Check for Friend Requests](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/Inbox.js#L40)
[Clearing Friend Request](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/25547598ee98a3546eaca3c2d50fe3c56ed2352b/frontend/src/components/pages/Inbox.js#L172)
[Friends List](https://github.com/CMPUT404-stev-sand-pant-ashw-mehr/CMPUT404-stev-sand-pant-ashw-mehr-repo/blob/999fd5dccb5f130615ff59cb30e19d3a20dcdf9e/frontend/src/components/pages/Inbox.js#L29)





## References

##### [Django Documentation](https://docs.djangoproject.com/en/3.2/)

##### [Django REST framework](https://www.django-rest-framework.org/api-guide/serializers/)

##### [Django-Rest-Knox](https://james1345.github.io/django-rest-knox/)

##### [React](https://reactjs.org/docs/getting-started.html)

##### [Redux](https://redux.js.org/introduction/getting-started)

##### [Stackoverflow - Sort an object by date](https://stackoverflow.com/questions/10123953/how-to-sort-an-object-array-by-date-property)

##### [Mozilla - Array sort documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

##### [Stackoverflow - Array frontend pagination](https://stackoverflow.com/questions/48405643/reactjs-how-to-always-show-only-certain-number-of-array-items)

##### [Stackoverflow - React dynamic state fields](https://stackoverflow.com/questions/53349628/how-to-make-dynamic-state-for-multiple-fields-in-react)

##### [Stackoverflow - React state modification](https://stackoverflow.com/questions/26253351/correct-modification-of-state-arrays-in-react-js)

##### [Stackoverflow - React state modify object slice](https://stackoverflow.com/questions/29537299/react-how-to-update-state-item1-in-state-using-setstate)

##### [Bootstrap card with image to left](https://tarkhov.github.io/postboot/card/image-left/)

##### [Bootstrap - Flex properties](https://getbootstrap.com/docs/5.0/utilities/flex/)

##### [Bootstrap - Spacing properties](https://getbootstrap.com/docs/5.0/utilities/spacing/)

##### [Django Authentication](https://docs.djangoproject.com/en/3.2/topics/auth/)

##### [Django Custom Permissions](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/)


#### [Github Events API](https://developer.github.com/v3/activity/events/types/)  
##### [SVG Text Generation](https://maketext.io/)
