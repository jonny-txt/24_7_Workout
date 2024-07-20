from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import workout

class User:
    DB="24_7_workout"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.workouts=[]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"        
        results = connectToMySQL(cls.DB).query_db(query)        
        users = []        
        for user in results:
            users.append(cls(user))
        return users

    @classmethod 
    def save_user(cls,data):
        query="INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        result=connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users LEFT JOIN workouts on users.id=workouts.user_id WHERE users.id=%(id)s;"
        result=connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        user=cls(result[0])
        for one_workout in result:
            n = {
                'id': one_workout['workouts.id'],
                'user_id': one_workout['user_id'],
                'name': one_workout['name'],
                'description': one_workout['description'],
                'instructions': one_workout['instructions'],
                'date_cooked_or_made': one_workout['date_cooked_or_made'],
                'under_30_minutes': one_workout['under_30_minutes'],
                'created_at': one_workout['workouts.created_at'],
                'updated_at': one_workout['workouts.updated_at']
            }        
            user.workouts.append(Workout(n))
            print(one_workout)
        return user    

    @classmethod
    def get_user_by_email(cls,str):
        data = {"email":str}
        query = "SELECT * FROM users WHERE email=%(email)s;"              
        results = connectToMySQL(cls.DB).query_db(query,data)   
        print("---------r----------",results)
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        
        query = "SELECT * FROM users WHERE id=%(id)s;"        
        results = connectToMySQL(cls.DB).query_db(query,data)        

        print("\n\n\n-------->results: ", results)
        return cls(results[0])
        
    @staticmethod
    def validate_user(user):
        is_valid=True
        query = "SELECT * FROM users WHERE email=%(email)s;"        
        connectToMySQL(User.DB).query_db(query,user)
        return is_valid

    @staticmethod
    def validate_registration(user):
        is_valid=True
        query = "SELECT * FROM users WHERE email=%(email)s;"        
        results=connectToMySQL(User.DB).query_db(query,user)
        if(len(results)>=1):
            flash("An user is registered with that email, register with a different email", "register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email was not found, please register", "register")
            is_valid=False
        if len(user['first_name'])<2:
            flash('First name must be at least two letters', "register")
            is_valid=False
        if len(user['last_name'])<2:
            flash('Last name must be at least two letters', "register")
            is_valid=False
        if len(user['password'])<8:
            flash('Password must be at least 8 characters', "register")
            is_valid=False 
        if user['password']!=user['confirm_password']:
            flash('Passwords do not match',"register")
            is_valid=False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid=True
        query = "SELECT * FROM users WHERE email=%(email)s;"        
        results=connectToMySQL(User.DB).query_db(query,user)
        if(len(results)==0):
            flash("Invalid Credentials", "login")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email was not found, please register", "register")
            is_valid=False
        
        return is_valid