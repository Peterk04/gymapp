# Gym App
This is a small lightweight Python app that helps you track your workouts.
It has no GUI just CURL endpoints: workouts, exercises, sets (weights and reps). 
There is no DB implemented yet so only uses in-memory storage.
It runs inside a container so you dont have to set up python or flask yourself.

How to run it
1.Build the image.
podman build -t gymapp:0.1 .

2.Run the app in a container.
podman run -d -p 8080:8080 --name gymapp gymapp:0.1

3.Test it with curl (Use -4 so it connects over ipv4 (by default curl tries ipv6 but the container is published on ipv4 so the ipv6 request will fail)).
curl -4 -i http://localhost:8080/workouts           this should return []


Example flow
1.Create a workout.
curl -4 -i -X POST http://localhost:8080/workouts -H "Content-Type: application/json" -d '{"name":"push"}'

2.Add an exercise.
curl -4 -i -X POST http://localhost:8080/workouts/1/exercises -H "Content-Type: application/json" -d '{"name":"bench press"}'

3.Log a set.
curl -4 -i -X POST http://localhost:8080/workouts/1/exercises/1/sets -H "Content-Type: application/json" -d '{"weight":60,"reps":10}'

4.Review full workout.
curl -4 -i http://localhost:8080/workouts


I built this project to learn about containers.
I plan to keep using it as a sandbox to practice new stuff as i learn it.
I’d be happy to receive to suggestions on features or improvements that could help me learn in general using this as a sandbox (maybe adding a DB or trying out kubernetes?)



