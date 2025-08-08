FROM python:3.8-buster

# Set the working directory to /app
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc libpcre3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
#ENV REGION=Europe

CMD ["uwsgi", "--ini", "uwsgi.ini"]
#CMD ["python", "wsgi.py"]

