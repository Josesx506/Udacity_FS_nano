/*
 * Programming Quiz: Quidditch Cup (6-5)
 * 
 * In the Harry Potter novels, children attending the Hogwarts School of Witchcraft and Wizardry 
 * belong to one of four houses: Gryffindor, Hufflepuff, Ravenclaw, or Slytherin. Each year, the 
 * houses assemble a Quidditch team of seven players to compete for the coveted Quidditch Cup.
 * 
 * Create a function called hasEnoughPlayers() that takes the team array as an argument and returns
 * true or false depending on if the array has at least seven players.
 * 
 */
/*
 * QUIZ REQUIREMENTS
 * - Your code should have a function `hasEnoughPlayers()`
 * - Your function `hasEnoughPlayers()` should accept one parameter
 * - Your function `hasEnoughPlayers()` should return the expected output - a Boolean value - true or false
 * - Return true if the array size is atleast 7, otherwise false. 
 */
 
// your code goes here
function hasEnoughPlayers(array) {
    if (array.length >= 7) {
        return true;
    } else {
        return false;
    }
}

var team = ["Oliver Wood", "Angelina Johnson", "Katie Bell", "Alicia Spinnet", "George Weasley", "Fred Weasley", "Harry Potter"];
console.log(hasEnoughPlayers(team));
