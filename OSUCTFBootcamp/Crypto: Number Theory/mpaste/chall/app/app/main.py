import app
from dotenv import load_dotenv

load_dotenv()
app = app.create_app()

if __name__ == "__main__":
    app.run()
