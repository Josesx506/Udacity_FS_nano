/*
 * Programming Quiz: Facebook Friends (7-5)
 */

/*
 * QUIZ REQUIREMENTS
 * - Your code should have an object `facebookProfile`
 * - The `facebookProfile` object should have the `name` (string), `friends` (number), and `messages` (array of strings) property
 * - Your `facebookProfile` object should have the `postMessage()`, `deleteMessage()`, `addFriend()` and `removeFriend()` method
 * - Carefully implement the desired functionality of each method, as decribed above
 * 1. postMessage(message) - adds a new message string to the array
 * 2. deleteMessage(index) - removes the message corresponding to the index provided
 * 3. addFriend() - increases the friend count by 1
 * 4. removeFriend() - decreases the friend count by 1
 * 
 */


// TIP - 
// In an array, 
// - addition at the end is done using push() method
// - addition at a specific index is done using splice() method
// - deletion from the beginning is done using pop() method
// - deletion from a specific index is done using splice() method

// your code goes here
var facebookProfile = {
    name: "JoeBaba",
    friends: 5,
    messages: ["Hello", "Where", "Udacity"],
    postMessage: function (message) {
        facebookProfile.messages.push(message);
    },
    deleteMessage: function(index) {
        facebookProfile.messages.splice(index, 1);
    },
    addFriend: function () {
        facebookProfile.friends += 1;
    },
    removeFriend: function () {
        facebookProfile.friends -= 1;
    }
}

console.log(facebookProfile)
