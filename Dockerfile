# Use a lightweight Python image
FROM python:3.11-slim

# Install dependencies
RUN pip install reportlab

# Create working directory
WORKDIR /app

# Copy script into container
COPY make_labels.py /app/make_labels.py

# Default command (can be overridden)
ENTRYPOINT ["python", "/app/make_labels.py"]

# docker build -t make_labels .
# docker run --rm -v "$(pwd)":/app make_labels addresses.csv labels.pdf

