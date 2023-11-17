### This hosts a dummy app to replicate a CRUD workflow
1. **`app01.py`** - Allows you to manually specify a dictionary as the `data` attribute of the index html list. <br>
This mimics the CREATE in **C**RUD. <br><br>
2. **`app02.py`** - Uses a psql database, and specifies the `data` attribute as a SQLAlchemy query that does `SELECT * FROM <table>`. <br>
This mimics the READ in C**R**UD. <br>
In the Model-View-Controller (MVC) cycle for this app,
    - The Todo class is the **Model**. *Models manage data and business logic for us. What happens inside models and databases, capturing logical relationships and properties across the web app objects*.
    - The index.html is the **View**. *Views handle display and representation logic. What the user sees (HTML, CSS, JS from the user's perspective)*.
    - The index function is the **Controller**. *Controllers: routes commands to the models and views, containing control logic. Control how commands are sent to models and views, and how models and views wound up interacting with each other*.
<br><br>

3. **`app03.py`** - This describes how data from html can be used to update the databse. <br>
This mimics the UPDATE in CR**U**D using synchronous workflows.<br>
Data can be updated using (This app uses the *form* method with the `index_form.html` template),
    - **URL query parameters** are listed as key-value pairs at the end of a URL, preceding a "?" question mark. E.g. `www.example.com/hello?my_key=my_value`.
    - **Form data** `request.form.get('<name>')` reads the `value` from a form input control (text input, number input, password input, etc) by the `name` attribute on the input HTML element. Default values can also be embedded into the forms to avoid nulls. `request.args.get`, `request.form.get` both accept an optional second parameter, e.g. `request.args.get('foo', 'my default')`, set to a default value, in case the result is empty.
    - **JSON** `request.data` retrieves JSON as a string. Then we'd take that string and turn it into python constructs by calling `json.loads` on the `request.data` string to turn it into lists and dictionaries in Python.<br><br>

    - Forms can only send POST and GET requests.
        - POST submission
            - On submit, we send off an HTTP POST request to the route `/create` with a **request body**.
            - The request body stringifies the key-value pairs of fields from the form (as part of the `name` attribute) along with their values.
            - POSTs are ideal for longer form submissions, since URL query parameters can only be so long compared to request bodies (max 2048 characters).
        - GET submission
            - Sends off a GET request with **URL query parameters** that appends the form data to the URL.
            - Ideal for smaller form submissions.
<br>

4. **`app04.py`** - builds on the UPDATE steps but shows how to send requests asynchronously (This app uses the *form* method with the `index_form_async.html` template). Async data requests are requests that get sent to the server and back to the client without a page refresh. Async requests (AJAX requests) use one of two methods:
    - **XMLHttpRequest** (this is slightly old and can be implemented by including a script in the html file) e.g.
    ```js
    var xhttp = new XMLHttpRequest();
    description = document.getElementById("description").value;
    xhttp.open("GET", "/todos/create?description=" + description);
    xhttp.send();

    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) { 
        // on successful response
        console.log(xhttp.responseText);
        }
    };
    ```
    - **Fetch** (modern way. It also uses javascript)
    ```js
    // example of a request_route_name is todos/create
    fetch('/<request_route_name>', {
        // method type
        method: 'POST',
        // json formatted string
        body: JSON.stringify({'description': 'some description here'}),
        // specify the data type as json so the server understands how to read it
        headers: {'Content-Type': 'application/json'
        }
    });
    ```

