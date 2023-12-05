### Identity_Access_Management (IAM)

The first chapter was a recap on FLASK, DB's and decorators. <br>
The `POSTMAN` program was used for testing endpoints in lieu of curl. <br> 
Examples of custom wrappers were also implemented in python. <br><br>

Authentication methods
- **Usernames and Passwords** (weakest link)
- **Single Signon** - using secure services like google/facebook login accounts for user authentication.
- **Multi-factor authentication** - using third party physical devices or apps. This can involve sending codes via text that are synchronized to the time the user requests access
- **Passwordless** - uisng secure platforms like the google/github apps to verify codes and authenticate users. Slack also has a magic link
- **Biometric authentication** - This is one of the hardest to implement/breach because of its uniqueness and its requirement of the users physical presence. 

This module uses `Auth0` for third party authentication. <br>

### Auth0
Sign up and create an application and api. Custom domain names are recommended but they were not available for my free account.
- Specify the callback urls and allowed login and logout endpoint names
- Create an Auth0_authentication url by filling in the placeholders with values from the created application and api in Auth0 `https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}`
- Include the authentication url as an anchor link in your html file `<a href="{{AUTH0_AUTHORIZE_URL}}">Login</a>`

### Json Web Tokens (JWTs)
JWTs are intrinsically stateless, meaning that our server knows that this token is valid and works regardless of the state of a session. When JWT is passed to the front-end then to the server, that server only has to fetch a public key one time from the authentication service. The key will then be stored in the server to verify the JWT. Stateless also solves the problem of scalability.

