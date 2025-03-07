FROM python:3.12.5-slim

COPY . /app
WORKDIR /app

# install dependencies
RUN apt-get update
RUN apt-get install -y libmariadb3 libmariadb-dev gcc wget curl python3-dev default-libmysqlclient-dev build-essential

# set up database
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup

# install python dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python","app.py"]
