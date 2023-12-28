## JS - JavaScript
**TIP**: `HTML` and `CSS` are *markup* languages. Markup languages are used to **describe and define elements** within a document. `JavaScript` is a *programming* language. Programming languages are used to **communicate instructions to a machine**. Programming languages can be used to control the behavior of a machine and to express algorithms.

### console.log
`console.log()` is the equivalent of a python print statement. It can be used to test js syntax and debug multiple lines of code. An example is `console.log("hiya friend!");`.

### Data Tyoes and Variables
Popular datatypes include numbers, strings, variables etc.

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

- **Variables** can allow repeated use of assigned values compared to undefined strings and numbers. 
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
