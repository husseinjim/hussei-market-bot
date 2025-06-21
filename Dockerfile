FROM node:18-bullseye

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python & Node.js dependencies
RUN pip3 install -r requirements.txt
RUN npm install

# Start both scripts
CMD ["bash", "start.sh"]
