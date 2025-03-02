# Use Python 3.8 as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Run migrations and the management command
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_person && python manage.py runserver --insecure 0.0.0.0:8000"]
