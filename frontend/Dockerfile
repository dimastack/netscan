# Step 1: Build the React application
FROM node:23 AS build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application for production
RUN npm run build

# Step 2: Serve the React application using an Nginx server
FROM nginx:alpine

# Copy the built app from the previous stage to the Nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 (the default port for Nginx)
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
