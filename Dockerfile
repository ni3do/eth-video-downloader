# Use an official Python runtime as a parent image
FROM python:latest

RUN mkdir /app
ADD . /app
# Set the working directory to /app
WORKDIR /app

RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD python /app/downloader.py
