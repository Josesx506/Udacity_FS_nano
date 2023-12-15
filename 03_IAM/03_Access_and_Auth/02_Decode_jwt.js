function parseJwt (token) {
    // This function shows how to decode a jwt directly in our frontend with js
    // It improves the user experience by limiting the interactions to only those that can be fufilled
    // It all reduces the number of requests that cannot be fufilled by the server
    // It's a good replace for jwt.io that can be implemented in console or within a js script
    // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript
   var base64Url = token.split('.')[1];
   var base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));

   return JSON.parse(base64);
};