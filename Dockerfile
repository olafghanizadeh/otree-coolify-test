# syntax=docker/dockerfile:1
FROM python:3.10

# Ensuring that Python output is displayed immediately
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
