from flask_app.config.mysqlconnection import connectToMySQL

DB = "Workout"

def initialize_categories():
    categories = [(1, "Strength"), (2, "Cardio"), (3, "Yoga")]
    connection = connectToMySQL(DB)
    
    for category_id, category_name in categories:
        query = "SELECT * FROM workout_categories WHERE id = %s"
        result = connection.query_db(query, (category_id,))
        if not result:
            query = "INSERT INTO workout_categories (id, name) VALUES (%s, %s)"
            connection.query_db(query, (category_id, category_name))
            print(f"Category with ID '{category_id}' and name '{category_name}' added to the database.")
    
    
    connection.close_connection()

if __name__ == "__main__":
    initialize_categories()
    print("Database initialized with default categories.")

# Initiate categories if not present in database