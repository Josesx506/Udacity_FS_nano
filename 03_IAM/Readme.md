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

This module uses `Auth0` for third party authentication.