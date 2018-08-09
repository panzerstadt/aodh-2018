## docker commands for updating the backend container

`docker build -t aodh-2018-backend .` (make that container)
`docker tag aodh-2018-backend gcr.io/asia-open-data-hacktahon-2018/aodh-2018-backend:latest` (label for google)
`gcloud docker -- push gcr.io/asia-open-data-hacktahon-2018/aodh-2018-backend:latest` (google's github for containers)
then go and delete your currently running container first before doing the next step
`kubectl run aodh-2018-backend-app --image=gcr.io/asia-open-data-hacktahon-2018/aodh-2018-backend:latest --port=5000` (start a container on kubernetes)
