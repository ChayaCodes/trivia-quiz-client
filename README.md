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

# The server side still dont working! you need only to run the client side!

    ```sh
    npm start
    ```
    The client will run at [http://localhost:3000](http://localhost:3000).

### Server Setup
1. Navigate to the server directory:
    ```sh
    cd server
    ```

2. Run the app file:
    ```sh
    py app.py
    ```
    or
    ```sh
    python app.py
    ```


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
