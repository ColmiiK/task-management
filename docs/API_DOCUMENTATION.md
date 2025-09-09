# API Documentation

## Authentication

This API provides endpoints for user authentication, including registration, login, logout, CSRF token setup, and session refresh.

### `GET /csrf_token/`

Sets the CSRF cookie required for secure requests.

#### Response

- **200 OK**

```json
{
  "success": "CSRF cookie set"
}
```

### `POST /auth/register/`

Registers a new user.

#### Request Body

```json
{
  "username": "johndoe",
  "password": "password123",
  "confirm_password": "password123",
  "email": "johndoe@example.com" // optional
}
```

#### Responses

- **200 OK**

```json
{
  "success": "User johndoe registered successfully"
}
```

- **400 Bad Request**

```json
{
  "error": "Username and password are required"
}
```

```json
{
  "error": "Passwords don't match"
}
```

```json
{
  "error": "Username already exists"
}
```

```json
{
  "error": "Invalid JSON"
}
```

### `POST /auth/login/`

Authenticates an existing user and starts a session.

#### Request Body

```json
{
  "username": "johndoe",
  "password": "password123"
}
```

#### Responses

- **200 OK**

```json
{
  "success": "Login successful"
}
```

- **400 Bad Request**

```json
{
  "error": "Username and password are required"
}
```

- **401 Unauthorized**

```json
{
  "error": "Invalid credentials"
}
```

- **400 Bad Request**

```json
{
  "error": "Invalid JSON"
}
```

### `POST /auth/logout/`

Logs out the current authenticated user.

#### Responses

- **200 OK**

```json
{
  "success": "Logout successful"
}
```

- **401 Unauthorized**

```json
{
  "error": "User not authenticated"
}
```

### `POST /auth/refresh/`

#### Responses

- **200 OK**

```json
{
  "is_authenticated": true,
  "username": "johndoe",
  "email": "johndoe@example.com"
}
```

- **401 Unauthorized**

```json
{
  "is_authenticated": false
}
```

## User management

### `GET /users/`

Returns a paginated list of users.

#### Query Parameters

| Parameter   | Type | Default | Description              |
| ----------- | ---- | ------- | ------------------------ |
| `page`      | int  | `1`     | Page number              |
| `page_size` | int  | `10`    | Number of users per page |

#### Responses

- **200 OK**

```json
{
  "users": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "johndoe@example.com"
    },
    ...
  ],
  "total_pages": 5,
  "current_page": 1,
  "total_users": 42
}
```

- **401 Unauthorized**

```json
{
  "error": "Authentication required"
}
```

### `GET /users/<id>/`

Returns details of a single user by ID.

#### URL Parameters

| Parameter | Type | Description    |
| --------- | ---- | -------------- |
| `id`      | int  | ID of the user |

- **200 OK**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "johndoe@example.com"
}
```

- **401 Unauthorized**

```json
{
  "error": "Authentication required"
}
```

- **404 Not found**

```json
{
  "error": "User not found"
}
```

### `PUT /users/<id>/`

Updates a user's `username` and/or `email`.

#### Request Body

```json
{
  "username": "newname",
  "email": "newemail@example.com"
}
```

#### Responses

- **200 OK**

```json
{
  "id": 1,
  "username": "newname",
  "email": "newemail@example.com"
}
```

- **400 Bad Request**

```json
{
  "error": "Invalid JSON"
}
```

- **401 Unauthorized**

```json
{
  "error": "Authentication required"
}
```

- **404 Not Found**

```json
{
  "error": "User not found"
}
```

### `GET /users/me/`

Returns details of the currently authenticated user.

- **200 OK**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "johndoe@example.com"
}
```

- **401 Unauthorized**

```json
{
  "error": "Authentication required"
}
```

## Task management

### `GET /tasks/`

List all tasks with optional filters and pagination.

#### Query Parameters

| Name        | Type   | Description                    |
| ----------- | ------ | ------------------------------ |
| `search`    | string | Search by title or description |
| `priority`  | string | Filter by priority             |
| `status`    | string | Filter by status               |
| `page`      | int    | Page number (default: 1)       |
| `page_size` | int    | Items per page (default: 10)   |

