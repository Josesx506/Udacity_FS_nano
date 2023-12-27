## HTML - HyperText Markup Language
HTML templates can be broken down into 3 parts:

1. `DOCTYPE`: Describes the type of HTML. While there are technically different types, for 99.999% of the HTML you'll write, you’ll likely be fine with `<!DOCTYPE html>`.
2. `<head>`: Describes meta information about the site, such as the title, and provides links to scripts and stylesheets the site needs to render and behave correctly.
3. `<body>`: Describes the actual content of the site that users will see.

All of the HTML syntax that you’ve learned in this lesson will help you create the content of the page, which is always contained inside the  `<body>`tags. The `<body>` is always visible. <br>

The `<head>`, on the other hand, is never visible, but the information in it describes the page and links to other files the browser needs to render the website correctly. For instance, the `<head>` is responsible for:
- the document’s **title** (the text that is displayed in the tab of a browser window): `<title>About Me</title>`.
- associated CSS files (for style): `<link rel="stylesheet" type="text/css" href="style.css">`.
- associated JavaScript files (multipurpose scripts to change rendering and behavior): `<script src="animations.js"></script>`.
- the charset being used (the text's encoding): `<meta charset="utf-8">`.
- keywords, authors, and descriptions (often useful for SEO): `<meta name="description" content="This is what my website is all about!">`.
- … and more!

[**HTML Validators**](https://validator.w3.org/#validate_by_uri) can be used to analyze your website/text and verify that you're writing valid HTML. <br>

[Void elements](https://html.spec.whatwg.org/multipage/syntax.html#void-elements) like `img` do not require closing tags.