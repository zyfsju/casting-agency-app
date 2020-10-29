# casting-agency-app

The app has been deployed to [Heroku](https://react-casting.herokuapp.com). It displays a token (JWT) in `External API` tab, after user is logged in. The API path can only be accessed via HTTP requests with a valid bearer token.

## Authentication and Authorization

Set up with [Auth0](https://auth0.com/). The user will be re-directed to an Auth0 page for sign-on and back to the website if the log-on attempt is successful. Role-based access control (RBAC) is enabled. The roles and permissions are as follows:

1. Casting Assistant
    - `get:actors`
    - `get:movies`
2. Casting Director has all permissions the casting assistant has and
    - `patch:actors`
    - `patch:movies`
    - `delete:actors`
    - `post:actors`
3. Executive Producer has all permissions the casting director has and
    - `delete:movies`
    - `post:movies`

### Backend

Flask server + SQLAlchemy + SQLite

The Flask server olso serves a static HTML file in `static/`, built from `/frontend` react code.

#### Start Server

Create a virtual environment and install dependencies:

```bash
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To run the development server,

```bash
python3 app.py
```

#### Run Tests

Import the collection `./casting-api-tests.postman_collection.json` in Postman and send requests.

### Frontend

React

`cd` into the `frontend` directory and install dependencies by running

```bash
cd frontend
npm install
```

To run the development server:

```bash
npm start
```

To build:

```bash
npm run build
```
