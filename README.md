# Task API

A simple fastapi CRUD API for managing tasks.

## Getting started

Start the server:

```bash
uv run fastapi dev
```
The API runs at `http://localhost:8000`.

Stage 5: Swagger UI
OpenAPI docs (Swagger UI) are at [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

### `GET /`

Returns metadata about the API.

**Response**

```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}
```

**Example**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: */*'
  ```

### `GET /health`

Health check endpoint.

**Response**

```json
{
  "status": "ok"
}
```

**Example**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: */*'
```

### `GET /tasks`

Returns all the tasks.

**Response**

```json
[
  {
    "id": 1,
    "title": "surat al-kahf",
    "done": false
  },
  {
    "id": 2,
    "title": "clean room",
    "done": false
  },
  {
    "id": 3,
    "title": "eat breakfast",
    "done": true
  }
]
```

**Example**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: */*'
  ```

### `GET /tasks/{id}`

Returns a single task by id.

**Response (200)**

```json 
{
  "id": 1,
  "title": "surat al-kahf",
  "done": false
}
```

**Response (404)**

```json
{
  "detail": "item 555 not found"
}
```

**Example**

```bash

curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/1' \
  -H 'accept: */*'

curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/555' \
  -H 'accept: */*'
  ```

### `POST /tasks`

Creats a new task.

**Request body**

```json
{
  "title": "make dinner"
}
```

**Response (201)**

```json 
{
  "id": 4,
  "title": "make dinner",
  "done": false
}
```

**Response (400)**

```json
{
  "detail": "Title cannot be empty"
}
```

**Example**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": " make dinner"
}'
```

### `PUT /tasks/:id`

Updates a task's `title` and/or `done` by id. Send one or both fields; omitted fields stay unchanged.

**Request body**

```json 
{
  "id": 1,
  "title": "go for a run ",
  "done": true
}
```
**Response (200)**

```json 
{
  "id": 1,
  "title": "go for a run ",
  "done": true
}
```

**Response (400)**

```json
{
  "detail": "Envalid/Empty Bady"
}
```

**Response (404)**

```json 
{
  "detail": "item 100 not found"
}
```

### `DELETE /task/{id}`

Delete a task.

**Response (204)**

Empty body — success, nothing to return.

**Return (404)**

```json
{
  "detail": "task 2222 is not found"
}
```

**Example**

```bash 
curl -X 'DELETE' \
  'http://127.0.0.1:8000/task/1' \
  -H 'accept: */*'
  ```
  