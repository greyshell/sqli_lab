FROM python:3.9.14-slim
RUN apt-get update

COPY . /app
WORKDIR /app

RUN apt-get install -y gcc wget curl
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"
RUN apt-get install libmariadb3 libmariadb-dev -y

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python","app.py"]