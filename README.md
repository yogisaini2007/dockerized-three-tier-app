# Dockerized Three-Tier Task Manager

A beginner-friendly DevOps project with:
- **Frontend:** HTML/CSS/JavaScript served by Nginx
- **Backend:** Python + Flask REST API
- **Database:** MySQL 8.4
- **Orchestration:** Docker Compose
- **Persistence:** named Docker volume for MySQL data
- **Networking:** frontend proxies `/api/` requests to the backend on a private Compose network

## Prerequisites

- Docker Engine
- Docker Compose plugin (`docker compose`)
- Git (optional, for version control)

Check your installation:

```bash
docker --version
docker compose version
```

## Run locally on Ubuntu/Linux

1. Open a terminal in this project folder.
2. Create your local environment file:

```bash
cp .env.example .env
```

3. Build and start all services:

```bash
docker compose up --build -d
```

4. Check service status:

```bash
docker compose ps
```

5. Open the application in your browser:

```text
http://localhost:8080
```

6. Check the API and database connection:

```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/tasks
```

Add a task through the browser; it should appear in the task list.

## Useful troubleshooting commands

```bash
docker compose logs -f
docker compose logs -f backend
docker compose logs -f db
docker compose exec backend python -c "print('Backend container is running')"
docker compose ps
```

If port 8080 is already in use, change the left side of `"8080:80"` in `docker-compose.yml` to another free port, such as `"8081:80"`.

## Test database persistence

1. Add a task in the browser.
2. Restart the services:

```bash
docker compose down
docker compose up -d
```

3. Refresh the page. The task should still exist because the `mysql_data` named volume persists.

**Do not** run `docker compose down -v` for this test: `-v` deletes the database volume and its stored data.

## Stop the project

```bash
docker compose down
```

To delete containers AND the local database volume (destructive):

```bash
docker compose down -v
```

## DevOps learning challenges

1. Add a DELETE endpoint and a delete button.
2. Add a backend unit test and run it in GitHub Actions.
3. Add a non-root container user and explain why it helps.
4. Add a health check for the backend.
5. Build and publish the backend image to a container registry.
6. Deploy to an AWS EC2 test instance after learning security groups and secrets management.

## Security notes

- `.env` is excluded from Git; never commit real credentials.
- The credentials in `.env.example` are for local practice only. Do not use them for an internet-facing deployment.
- The database is not published to the host; it is reachable only by services on the Compose network.
- For production, use managed secrets, strong credentials, TLS, restricted network access, dependency updates and backups.
Learning Git branching and DevOps CI/CD.
