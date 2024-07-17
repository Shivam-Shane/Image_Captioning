FROM python:3.11-slim-buster

LABEL image="image_caption_generator"

# Set the working directory
WORKDIR /application

# Copy all data to working directory app
COPY . /application

# Update the package list and install dependencies
RUN apt-get update -y && apt-get install -y awscli 

# installing vim editor for file read/write
RUN apt-get install vim -y 

# Install Python dependencies
RUN pip install uv && pip install -r requirements.txt

# Expose port 8080 for external access
EXPOSE 8080

# Define environment variable
ENV NAME=PROD

# Run the application
CMD ["sh", "-c", "python3 /application/IC_django/manage.py runserver 0.0.0.0:8080"]
