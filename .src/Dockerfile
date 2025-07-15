# Use an official Python runtime as the base image.
# We specify a version for consistency. 'slim-buster' versions are smaller.
# CHANGED: Updated Python version to 3.10 to meet pymodbus==3.9.2 requirements.
# CHANGED: Updated base image from 'buster' to 'slim' (Debian Bookworm).
FROM python:3.10-slim

# Set the working directory inside the container.
# All subsequent commands will run from this directory.
WORKDIR /app

# Install essential tools (curl, gnupg) and system dependencies for ODBC.
# Purge conflicting pre-installed ODBC packages first to avoid dpkg errors.
# The 'slim' image is based on Debian Bookworm (Debian 12).
# CHANGED: Added 'gnupg' to this install step.
RUN apt-get update && \
    apt-get purge -y --auto-remove \
        libodbc2 \
        libodbccr2 \
        libodbcinst2 \
        unixodbc-common && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        curl \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft's repository key and source list for MS SQL Server ODBC Driver.
# Using the modern, recommended way to add GPG keys for Debian Bookworm.
# CHANGED: Updated Debian version in the URL to '12' for Bookworm compatibility.
# CHANGED: Added separate steps to create keyrings directory and download key.
# CHANGED: Modified prod.list URL to include 'signed-by' option.
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list

# Install the Microsoft ODBC Driver for SQL Server and SQL Server tools.
# This will automatically pull in compatible unixodbc-dev and odbcinst1debian2 from Microsoft's repo.
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql17 \
        mssql-tools && \
    rm -rf /var/lib/apt/lists/*

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

# docker build -t tower-light-controller .
# docker run -d --name tower-light-controller-service --restart unless-stopped -e APP_NAME="Docker User" tower-light-controller