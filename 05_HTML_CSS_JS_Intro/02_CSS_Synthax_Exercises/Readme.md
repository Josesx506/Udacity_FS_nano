## CSS - Cascading Style Sheets
CSS is made of rulesets. A selector e.g `div`, and a declaration block which is the text written within the curly braces e.g. `text-align: right`. A complete example of a ruleset is
```css
div {
    text-align: right;
}
```
In the example above, `text-align` is the property being modified, and `right` is the value of how the feature should modified. The example aligns all the text in a *div* to the right. <br>

### CSS Selectors
HTML elements can be styled with css by targeting:
- tags
- attributes (id or class)
    - *id* should only be used **sparingly** because a html element can only use one id, and the same id once per page
    - *classes* can be used repeatedly when you want to implement the same styling to multiple elements. More than one class can be applied to an element and the order of the classes doesn't matter.

**Tag Selectors** 
- Tags like `p`, `h1`, etc. are useful when you want to change the properties of every tag that matches the selector in css. E.g. Change the background color of all the elements.
    ```css
    h1 {
        color: green;
    }
    ```
<br>

**Attribute Selectors** <br>
- `id` - html elements can be styled using id attributes by including a pound *#* before the class name e.g.
    ```css
    #site-description {
        color: red;
    }
    ```
- `class` - html elements can be styled using class attributes by including a period *.* before the class name e.g.
    ```css
    .book-summary {
        color: blue;
    }
    ```

[Hundreds of CSS properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference) can be modified to adjust text. Some examples include
| Effect | CSS syntax |
| :----- | ---------: |
| *italicize* | font-style |
| underline | text-decoration |
| UPPERCASE | text-transform |
| **bold** | font-weight |

Additional css property synthax can be view at [css-tricks](https://css-tricks.com/almanac/). <br><br>

Example style properties learnt in class include:
- [border](https://developer.mozilla.org/en-US/docs/Web/CSS/border)
- [cursor](https://css-tricks.com/almanac/properties/c/cursor/).
- [box-shadow](http://www.cssmatic.com/box-shadow)
- [fonts](https://www.cssfontstack.com/)
    Because all fonts are not available on every operating system, multiple font-families can be specified as options for the browser to check when rendering a page.


### CSS Units
CSS units of length can be `Absolute` or `Relative`. Resources on units can be view on [MDN CSS length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) and [css-tricks length](https://css-tricks.com/the-lengths-of-css/)

- Absolute units - The most popular unit is pixels `px`. However, other units like `mm`, `in`, `cm` among others can also be used. These are rarely used.
- Relative units - The most popular unit is percent `%`. However, other units like `em`, viewport width `vw`, viewport height `vh` among others can also be used. These are used more in responsive web design templates.

### CSS Colors
Can be defined using the [RGB Convention](https://www.webfx.com/web-design/hex-to-rgb/) or [Hexadecimal Numeral System](https://en.wikipedia.org/wiki/Hexadecimal). There are over 16 million color combinations that can be used.


- RGB - Uses a red, green, blue convention with values for each band ranging between 0-255. An example of magenta which is a combination of red and blue is
    ```css
    body {
        background-color: rgb(255, 0, 255);
    }
    ```
- Hexadecimal system - Uses a similar arrangement of RGB but with values ranging between 00-FF. This is essentially 0 to 255 represented as hexadecimals. A pound `#` sign is usually included before the hex code to let the browser know that a hexadecimal color should be applied. An example of magenta which is a combination of red and blue is
    ```css
    body {
        background-color: #ff00ff;
    }
    ```

Browsers like Chrome come with a color picker tool that can be used to select different colors from a webpage. By navigating to developer tools and viewing css syntax for elements, select any color and used in the css tab, and the color picker tool is activated. <br>

References <br>
- [Named Colors and Hex Equivalents](https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/)
- [CSS Shorthand Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties)
- [CSS Shorthand Hexadecimal form](https://en.wikipedia.org/wiki/Web_colors#Shorthand_hexadecimal_form)

<br>

### CSS Stylesheets
Stylesheets are used when we want to use the same CSS styles on more than one webpage. A stylesheet is a file containing the code that describes how elements on your webpage should be displayed. To link a stylesheet to a html file
```html
<link href="path-to-stylesheet/stylesheet.css" rel="stylesheet">
```
This is usually included in the header tag of the html file.