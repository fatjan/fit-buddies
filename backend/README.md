# Fit-Buddies Backend App

The Fit-Buddies Backend App is the server-side application built with Python and Flask. It provides the RESTful API endpoints and handles the backend logic for user management, workout tracking, challenges, messaging, and more.

## Tech Stack

The Fit-Buddies backend app is built using the following technologies:

- **Python**: Programming language
- **Flask**: Micro web framework for building the API
- **MongoDB**: Database for storing user data, workouts, challenges, and messages
- **MongoEngine**: Object-Document Mapping (ODM) library for MongoDB
- **JWT**: Authentication and authorization using JSON Web Tokens

## Installation

To set up the Fit-Buddies backend app locally, please follow the instructions below:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fit-buddies-backend.git

2. Install the dependencies:
    cd fit-buddies/backend
    pip install -r requirements.txt

3. Set up the environment variables:
    Create a .env file in the root directory.
    Provide the required environment variables in the .env file. Refer to the .env.template file for the necessary variables.

4. Start the development server:
    python run.py

    This will start the Flask development server and provide the API endpoints for the frontend app.

### API Documentation
The Fit-Buddies backend app provides a RESTful API to interact with the frontend app. Detailed documentation for the API endpoints can be found in the API Documentation file.

### Contributing
We welcome contributions to the Fit-Buddies backend app! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: git checkout -b my-feature.
3. Make your changes and commit them: git commit -am 'Add new feature'.
4. Push to the branch: git push origin my-feature.
5. Submit a pull request.
6. Please ensure that your code follows the project's coding style and includes appropriate tests.

### License
The Fit-Buddies Backend App is licensed under the MIT License.