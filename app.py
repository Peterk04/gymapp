from flask import Flask, jsonify, request, abort

app = Flask(__name__)

#in memory storage for now
workouts = {}
next_workout_id = 1

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

#error handler to keep json errors consisten
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.description if hasattr(e, "description") else "error"}), e.code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
