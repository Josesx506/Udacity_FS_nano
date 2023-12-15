## Identity and Authentication

The first chapter was a recap on FLASK, DB's and decorators. <br>
The `POSTMAN` program was used for testing endpoints in lieu of curl. <br> 
Examples of custom wrappers were also implemented in python. <br><br>

### Authentication methods
- **Usernames and Passwords** (weakest link)
- **Single Signon** - using secure services like google/facebook login accounts for user authentication.
- **Multi-factor authentication** - using third party physical devices or apps. This can involve sending codes via text that are synchronized to the time the user requests access
- **Passwordless** - uisng secure platforms like the google/github apps to verify codes and authenticate users. Slack also has a magic link
- **Biometric authentication** - This is one of the hardest to implement/breach because of its uniqueness and its requirement of the users physical presence. 

This module uses **`Auth0`** for third party authentication. <br>


#### --------------------------------------------------------------------------------------------------------------------

### Auth0
- Sign up to `Auth0` and create an **application** and **api**. 
    - Custom domain names are recommended but they were not available for my free account.
    - Specify the callback urls and allowed login and logout endpoint names
    - After creating it, extract the following key values from your application and api
        - Domain Name - `dev-**********.us.auth0.com`
        - Audience - `image`.              Any string works. Different strings can be used for different website services e.g. calendar.
        - Scope - ''.                      This can be set to an empty string initially
        - Response Type - `token`.         This indicates a token value should be returned.
        - Client ID - `*****VFFgf9******`. Random base64 encoded string
        - Redirect/Callback URL - `https://127.0.0.1:8080/login-results`. This can be any endpoint but this is where the Auth0 api will reroute the token each time a user tries to log in.
- Create an Auth0_authentication url by filling in the placeholders with values from the created application and api in Auth0 `https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}`
- Include the authentication url as an anchor link in your html file `<a href="{{AUTH0_AUTHORIZE_URL}}">Login</a>`
- Check how this is done in `05_Auth0_link.html`.

### Json Web Tokens (JWTs)
JWTs are intrinsically stateless, meaning that our server knows that this token is valid and works regardless of the state of a session. When JWT is passed to the front-end then to the server, that server only has to fetch a public key one time from the authentication service. The key will then be stored in the server to verify the JWT. Stateless also solves the problem of scalability.
- A JWT has 3 parts namely a header, payload, and signature.
- The 3 parts are merged into a single string that can be used to calidate the authenticity of a request
- Sensitive information like passwords should not be stored in JWT payloads because it can be easily decoded with a `Base64` algotrithm
    - Instead store generic data like usernames / emails that are not sensitive
- **Header** includes an algorithm used to sign the token such as HS256
- **Payload** stores specific information about the user such as a username or user ID.
- **Signature** of the JWT is used to validate its authenticity. 
    - It is created by encoding the header, payload, and a specified `secret` key. 
    - The signature is generated on the authentication service and our backend independently for validation
    - If the header,payload, or secret key is tampered with, the signature is affected, and the server will reject the request
- The default expiration time for the token is **`36000 s`** but this should be shortened for real-life applications
- *jwt python library* `pip install pyjwt`


### Local Storage (Retrieve tokens and Payloads from browsers)
- It is an implementation of a **key-value store** that is accessible through a **javascript** interface in most modern browsers.
- It is a general purpose interface to store strings which will persist in memory from session to session. 
- It is designed for smaller strings and alternative opensource systems like `localForage` exist for large amounts of data. 
- It is **domain specific** and **persistent** across multiple sessions.
- Local storage helps to store, and retreive/get jwts for each browser session/tab. i.e. Each jwt associated with a particular domain name e.g udacity.com can always retrieve validation credentials from local storage.
```js
// To store the jwt in a js script. Token is obtained from successful Auth0 request
jwt = response.jwt
localStorage.setItem("token", jwt)

// To retrieve it for use
jwt = localStorage.getItem("token")
``` 
<br>

- There are inherent risks associated with using local storage. 
    - For example, a malicious attack can inject foreign code into a website to execute on that website to access all of the keys within the local store and drops it into the malicious server.
    - **Cross-Site-Scripting (XSS)** attacks can be used to download all the valid keys from localStorage or even inject data into our db. 
    - For this reason, users of our apps/pages should never be allowed to run javascript from open ended form inputs. This can be avoided by using JS libraries like `DOMPurify` to sanitize our website strings. <br>
    - Packages installed with package managers like pip, brew, or npm should also be carefully vetted before using them to install any packages to avoid malicious attacks.
- Check how the values of payload can be retrieved with localStorage in `02_Extract_LocalStorage_token.html`.


### Sending Tokens either locally or retrieving them from request headers
- Tokens can be extracted from the request header under the `Authorization` key. 
- Usually, the token can have a string *`Bearer`* append to it, however, this can excluded with python split string.
    - e.g. `Bearer <token_value>`
    - Test tokens can be implemented with **POSTMAN** GET requests. 
        - The `04_retrieve_token_app.py` shows how to create a decorator that extracts the jwt tokens from a request header.
- Combine steps 3 and 4 to both extract the Auth0 token from the request header and validate it with Auth0. 
- This is used to determine `Who` is performing the request.
- In step **05** 
    - generate a valid Auth0 token with the html page, 
    - start the flask server that can validate the token, 
    - embed the token within a GET request header in POSTMAN, 
    - send the request to the server to validate that its authenticity.