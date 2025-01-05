# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app/ExploreBlog

# Install system dependencies and Python build dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    libpq-dev \
    wget \
    curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.12 python3.12-venv python3.12-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Set Python 3.12 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --config python3

# Upgrade pip to the latest version
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Copy the requirements file and install dependencies
COPY /ExploreBlog/requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY /ExploreBlog .

# Expose the port the app runs on
EXPOSE 8000

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Make migrations
RUN python3 manage.py makemigrations

# Run migrations
RUN python3 manage.py migrate

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]