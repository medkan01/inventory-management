FROM node:22-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --omit=dev

# Copy application code
COPY . .

# Build arguments for Supabase
ARG SUPABASE_URL
ARG SUPABASE_ANON_KEY

# Set environment variables for build
ENV SUPABASE_URL=$SUPABASE_URL
ENV SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY

# Build the application
RUN npm run build

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]