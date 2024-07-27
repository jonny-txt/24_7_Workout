from flask_app import app
from flask_app.controllers import users, workouts
from flask_app.init_db import initialize_categories

initialize_categories()
print("Database initialized with default categories.")

if __name__=="__main__":            
    app.run(debug=True)    