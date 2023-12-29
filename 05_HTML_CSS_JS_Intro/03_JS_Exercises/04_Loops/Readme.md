## Loops
There are many different kinds of loops, but they all essentially do the same thing: they repeat an action some number of times.

Three main pieces of information that any loop should have are:
1. **When to start**: The code that sets up the loop — defining the starting value of a variable for instance.
2. **When to stop**: The logical condition to test whether the loop should continue.
3. **How to get to the next item**: The incrementing or decrementing step — for example, `x = x * 3` or `x = x - 1`

### While Loops
Here's a basic while loop example that includes all three parts.
```js
var start = 0; // when to start
while (start < 10) { // when to stop
    console.log(start);
    start = start + 2; // how to get to the next item (increments by 2)
}
```
Forgetting any of the 3 tenets of a loop when implementing 'while' loops will create an infinite loop that ca crash the browser tab or the entire browser.

### For Loops
They are the most common loops in js. The `for loop` explicitly forces you to define the start point, stop point, and each step of the loop. In fact, you'll get an `Uncaught SyntaxError: Unexpected token )` if you leave out any of the three required pieces. 
```js
// wildcard loop
> for ( start; stop; step ) {
    // do this thing
}


// example implementation
> for (var i = 0; i < 6; i = i + 1) {
    console.log("Printing out i = " + i);
}
```

#### Nested Loops
Loops can also be nested within each other just like conditional statements. It's an additional level of complexity compared to basic loops.
```js
> for (var x = 0; x < 5; x = x + 1) {
    for (var y = 0; y < 3; y = y + 1) {
        console.log(x + "," + y);
    }
}
```

#### Increment and Decrement operators
These operators can be used to shorten code syntax while running loops
``` js
// Example operators are
x++ or ++x // same as x = x + 1 
x-- or --x // same as x = x - 1
x += 3 // same as x = x + 3
x -= 6 // same as x = x - 6
x *= 2 // same as x = x*  2
x /= 5 // same as x = x / 5
```
