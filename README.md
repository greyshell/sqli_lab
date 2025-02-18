# sqli_lab

Play with `INSERT` and `SELECT` query.

## How to use

- Run the docker compose file

```bash
# run the app in detached  mode
sudo docker-compose up --build -d

# stop and delete the container
sudo docker-compose down

# clean the docker images
chmod a+x clean_docker.sh 
./clean_docker.sh
```
- Open `http://127.0.0.1:8000/scenario-1`
