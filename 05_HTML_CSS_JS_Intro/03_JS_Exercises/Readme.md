## JS - JavaScript
**TIP**: `HTML` and `CSS` are *markup* languages. Markup languages are used to **describe and define elements** within a document. `JavaScript` is a *programming* language. Programming languages are used to **communicate instructions to a machine**. Programming languages can be used to control the behavior of a machine and to express algorithms.

### console.log
`console.log()` is the equivalent of a python print statement. It can be used to test js syntax and debug multiple lines of code. An example is `console.log("hiya friend!");`.

Learnt about:
- [x] Data Types and Variables
- [x] Conditionals
- [x] Loops

### TIPS
1. Float values can be rounded off with the `.toFixed()` method. e.g
    ```js
    > var balance = 325.2583;
    > console.log(balance.toFixed(2)) // Returns 325.26
    ```
    <br>

2. Integers can be printed as formatted strings with the `.toLocaleString()` method. e.g
    ```js
    > var salary = 300000;
    > console.log(salary.toLocaleString("en-US")) // Returns 300,000
    ```
    <br>

3. Strings can be indexed with the `.charAt()` method. When using this, remember that js has zero-indexing e.g
    ```js
    > "How are you?".charAt(5); // returns "r"
    ```
    The index of a value can also be obtained with the `.indexOf()` method.
    ```js
    > let text = "Hello world, welcome to the universe.";
    > let result = text.indexOf("welcome"); // returns "13" where the welcome word starts
    ```