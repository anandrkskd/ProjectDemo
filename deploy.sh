docker build -t anandrkskd/flaskapp:latest -t anandrkskd/flaskapp:$SHA -f .

docker push anandrkskd/flaskapp:latest
docker push anandrkskd/flaskapp:$SHA

kubectl apply -f ./flaskblog/k8s
kubectl set image deployments/server-deployment server=anandrkskd/flaskapp:$SHA