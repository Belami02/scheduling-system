# Scheduling System

This is a scheduling system API built with FastAPI and MongoDB. The system allows users to manage bookings, courses, roles, tutor availabilities, and users.


## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd scheduling-system
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/12) file in the root directory and add your MongoDB URI:
    ```env
    MONGO_URI=<your-mongodb-uri>
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000` to see the welcome message.

3. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Project Modules

- **Database**: Contains the database connection setup.
  - [db.py](http://_vscodecontentref_/13): Sets up the MongoDB connection using [motor](http://_vscodecontentref_/14).

- **Models**: Contains the data models for the application.
  - [booking.py](http://_vscodecontentref_/15): Booking model.
  - [course.py](http://_vscodecontentref_/16): Course model.
  - [role.py](http://_vscodecontentref_/17): Role model.
  - [tutor_availability.py](http://_vscodecontentref_/18): Tutor availability model.
  - [user.py](http://_vscodecontentref_/19): User model.

- **Routes**: Contains the API routes.
  - [routes.py](http://_vscodecontentref_/20): Defines the API endpoints for bookings, courses, roles, tutor availabilities, and users.

- **Schemas**: Contains the Pydantic models for request and response validation.
  - [models.py](http://_vscodecontentref_/21): Pydantic models for bookings, courses, roles, tutor availabilities, and users.

- **Main**: The entry point of the application.
  - [main.py](http://_vscodecontentref_/22): Initializes the FastAPI application and includes the router.

## API Endpoints

- **Bookings**
  - `POST /api/bookings`: Create a new booking.
  - `GET /api/bookings`: Get all bookings.
  - `GET /api/bookings/{booking_id}`: Get a booking by ID.
  - `DELETE /api/bookings/{booking_id}`: Delete a booking by ID.

- **Courses**
  - `POST /api/courses`: Create a new course.
  - `GET /api/courses`: Get all courses.
  - `GET /api/courses/{course_id}`: Get a course by ID.
  - `DELETE /api/courses/{course_id}`: Delete a course by ID.

- **Roles**
  - `POST /api/roles`: Create a new role.
  - `GET /api/roles`: Get all roles.
  - `GET /api/roles/{role_name}`: Get a role by name.
  - `DELETE /api/roles/{role_name}`: Delete a role by name.

- **Tutor Availabilities**
  - `POST /api/tutor_availabilities`: Create a new tutor availability.
  - `GET /api/tutor_availabilities`: Get all tutor availabilities.
  - `GET /api/tutor_availabilities/{user_id}`: Get a tutor availability by user ID.
  - `DELETE /api/tutor_availabilities/{user_id}`: Delete a tutor availability by user ID.

- **Users**
  - `POST /api/users`: Create a new user.
  - `GET /api/users`: Get all users.
  - `GET /api/users/{user_id}`: Get a user by ID.
  - `DELETE /api/users/{user_id}`: Delete a user by ID.

