### Data Types and Variables
Popular datatypes include numbers, strings, booleans, null, and undefined etc. Variables can be defined for any data type.

- **Numbers** are values like integers or floats. Arithmetic operations and boolean comparisons can be performed for numbers
    | Operator | Meaning |
    | :------: | :------ |
    | < | Less than |
    | > | Greater than |
    | <= | Less than or Equal to |
    | >= | Greater than or Equal to |
    | == | Equal to |
    | != | Not Equal to |

- **Strings** can be concatenated with a `+` sign e.g. `console.log("Hello," + " New York City")`. <br>
    *Implicit type coercion* can occur if a string is concatenated with an integer e.g. `console.log("Hello" + 5*10) -> Hello50`. <br>
    Strings in Js are case sensitive, and can be compared with `==` and `!=` arithmetic operations. <br>

- **Variables** can allow repeated use of assigned values compared to undefined strings and numbers. Semicolons make it clear where one statement ends and another begins. They can be used to differentiate variables.
    - **Naming Conventions** - When you create a variable, you write the name of the variable using camelCase (the first word is lowercase, and all following words are uppercase). Also try to use a variable name that accurately, but succinctly describes what the data is about.
    - **Indexing** - JS uses zero-indexing like python and strings and list/array items can be accessed using their indices.  To access an individual character, you can use the character's location.
        ```js
        > var quote = "Stay awhile and listen!";
        > console.log(quote[6]);
        <. w
        // Alternatively, you can use the String’s charAt() method to access individual characters. For example, quote.charAt(6) would also return "w"
        ```
    - **Escaping characters** - This is similar to using quotation inside strings. It will typically return an error except a alternating quotations are used or a *backslash character* is used.
        ```js
        // Invalid syntax
        > console.log("The man whispered, "please speak to me."")
        // Valid syntax
        > console.log("The man whispered, 'please speak to me.'");
        > console.log('The man whispered, "please speak to me."');
        > console.log("The man whispered, \"please speak to me.\"");
        ```
        Quotes aren’t the only special characters that need to be escaped, there’s actually quite a few. However, to keep it simple, here’s a list of some common special characters in JavaScript.

        | Code | Character |
        | :--: | :------ |
        | \\\\ | \ (backslash) |
        | " | "(double quote) |
        | ' | ' (single quote) |
        | \n | newline |
        | \t | tab |

        The special characters can be combined with inline code
        ```js
        > console.log("Up up\n\tdown down")
        // Returns:
        // Up up
        //     down down 
        ```
    - **Implicit type coercion** - JavaScript is known as a loosely typed language. Basically, this means that when you’re writing JavaScript code, you do not need to specify data types. Instead, when your code is interpreted by the JavaScript engine it will automatically be converted into the "appropriate" data type. Considering these examples below:
        ```bash
        > "1" == 1
        > 0 == false
        > ' ' == false
        ```
        All the three statements above evaluate to true. The reason for such interesting outcomes is ***Type Conversion***. In the case of regular comparison, the operands on either side of the == operator are first converted to numbers, before comparison. Therefore, a ' ', false, and 0 are all considered equal. Similarly, a '1' and 1 are also considered equal. If we don't want to convert the operands, before comparison, we have to use a ***Strict Comparison*** (triple equal signs) **`===`**. <br>
        When you use the `==` or `!=` operators, JavaScript first converts each value to the same type (if they’re not already the same type); this is why it's called "type coercion"! This is often not the behavior you want, and **it’s actually considered bad practice to use the `==` and `!=` operators when comparing values for equality**. Instead use `===` and `!==`.

- **Booleans** - A "true" statement corresponds to number 1, whereas a "false" statement represents a number 0. Boolean responses can be obained from comparison statements. <br>

- **Null, Undefined, and NaN** - NaN stands for "Not-A-Number" and it's often returned indicating an error with number operations. For instance, if you wrote some code that performed a math calculation, and the calculation failed to produce a valid number, NaN might be returned.
    ```js
    // calculating the square root of a negative number will return NaN
    > Math.sqrt(-10)

    // trying to divide a string by 5 will return NaN
    > "hello"/5

    // undefined variable
    > var signedIn;
    > console.log(signedIn);

    // null value
    > var signedIn = null;
    > console.log(signedIn);
    ```