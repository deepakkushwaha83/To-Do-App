from app import create_app

# Create the Flask app
flask_app = create_app()

# Vercel looks for `app`
app = flask_app
