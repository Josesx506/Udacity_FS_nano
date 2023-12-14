## Passwords

**Hypocratic Oath** - `As a developer, it is my responsibility to take security seriously and not implement weak systems including storing plain text passwords.` <br>

Plain text passwords are never recommended and can be breached by `Cross-Site-Scripting(XSS)` and `SQL Injection`. We can mitigate brute force attacks using a few techniques:
- Prevent or ratelimit multiple incorrect login attempts
- Include <a target="_blank" href="https://developers.google.com/recaptcha/docs/v3">Google reCAPTCHA</a> to prevent bot logins
- Do not allow common passwords
- Enforce a reasonable password policy
- Log and monitor for attack
<br>

Other techniques for mitigating passwords breach are