from flask import Flask, jsonify, request, abort


app = Flask(__name__)


#in memory storage for now
#Workouts storage
workouts = {}
next_workout_id = 1

#Exercises storage (also in memory for now, will add db at later stage)
exercises = {}
next_exercise_id = 1


#Workouts endpoints
@app.get("/workouts")
def list_workouts():
    return jsonify(list(workouts.values()))

@app.post("/workouts")
def create_workout():
    global next_workout_id
    if not request.is_json:
        abort(400, description="invalid input")

    data = request.get_json()
    name = (data.get("name") or "").strip()

    if not name:
        abort(400, description="invalid input")

    workout = {"id": next_workout_id, "name": name}
    workouts[next_workout_id] = workout
    next_workout_id += 1
    return jsonify(workout), 201

#Exercises endpoints
@app.post("/workouts/<int:wid>/exercises")
def create_exercise(wid):
    global next_exercise_id
    if wid not in workouts:
        abort(404, description="not found")

    if not request.is_json:
        abort(400, description="invalid inpurt")

    data = request.get_json()
    name = (data.get("name") or "").strip()
    if not name:
        abort(400, desription="invalid input")

    exercise = {"id": next_exercise_id, "workout_id": wid, "name": name}
    exercises[next_exercise_id] = exercise
    next_exercise_id += 1
    return jsonify({"id": exercise["id"], "name": exercise["name"]}), 201

@app.get("/workouts/<int:wid>/exercises")
def list_exercises(wid):
    if wid not in workouts:
        abort(404, description="not found")

    exs = [
        {"id": e["id"], "name": e["name"]}
        for e in exercises.values()
        if e["workout_id"] == wid
    ]
    return jsonify(exs)


#error handler to keep json errors consisten
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.description if hasattr(e, "description") else "error"}), e.code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
