/*
 * Programming Quiz: Build A Triangle (5-3)
 * 
 * For this quiz, you're going to create a function called buildTriangle() that will accept an 
 * input (the triangle at its widest width) and will return the string representation of a triangle. 
 * You will need to call this makeLine() function in buildTriangle().
 * 
 */

/*
 * QUIZ REQUIREMENTS
 * - Your code should have a `buildTriangle()` function
 * - Your `buildTriangle()` function should take one argument (or you can say parameter)
 * - Your `buildTriangle()` function should build the triangle as describe above
 */


// creates a line of * for a given length
function makeLine(length) {
    var line = "";
    for (var j = 1; j <= length; j++) {
        line += "* ";
    }
    return line + "\n";
}

// your code goes here.  Make sure you call makeLine() in your own code.
function buildTriangle(numLines) {
    let triangle=""
    for (var l = 1; l <= numLines; l++) {
        triangle += makeLine(l);
    }
    return triangle;
}


// test your code by uncommenting the following line
console.log(buildTriangle(10));