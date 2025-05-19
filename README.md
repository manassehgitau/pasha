# Pasha - Social Media Networking App

Pasha is a social media networking application designed for sharing posts, comments, and connecting with other users. It's built with Django and Django REST Framework, featuring user authentication, profile management, post and comment functionalities, and a "like" system.

- **Version:** v1
- **Contact:** gitaumanasseh1@gmail.com
- **License:** MIT License

## Features

*   **User Management:**
    *   User registration and login (JWT-based authentication)
    *   View and update user profiles (bio, profile picture, location, contact)
    *   Profile pictures are handled via Cloudinary.
    *   Automatic profile creation upon user registration.
*   **Social Interaction:**
    *   Follow and unfollow other users
    *   List a user's followers
    *   Search for users by username or email
*   **Content Creation & Interaction:**
    *   Create, retrieve, update, and delete posts (text and optional image via Cloudinary)
    *   Create, retrieve, update, and delete comments on posts
    *   Like and unlike posts
    *   Like and unlike comments
*   **API Documentation:**
    *   Interactive API documentation available via Swagger UI and ReDoc.

## Technologies Used

*   **Backend:** Python, Django, Django REST Framework
*   **Database:** PostgreSQL (configurable)
*   **Authentication:** djangorestframework-simplejwt (JWT Tokens)
*   **Image Storage:** Cloudinary
*   **API Documentation:** drf-yasg (Swagger/OpenAPI)
*   **Environment Variables:** python-decouple

## Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   PostgreSQL server
*   A Cloudinary account (for API key, secret, and cloud name)

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/manassehgitau/pasha.git
    cd pasha
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    # venv/Scripts/activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    Django
    djangorestframework
    djangorestframework-simplejwt
    drf-yasg
    cloudinary
    python-decouple
    psycopg2-binary
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project (where `manage.py` is located). Add the following environment variables with your specific configurations:

    ```env
    SECRET_KEY=your_django_secret_key

    DATABASE_ENGINE=django.db.backends.postgresql
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=localhost # or your db host
    DATABASE_PORT=5432 # or your db port

    CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
    CLOUDINARY_API_KEY=your_cloudinary_api_key
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret
    ```
    *   Replace placeholder values with your actual credentials.
    *   Ensure your PostgreSQL database is created and accessible with the provided credentials.

5.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for accessing the Django admin panel):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create a username and password.

## Running the Application

1.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

2.  **Accessing the application:**
    *   **Django Admin:** `http://127.0.0.1:8000/admin/`
    *   **Accounts App Index:** `http://127.0.0.1:8000/accounts/` (Returns "My app is running!")
    *   **Posts App Index:** `http://127.0.0.1:8000/feed/` (Returns "My app is running!")

## API Endpoints and Documentation

The API is built using Django REST Framework. You can explore and interact with the API endpoints using the Swagger UI or ReDoc documentation.

*   **Swagger UI:** `http://127.0.0.1:8000/swagger/`
*   **ReDoc:** `http://127.0.0.1:8000/redoc/`

### Main API Prefixes:

*   **Accounts API:** `/accounts/api/`
    *   `register/`
    *   `login/`
    *   `profile/`
    *   `profile/update`
    *   `users/<int:user_id>/follow/`
    *   `users/<int:user_id>/unfollow/`
    *   `users/<int:user_id>/followers/`
    *   `search/users/`
*   **Feed (Posts & Comments) API:** `/feed/api/`
    *   `create_post/`
    *   `posts/<int:post_id>/`
    *   `posts/<int:post_id>/delete/`
    *   `posts/<int:post_id>/comments/` (List comments for a post)
    *   `posts/<int:post_id>/create_comment/`
    *   `comments/<int:comment_id>/`
    *   `comments/<int:comment_id>/delete/`
    *   `posts/<int:post_id>/like/`
    *   `posts/<int:post_id>/unlike/`
    *   `comments/<int:comment_id>/like/`
    *   `comments/<int:comment_id>/unlike/`

Refer to the Swagger/ReDoc documentation for detailed information on request/response formats, required parameters, and authentication for each endpoint.

## Project Structure

*   `pasha/`: Main project directory.
    *   `settings.py`: Django project settings.
    *   `urls.py`: Project-level URL configurations.
*   `accounts/`: Django app for user authentication, profiles, and follow system.
    *   `models.py`: User `Profile` and `Follower` models.
    *   `serializers.py`: Serializers for user, profile, and follower data.
    *   `views.py`: API views for account-related functionalities.
    *   `urls.py`: URL configurations for the accounts app.
*   `posts/`: Django app for posts, comments, and likes.
    *   `models.py`: `Post`, `Comment`, `Like`, `LikeComment` models.
    *   `serializers.py`: Serializers for post, comment, and like data.
    *   `views.py`: API views for post and comment-related functionalities.
    *   `urls.py`: URL configurations for the posts app.
*   `manage.py`: Django's command-line utility.
*   `.env`: (You need to create this) For environment variables.
*   `requirements.txt`: (You need to create this) For project dependencies.

## How to Use with Swagger

1.  **Run the application:**
    ```bash
    python manage.py runserver
    ```
2.  **Open Swagger UI in your browser:**
    Navigate to `http://127.0.0.1:8000/swagger/`.

3.  **Authentication:**
    *   Most endpoints require authentication. First, you need to obtain an access token.
    *   Expand the `accounts` section and find the `/accounts/api/login/` endpoint.
    *   Click "Try it out".
    *   Enter the `username` and `password` of a registered user in the request body.
    *   Click "Execute". You will receive an `access` token and a `refresh` token in the response.
    *   Copy the `access` token.
    *   At the top right of the Swagger UI page, click the "Authorize" button.
    *   In the "Value" field of the "BearerToken (JWT)" dialog, paste your `access` token prefixed with `Bearer ` (e.g., `Bearer your_access_token_here`).
    *   Click "Authorize" and then "Close".

4.  **Making Authenticated Requests:**
    *   Now you can try out other protected endpoints. For example, to create a post:
        *   Expand the `feed` section and find the `/feed/api/create_post/` endpoint.
        *   Click "Try it out".
        *   Fill in the required fields for the post (e.g., `title`, `body`). The `writer` will be automatically set to the authenticated user.
        *   Click "Execute".

5.  **Exploring Endpoints:**
    *   Use the Swagger UI to explore all available endpoints, view their expected request bodies and parameters, and see example responses.
    *   You can directly interact with the API through this interface for testing and development.

## Contributing

Contributions are welcome! Please feel free to fork the repository, make changes, and submit pull requests.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

This README should provide a good starting point for anyone looking to understand, set up, and use your Pasha application.