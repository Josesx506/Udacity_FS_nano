### Access and Authorization
The more people have access to a role, the less actions they should be able to performed to reduce the risk of a data breach.


#### Creating roles and permissions in Auth0
1. Go to API-><Selected_API>->Permissions->Add_New
2. Go to User_Management->Roles->New_Roles
    - Add a new role and description
    - Assign permissions that each role has 
3. Go to API-><Selected_API>->Settings
    - Authorize Role Based Authentication (RBAC)
    - Allow Permissions to be added to the access token
4. Go to User_Management->Users
    - Manually assign a role to each user.
    - Now when a user logs in, the jwt payload has key called permissions that lists what the user can do
    - ```python
            {
        "iss": "https://bdmfflf.auth0.com/",
        "sub": "auth0|"****************",",
        "aud": "image",
        "iat": 100000000,
        "exp": 100000000,
        "azp": "****************",
        "scope": "",
        "permissions": [
            "get:images"
        ]
        }
        ```

Now when each new user is added, their roles are added to the permission json web token. <br>

In Auth0, you can define all the permissions that the API uses. **Note:** that the permissions are heavily dependent on the actions that your API will be fulfilling and you should be careful about assigning each endpoint its own permission.