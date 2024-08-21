# Dockerfile to run the application in development mode on Local Machine
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /application
#RUN mkdir /application/app

# Installing python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY app/ /application/app

# Copy the environment variables file into the container
COPY config/env/.env.dev /application/.env

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]