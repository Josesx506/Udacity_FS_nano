## Objects
An Object is a data structure in JavaScript that lets you store data about a particular thing, and helps you keep track of that data by using a "key". Objects are like python dictionaries with keys and values, but they can also have methods like python classes. They are originally defined as variables with curly brackets `{}`. Unlike strings, numbers, booleans, null and undefined, an array is a type of **object**. An example object is
```js
// Define the umbrella variable
> var umbrella = { 
    color: "pink",
    isOpen: false,
    open: function() {
        if (umbrella.isOpen === true) {
            return "The umbrella is already opened!";
        } else {
            umbrella.isOpen = true;
            return "Julia opens the umbrella!";
        }
    }
};

// Access the function method
> umbrella.open();
```
**TIP**: It’s worth noting that while we can represent real-world objects as JavaScript objects, the analogy does not always hold. This is a good starting place for thinking about the structure and purpose of objects, but as you continue your career as a developer, you’ll find that JavaScript objects can behave wildly different than real objects. <br>


The syntax in the example above is called **object-literal notation**. There are some important things you need to remember when you're structuring an object literal:
- The "key" (representing a **property** or **method** name) and its "value" are separated from each other by a **colon**.
- The `key: value` *pairs* are separated from each other by **commas**.
- The entire object is wrapped inside curly braces { }.
    ```js
    // two equivalent ways to use the key to return its value
    > sister["parents"] // returns [ "alice", "andy" ] This is bracket notation
    > sister.parents // also returns ["alice", "andy"]. This is dot notation 
    ```

### Naming Conventions
When creating key names for js objects:
1. don't start the key names with **numbers** e.g `"1stChild"`. Even if the key names are wrapped as strings, attempting to access them with **dot notations** will raise *SyntaxError*.
2. don't include **spaces** or **dashes** in key names when defining objects e.g. `"fire truck" or "race-car"`. This also raises SyntaxError.
3. Use camelCase patterns where the new words start with one uppercase letter when defining keys e.g `camelCase`

Objects are one of the most important data structures in JavaScript. Get ready to see them everywhere! <br>
They have properties (information about the object) and methods (functions or capabilities the object has). Objects are an incredibly powerful data type and you will see them all over the place when working with JavaScript, or any other object-oriented programming language.

```js
// object-literal notation
> var myObj = { 
    color: "orange",
    shape: "sphere",
    type: "food",
    eat: function() { return "yummy" }
};

myObj.eat(); // method
myObj.color; // property

// naming conventions
> var richard = {
    "1stSon": true;
    "loves-snow": true;
};

richard.1stSon // error
richard.loves-snow // error
```

