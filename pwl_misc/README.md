## Description
This allows you to implement a mask across a map with a hole in the middle using polygons. <br>
You'll also need to provide a google maps api key (I used my personal key to test this, and replaced it with a placeholder for upload). <br><br>
- The polygon will need two boundaries. 
    - **Outer boundary** (This can be anywhere in the world but it must contain at least 3 points)
    - **Inner boundary** (This will remained fixed. I used a manually created polygon for simplicity but this where you'll read the kml file)
<br>

The `index.js` script will be used to update the outer boundary of the polygon each time the map is updated while the inner boundary remains fixed. <br>
For the hole to be created, the boundary polylines **MUST** be in opposite directions. e.g. If the outer boundary is drawn in a *clockwise* direction, the inner boundary will be *anti-clockwise*. <br>
If they are in the same direction, the hole will not be created. <br>
After the polygon has been created, *mouse-click* events will only work for unshaded areas.<br>
![alt text](https://i.stack.imgur.com/4WM4I.jpg)
