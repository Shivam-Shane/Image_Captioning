FROM python:3.11-slim-buster
LABEL image="image_caption_generator"
# Set the working directory
WORKDIR /app 
# coping all data to working directory app
COPY . /app  
# updating the linux os
RUN apt update -y && apt install awscli -y
# installing all the dependencies of project
RUN apt-get update && pip install -r requirements.txt
# exposing port 1001 for external access
EXPOSE 1001:1001
# Define environment variable
ENV NAME UAT
# at last running the application
CMD ["sh", "-c", "python3 /app/IC_django/manage.py runserver 1001"]