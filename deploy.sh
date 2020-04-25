echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t anandrkskd/flaskapp:latest -tanandrkskd/flaskapp:$SHA -f .
docker build -t anandrkskd/flaskapp:$SHA -t anandrkskd/flaskapp:latest .
docker build -t anandrkskd/flaskapp:latest .

docker push anandrkskd/flaskapp:latest
docker push anandrkskd/flaskapp:$SHA

kubectl apply -f ./k8s
kubectl set image deployments/flask-deployment falsk=anandrkskd/flaskapp:$SHA