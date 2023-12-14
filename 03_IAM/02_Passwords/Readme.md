## Passwords

**Hypocratic Oath** - `As a developer, it is my responsibility to take security seriously and not implement weak systems including storing plain text passwords.` <br>

Plain text passwords are never recommended and can be breached by `Cross-Site-Scripting(XSS)` and `SQL Injection`. We can mitigate brute force attacks using a few techniques:
- Prevent or ratelimit multiple incorrect login attempts
- Include <a target="_blank" href="https://developers.google.com/recaptcha/docs/v3">Google reCAPTCHA</a> to prevent bot logins
- Do not allow common passwords
- Enforce a reasonable password policy
- Log and monitor for attack
<br>

Serialization and Logging are additional steps that should be implemented/reviewed to ensure that no password breaches are occurring. <br><br>

**Serialization** is the process of transforming a data model into a more easily shared format. For example, this is commonly performed when sending information as a response from a server to the requesting client in the form of a JSON object.
<br><br>

Logs help us with security for many reasons.
- Logging leaves a solid audit trail
    - Login attempts (ids)
    - Login sources
    - Requested resources
<br>

But we should never log:
- Personally identifiable information
- Secrets
- Passwords

### Encryption
Other techniques for mitigating passwords breach are implementing encryption. Simple examples of encryption methods are **simple substitution** and **Polyalphabetic cipher**. Both techniques can be easily decoded with modern computers and are not recommended.<br><br>

Modern encryption workflows rely on this four main components in practice:
- Plaintext block: input data
- Ciphertext block: output from the function
- Function: the algorithm used to perform the encryption
- Key: the cipher
<br>

Three common encryption algorithms are:
- 3DES (Data Encryption Standard invented in the 1970)
- Blowfish
- AES (Advanced Encryption Standard)
<br><br>

Encrypting passwords stored in a db reduces the damage from sql injection, bad db passwords, and bad backup security. If the `username, password` table is breached, the intruder only gets a list of jumbled text that cannot be decrypted without the key. The input text is usually compared to the decrypted password on the server.<br><br>

**Asymmetric Encryption** is used to encrypt data while communicating between services. It uses a **private** key to encypt data from the server, and uses a **public** key to decrpyt data on the front-end. The types of keys can also be reversed. This is typically implemented with HTTPS, TLS/SSL<br><br>


### Hashing
Hashing is a one-way function that jumbles in only one direction. Compared to encryption, hashing eliminates the key and eliminates the ability to go backwards to the original string.

Some common hashing functions are:
- bcrypt (recommended)
- scrypt (recommended)
- SHA-1
- MD5
The output from the hashing function is called a `hash` or a `message digest`. Simple hashing functions like SHA-1 or MD5 can be beaten by creating a **rainbow table** for each word that is tested and generating it's corresponding hash. This is why they are not recommended.
<br><br>

To prevent rainbow table attacks, we can implement **salted hashes**. This is when a random string is encrypted multiple times and appended as a plaing text to the hashed string e.g.  `c76b34f8687e46a.941c76b34f8687e46af0d94c167d1403`. All the values before the **.** are part of the **salt**, and are generated randomly each time a new password is saved or updated. The number of times the string is encrypted is known as the **salt rounds**.
<br><br>

This is a cost factor for how many times a password and salt should be re-hashed. In other words if you choose 10 salt rounds, the calculation is performed `2^10` or `1024 times`. Each attempt takes the hash from the previous round as an input. The more rounds performed, the more computation is required to compute the hash. This will not cause significant time for a single attempt (i.e. checking a password at login), but will introduce significant time when attempting to brute force or generate rainbow tables.
<br><br>


Here is a list of topics we talked about in the lesson.
- Problems with plain text
- Problems - Brute force attacks
- Problems - Data handling and logging
- Introduction to encryption
- Using encryption for user tables
- Asymmetric encryption
- Hashing
- Hashing with salts