# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system build dependencies required for machine learning libraries (like scipy/scikit-learn)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first (this caches the installation step to save time on future builds)
COPY requirements.txt .

# Install the Python dependencies (upgrade pip and setuptools first to fix wheel build errors)
RUN pip install --no-cache-dir --upgrade pip "setuptools<70.0.0" wheel
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# 1. Copy only the files needed to build the vector database
COPY app/ app/
COPY scripts/ scripts/
COPY sample_guidelines.json .

# Run the seeding script to pre-download HuggingFace models and build ChromaDB
# Because this is done BEFORE copying frontend files, UI changes won't trigger a rebuild of this slow step!
RUN python scripts/seed_vector_db.py

# 2. Copy the rest of the application code (like frontend.html)
COPY . .

# Expose port 7860 for the FastAPI server (HuggingFace default)
EXPOSE 7860

# Command to run the Uvicorn server when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]