FROM python:3.11-slim-buster

LABEL image="image_caption_generator"

# Set the working directory
WORKDIR /app 

# Copy all data to working directory app
COPY . /app  

# Update the package list and install dependencies
RUN apt-get update -y && apt-get install -y awscli

# Install Python dependencies
RUN pip install uv && pip install -r requirements.txt

# Expose port 1001 for external access
EXPOSE 1001

# Define environment variable
ENV NAME=UAT

# Run the application
CMD ["sh", "-c", "python3 /app/IC_django/manage.py runserver 0.0.0.0:1001"]
