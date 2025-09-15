from flask import Flask, jsonify, request, abort


app = Flask(__name__)


#in memory storage for now will add a db at a later stage
#Workouts storage
workouts = {}
next_workout_id = 1

#Exercise storage
exercises = {}
next_exercise_id = 1

#Set storage
sets = {}
next_set_id = 1


# - Workouts endpoints
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

# - Exercises endpoints
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

# - Sets endpoints
@app.post("/workouts/<int:wid>/exercises/<int:eid>/sets")
def create_set(wid, eid):
    global next_set_id
    if wid not in workouts:
        abort(404, description="not found")
    #check exercise exists and belongs to the right workout
    exercise = exercises.get(eid)
    if not exercise or exercise["workout_id"] != wid:
        abort(404, description="not found")

    if not request.is_json:
        abort(400, description="invalid input")

    data = request.get_json()
    try:
        weight = float(data.get("weight"))
        reps = int(data.get("reps"))
    except Exception:
        abort(400, description="invalid input")

    if weight <= 0 or reps <= 0:
        abort(400, description="invalid input")

    s = {"id": next_set_id, "exercise_id": eid, "weight": weight, "reps": reps}
    sets[next_set_id] = s
    next_set_id += 1
    return jsonify(s), 201

@app.get("/workouts/<int:wid>/exercises/<int:eid>/sets")
def list_sets(wid, eid):
    if wid not in workouts:
        abort(404, description="not found")
    exercise = exercises.get(eid)
    if not exercise or exercise["workout_id"] != wid:
        abort(404, description="not found")

    ss = [s for s in sets.values() if s["exercise_id"] == eid]
    return jsonify(ss)


#error handler to keep json errors consisten
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.description if hasattr(e, "description") else "error"}), e.code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
