FROM node:18-bullseye

# Install Python3 & pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Node.js dependencies
RUN npm install

# Install Python dependencies if needed
# RUN pip3 install -r requirements.txt

# Make script executable
RUN chmod +x start.sh

# Start the script
CMD ["./start.sh"]
