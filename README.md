# Blog API

This is a simple blog API built with FastAPI.

## API Endpoints

### Posts

*   **GET /posts**

    *   Description: Get all posts.
    *   Response:

        ```json
        [
            {
                "id": 1,
                "title": "My First Post",
                "content": "This is my first post."
            },
            {
                "id": 2,
                "title": "My Second Post",
                "content": "This is my second post."
            }
        ]
        ```

*   **GET /posts/{post_id}**

    *   Description: Get a single post by ID.
    *   Response:

        ```json
        {
            "id": 1,
            "title": "My First Post",
            "content": "This is my first post."
        }
        ```

*   **POST /posts**

    *   Description: Create a new post.
    *   Request Body:

        ```json
        {
            "title": "My New Post",
            "content": "This is my new post."
        }
        ```

    *   Response:

        ```json
        {
            "id": 3,
            "title": "My New Post",
            "content": "This is my new post."
        }
        ```

*   **PUT /posts/{post_id}**

    *   Description: Update a post.
    *   Request Body:

        ```json
        {
            "title": "My Updated Post",
            "content": "This is my updated post."
        }
        ```

    *   Response:

        ```json
        {
            "id": 1,
            "title": "My Updated Post",
            "content": "This is my updated post."
        }
        ```

*   **DELETE /posts/{post_id}**

    *   Description: Delete a post.
    *   Response:

        ```json
        {
            "message": "Post deleted successfully."
        }
        ```
