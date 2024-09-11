# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /media/bucardo/conf

# Install required Python libraries
RUN pip install boto3

# Copy the current directory contents into the container
COPY app.py .

# Run the Python script
CMD ["python", "app.py"]

