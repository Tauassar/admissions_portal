# pull official base image
FROM python:3

# install dependencies
RUN pip install --upgrade pip
COPY ./dev_requirements.txt .
RUN pip install -r dev_requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY ./admissions /app

# set work directory
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
