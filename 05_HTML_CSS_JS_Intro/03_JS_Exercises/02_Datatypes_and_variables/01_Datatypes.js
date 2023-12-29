// Numbers
console.log(2 + 10 - 19 + 4 - 90 + 1);
console.log(-20 + -19 - (-10) - (-1) + 24);
console.log((10/5) * 4 - 20);
console.log(4096 % 12);

// Strings
console.log("Hello" + "World!");
console.log("Hello," + " New York City");
console.log("Hello" + 5*10);

// Variables
var greeting = "Hello Juice World!";
console.log(greeting);
var filePath = "The file located at \"C:\\\\Desktop\\My Documents\\Roster\\names.txt\" contains the names on the roster.";
console.log(filePath);

// Loops - Iterate using a Loop
var my_string = "Udacity";
for (var i = 0; i < my_string.length; i++) {
    console.log(my_string.charCodeAt(i));
}

// Nice! When checking if a string is "greater than" or "less than" another string, JavaScript compares individual 
// characters using a numerical value. Each character is assigned a numerical value that essentially corresponds to 
// the character's location in an ASCII table: http://www.ascii-code.com/. Strings are also case-senstive.
console.log("green" > "Green");  //True
console.log("green" > "blue");   // true
console.log("green" == "Green"); // false

// Booleans
// A "true" statement corresponds to number 1, whereas a "false" statement represents a number 0
var studentName = "John";
var haveEnrolledInCourse = true;
var haveCompletedTheCourse = false;
if (haveEnrolledInCourse){ 
    console.log("Welcome "+studentName+" to Udacity!"); // Will run only if haveEnrolledInCourse is true
}

var a = 10;
var b = 20;
// comparison statements
if (a>b) // The outcome of a>b will be a boolean
	console.log("Variable `a` has higher value"); // if a>b is true
else 
	console.log("Variable `b` has higher value"); // if a>b is false

console.log();
console.log();
console.log();