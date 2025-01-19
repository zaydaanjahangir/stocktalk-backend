
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

# Setting Up and Running StockTalk Backend

This document provides step-by-step instructions to set up the StockTalk backend, including handling migrations, installing `pgvector`, and populating the database.

## 1. Install `pgvector` Manually

If you're using the default PostgreSQL image and need to install `pgvector` manually:

1. **Connect to the `db` Container**:
   ```bash
   docker exec -it stocktalk-backend-db-1 /bin/bash
   ```

2. **Install `pgvector`**:
   - Update the package list:
     ```bash
     apt-get update
     ```
   - Install `pgvector`:
     ```bash
     apt-get install postgresql-14-pgvector
     ```

3. **Exit the Container Shell**:
   ```bash
   exit
   ```

4. **Enable the Extension**:
   - Access the PostgreSQL container:
     ```bash
     docker exec -it stocktalk-backend-db-1 psql -U postgres
     ```
   - Inside the PostgreSQL prompt:
     - Connect to the database:
       ```sql
       \c stocktalk_db
       ```
     - Enable the `pgvector` extension:
       ```sql
       CREATE EXTENSION IF NOT EXISTS vector;
       ```

## 2. Fixing `pgvector` in Migrations

To fix the `NameError: pgvector` issue in your migration file:

1. **Exit the PostgreSQL Prompt**:
   ```sql
   \q
   ```

2. **Open a Shell in the App Container**:
   ```bash
   docker exec -it stocktalk-backend-app-1 /bin/bash
   ```

3. **Navigate to the Migrations Directory**:
   ```bash
   cd migrations/versions
   ```

4. **Edit the Migration File**:
   - Install a text editor if needed:
     ```bash
     apt-get update && apt-get install nano -y
     ```
   - Open the migration file for editing (e.g., `7fd185687244_initial_migration.py`):
     ```bash
     nano 7fd185687244_initial_migration.py
     ```
   - Add the following line at the top of the file:
     ```python
     import pgvector
     ```

5. **Save and Exit the Editor**:
   - Press `CTRL + O` to save.
   - Press `CTRL + X` to exit.

6. **Exit the App Container Shell**:
   ```bash
   exit
   ```

## 3. Apply Migrations

1. **Generate Migrations**:
   Inside the running app container or locally:
   ```bash
   flask db migrate -m "Initial migration"
   ```

2. **Apply Migrations**:
   ```bash
   flask db upgrade
   ```

3. **Run Scripts to Populate the Database**:
   ```bash
   docker exec -it stocktalk-backend-app-1 python populate_db.py
   docker exec -it stocktalk-backend-app-1 python compute_embeddings.py
   ```

---

This completes the setup of the StockTalk backend. For additional details, refer to the project documentation.

