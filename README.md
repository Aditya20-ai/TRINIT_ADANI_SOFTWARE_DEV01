# DEV01 Submission

This project is a submission for tri-nit hackathon event. It is a full-stack web application that consists of a Python server and a Next.js frontend with React.js. The server connects to a MySQL database for storing data.

## Server

The server is built using the Flask framework and is responsible for handling incoming requests from the frontend and interacting with the database.

The server has the following API endpoints for various operations:

- `GET /get-profile`: Retrieves the profile information of a user
- `GET /get-crowdfunding`: Retrieves information about ongoing crowdfundings
- `POST /create-profile`: Allows the user to create their profile
- `POST /create-crowdfunding`: Allows the user to create a crowdfunding campaign
- `POST /update-crowdfunding`: Allows the user to update an existing crowdfunding campaign
- `POST /delete-crowdfunding`: Allows the user to delete a crowdfunding campaign
- `POST /update-profile`: Allows the user to update their profile information
- `POST /delete-profile`: Allows the user to delete their profile
- `POST /upload-image`: Allows the user to upload an image
- `POST /create-meeting`: Allows the user to schedule a meeting

To run the server, follow these steps:

1. Install the required packages by running `pip install -r requirements.txt`
2. Create a MySQL database and update the credentials in the `config.py` file.
3. Start the server by running `python app.py`

## Frontend

The frontend is built using the Next.js framework and React.js. It communicates with the server to retrieve data and display it to the user.

To run the frontend, follow these steps:

1. Install the required packages by running `npm install`
2. Start the development server by running `npm run dev`

## Features

- The user can create profiles either as an NGO or as a Philanthrophist in the onboarding screen
- The user is able to input all the required details both as an NGO and as an Philanthrophist
- In the backend, the Philanthrophist is able to generate meetings with the NGO's

## Deployment

The project can be deployed to a hosting platform like Heroku or AWS. The server can be deployed using a web server like Gunicorn and the frontend can be built and served using a static file server like Nginx.