#### Response — 200 OK

```json
{
  "tasks": [
    /* list of task objects */
  ],
  "total_pages": 5,
  "current_page": 1,
  "total_users": 42
}
```

### `POST /tasks/`

Create a new task.

#### Request Body

```json
{
  "title": "Fix login bug",
  "description": "Investigate and fix the issue",
  "status": "open",
  "priority": "high",
  "due_date": "2025-09-10",
  "estimated_hours": 4,
  "actual_hours": 0,
  "metadata": { "component": "auth" },
  "parent_task": null,
  "assigned_to": [1, 2],
  "tags": [3, 4]
}
```

#### Response — 201 Created

```json
{
  "id": 12,
  "title": "Fix login bug",
  "description": "Investigate and fix the issue",
  "status": "open",
  "priority": "high",
  "due_date": "2025-09-10",
  "estimated_hours": 4.0,
  "actual_hours": 0.0,
  "created_by": "alice",
  "assigned_to": ["bob", "eve"],
  "tags": ["backend", "urgent"],
  "parent_task": null,
  "metadata": { "component": "auth" },
  "created_at": "...",
  "updated_at": "..."
}
```

#### Error Responses

- **400 Bad Request** — Missing required fields or invalid JSON.
- **401 Unauthorized** — Authentication required.

### `GET /tasks/<id>/`

Get details of a specific task by ID.

#### Response — 200 OK

```json
{
  "id": 12,
  "title": "Fix login bug",
  ...
}
```

#### Errors

- **401 Unauthorized**
- **404 Not Found**

### `PUT /tasks/<id>/`

Fully update a task (all fields expected).

#### Request Body

Same as POST `/tasks/` above.

#### Response — 200 OK

```json
{
  "id": 12,
  "title": "Updated task title",
  ...
}
```

#### Errors

- **400 Bad Request** — Invalid JSON
- **401 Unauthorized**
- **404 Not Found**

### `PATCH /tasks/<id>/`

Partially update a task (only include fields to be changed).

#### Request Body (example)

```json
{
  "status": "in_progress",
  "priority": "medium"
}
```

#### Response — 200 OK

```json
{
  "id": 12,
  "status": "in_progress",
  "priority": "medium",
  ...
}
```

#### Errors

Same as `PUT /tasks/<id>/`

### `DELETE /tasks/<id>/`

Soft-delete (archive) a task.

#### Response — 200 OK

```json
{
  "success": "Task archived"
}
```

#### Errors

- **401 Unauthorized**
- **404 Not Found**

### `POST /tasks/<id>/assign/`

Assign users to a task.

#### Request Body

```json
{
  "assigned_to": [1, 2, 3]
}
```

#### Response — 200 OK

```json
{
  "success": "Users assigned",
  "assigned_to": [1, 2, 3]
}
```

#### Errors

- **400 Bad Request** — Invalid JSON
- **404 Not Found** — Task or User not found
- **401 Unauthorized**

### `GET /tasks/<id>/comments/`

Get all comments for a task.

#### Response — 200 OK

```json
{
  "comments": [
    {
      "id": 5,
      "content": "Started working on this",
      "author": "bob",
      "created_at": "2025-09-08T12:00:00Z"
    }
  ]
}
```

#### Errors

- **401 Unauthorized**
- **404 Not Found**

### `POST /tasks/<id>/comments/`

Add a comment to a task.

#### Request Body

```json
{
  "content": "This needs testing."
}
```

#### Response — 200 OK

```json
{
  "id": 6,
  "content": "This needs testing.",
  "author": "alice",
  "created_at": "2025-09-09T10:00:00Z"
}
```

#### Errors

- **400 Bad Request** — Missing content or invalid JSON
- **401 Unauthorized**
- **404 Not Found**

### `GET /tasks/<id>/history/`

Retrieve the change history of a task.

#### Response — 200 OK

```json
{
  "history": [
    {
      "timestamp": "2025-09-08T14:30:00Z",
      "user": "alice",
      "action": "Updated priority",
      "old_value": "low",
      "new_value": "high"
    },
    ...
  ]
}
```

#### Errors

- **401 Unauthorized**
- **404 Not Found**
