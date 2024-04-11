# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .
COPY ../database/scrapy/recboj/recboj/Spiders /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory to the Scrapy project root directory
WORKDIR /usr/src/app/recboj/spiders

