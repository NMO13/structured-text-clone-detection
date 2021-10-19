from app import create_app

if __name__ == "__main__":
    import os

    os.environ["FLASK_ENV"] = "development"
    application = create_app()
    application.debug = True
    application.run()