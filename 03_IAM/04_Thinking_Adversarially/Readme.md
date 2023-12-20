## Thinking Adversarially
The topics learnt include:
- Limiting access to code and systems
    - Creating multiple layers of repositories like dev,staging, and production
- Code review for security
    - Creating roles and permissions for git repositories
- Auth validation testing
    - Perform integration and unit tests with postman
    - For each request, a test can be included to validate the expected response
        - Postman tests are written with javascript
            ```js
            pm.test("Status code is 401", function(){
                pm.response.to.have.status(401);
                });
            ```
    - Multiple requests can be added to the same folder as a **collection**.
    - The entire connection can be run using **collection runner**.
        - Can be implemented to review security and bugs in endpoints.
        - The tests can be scheduled to run automatically or integrated within CI/CD pipelines
    - **Penetration testing** means that we hire a hacker to attack our system and tell us which points are most vulnerable.
- Alternative attack vectors
    - Phising and Social Engineering attacks that can be used to gain malicious access
- Staying ahead of the attackers
    - Read tech savvy news feeds, blogs, and apps to get vulnerability updates
    - Always check that the service you sign up for is secure. Github provides recommendations on breached services/package dependencies
    - Review data management policies from third party vendors to minimize risk of data breach
        - How is data stored? Is it encrypted?
        - How is data destroyed?
        - Do they use secure 3-rd parties?
        - Who has access?
        - Do they have any certifications?


<br><br><br>

`@TODO - configure request limit for websites to enhance security against brute force attacks`