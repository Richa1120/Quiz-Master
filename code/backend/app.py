from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
