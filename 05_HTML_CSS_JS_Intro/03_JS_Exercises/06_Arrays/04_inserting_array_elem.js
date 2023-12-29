/*
 * Programming Quiz: Colors of the Rainbow (6-4)
 *
 * James was creating an array with the colors of the rainbow, and he forgot some colors. 
 * The standard rainbow colors are usually listed in this order:
 * var rainbow = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"];
 * but james had this 
 * var rainbow = ["Red", "Orange", "Blackberry", "Blue"];
 * 
 * Use only the splice() method to modify the rainbow variable:
 *  - remove "Blackberry"
 *  - add "Yellow" and "Green"
 *  - add "Purple"
 */

var rainbow = ['Red', 'Orange', 'Blackberry', 'Blue'];

// your code goes here
rainbow.splice(2, 1, "Yellow", "Green");
rainbow.splice(5, 0, "Purple");

console.log(rainbow);
