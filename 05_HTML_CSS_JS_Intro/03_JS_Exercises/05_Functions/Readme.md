## Functions
Functions allow you to package up lines of code that you can use (and often reuse) in your programs. <br>

Sometimes they take **parameters** like the pizza button from the beginning of this lesson. reheatPizza() had one parameter: the number of slices.
```js
function reheatPizza(numSlices) {
    // code that figures out reheat settings!
}
```
<br>

The parameter is listed as a variable after the function name, inside the parentheses. And, if there were multiple parameters, you would just separate them with commas (**Note**: This is different from for loops that are separated by semi-colons "; within parentheses).
```js
function doubleGreeting(name, otherName) {
  // code to greet two people!
}
```
<br>

Function arguments can also be empty. Take this one for example. Here's a simple function that just prints out `"Hello!"`.
```js
// accepts no parameters! parentheses are empty
function sayHello() {
    var message = "Hello!"
    console.log(message);
}
```
`undefined` is the default return value on the console when nothing is *explicitly* returned using the special `return` keyword.

### Return statements
It’s important to understand that **return** and **print** are not the same thing. Printing a value to the JavaScript console only displays a value (that you can view for debugging purposes), but the value it displays can't really be used for anything more than that. For this reason, you should remember to only use `console.log` to test your code in the JavaScript console. <br>

The function exits after the first return statement, and if two return statements are used, only the first one is returned from the function. Multiple return statements can be implemented using conditional statements to alternate between the functions output. A function's return value can be stored in a variable or reused throughout your program as a function argument. <br>

In the `sayHello()` function above, a value is **printed** to the console with `console.log`, but not explicitly returned with a **return statement**. You can write a `return` statement by using the return keyword followed by the expression or value that you want to return.
```js
function sayHello() {
    var message = "Hello!"
    return message; // returns value instead of printing it
}
```

### How to (run) a function
Now, to get your function to do *something*, you have to **invoke** or **call** the function using the function name, followed by parentheses with any **arguments** that are passed into it. Functions are like machines. You can build the machine, but it won't do anything unless you also turn it on. Here's how you would call the `sayHello()` function from before, and then use the return value to print to the console:
```js
// declares the sayHello function
> function sayHello() {
    var message = "Hello!"
    return message;
}

// function returns "Hello!" and console.log prints the return value
> console.log(sayHello());
```

### Parameters vs. Arguments
At first, it can be a bit tricky to know when something is either a parameter or an argument. The key difference is in where they show up in the code. A **parameter** is always going to be a *variable* name and appears in the function declaration. On the other hand, an **argument** is always going to be a *value* (i.e. any of the JavaScript data types - a number, a string, a boolean, etc.) and will always appear in the code when the function is called or invoked. Example
```js
// x & y are parameters
> function findAverage(x, y) {
    var answer = (x + y) / 2;
    return answer;
}
// 5 & 9 are arguments
> var avg = findAverage(5, 9);
```
- **Parameters** are variables that are used to store the data that's passed into a function for the function to use. 
- **Arguments** are the actual data that's passed into a function when it is invoked.


### Scope, Shadowing, and Hoisting
- **Functions** can be defined within the global, function, or block scopes.
- **Shadowing** is when a block or function scope variable overwrites a pre-existing global variable. It can be avoided by explicitly defining the secondary variable with the `var ` prefix.
- **Hoisting** is the rearrangement of all functions at the top of a js script before the script is executed. This means that a function can be called before it's executed, because all functions are hoisted to the top of their current scope. Variable declarations also get hoisted, but variable assignments stay put. To avoid debugging errors, js developers typically **define functions at the top of their scripts, and variables at the top of the functions**. That way the appearance of the code and execution steps are consistent with each other.
    - JavaScript hoists function declarations and variable declarations to the top of the current scope.
    - Variable assignments are not hoisted.
    - Declare functions and variables at the top of your scripts, so the syntax and behavior are consistent with each other.


### Function Types
This means that functions can be defined as 
- Declarations (Assigned independently with a function name)
- Expressions (Assigned to a variable)
    - Inline function expressions


### Function Expressions
When you store a function within a variable, the function name is ignored, and the function is generally **anonymous**. This is known as a **Function expression**. 
```js
// Function expression
var catSays = function(max) {
    var catMessage = "";
    for (var i = 0; i < max; i++) {
        catMessage += "meow ";
    }
    return catMessage;
};

// The function can be accessed with the variable name
// You'll even see the function returned back to you.
> catSays;
// Run the function
> catSays(3);
```
<br>

If a name is specified for the function expression, it is called a **named function expression**. Function names are still **ignored** in function expressions and only the variable name can be used to access the function. 
```js
> var favoriteMovie = function movie() {
    return "The fountain";
}
> favoriteMovie(); // valid: variable name is used to access the function
> movie();         // invalid: named function will return a reference error!
```

All **function declarations are hoisted** and loaded before the script is actually run. **Function expressions are not hoisted**, since they involve variable assignment, and only variable declarations are hoisted. The function expression will not be loaded until the interpreter reaches it in the script. <br>

Being able to store a function in a variable makes it really simple to pass the function into another function. A function that is passed into another function is called a **callback**. Let's say you had a `helloCat()` function, and you wanted it to return "Hello" followed by a string of "meows" like you had with `catSays`. Well, rather than redoing all of your hard work, you can make `helloCat()` accept a callback function, and pass in `catSays`.
```js
// function expression catSays
var catSays = function(max) {
  var catMessage = "";
  for (var i = 0; i < max; i++) {
    catMessage += "meow ";
  }
  return catMessage;
};

// function declaration helloCat accepting a callback
function helloCat(callbackFunc) {
  return "Hello " + callbackFunc(3);
}

// pass in catSays as a callback function
helloCat(catSays);
```
<br>

**Inline function expressions** can be created by defining anonymous functions inline once as a callback within a parent function. This pattern is commonly used in JavaScript, and can be helpful streamlining your code.
```js
// Parent function declaration that takes in two arguments: a function for displaying
// a message, along with a name of a movie
// messageFunction parameter is a callback
> function movies(messageFunction, name) {
    messageFunction(name);
}

// Call the movies function, pass in the inline function expression and name of movie
> movies(function displayFavorite(movieName) { // start of inline expression
    console.log("My favorite movie is " + movieName);
    }, 
    "Finding Nemo"); // second function parameter
```
**Why use anonymous inline function expressions?** <br>
Using an anonymous inline function expression might seem like a very not-useful thing at first. Why define a function that can only be used once and you can't even call it by name? <br>

Anonymous inline function expressions are often used with function callbacks that are probably not going to be reused elsewhere. Yes, you could store the function in a variable, give it a name, and pass it in like you saw in the examples above. However, when you know the function is not going to be reused, it could save you many lines of code to just define it inline.