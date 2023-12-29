### Conditionals
A **flowchart** is a visual diagram that outlines the solution to a problem through a series of logical statements. The order in which statements are evaluated and executed is called the **control flow**. <br>
![flowChart](../../figures/buy-the-item-flowchart.jpeg)

<br><br>

- **If...else statements** allow you to execute certain pieces of code based on a condition, or set of conditions, being met.
    ```js
    > if ( /*this expression is true*/ ) {
        // run this code
    } else {
        // run this code
    }
    ```
    The value inside the `if` statement is always *converted* to true or false. Depending on the value, the code inside the `if` statement is run or the code inside the `else` statement is run, but **not both**. The code inside the `if` and `else` statements are surrounded by **curly braces** `{...}` to separate the conditions and indicate which code should be run. <br>
    **TIP**: You can have an independent `if` statement but you can’t have an `else` statement without first having an `if` statement.
    <br><br>

- **Else If Statements** - In some situations, two conditionals aren’t enough. Consider the following situation. <br>
    You're trying to decide what to wear tomorrow. If it is going to snow, then you’ll want to wear a coat. If it's not going to snow and it's going to rain, then you’ll want to wear a jacket. And if it's not going to snow or rain, then you’ll just wear what you have on.
    ```js
    > var weather = "sunny";

    > if (weather === "snow") {
        console.log("Bring a coat.");
    } else if (weather === "rain") {
        console.log("Bring a rain jacket.");
    } else {
        console.log("Wear what you have on.");
    }
    ```
    By adding the extra `else if` statement, you're adding an extra conditional statement.
    <br><br>

- **Logical Operators** - This is when `if` statements are chained with `and/or` statements for more complex comparisons.
    ```js
    > var colt = "not busy";
    > var weather = "nice";

    > if (colt === "not busy" && weather === "nice") {
        console.log("go to the park");
    }
    ```
    The `&&` symbol is the logical AND operator, and it is used to combine two logical expressions into one larger logical expression. If **both** smaller expressions are true, then the entire expression evaluates to true. If **either one** of the smaller expressions is false, then the whole logical expression is false. <br>
    **Logical expressions** are similar to mathematical expressions like `11 != 12`, except logical expressions evaluate to either true or false. Similar to mathematical expressions that use `+, -, *, /, %`, there are logical operators **`&&, ||, !`** that you can use to create more complex logical expressions. <br>
    **Logical operators** can be used in conjunction with boolean values (true and false) to create complex logical expressions. <br>

    | Operator | Meaning | Example | How it works |
    | :------- | :------ | :-----: | :----------- |
    | `&&` | Logical AND | `value1 && value2` | Returns `true` if **both** `value1` **and** `value2` evaluate to `true`. |
    | `\|\|` | Logical OR | `value1 \|\| value2` | Returns `true` if **either** `value1` **or** `value2` (**or even both**!) evaluates to true. |
    | `!` | Logical NOT | `!value1` | Returns the **opposite** of `value1`. If `value1` is `true`, then `!value1` is `false`. |
    <br>

    **TIP**: Logical expressions are evaluated from **left to right**. Similar to mathematical expressions, logical expressions can also use parentheses to signify parts of the expression that should be evaluated first. <br>

    **TIP**: Float values can be rounded off with the `.toFixed()` method. e.g
    ```js
    > var balance = 325.2583;
    > console.log(balance.toFixed(2)) // Returns 325.26
    ```

- **Truthy and Falsy statements** - Every value in JavaScript has an inherent boolean value. When that value is evaluated in the context of a boolean expression, the value will be transformed into that inherent boolean value. <br>
These are similar to python values that default to true or false like 0 and 1 even when equal statements are not provided.
    1. **Falsy values** - A value is **falsy** if it converts to `false` when evaluated in a boolean context. For example, an empty String `""` is falsy because, `""` evaluates to `false`. You already know if...else statements, so let's use them to test the truthy-ness of `""`.
        ```js
        > if ("") {
            console.log("the value is truthy");
        } else {
            console.log("the value is falsy");
        }
        ```

        Here’s the list of all of the falsy values:
        1. the Boolean value false
        2. the null type
        3. the undefined type
        4. the number 0
        5. the empty string ""
        6. the odd value NaN (stands for "not a number", check out the `NaN` [MDN article](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN))
        
        That's right, there are only *six falsy values* in all of JavaScript! <br><br>


    2. **Truthy values** - A value is **truthy** if it converts to true when evaluated in a boolean context. For example, the number `1` is truthy because, `1` evaluates to `true`. Let's use an if...else statement again to test this out:

        ```js
        > if (1) {
            console.log("the value is truthy");
        } else {
            console.log("the value is falsy");
        }
        ```

        Here are some other examples of truthy values:

        ```bash
        true
        42
        "pizza"
        "0"
        # Note the null and undefined are wrapped as strings. Using it without the inverted commas will make it falsy.
        "null"
        "undefined"
        {}
        []
        ```

- **Ternary Operator** - is when you assign values to a variable based on the outcome of another boolean variable. The **ternary operator** provides you with a shortcut alternative for writing lengthy if...else statements. It is similar to lambda if-else statements in python.
    ```js
    conditional ? (if condition is true) : (if condition is false)
    ```
    An example of a ternary operator implementation is
    ```js
    > var isGoing = true;
    > var color;

    // Original if else statement
    > if (isGoing) {
        color = "green";
    } else {
        color = "red";
    }
    > console.log(color); // green

    // Ternary statement
    > var color = isGoing ? "green" : "red";
    > console.log(color); // green
    ```


    