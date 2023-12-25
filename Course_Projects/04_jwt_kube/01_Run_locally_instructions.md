### Steps to run the App Locally
The following steps describe how to run the Flask API locally with the standard Flask server, so that you can test endpoints before you containerize the app:

1. **Install python dependencies** <br>
    These dependencies are kept in a requirements.txt file in the root directory of the repository. To install them, go to the project directory that you’ve just downloaded, and run the command:
    ```bash
    # Assuming you are in the cd0157-Server-Deployment-and-Containerization/ directory
    ~ $pip install -r requirements.txt
    ```
2. **Set up the environment** <br>
    You will need the following two variables available in your terminal environment:
    - *JWT_SECRET* - The text string to be used for creating the JWT.
    - *LOG_LEVEL* - It represents the level of logging. It is optional to be set. It has a default value as 'INFO', but when debugging an app locally, you may want to set it to 'DEBUG'.
    To add these to your terminal environment, run the following: 
    ```bash 
    # A secret text string to be used to creating a JWT 
    ~ $export JWT_SECRET='myjwtsecret' 
    ~ $export LOG_LEVEL=DEBUG 
    # Verify 
    ~ $echo $JWT_SECRET 
    ~ $echo $LOG_LEVEL
    ```
3. **Run the app** <br>
    Run the app using the Flask server, from the root directory of the downloaded repository, run:
    ```bash 
    ~ $python main.py
    ```
    Open http://127.0.0.1:8080/ in a new browser OR run `curl --request GET http://localhost:8080/` on the command-line terminal. It will give you a response as "Healthy".
4. **Install a command-line JSON processor** <br>
    Before trying to access other endpoints of the app, we need the `jq`, a package that helps to pretty-print JSON outputs. In simple words, the JQ package helps you parse, filter, or modify JSON outputs. Open a new terminal window, and run the command below.
    ```bash
    # For Linux
    ~ $sudo apt-get install jq  
    # For Mac
    ~ $brew install jq 
    # For Windows, 
    ~ $chocolatey install jq
    ```
    For detailed information, refer to a simple tutorial [here](https://stedolan.github.io/jq/tutorial/), though it's not required for the final submission.
5. **Access endpoint /auth** <br>
    To try the `/auth` endpoint, use the following command, replacing email/password as applicable to you:
    ```bash
    ~ $export TOKEN=`curl --data '{"email":"abc@xyz.com","password":"mypwd"}' --header "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`
    ```
    This calls the endpoint `localhost:8080/auth` with the email/password as the message body. The return value is a JWT token based on the secret string you supplied. We are assigning that secret to the environment variable 'TOKEN'. To see the JWT token, run:
    ```bash
    ~ $echo $TOKEN
    ```
6. **Troubleshoot** <br>
    If you are facing any of the following errors, then it is related to the pyjwt package version issue.
    - *parse error: Invalid numeric literal at line 1, column 10*
    - *AttributeError: 'str' object has no attribute 'decode',*
    We have installed the *pyjwt==1.7.1* package using the *requirements.txt* file. If you have a higher version, then the commands above may not work. PyJWT 2.0.0 or a higher version does not have a `decode()` method, causing the error mentioned above. You can uninstall the current version, and install the desired version as:
    ```bash
    ~ $pip uninstall pyjwt
    ~ $pip install pyjwt==1.7.1
    # Personally I used python-jose instead of pyjwt because it has less dependency errors
    ~ $pip install python-jose==3.3.0
    ```
7. **Access endpoint /contents** <br>
    To try the `/contents` endpoint which decrypts the token and returns its content, run:
    ```bash
    ~ $curl --request GET 'http://localhost:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
    # Output
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    71  100    71    0     0  23986      0 --:--:-- --:--:-- --:--:-- 35500
    {
    "email": "abc@xyz.com",
    "exp": 1704673380,
    "nbf": 1703463780
    }
    ```
    You should see the email id that you passed in as one of the values.

    