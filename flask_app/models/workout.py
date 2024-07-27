from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Workout:
    DB = "Workout"
    
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.category_id = data['category_id']
        self.date = data['date']
        self.details = data['details']
        self.duration = data['duration']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.category = data['category'] if 'category' in data else None

    @classmethod 
    def save_workout(cls, data):
        
        query = "INSERT INTO workouts (user_id, category_id, date, details, duration) VALUES (%(user_id)s, %(category_id)s, %(date)s, %(details)s, %(duration)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def update_workout(cls, data):
        query = "UPDATE workouts SET category_id = %(category_id)s, date = %(date)s, details = %(details)s, duration = %(duration)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def delete_workout(cls, workout_id):
        query = "DELETE FROM workouts WHERE id = %(workout_id)s;"
        data = {'workout_id': workout_id}
        connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_workouts(cls):
        query = """
            SELECT workouts.*, workout_categories.name AS category 
            FROM workouts 
            LEFT JOIN workout_categories ON workouts.category_id = workout_categories.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return []
        workouts = []
        for workout in results:
            workouts.append(cls(workout))
        return workouts
    
    @classmethod
    def get_one_workout_id(cls, workout_id):
        query = """
            SELECT workouts.*, workout_categories.name AS category 
            FROM workouts 
            LEFT JOIN workout_categories ON workouts.category_id = workout_categories.id 
            WHERE workouts.id = %(workout_id)s;
        """
        data = {'workout_id': workout_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return None
        return cls(result[0])  

    @classmethod
    def get_all_workouts_by_user(cls, user_id):
        query = """
            SELECT workouts.*, workout_categories.name AS category 
            FROM workouts 
            LEFT JOIN workout_categories ON workouts.category_id = workout_categories.id 
            WHERE workouts.user_id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return []
        workouts = []
        for row in results:
            workouts.append(cls(row))
        return workouts

    @classmethod
    def get_one_workout_with_creator(cls, workout_id):
        query = """
            SELECT workouts.*, workout_categories.name AS category, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at 
            FROM workouts 
            LEFT JOIN users ON workouts.user_id = users.id 
            LEFT JOIN workout_categories ON workouts.category_id = workout_categories.id 
            WHERE workouts.id = %(workout_id)s;
        """
        data = {'workout_id': workout_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        workout_object = cls(results[0])
        author_info = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        author_object = user.User(author_info)
        workout_object.creator = author_object
        return workout_object

    @staticmethod
    def validate_workout(workout):
        is_valid = True        
        if not workout.get('details'):
            flash('Workout details are required', "new_workout")
            is_valid = False
        if not workout.get('duration') or not str(workout['duration']).isdigit() or int(workout['duration']) <= 0:
            flash('Duration must be a positive number', "new_workout")
            is_valid = False
        return is_valid
