FROM python:3.11-slim-buster

LABEL image="image_caption_generator"

# Set the working directory
WORKDIR /application

# Install build dependencies to compile SQLite
RUN apt-get update -y && apt-get install -y \
    build-essential \
    wget \
    libsqlite3-dev \
    vim

# Download, compile, and install the latest SQLite version
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3460100.tar.gz \
    && tar xvfz sqlite-autoconf-3460100.tar.gz \
    && cd sqlite-autoconf-3460100 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3460100 sqlite-autoconf-3460100.tar.gz

# Update the shared libraries cache
RUN ldconfig

# Verify SQLite version
RUN sqlite3 --version

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
