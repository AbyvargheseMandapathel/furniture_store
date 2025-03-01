# Use Python 3.12 official image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Expose the port for Django
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
