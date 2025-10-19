# Use the official Python image
FROM python:3.13-slim

# Set the UID and GID for the new user. Choose unique numbers (e.g., 1001).
# This helps avoid conflicts with existing users on the host when mounting volumes.
ARG UID=1001
ARG GID=1001

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a group and user with fixed UID/GID
RUN groupadd -g $GID appuser && \
    useradd -u $UID -g $GID -m -s /bin/bash appuser

# Install Python dependencies as root (this is safe, pip installs to /usr/local)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the working directory and make the user the owner
WORKDIR /app
RUN chown -R appuser:appuser /app

# Switch to the appuser
USER appuser

# Copy the application code as the appuser (optional but logical)
# Copying usually happens before USER, but can also happen after, as long as permissions are correct
COPY --chown=appuser:appuser main.py .

# Ensure the user has permissions on the data directory (if mounted as an empty volume)
# RUN mkdir -p /app/data && chown appuser:appuser /app/data
# (This might not be needed if /app/data is created by the Python code or permissions are set on the volume)

# Specify the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
