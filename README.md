### fastapi template project, with poetry, click, postgres
## Running the DB
```sh
cd postgres
docker compose up -d
```

## Installation
```sh
poetry install
```

## Running
```sh
poetry run python -m fastapi dev ./server_with_db.py
```
Or use the provided `launch.json` from vscode

## Inspecting the DB using pgadmin
In a browser, connect to http://127.0.0.1:5050/browser/ with email admin@admin.com and password `root`
