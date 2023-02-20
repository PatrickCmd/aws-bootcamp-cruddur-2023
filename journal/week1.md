# Week 1 — App Containerization

## Push and tag a images to DockerHub
### Build backend container
```sh
docker build -t  backend-flask ./backend-flask
```

![backend flask build](assets/week-1/backend-flask-build-01.png)

![docker images backend flask local](assets/week-1/docker-images-backend-flask.png)

### Tag and push backend-flask image to remote repository on docker hub

- Create an account on [docker hub](https://hub.docker.com/) and generate an access token. Go to `account settings` and then `security`. I use this access token to login to docker hub via `CLI`.

![docker hub access token](assets/week-1/docker_hub_access_token.png)

Export your access token as an environment variable in gitpod
Remember to replace the `DOCKER_ACCESS_TOKEN` with your generated access token

```sh
export DOCKER_ACCESS_TOKEN="dckr_xxxxxxxxxxxxxxxxxxxxxxxxx_nRpk"
gp env DOCKER_ACCESS_TOKEN=$DOCKER_ACCESS_TOKEN
```

I use the commands below to tag the backend flask image to my remote docker hub registry and push

```sh
REPOSITORY_NAME=cruddur-backend-flask
DOCKER_HUB_USERNAME=patricktcmd
PREFIX=${DOCKER_HUB_USERNAME}/${REPOSITORY_NAME}

BACKEND_IMAGE_LOCAL=backend-flask:latest
BACKEND_IMAGE_REMOTE=${PREFIX}:v01
docker tag ${BACKEND_IMAGE_LOCAL} ${BACKEND_IMAGE_REMOTE}

echo $DOCKER_ACCESS_TOKEN | docker login -u patricktcmd --password-stdin

docker push ${BACKEND_IMAGE_REMOTE}
```

![docker backend flask image remote](assets/week-1/docker-images-backend-flask-remote.png)

![docker backend flask image push remote](assets/week-1/docker-images-backend-flask-push-remote.png)

![cruddur backend flask remote image](assets/week-1/cruddur-backend-flask-remote-image.png)