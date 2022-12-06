FROM python:3.8.12
# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# copy project
COPY . .
