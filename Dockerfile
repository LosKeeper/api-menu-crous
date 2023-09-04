# Use the official image as a parent image.
FROM python:3

# Set the working directory.
WORKDIR /app

# Copy the file from your host to your current location.
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY parsing.py parsing.py

# Expose the port the app runs in.
EXPOSE 5000

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run the API
CMD ["python3", "main.py"]
