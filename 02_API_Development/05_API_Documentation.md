# Introduction
The Bookshelf API is organized around REST. Our API accepts form-encoded request bodies and returns json-encoded responses. It also uses standard HTTP response codes and verbs. <br>
The Bookshelf api allows users to hosts different books from a variety of authors and perform queries to support their applications.

# Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1/5000`, which is set as a proxy in the frontend configuration. <br>
- Authentication: This version of the application does not require authentication or API keys. Future API keys will be configured from <a src="">here</a>.<br>

# Errors
The Bookshelf api uses conventional HHTP response codes to indicate the success or failure of an API request. Errors are returned as json objects. Codes in the `2.x.x` range indicate success. Codes in the `4.x.x` range indicate an error from the request body.

### Attributes
**success** *string* <br>
The status of the error as a boolean. This can be True or False. <br>

**error** int <br>
This indicates the HTTP error status code. It is usually in the `2.x.x` and `4.x.x` range. <br>

**message** *string* <br>
The error description returned as a string An example is `unprocessable`. <br><br>

<table>
    <thead>
        <tr>
            <th colspan=2 style="text-align: center;">HTTP STATUS CODE SUMMARY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: right;"><b>200 - OK</b></td>
            <td style="text-align: left;">Request was successful, and the server has responded</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>400 - Bad request</b></td>
            <td style="text-align: left;">The request cannot be processed because required fields are missing</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>404 - Resource not found</b></td>
            <td style="text-align: left;">The requested result doesn't exist</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>422 - Unprocessable</b></td>
            <td style="text-align: left;">The server understands the content type but it is unable to process the request.</td>
        </tr>
    </tbody>
</table>


# Resource Endpoint Library
### Retrieve Books
- **GET /books**
    - Arguments
        - base_url (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/books` <br><br>
    - Returns: A list of book objects arranged by book ID, success value, and total number of books. Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
    ```bash
    {
    "books": [
        {
        "author": "Stephen King",
        "id": 1,
        "rating": 5,
        "title": "The Outsider: A Novel"
        },...
    ],
    "success": true,
    "total_books": 20
    }
    ```
<br><br>

### Update Book Ratings
- **PATCH /books/{book_id}**
- Update the rating of a specific book.
    - Arguments
        - base_url (*required*)
        - book_id (*required*)
        - rating (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/books/8 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'` <br><br>
    - Returns: The success value and id of the modified book.
    ```bash
    {
    "success": true
    }
    ```
<br><br>

### Delete Book
- **DELETE /books/{book_id}**
- Delete a specific book from your database.
    - Arguments 
        - base_url (*required*)
        - book_id (*required*) <br><br>
    - Example
        - `curl -X DELETE http://127.0.0.1:5000/books/32` <br><br>
    - Returns: The id of the deleted book, success value, total books, and book list based on current page number to update the frontend.
    ```bash
    {
    "books": [
        {
        "author": "Stephen King",
        "id": 1,
        "rating": 5,
        "title": "The Outsider: A Novel"
        },...
    ],
    "success": true,
    "total_books": 19
    }
    ```
<br><br>

### Create a Book
- **POST /books**
- Creates a new book using the submitted title, author and rating.
    - Arguments 
        - base_url (*required*)
        - title (*required*)
        - author
        - rating <br><br>
    - Example
        - `curl -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}' http://127.0.0.1:5000/books` <br><br>
    - Returns: The id of the created book, success value, total books, and book list based on current page number to update the frontend.
    ```bash
    {
    "books": [
        {
        "author": "Stephen King",
        "id": 1,
        "rating": 5,
        "title": "The Outsider: A Novel"
        },...
    ],
    "created": 34,
    "success": true,
    "total_books": 20
    }
    ```
<br><br>

### Search for a book using its title
- **POST /books**
    - Arguments 
        - base_url (*required*)
        - search_title (*required*)<br><br>
    - Example
        - `curl -X POST -H "Content-Type: application/json" -d '{"search_title":"The"}' http://127.0.0.1:5000/books` <br><br>
    - Returns: The keyword that was searched, success value, the number of books titles that match that keyword, and  book list based on current page number to update the frontend.
    ```bash
    {
    "books": [
        {
        "author": "Stephen King",
        "id": 1,
        "rating": 5,
        "title": "The Outsider: A Novel"
        },
        {
        "author": "Kristin Hannah",
        "id": 3,
        "rating": 4,
        "title": "The Great Alone"
        },...
    ],
    "count_books": 4,
    "success": true,
    "keyword_title": "The"
    }
    ```
<br><br>

