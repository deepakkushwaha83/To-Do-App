from app import create_app
# from vercel_wsgi import handle

flask_app = create_app()

# Vercel entry point
def handler(request, response):
    return handle(flask_app, request, response)
