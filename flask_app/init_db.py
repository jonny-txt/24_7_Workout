from flask_app.config.mysqlconnection import connectToMySQL

DB = "24_7_workout"

def initialize_categories():
    categories = ["Strength", "Cardio", "Yoga"]
    connection = connectToMySQL(DB)
    
    for category in categories:
        query = "SELECT * FROM workout_categories WHERE name = %s"
        result = connection.query_db(query, (category,))
        if not result:
            query = "INSERT INTO workout_categories (name) VALUES (%s)"
            connection.query_db(query, (category,))
            print(f"Category '{category}' added to the database.")
    
    connection.close_connection()

if __name__ == "__main__":
    initialize_categories()
    print("Database initialized with default categories.")

# Initiate categories if not present in database