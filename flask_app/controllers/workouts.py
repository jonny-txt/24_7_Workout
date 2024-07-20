from flask import Flask, render_template, request, redirect, session  
from flask_app import app
from flask_app.models.workout import Workout
from flask_app.models.user import User
from flask_app.models import user, workout
from flask import flash


@app.route('/workout/add', methods=['POST'])         
def add_workout():  
    if 'user_id' not in session:
        return redirect('/logout')    
    
    if not Workout.validate_workout(request.form):
        return redirect('/workout/new')
    
    workout.Workout.save_workout(request.form)   
    return redirect("/dashboard")



@app.route('/workouts')         
def all_workouts():   
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    workouts = Workout.get_all_workouts_with_creator()
    
    return render_template("dashboard.html",user=User.get_user_by_id(data), all_workouts=workouts)

@app.route('/workout/create', methods=['POST'])
def create_workout():
    data={
        "name":request.form['name'],
        "user_id":session['user_id']
    }
    Workout.save_workout(data)

@app.route('/workout/view/<workout_id>')
def view_workout(workout_id,):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    workouts = Workout.get_all_workouts_with_creator()
    workout_=workout.Workout.get_one_workout_id(workout_id)
    
    workout_posted_by=Workout.get_one_workout_with_creator(workout_id)
    

    return render_template('view_workout.html',workout_with_author=workout_posted_by, workout=workout_, all_workouts=workouts, user=User.get_user_by_id(data))

@app.route('/workout/edit/<workout_id>')
def edit_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')  
    
    data = {
        'id':session['user_id']
    }

    workout_=workout.Workout.get_one_workout_id(workout_id)    
    return render_template('edit_workout.html',workout=workout_, user=User.get_user_by_id(data))

@app.route('/workout/update/<workout_id>', methods=['POST'])         
def update_workout(workout_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    workout_=workout.Workout.get_one_workout_id(workout_id)

    if not Workout.validate_workout(request.form):
        return render_template('edit_workout.html',workout=workout_,user=User.get_user_by_id(data))
    
    workout.Workout.update_workout(request.form)   
    return redirect('/workouts')

 
@app.route('/workout/delete/<workout_id>')         
def delete_workout(workout_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    
    workout.Workout.delete_workout(workout_id)
    return redirect('/dashboard')  