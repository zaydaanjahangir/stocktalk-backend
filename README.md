
# StockTalk Backend

This is the backend application for StockTalk, powered by Flask and PostgreSQL, running inside Docker containers.

## Prerequisites
- Docker installed on your system
- Git installed

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stocktalk-backend.git
   cd stocktalk-backend
   ```

2. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Flask app: [http://localhost:5001](http://localhost:5001)

5. Stop the containers:
   ```bash
   docker-compose down
   ```

## Notes
- The database is initialized using the `docker-compose.yml` configuration.
- To clear all data, remove the volume:
  ```bash
  docker volume rm stocktalk-backend_postgres_data
  ```
