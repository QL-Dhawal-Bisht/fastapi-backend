## APIs

The following APIs are available:

### User APIs

- **`POST /register`**: Register a new user.
- **`POST /login`**: Log in a user and receive a JWT token.
- **`GET /me`**: Get the profile of the currently authenticated user.
- **`PUT /me`**: Update the profile of the currently authenticated user.
- **`DELETE /me`**: Delete the profile of the currently authenticated user.

### Post APIs

- **`GET /posts/`**: Get a list of all posts with pagination and sorting.
- **`GET /posts/{id}`**: Get a single post by its ID.
- **`POST /posts/`**: Create a new post (requires authentication).
- **`PUT /posts/{id}`**: Update a post by its ID (only the author is allowed).
- **`DELETE /posts/{id}`**: Delete a post by its ID (only the author or an admin is allowed).

### Comment APIs

- **`GET /posts/{post_id}/comments`**: Get all comments for a specific post.
- **`POST /posts/{post_id}/comments`**: Add a new comment to a post (requires authentication).
- **`DELETE /comments/{id}`**: Delete a comment by its ID (only the author or an admin is allowed).
