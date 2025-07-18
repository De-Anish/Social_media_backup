# Social Media Web App

A modern Django-based social media platform with features like user authentication, tweet posting, profile editing, following, liking, commenting, and a responsive UI.

## Features
- User authentication (signup, login, logout)
- Post tweets with optional images
- Like and comment on tweets
- Follow/unfollow users
- Edit profile and upload profile photo
- Responsive, modern UI

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/De-Anish/Social_media_web.git
   cd Social_media_web
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Usage
- Visit `http://localhost:8000` in your browser.
- Sign up, create posts, follow users, and enjoy the platform!

## Deployment
- For production, use a WSGI server like Waitress or Gunicorn (on Linux), and configure static/media file serving.

---

**Author:** [De-Anish](https://github.com/De-Anish) 
