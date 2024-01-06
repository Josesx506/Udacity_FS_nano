// Current date to quality check calendar
var today = new Date();

// Assume the submit form is not in edit mode by default
var editMode = false; 

// Array of colors to be used to style booked event icons
var colorArray = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

// Random selector function to select from the array of colors above
function getRandom(a) {
    return Math.floor(Math.random() * a);
}

// Random Text Generator as function. You can change 7 to 12 for longer results.
let rtg = (Math.random() + 1).toString(36).substring(7);

// Obtain the user role for front-end rendering
var userRoles = document.getElementById('user-role').textContent;


// --------------------------------------------------------------------------------------------
// On page load, initialize the Calendar
// --------------------------------------------------------------------------------------------
$(document).ready(function () {
    $("#calendar").evoCalendar({
        format: "mm/dd/yyyy", // "MM dd, yyyy",
        theme: 'Default',
        language: 'en',
        titleFormat: "MM yyyy",
        todayHighlight: false,
        sidebarToggler: false,
        eventListToggler: false,
        eventDisplayDefault: true,
        canAddEvent: false,
        // calendarEvents: null,
    });

    // Update list of calendar events with this get command
    updateCalendarView();
});


// --------------------------------------------------------------------------------------------
// Function to perform async GET request that obtains all the saved booking events from the db.
// This is the first section that runs and updates the user view
// --------------------------------------------------------------------------------------------
function updateCalendarView() {
    // Remove all the events that might exist in the calendar
    $('#calendar').evoCalendar('removeEventList')

    // Uncomment the following line if you want the function to return a variable
    // var eventList = [];
    // var roles_list = [];

    fetch("/appointments/refresh", {
        // method type
        method: 'GET',
        // specify the data type as json so the server understands how to read it
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json())
        .then(data => {
            var event = data.booked_slots;
            
            event.forEach(function(slotEvent) {
                existingEvent = {
                    // Using only the numbers for the id generates an error. I included a random 
                    // text that can be separated with an underscore to get the original event id
                    id: rtg + "_" + slotEvent.id, 
                    name: slotEvent.name,
                    date: slotEvent.date,
                    color: colorArray[getRandom(colorArray.length)],
                    description: slotEvent.description,
                    type: slotEvent.type,
                    phone: slotEvent.phone,
                    email: slotEvent.email,
                    time: slotEvent.time,
                    verified: slotEvent.verified
                };

                // The values here are appended to the `eventList` array above
                // eventList.push(existingEvent);
                
                // Add the event to the calendar asynchronously
                $('#calendar').evoCalendar('addCalendarEvent',existingEvent);
            });

            // Update the views
            user_roles = data.roles;

            // Update the number of daily events in visible calendar
            updateDailyAppointmentsCalendarView()
            
            // Update the add event button
            if (user_roles === 'SalonAdmin' || user_roles === 'SalonStylist' || user_roles === 'SalonUser') {
                qualityCheckAddBtn();
            };
            
            
            // Insert an edit and delete button
            insertEditEventButton();
            insertDeleteEventButton();
        
        }).catch(error => {
            console.error('Error fetching available times:', error);
        });
    
}


// --------------------------------------------------------------------------------------------
// Function to create an `Edit button` element dynamically for each new booking appointment that 
// is made. Execution varies depending on the user roles
// --------------------------------------------------------------------------------------------
function insertEditEventButton(activeDt) {
    // Function to add an edit button to an Event element
    var active_date = $('#calendar').evoCalendar('getActiveDate');
    
    // Select the events for the provided date
    $("#calendar").evoCalendar('selectDate',active_date);

    // Get the list of active events for the day of interest
    var allActiveEvents = $('#calendar').evoCalendar('getActiveEvents');

    // Check if an event-container exists for the selected date
    var eventContainer = $(`.event-container[role='button']`);
    
    // Your logic for handling the existence of an event-container goes here
    for (i=0;i<eventContainer.length; i++) {
        var eventElement = eventContainer[i];
        var editButtonAdded = eventElement.dataset.insertButtonAdded; 

        if ((user_roles === 'SalonAdmin' || user_roles === 'SalonStylist') && !editButtonAdded) {
            // Extract the event id from the data-event-index attribute
            var eventId = eventElement.getAttribute('data-event-index');

            // Add an Event button
            var editEventButton = document.createElement('button');
            editEventButton.className = `editEventButtons ${eventId}`;
            editEventButton.innerHTML = `<i style="font-size:24px" class="far fa-edit"></i>`;

            $(`.event-container[role='button']`)[0].style.zIndex = 10;

            // Append the edit buttons to the parent div
            eventElement.appendChild(editEventButton);

            // Add an attribute to let the element know if the button already exists
            eventElement.dataset.insertButtonAdded = true;

        } else if (user_roles === 'SalonUser' && !editButtonAdded) {
            // Extract the event id from the data-event-index attribute
            var eventId = eventElement.getAttribute('data-event-index');
            
            // Find the active event with a matching id from the list of active events
            var activeEvent = allActiveEvents.find(function(listEvent) {
                return listEvent.id === eventId;
            });

            if (activeEvent.verified) {
                // Add an Event button
                var editEventButton = document.createElement('button');
                editEventButton.className = `editEventButtons ${eventId}`;
                
                editEventButton.innerHTML = `<i style="font-size:24px" class="far fa-edit"></i>`;

                $(`.event-container[role='button']`)[0].style.zIndex = 10;

                // Append the edit buttons to the parent div
                eventElement.appendChild(editEventButton);

                // Add an attribute to let the element know if the button already exists
                eventElement.dataset.insertButtonAdded = true;
            };
        };
    };
};

// --------------------------------------------------------------------------------------------
// Function to create a `Delete button` element dynamically for each new booking appointment that 
// is made. Execution varies depending on the user roles
// --------------------------------------------------------------------------------------------
function insertDeleteEventButton() {
    // Function to add a delete button to an Event element
    var active_date = $('#calendar').evoCalendar('getActiveDate');

    // Select the events for the provided date
    $("#calendar").evoCalendar('selectDate',active_date);

    // Get the list of active events for the day of interest
    var allActiveEvents = $('#calendar').evoCalendar('getActiveEvents');

    // Check if an event-container exists for the selected date
    var eventContainer = $(`.event-container[role='button']`);
    
    // Your logic for handling the existence of an event-container goes here
    for (i=0;i<eventContainer.length; i++) {
        var eventElement = eventContainer[i];
        var deleteButtonAdded = eventElement.dataset.deleteButtonAdded;

        if ((user_roles === 'SalonAdmin' || user_roles === 'SalonStylist') && !deleteButtonAdded) {
            // Extract the event id from the data-event-index attribute
            var eventId = eventElement.getAttribute('data-event-index');
            
            // Add a Delete button
            var deleteButton = document.createElement('button');
            deleteButton.className = `deleteEventButtons ${eventId}`;
            // You can replace this with an "x-icon" HTML or use an image
            deleteButton.innerHTML =  `<i style="font-size:24px" class="fa">&#xf014;</i>`;

            $(`.event-container[role='button']`)[0].style.zIndex = 10;

            // Append the delete buttons to the parent div
            eventElement.appendChild(deleteButton);

            // Add an attribute to let the element know if the button already exists
            eventElement.dataset.deleteButtonAdded = true;
        
        } else if (user_roles === 'SalonUser') {
            // Extract the event id from the data-event-index attribute
            var eventId = eventElement.getAttribute('data-event-index');

            // Find the active event with a matching id from the list of active events
            var activeEvent = allActiveEvents.find(function(listEvent) {
                return listEvent.id === eventId;
            });

            if (activeEvent.verified) {
                // Add a Delete button
                var deleteButton = document.createElement('button');
                deleteButton.className = `deleteEventButtons ${eventId}`;
                // You can replace this with an "x-icon" HTML or use an image
                deleteButton.innerHTML =  `<i style="font-size:24px" class="fa">&#xf014;</i>`;

                $(`.event-container[role='button']`)[0].style.zIndex = 10;

                // Append the delete buttons to the parent div
                eventElement.appendChild(deleteButton);

                // Add an attribute to let the element know if the button already exists
                eventElement.dataset.deleteButtonAdded = true;
            };
        };
    };
};


// --------------------------------------------------------------------------------------------
// Function to create a `Add event` button. Execution varies depending on the user roles
// --------------------------------------------------------------------------------------------
function insertAddEventButton() {

    // Check if an event-container exists for the event header
    var eventHeaderContainer =  $(`.calendar-events`);

    // Flag for checking the button exists
    var addButtonAdded = eventHeaderContainer.data('addButtonAdded'); 

    if (!addButtonAdded) {
        // Header Element for existing event
        var eventHeaderElement = eventHeaderContainer[0];
        
        // Include an event Add button
        var addButton = document.createElement('button');
        addButton.id = ("addBtn");
        addButton.className = `addEventButtons`;
        addButton.innerHTML = `<i style="font-size:60px" class="fa-solid fa-plus"></i>`;

        // Append the Add buttons to the header div
        eventHeaderElement.appendChild(addButton);

        // Set the flag to indicate that the button has been added
        eventHeaderContainer.data('addButtonAdded', true);
    };
};

// --------------------------------------------------------------------------------------------
// Function to make sure that new events can only be added on the current or future dates
// --------------------------------------------------------------------------------------------
function qualityCheckAddBtn() {
    // Close the form if it has the "open" class
    if ($('.bookingForm').hasClass('open')) {
        $('.bookingForm').removeClass('open');
    }

    // Disable the add event button for dates older than today
    var check_date = new Date($('#calendar').evoCalendar('getActiveDate'));

    // Change the hours of both dates to midnight
    check_date.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // Perform the comparison with if statement
    if (user_roles === 'SalonAdmin' || user_roles === 'SalonStylist' || user_roles === 'SalonUser') {
        if (check_date >= today) {
            var buttonIndicator = document.getElementById('addBtn');
            if (buttonIndicator) {
                // Remove the data attributes from the calendar events
                $(`.calendar-events`).removeData('addButtonAdded');
                // Remove the pre-existing button
                buttonIndicator.remove();
                // Add a new button
                insertAddEventButton();
                $("#addBtn").prop("disabled", false);
            } else {
                insertAddEventButton();
                $("#addBtn").prop("disabled", false);
            };
        
        } else {
            var buttonIndicator = document.getElementById('addBtn');
            if (buttonIndicator) {
                // Remove the data attributes from the calendar events
                $(`.calendar-events`).removeData('addButtonAdded');
                // Remove the pre-existing button
                buttonIndicator.remove();
                // Add a new button
                insertAddEventButton();
                $("#addBtn").prop("disabled", true);
            } else {
                insertAddEventButton();
                $("#addBtn").prop("disabled", true);
            };
        };
    };


    // --------------------------------------------------------------------------------------------
    // Event Listener to allow functionality to identify booked timeslots on the Calendar
    // --------------------------------------------------------------------------------------------
    document.getElementById('addBtn').onclick = function (e) {
        // Make the form element visible
        $('.bookingForm').toggleClass('open');

        // Clear the form input
        $('.bookingForm')[0].reset();

        // Select the date of interest - Perform get request to blank out times that have been selected for that day
        var doi = $("#calendar").evoCalendar('getActiveDate').replace("/", "-").replace("/", "-")
        fetch("/appointments/" + doi, {
            // method type
            method: 'GET',
            // specify the data type as json so the server understands how to read it
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json())
            .then(data => {
                // Update the form options to show only available time slots
                updateFormOptions(data);
            }).catch(error => {
                console.error('Error fetching available times:', error);
            });
    };
};



// --------------------------------------------------------------------------------------------
// Function to modify the dropdown of available times to exclude booked slots.
// --------------------------------------------------------------------------------------------
function updateFormOptions(data) {
    // Assuming you have a <select> element with the class 'time_availability'
    var selectElement = document.getElementsByClassName('time_availability')[0];

    // Extract all timeslots that should be displayed and unavailable time slots
    var allTimes = data.all_times;
    var unavailable = data.booked_times;

    // Clear existing options
    selectElement.innerHTML = '';

    // Populate options based on availableTimes with an js version of enumerate
    allTimes.forEach(time => {
        var option = document.createElement('option');
        option.value = time;
        option.textContent = time;
        if (unavailable.includes(time)) {
            option.disabled = true;
        }
        selectElement.appendChild(option);
    });
};




// --------------------------------------------------------------------------------------------------------------
// Event Listener to enable functionality that will include dynamic add, edit, and delete buttons to the Calendar
// ---------------------------------------------------------------------------------------------------------------

// ------------------------------------ Update the annual view ------------------------------------
$("#calendar").on('click', '.calendar-year', function (e) {
    // Select the first day of the new month & year from the day element and make it active
    firstDayOfMonth = $(".day")["0"].getAttribute('data-date-val');
    $('#calendar').evoCalendar('selectDate', firstDayOfMonth);

    // Update the add event button
    if (user_roles === 'SalonAdmin' || user_roles === 'SalonStylist' || user_roles === 'SalonUser') {
        qualityCheckAddBtn();
    };

    // Update the daily event count on the visible calendar
    updateDailyAppointmentsCalendarView();

    // Insert an edit and delete button
    insertEditEventButton();
    insertDeleteEventButton();
});


// ------------------------------------ Update the monthly view ------------------------------------
$("#calendar").on('click', '.month', function (e) {
    // Select the first day of the new month from the day element and make it active
    firstDayOfMonth = $(".day")["0"].getAttribute('data-date-val');
    $('#calendar').evoCalendar('selectDate', firstDayOfMonth);

    // Update the add event button
    if (user_roles === 'SalonAdmin' || user_roles === 'SalonStylist' || user_roles === 'SalonUser') {
        qualityCheckAddBtn();
    };

    // Update the daily event count on the visible calendar
    updateDailyAppointmentsCalendarView();

    // Insert an edit and delete button
    insertEditEventButton();
    insertDeleteEventButton();
});


// --------------------------------- Update the daily view on the sidebar ---------------------------------
$('#calendar').on('click', '.calendar-day', function() {
    // $(this)[0] // - Print the active div from the listener

    // Update the add event button
    if (user_roles === 'SalonAdmin' || user_roles === 'SalonStylist' || user_roles === 'SalonUser') {
        qualityCheckAddBtn();
    };

    // Update the daily event count on the visible calendar
    updateDailyAppointmentsCalendarView();

    // Insert an edit and delete button
    insertEditEventButton();
    insertDeleteEventButton();
});


// ---- Function to update daily booking numbers for visible number of days in calendar body ----
function updateDailyAppointmentsCalendarView() {
    // Get the list of active events for the day of interest
    var currentActiveDate = $("#calendar").evoCalendar('getActiveDate');
    
    // Loop over all the visible calendar days that are accessed from a NodeList
    document.querySelectorAll('.calendar-day').forEach(function(dateDiv) {
        // Get the date string of each visible day div
        var dateString = dateDiv.querySelector(".day").getAttribute('data-date-val');
        // Make that day active and count the number of visible events
        $('#calendar').evoCalendar('selectDate', dateString);
        var allActiveEvents = $('#calendar').evoCalendar('getActiveEvents');

        // Syntax to check if the event-indicator span exists in the .calendar-day div
        var eventIndicator = dateDiv.querySelector('.event-indicator');

        // Change the value of the event-indicator span
        if (allActiveEvents.length > 0) {
            dateDiv.querySelector('.event-indicator').textContent = allActiveEvents.length;
        } else if (allActiveEvents.length === 0 && eventIndicator) {
            eventIndicator.remove();
        };
    });

    // After updating the list, change the active date back to what it was 
    $('#calendar').evoCalendar('selectDate', currentActiveDate);
};
// --------------------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------------------


// ----------------------------------------------------------------------------------------------
// Event listener that DELETEs the form on click. It also dynamically updates the frontend
// ----------------------------------------------------------------------------------------------
$('#calendar').on('click', '.deleteEventButtons', function(e) {
    // Get the list of active events for the day of interest
    var allActiveEvents = $('#calendar').evoCalendar('getActiveEvents');

    // Get the event id from the parent node of the button
    var evoId = e.target.parentNode.className.split(" ")[1];
    var eventId = evoId.split("_")[1];

    // Find the active event with a matching id from the list of active events
    var activeEvent = allActiveEvents.find(function(listEvent) {
        return listEvent.id === evoId;
    });

    // Implement the asynchronous fetch
    fetch("/appointments/book/" + eventId, {
        // method type. Delete request has no body
        method: 'DELETE',
        // specify the data type as json so the server understands how to read it
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json())
    .then(data => {
        // Remove the old event from the calendar
        $("#calendar").evoCalendar("removeCalendarEvent", evoId);

        // Update the add event button
        qualityCheckAddBtn();

        // Update the daily event count on the visible calendar
        updateDailyAppointmentsCalendarView();

        // Update the calendars view
        insertEditEventButton();
        insertDeleteEventButton();
    
    }).catch(error => {
        console.error('Error during delete request:', error);
    });
});


// -------------------------------------- PATCH AND POST ---------------------------------------
// ----------------------------------------------------------------------------------------------
// Event listener that updates the form prior to performing a PATCH update to an existing booking
// ----------------------------------------------------------------------------------------------
$('#calendar').on('click', '.editEventButtons', function(e) {
    editMode = true;

    // Get the list of active events for the day of interest
    var allActiveEvents = $('#calendar').evoCalendar('getActiveEvents');

    // Get the event id from the parent node of the button
    var evoId = e.target.parentNode.className.split(" ")[1];
    var eventId = evoId.split("_")[1];

    // Find the active event with a matching id from the list of active events
    var activeEvent = allActiveEvents.find(function(listEvent) {
        return listEvent.id === evoId;
    });
    
    // Toggle on the form with the display
    $('.bookingForm').toggleClass('open');

    // var editForm = $('.bookingForm')[0];
    // var formStyle = getComputedStyle(editForm).getPropertyValue("display");
    // if (formStyle === 'none') {
    //     // Hide the form after booking the appointment
    //     $('.bookingForm').toggleClass('open');
    // }
    
    // Attach the event id to the form's dataset
    $('.bookingForm')[0].dataset.evoId =  evoId;
    $('.bookingForm')[0].dataset.event_id =  eventId;

    // Event description that contains first and last names
    var activeEventDesc = activeEvent['description'];

    // Update the prexisting values of the form that is being edited
    // ----------------------------------------------------------------------------------------
    document.getElementById('firstName').value = activeEventDesc.split(' ')[4];
    document.getElementById('lastName').value = activeEventDesc.split(' ')[5];
    document.getElementsByClassName('bookPhoneNum')[0].value = activeEvent.phone;
    document.getElementsByClassName('bookEmail')[0].value = activeEvent.email;
    // Update the available times in the form while ensuring the previous appointment time
    // is not blocked off. Start with selecting the date of interest
    var doi = $("#calendar").evoCalendar('getActiveDate').replace("/", "-").replace("/", "-")
    fetch("/appointments/" + doi, {
        // method type
        method: 'GET',
        // specify the data type as json so the server understands how to read it
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json())
        .then(data => { // booked Time Slots
            // Find the index of the previous time slot and remove it from disabled time slots
            previousBookingIndex = data.booked_times.indexOf(activeEvent.time);
            data.booked_times.splice(previousBookingIndex, 1);
            // Update the form options to show only available time slots
            updateFormOptions(data);
            // Define the active option that's available
            document.getElementsByClassName('time_availability')[0].value = activeEvent.time;
        }).catch(error => {
            console.error('Error updating available times:', error);
        });
    
    // Update the booking submit button text
    $('.submitBooking')[0].textContent = 'Modify Booking';
});

// --------------------------------------------------------------------------------------------
// Event Listener to allow PATCH and POST functionality for an existing/new event in the Calendar
// --------------------------------------------------------------------------------------------
document.getElementsByClassName('bookingForm')[0].onsubmit = function (e) {
    e.preventDefault();
    // Extract the items from the form
    var firstName = document.getElementById('firstName').value
    var lastName = document.getElementById('lastName').value
    var phoneNum = document.getElementsByClassName('bookPhoneNum')[0].value
    var emailAdd = document.getElementsByClassName('bookEmail')[0].value
    var actDate = $("#calendar").evoCalendar('getActiveDate').replace("/", "-").replace("/", "-")
    var selectedTime = document.getElementsByClassName('time_availability')[0].value
    var dateTime = actDate + " " + selectedTime;


    if (editMode) {
        var evoId = $('.bookingForm')[0].dataset.evoId;         // Id for evo calendar with random string appended
        var eventId = $('.bookingForm')[0].dataset.event_id;    // Id for psql db as incrementing integers

        // Implement the asynchronous fetch
        fetch("/appointments/book/" + eventId, {
            // method type
            method: 'PATCH',
            // json formatted string from the form input
            body: JSON.stringify({
                'first_name': firstName,
                'last_name': lastName,
                'phone': phoneNum,
                'email': emailAdd,
                'start_time': dateTime
            }),
            // specify the data type as json so the server understands how to read it
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json())
        .then(data => {
            // Remove the old event from the calendar
            $("#calendar").evoCalendar("removeCalendarEvent", evoId);

            // Insert the new event from the response
            var addEvent = {
                id: rtg + "_" + data.event[0].id,
                name: data.event[0].name,
                date: data.event[0].date,
                color: colorArray[getRandom(colorArray.length)],
                description: data.event[0].description,
                type: data.event[0].type,
                phone: data.event[0].phone,
                email: data.event[0].email,
                time: data.event[0].time,
                verified: true
            };
            // Update the calendar with the latest event
            $("#calendar").evoCalendar('addCalendarEvent', [addEvent]);

            // Update the add event button
            qualityCheckAddBtn();

            // Update the daily event count on the visible calendar
            updateDailyAppointmentsCalendarView();

            // Update the calendars view
            insertEditEventButton();
            insertDeleteEventButton();

            // Update the booking submit button text
            $('.submitBooking')[0].textContent = 'Book';
        }).catch(error => {
            console.error('Error modifying appointment:', error);
        });

        // After editing, switch off the edit mode
        editMode = false;



    } else {


        // Implement the asynchronous fetch to POST an event to the db
        fetch("/appointments/book", {
            // method type
            method: 'POST',
            // json formatted string from the form input
            body: JSON.stringify({
                'first': firstName,
                'last': lastName,
                'phone': phoneNum,
                'email': emailAdd,
                'date_time': dateTime
            }),
            // specify the data type as json so the server understands how to read it
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json())
            .then(data => {

                var addEvent = {
                    id: rtg + "_" + data.event[0].id,
                    name: data.event[0].name,
                    date: data.event[0].date,
                    color: colorArray[getRandom(colorArray.length)],
                    description: data.event[0].description,
                    type: data.event[0].type,
                    phone: data.event[0].phone,
                    email: data.event[0].email,
                    time: data.event[0].time,
                    verified: true
                };
                // Update the calendar with the latest event
                $("#calendar").evoCalendar('addCalendarEvent', [addEvent]);

                // Update the add event button
                qualityCheckAddBtn();

                // Update the daily event count on the visible calendar
                updateDailyAppointmentsCalendarView();

                // Update the calendars view
                insertEditEventButton();
                insertDeleteEventButton();

            }).catch(error => {
                console.error('Error creating new appointment:', error);
            });
    }

    // Hide the form after booking the appointment
    $('.bookingForm').toggleClass('open');  
};