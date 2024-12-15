# Trivia Quiz Application

## Description
The Trivia Quiz Application is an interactive platform that allows users to participate in real-time trivia quizzes through a web interface and their phones. It features user authentication, quiz creation and management, real-time participation, and a dynamic scoring system.

## Features
- **User Authentication**: Secure registration and login system.
- **Quiz Management**: Create, edit, and activate quizzes with multiple questions and options.
- **Real-Time Participation**: Users can join quizzes and answer questions in real-time.
- **Scoring System**: Tracks participant scores and provides quiz statistics.
- **Responsive Design**: Accessible on various devices with a user-friendly interface.

## Project Structure
```
/client
/server
```

## Installation

### Prerequisites
- Node.js (v14 or later)
- Python (v3.8 or later)
- SQLite

### Client Setup
1. Navigate to the client directory:
    ```sh
    cd client
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Start the development server:
    ```sh
    npm start
    ```
    The client will run at [http://localhost:3000](http://localhost:3000).

### Server Setup
1. Navigate to the server directory:
    ```sh
    cd server
    ```
2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
3. Activate the virtual environment:
    - **Windows**:
      ```sh
      venv\Scripts\activate
      ```
    - **macOS/Linux**:
      ```sh
      source venv/bin/activate
      ```
4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Set up environment variables:
    Create a `.env` file in the server directory with the following content:
    ```
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```
6. Initialize the database and run the server:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    flask run
    ```
    The server will run at [http://0.0.0.0:5000](http://0.0.0.0:5000).

## API Endpoints

### Authentication
- **Register User**: `POST /auth/register`
- **Login User**: `POST /auth/login`
- **Logout User**: `POST /auth/logout`
- **Get Current User**: `GET /auth/me`

### Quiz Management
- **Create Quiz**: `POST /admin/create_quiz`
- **Edit Quiz**: `PUT /admin/edit_quiz/<quiz_id>`
- **Activate Quiz**: `POST /admin/activate_quiz/<quiz_id>`
- **View Quizzes**: `GET /admin/view_quizzes`
- **Quiz Statistics**: `GET /admin/quiz_statistics/<quiz_id>`

### Quiz Service - Phone Interface
The phone interface utilizes the Azran interface. You can find the documentation here: [Azran Interface Documentation](https://www.hazran.online/FreeArena/content/instructions).

- **Quiz phone Service**: `POST /quiz_service_service`

## Technologies Used

### Client:
- React
- React Router DOM


### Server:
- Python
- Flask
- SQLite
- JWT for authentication

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
