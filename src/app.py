"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the soccer team and compete in inter-school tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Basketball Team": {
        "description": "Practice basketball and participate in local competitions",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Learn acting skills and perform in school plays",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities

# Validate student is not already signed up
def validate_student(activity, student_email):
    if student_email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    return True
# Sign up for an activity
@app.post("/activities/{activity_name}/signup")
def signup_activity(activity_name: str, student_email: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    validate_student(activity, student_email)
    activity["participants"].append(student_email)
    return {"message": f"Successfully signed up for {activity_name}"}
# Unsign up for an activity
@app.post("/activities/{activity_name}/unsignup")
def unsignup_activity(activity_name: str, student_email: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if student_email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not signed up for this activity")
    activity["participants"].remove(student_email)
    return {"message": f"Successfully unsignup from {activity_name}"}
# Get activity details
@app.get("/activities/{activity_name}")
def get_activity_details(activity_name: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity
# Get a list of all activities
@app.get("/activities/list")
def list_activities():
    return list(activities.keys())
# Get a list of all participants in an activity
@app.get("/activities/{activity_name}/participants")
def get_activity_participants(activity_name: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity["participants"]
# Get the maximum number of participants for an activity
@app.get("/activities/{activity_name}/max_participants")
def get_activity_max_participants(activity_name: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity["max_participants"]
# Get the schedule for an activity
@app.get("/activities/{activity_name}/schedule")
def get_activity_schedule(activity_name: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity["schedule"]
# Get the description for an activity
@app.get("/activities/{activity_name}/description")
def get_activity_description(activity_name: str):
    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity["description"]
# Get the list of all activities and their details
@app.get("/activities/all")
def get_all_activities():
    return activities
# Get the list of all participants in all activities
@app.get("/activities/participants")
def get_all_participants():
    all_participants = {}
    for activity_name, activity in activities.items():
        all_participants[activity_name] = activity["participants"]
    return all_participants
# Get the list of all activities and their schedules
@app.get("/activities/schedules")
def get_all_schedules():
    all_schedules = {}
    for activity_name, activity in activities.items():
        all_schedules[activity_name] = activity["schedule"]
    return all_schedules
# Get the list of all activities and their descriptions
@app.get("/activities/descriptions")
def get_all_descriptions():
    all_descriptions = {}
    for activity_name, activity in activities.items():
        all_descriptions[activity_name] = activity["description"]
    return all_descriptions
# Get the list of all activities and their maximum number of participants
@app.get("/activities/max_participants")
def get_all_max_participants():
    all_max_participants = {}
    for activity_name, activity in activities.items():
        all_max_participants[activity_name] = activity["max_participants"]
    return all_max_participants
# Get the list of all activities and their participants
@app.get("/activities/participants/all")
def get_all_activity_participants():
    all_participants = {}
    for activity_name, activity in activities.items():
        all_participants[activity_name] = activity["participants"]
    return all_participants
# Get the list of all activities and their details
@app.get("/activities/details")
def get_all_activity_details():
    all_details = {}
    for activity_name, activity in activities.items():
        all_details[activity_name] = {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"]
        }
    return all_details
# Get the list of all activities and their schedules
@app.get("/activities/schedules/all")
def get_all_activity_schedules():
    all_schedules = {}
    for activity_name, activity in activities.items():
        all_schedules[activity_name] = activity["schedule"]
    return all_schedules
# Get the list of all activities and their descriptions
@app.get("/activities/descriptions/all")
def get_all_activity_descriptions():
    all_descriptions = {}
    for activity_name, activity in activities.items():
        all_descriptions[activity_name] = activity["description"]
    return all_descriptions
# Get the list of all activities and their maximum number of participants
@app.get("/activities/max_participants/all")
def get_all_activity_max_participants():
    all_max_participants = {}
    for activity_name, activity in activities.items():
        all_max_participants[activity_name] = activity["max_participants"]
    return all_max_participants