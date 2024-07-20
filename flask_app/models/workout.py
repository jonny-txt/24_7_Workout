from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime


class Workout:
    DB="24_7_workout"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.location = data['location']
        self.date = data['date']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.what_happen=data['what_happen']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        
        self.creator= None
        

    @classmethod 
    def save_workout(cls,data):
        print('before saving workout')
        query="INSERT INTO workouts (user_id,location,date,number_of_sasquatches,what_happen) VALUES (%(user_id)s,%(location)s,%(selectedDate)s,%(number_of_sasquatches)s,%(what_happen)s);"
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return result
    
    @classmethod
    def update_workout(cls,data):
        print('----------------------before updating workout')
        query = """UPDATE workouts SET location=%(location)s, date=%(selectedDate)s, number_of_sasquatches=%(number_of_sasquatches)s, what_happen=%(what_happen)s WHERE id=%(id)s"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete_workout(cls,workout_id):
        query='DELETE FROM workouts WHERE id=%(workout_id)s'
        data={
            'workout_id':workout_id
        }
        connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_all_workouts(cls):
        query = "SELECT * FROM workouts;"        
        results = connectToMySQL(cls.DB).query_db(query)        
        workouts = []        
        for workout in results:
            workouts.append(cls(Workout))
        return workouts
    
    @classmethod
    def get_one_workout_id(cls,workout_id):
        query = """SELECT * FROM workouts WHERE id=%(workout_id)s"""
        data={
            'workout_id':workout_id
        }
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return cls(result[0])  

    @classmethod
    def get_all_workouts_with_creator(cls):
        query='SELECT * FROM workouts JOIN users ON workouts.user_id=users.id;'
        results=connectToMySQL(cls.DB).query_db(query)
        
        all_workouts=[]
        for row in results:

            one_workout=cls(row)

            one_workout_author_info={
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            author=user.User(one_workout_author_info)

            one_workout.creator=author

            all_workouts.append(one_workout)
        
        return all_workouts

    @classmethod
    def get_one_workout_with_creator(cls,workout_id):
        query='SELECT * FROM workouts LEFT JOIN users ON workouts.user_id=users.id WHERE workouts.id=%(workout_id)s'
        data={
            'workout_id':workout_id
        }
        results=connectToMySQL(cls.DB).query_db(query,data)
        workout_object = cls(results[0])
        
        author_info={
                'id':results[0]['users.id'],
                'first_name':results[0]['first_name'],
                'last_name':results[0]['last_name'],
                'email':results[0]['email'],
                'password':results[0]['password'],
                'created_at':results[0]['users.created_at'],
                'updated_at':results[0]['users.updated_at']
            }
        author_object = user.User(author_info)
        workout_object.creator = author_object
       
        return workout_object

    @staticmethod
    def validate_workout(workout):
        is_valid=True        
        
        if len(workout['location'])<=0:
            flash('workout location is required', "new_workout")
            is_valid=False
        if len(workout['number_of_sasquatches'])<=0:
            flash('Number of sasquatches must be at least 1', "new_workout")
            is_valid=False
        if len(workout['what_happen'])<=0:
            flash('Notes on what happen at location should be added', "new_workout")
            is_valid=False
        if len(workout['what_happen'])>50:
            flash('Notes on what happen should have a maximum of 50 characters', "new_workout")
            is_valid=False
          
        return is_valid