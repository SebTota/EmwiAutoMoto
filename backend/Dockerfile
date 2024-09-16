FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the backend directory
RUN mkdir backend

# Copy the backend directory contents into the container
COPY . ./backend/

# Set the Python path to include the app directory
ENV PYTHONPATH=/app

# Command to run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]