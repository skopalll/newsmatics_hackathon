FROM node:14

WORKDIR /app

# Copy dependency definitions
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
