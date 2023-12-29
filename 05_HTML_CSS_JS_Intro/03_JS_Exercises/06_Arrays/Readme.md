## Arrays
An array is a data structure that you can use to store and organize multiple values. Arrays are zero indexed and declared with square brackets like python lists.

```js
// creates a `donuts` array with three strings
> var donuts = ["glazed", "powdered", "jelly"];

// Like python lists, they are data agnostic
// creates a `mixedData` array with mixed data types
> var mixedData = ["abcd", 1, true, undefined, null, "all the things"];

// They can also be nested within each other
// creates a `arraysInArrays` array with three arrays
> var arraysInArrays = [[1, 2, 3], 
    ["Julia", "James"], 
    [true, false, true, false]
    ];
```

**Note**: ixed data arrays are typically not very useful. In most cases, you’ll want to use elements of the same type in your arrays. <br>

### Accessing Array Elements
Array elements can be accessed using the index values enclosed with square brackets. Each index references the element location in the array.
```js
> var donuts = ["glazed", "powdered", "sprinkled"];
> console.log(donuts[0]); // "glazed" is the first element in the `donuts` array
```
- If you try to access an element at an index that does not exist, a value of undefined will be returned back.
- if you want to change the value of an element in array, you can do so by setting it equal to a new value.
    ```js
    > donuts[1] = "glazed cruller"; // changes the second element in the `donuts` array to "glazed cruller"
    > console.log(donuts[1]); 
    ```

### Properties and Methods.
Arrays have different properties/attributes like `.length` which returns the **number of elements** in the array. Properties are not called with brackets. Strings have a `length` property too! You can use it to get the length of any string. For example, `"supercalifragilisticexpialidocious".length` returns `34`.<br>

Arrays also have methods which can be used to perform operations on the array. Methods are usually called with brackets e.g. `.reverse()`. Examples in include
```js
> array.reverse() // reverses the order of elements in an array
> array.sort() // sorts the elements in an array
> array.push() // append an element to the end of an array
> array.pop() // remove the last element from the array
> array.forEach((value, key)) // equivalent to enumerate([list]) in python
```
Other popular methods can be viewed [MDN Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array), or type []. into the JavaScript console for a list of all the available Array methods. <br>

The `push()` method requires the value of the element you want to add to the end of the array, and it returns the length of the array after an element has been added. <br>
The `pop()` method doesn't require any input, and it is used to remove elements from the end of an array.
```js
// Push
> var donuts = ["glazed", "chocolate frosted", "Boston creme", "glazed cruller", "cinnamon sugar", "sprinkled"];
> donuts.push("powdered"); // pushes "powdered" onto the end of the `donuts` array

// Pop
> var donuts = ["glazed", "chocolate frosted", "Boston creme", "glazed cruller", "cinnamon sugar", "sprinkled", "powdered"];
> donuts.pop(); // the `pop()` method returns "powdered" because "powdered" was the last element on the end of `donuts` array
```

You can use the `splice()` method to add or remove elements from anywhere within an array. `splice()` lets you specify the index location to add new elements, as well as the number of elements you'd like to delete (if any).
Splice syntax arguments are `arrayName.splice(arg1, arg2, item1, ....., itemX);` or `arrayName.splice(start, deleteCount, item1, item2, /* …, */ itemN)` where
- `arg1` = Mandatory argument. Specifies the starting index position to add/remove items. You can use a negative value to specify the position from the end of the array e.g., -1 specifies the last element.
- `arg2` = Optional argument. Specifies the count of elements to be removed. If set to 0, no items will be removed.
- `item1, ....., itemX` are the items to be added at index position arg1

`splice()` method returns the item(s) that were removed. An example is 
```js
> var donuts = ["glazed", "chocolate frosted", "Boston creme", "glazed cruller"];

// It starts checking from index 1 i.e arg1. arg2=1 removes one item from index 1 i.e "chocolate frosted"
// Then it add "chocolate cruller" and "creme de leche" items to the array starting at index 1
> donuts.splice(1, 1, "chocolate cruller", "creme de leche"); 

// If you want to perform only an insert action, set argument 2 to zero. If no elements are removed, an empty array is returned.
```
If the first argument in `splice()` is negative, it starts counting from the back of the array. However, unlilke python, the array elements cannot be indexed using negative values.
```js
> var donuts = ["cookies", "cinnamon sugar", "creme de leche"];
> donuts.splice(-2, 0, "chocolate frosted", "glazed");
// returns ["cookies", "chocolate frosted", "glazed", "cinnamon sugar", "creme de leche"]
```

