# Use an official Python runtime as a parent image
FROM python:3.10.4

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the 'app' directory to the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "/app/main.py"]

