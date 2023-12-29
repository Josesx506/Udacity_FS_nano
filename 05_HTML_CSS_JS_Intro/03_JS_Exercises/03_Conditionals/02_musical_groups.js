/*
 * Programming Quiz: Musical Groups (3-3)
 * Write a series of conditional statements that:
 * - Prints "not a group" if musicians is less than or equal to 0
 * - Prints "solo" if musicians is equal to 1
 * - Prints "duet" if musicians is equal to 2
 * - Prints "trio" if musicians is equal to 3
 * - Prints "quartet" if musicians is equal to 4
 * - Prints "this is a large group" if musicians is greater than 4
 * 
 */
/*
 * QUIZ REQUIREMENTS
 * 1. Your code should have a variable `musicians`, and include `if...else if...else` conditional statement
 * 2. Your code should produce the expected output, as mentioned above. Read each condition carefully. 
 */
 
// change the value of `musicians` to test your conditional statements
var musicians = 4;

// your code goes here
if (musicians <= 0) {
    console.log("not a group")
} else if (musicians === 1) {
    console.log("solo")
} else if (musicians === 2) {
    console.log("duet")
} else if (musicians === 3) {
    console.log("trio")
} else if (musicians === 4) {
    console.log("quartet")
} else if (musicians > 4) {
    console.log("this is a large group")
}
