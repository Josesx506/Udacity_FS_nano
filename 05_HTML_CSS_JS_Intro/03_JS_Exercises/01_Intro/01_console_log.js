// Print a string
console.log("hiya friend!");

// Print a for loop
for (var i = 0; i < 10; i++) {
    console.log(i);
  }

// Extract a h1 element and change the color to red
document.getElementsByTagName("h1")[0].style.color = "#ff0000";

// Include a dom listener with js that adds an image to a h1 element
// Each time any point is clicked on the image, a new random gif is added to the h1 element
document.body.addEventListener('click', function () {
    var myParent = document.getElementsByTagName("h1")[0]; 
    var myImage = document.createElement("img");
    myImage.src = 'https://thecatapi.com/api/images/get?format=src&type=gif';
    myParent.appendChild(myImage);
    myImage.style.marginLeft = "160px";
});