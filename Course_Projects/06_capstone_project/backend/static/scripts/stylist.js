editMode = false;

document.getElementById('createStylist').onclick = function (e) {
    // Make the form element visible
    $('.stylist-form-container').toggleClass('open');

    // Clear the form input
    $('.stylistForm')[0].reset();
};


document.getElementsByClassName('stylistForm')[0].onsubmit = function (e) {
    e.preventDefault();
    // Extract the items from the form
    var fname = document.getElementById('formName').value
    var frole = document.getElementById('formRole').value
    var phoneNum = document.getElementsByClassName('formPhoneNum')[0].value
    var emailAdd = document.getElementsByClassName('formEmail')[0].value
    var imgLink = document.getElementById('formImage').value
    var bioText = document.getElementById('formBio').value

    if (editMode) {
        console.log('edit not implemented yet')
    } else {
        // Implement the asynchronous fetch to POST an event to the db
        fetch("/stylists/create", {
            // method type
            method: 'POST',
            // json formatted string from the form input
            body: JSON.stringify({
                'stylist_name': fname,
                'stylist_salon_role': frole,
                'phone': phoneNum,
                'email': emailAdd,
                'img_link': imgLink,
                'bio': bioText
            }),
            // specify the data type as json so the server understands how to read it
            headers: { 'Content-Type': 'application/json' }
        }).then(function() {
            window.location.reload(true)
        }).catch(error => {
            console.error('Error creating stylist entry:', error);
        });};
    
    // Hide the form after creating the stylist
    $('.stylist-form-container').toggleClass('open');  
};