- **Removing the first element in an array** <br>
    - `shift()` will remove the first element from an array.
    - `splice()` can be used if you specify the index of the first element, and indicate that you want to delete 1 element.
    - Keep in mind that the `slice()` method allows you to create a copy of the array between two indices. Though you could just exclude the index of the first element, this approach does not directly modify a given array.

- You can **combine** the elements in an array to **form a string** using the `join()` method e.g. 
    ```js
    > var turnMeIntoAString = ["U", "d", "a", "c", "i", "t", "y"];
    > turnMeIntoAString.join(''); // Udacity
    ```
<br>

### Array Loops
Once the data is in the array, you want to be able to efficiently access and manipulate each element in the array without writing repetitive code for each element. Loops over arrays can be performed using
- a regular `for(var start; end; increment;)` loop with the array index.
- the `.forEach(value, key, array)` method.
- the `.map()` method which applies a function over the array.
<br><br>


#### for loop
For instance, if this was our original donuts array:
```js
> var donuts = ["jelly donut", "chocolate donut", "glazed donut"];
// and we decided to make all the same donut types, but only sell them as donut 
// holes instead, we could write the following code:
> donuts[0] += " hole";
> donuts[1] += " hole";
> donuts[2] += " hole"; // ["jelly donut hole", "chocolate donut hole", "glazed donut hole"]
```

This can also be achieved with loops
```js
> var donuts = ["jelly donut", "chocolate donut", "glazed donut"];

// the variable `i` is used to step through each element in the array
// Appends the hole word to each element and converts them to upper case
> for (var i = 0; i < donuts.length; i++) {
    donuts[i] += " hole";
    donuts[i] = donuts[i].toUpperCase();
}

// ["JELLY DONUT HOLE", "CHOCOLATE DONUT HOLE", "GLAZED DONUT HOLE"]
```
In this example, the variable `i` is being used to represent the index of the array. As `i` is incremented, you are stepping over each element in the array starting from `0` until `donuts.length - 1` (`donuts.length` is out of bounds). <br><br>



#### .forEach() method
The **`forEach()`** method can be used to enumerate over all the items in the list when performing loop operations on an array. In this example below, note how an inline function expression is used to obtain the same results as the prior example.
```js
> var donuts = ["jelly donut", "chocolate donut", "glazed donut"];

> donuts.forEach(function(donut) {
    donut += " hole";
    donut = donut.toUpperCase();
    console.log(donut);
});
```
The `forEach()` method iterates over the array without the need of an explicitly defined index. This is different from a for or while loop where an index is used to access each element in the array. <br>

The function that you pass to the `forEach()` method can take up to three parameters. In the video, these are called `element`, `index`, and `array`, but you can call them whatever you like. The forEach() method will call this function once for each element in the array (hence the name `forEach`.) Each time, it will call the function with different arguments. 
- The `element` parameter will get the value of the array element/value. 
- The `index` parameter will get the index of the element (starting with zero). 
- The `array` parameter will get a reference to the whole array, which is handy if you want to modify the elements.

Here's another example:
```js
> words = ["cat", "in", "hat"];
> words.forEach(function(word, num, all) {
    console.log("Word " + num + " in " + all.toString() + " is " + word);
});
// Prints:
// Word 0 in cat,in,hat is cat
// Word 1 in cat,in,hat is in
// Word 2 in cat,in,hat is hat
```
<br>



#### .map() method
Using `forEach()` will not be useful if you want to permanently modify the original array. `forEach()` always returns `undefined`. However, creating a new array from an existing array is simple with the powerful `map()` method. <br>

With the `map()` method, you can take an array, perform some operation on each element of the array, and return a new array.
```js
> var donuts = ["jelly donut", "chocolate donut", "glazed donut"];

> var improvedDonuts = donuts.map(function(donut) {
    donut += " hole";
    donut = donut.toUpperCase();
    return donut;
});
```
<br>



#### Looping across 2D arrays
2D arrays can also be accessed by their index values.

```js
> var donutBox = [
    ["glazed", "chocolate glazed", "cinnamon"],
    ["powdered", "sprinkled", "glazed cruller"],
    ["chocolate cruller", "Boston creme", "creme de leche"]
];

// Loop over every row and column
> for (var row = 0; row < donutBox.length; row++) {
    // here, donutBox[row].length refers to the length of the donut array currently being looped over
    for (var column = 0; column < donutBox[row].length; column++) {
        console.log(donutBox[row][column]);
  }
}
```
