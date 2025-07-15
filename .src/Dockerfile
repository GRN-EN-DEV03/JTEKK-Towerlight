# Use an official Python runtime as the base image.
# We specify a version for consistency. 'slim-buster' versions are smaller.
FROM python:3.9-slim-buster

# Set the working directory inside the container.
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy the requirements.txt file from your local machine to the /app directory in the container.
# This step is often done first to leverage Docker's build cache.
COPY requirements.txt .

# Install any Python packages listed in requirements.txt.
# --no-cache-dir reduces the image size by not storing build cache.
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of your application code from the current directory
# on your local machine to the /app directory in the container.
COPY . .

# Specify the command to run when the container starts.
# Use the "exec" form (CMD ["executable", "param1"]) for better compatibility.
CMD ["python", "main.py"]