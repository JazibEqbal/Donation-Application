# base image that already has Python 3.12 installed
FROM python:3.12-slim

# everything runs inside /app inside the container
WORKDIR /app

# Copy dependancy file, requirements.txt into the current working directory (/app)
# why copy requirements.txt? Because, If only your code changes → dependencies are reused else If requirements.txt changes → dependencies are rebuilt. This is only called Docker layer caching.
COPY requirements.txt .

# Install dependencies
# --no-cache-dir? Inside Docker, the pip cache isn't useful after the image is built. Therefore by using --no-cache-dir we disable it to keep the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# copies everything to /app
COPY . .

# Application port
EXPOSE 8000

# uvicorn: starts the server,
# app.main:app Import the app object from app/main.py,
# --host 0.0.0.0 Listen on all network interfaces inside the container. Note 127.0.0.1 is only accessible from inside the container while 0.0.0.0 allows Docker to forward traffic from your machine to the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]