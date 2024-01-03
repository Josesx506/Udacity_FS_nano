var today = new Date();

// Assume the submit form is not in edit mode by default
var editMode = false; 

// Array of colors to be used
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


function getRandom(a) {
    return Math.floor(Math.random() * a);
}

// Random Text Generator as function
//Can change 7 to 2 for longer results.
let rtg = (Math.random() + 1).toString(36).substring(7);



// Place holder event for tests
// var events = [{
//     id: "imwyx6S",
//     name: "Event #3",
//     description: "Lorem ipsum dolor sit amet.",
//     date: today.getMonth() + 1 + "/18/" + today.getFullYear(),
//     type: "event"
// }]



// document.querySelector(`.calendar-events`).onclick = function (e){

//     var eventHeaderContainer =  document.querySelector(`.calendar-events`);
//     console.log('Ptr')
    
// }

// if (eventHeaderContainer.length > 0) {
    
// };





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
    })

    function updateCalendarView() {
        // $('#calendar').evoCalendar('removeEventList')

        var eventList = [];

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
                        time: slotEvent.time
                    };

                    // The values don't have to be appended to the list above
                    eventList.push(existingEvent);
                    
                    // Add the event to the calendar asynchronously
                    $('#calendar').evoCalendar('addCalendarEvent',existingEvent);
                })
            
            }).catch(error => {
                console.error('Error fetching available times:', error);
            });
        
        return eventList;
    }

    // The list of events as a global variable
    var events = updateCalendarView();

    // Initially set to none and will be updated with dynamic clicks below
    // var activeEventEvo; 

    


    

    // $("#removeBtn").click(function(a) {
    //     curRmv = getRandom(active_events.length);
    //     $("#calendar").evoCalendar("removeCalendarEvent", active_events[curRmv].id);
    //     events.push(active_events[curRmv]);
    //     active_events.splice(curRmv, 1);
    //     if (0 === active_events.length) {
    //         a.target.disabled = true;
    //     }
    //     if (events.length > 0) {
    //         $("#addBtn").prop("disabled", false);
    //     }
    // });



    // function updateCalendarEvents() {
    //     $('#calendar').evoCalendar('removeAllEvents');

    //     for (const event of events) {
    //         const datetime = new Date(event.datetime);

    //         $('#calendar').evoCalendar('addCalendarEvent', {
    //             id: event.id,
    //             name: event.name,
    //             date: datetime.toISOString().split('T')[0], // Extract the date part
    //             type: 'time',
    //             color: 'red', // Set your desired color
    //             description: datetime.toLocaleTimeString(), // Display time in the description
    //         });
    //     }
    // }
});


// function createDeleteButton() {
//     var active = $("#calendar").evoCalendar('getActiveDate');
//     document.querySelector('.day calendar-active[role="button"][data-date-val='${active}']').onclick = (e) {
//         // Use this line to prevent the default page refresh each time there is an update
//         e.preventDefault();
//         console.log('got you')
//     }
// };
// createDeleteButton();


// Assuming you have a common ancestor element that contains all the delete buttons
// Replace "commonAncestor" with the actual parent element that holds the delete buttons
// var commonAncestor = document;


// commonAncestor.addEventListener('click', function(event) {
//     // Check if the clicked element has the class "deleteEventButtons"
//     if (event.target.classList.contains('deleteEventButtons')) {
//         // Retrieve the event index from the data attribute
//         var eventId = event.target.dataset.eventIndex;

//         // Perform your delete request using the eventId
//         // Example: You can use fetch to send a DELETE request to your server
//         fetch(`/delete-event/${eventId}`, {
//             method: 'DELETE',
//             // Additional options if needed (headers, body, etc.)
//         })
//         .then(response => {
//             if (response.ok) {
//                 // Successful delete, you may want to update the UI accordingly
//                 console.log(`Event ${eventId} deleted successfully.`);
//             } else {
//                 // Handle errors if needed
//                 console.error(`Failed to delete event ${eventId}.`);
//             }
//         })
//         .catch(error => {
//             console.error('Error during delete request:', error);
//         });
//     }
// });

function insertEditEventButton(element) {
    // Function to add an edit button to an Event element
    
    // Extract the event id from the data-event-index attribute
    var eventId = element.getAttribute('data-event-index');

    // Add an Event button
    var editEventButton = document.createElement('button');
    editEventButton.className = `editEventButtons ${eventId}`;
    editEventButton.innerHTML = `<i style="font-size:28px" class="far fa-edit"></i>`;

    $(`.event-container[role='button']`)[0].style.zIndex = 10;

    // Append the edit buttons to the parent div
    element.appendChild(editEventButton);

    // Add an attribute to let the element know if the button already exists
    element.dataset.insertButtonAdded = true;
};

function insertDeleteEventButton(element) {
    // Function to add a delete button to an Event element

    // Extract the event id from the data-event-index attribute
    var eventId = element.getAttribute('data-event-index');
    
    // Add a Delete button
    var deleteButton = document.createElement('button');
    deleteButton.className = `deleteEventButtons ${eventId}`;
    // You can replace this with an "x-icon" HTML or use an image
    deleteButton.innerHTML =  `<i style="font-size:28px" class="fa">&#xf014;</i>`;

    $(`.event-container[role='button']`)[0].style.zIndex = 10;

    // Append the delete buttons to the parent div
    element.appendChild(deleteButton);

    // Add an attribute to let the element know if the button already exists
    element.dataset.deleteButtonAdded = true;
};

// --------------------------------------------------------------------------------------------
// Event Listener to enable functionality that will include dynamic add, edit, and delete buttons to the Calendar
// --------------------------------------------------------------------------------------------
$("#calendar").on('selectDate', function (event, newDate, oldDate) {

    // Check if an event-container exists for the selected date
    var eventContainer = $(`.event-container[role='button']`);
    
    if (eventContainer.length > 0) {
        // Your logic for handling the existence of an event-container goes here
        for (i=0;i<eventContainer.length; i++) {
            var eventElement = eventContainer[i];

            // Flag for checking the button exists before creating edit button
            var editButtonAdded = eventElement.dataset.insertButtonAdded; 
            if (!editButtonAdded) {
                insertEditEventButton(eventElement);
            };

            // Flag for checking the button exists before creating delete button
            var deleteButtonAdded = eventElement.dataset.deleteButtonAdded; 
            if (!deleteButtonAdded) {
                insertDeleteEventButton(eventElement);
            };

            
            // // Extract the event id from the data-event-index attribute
            // var eventId = element.getAttribute('data-event-index');
            
            // // Add a Delete button
            // var deleteButton = document.createElement('button');
            // deleteButton.className = `deleteEventButtons ${eventId}`;
            // // You can replace this with an "x-icon" HTML or use an image
            // deleteButton.innerHTML =  `<i style="font-size:28px" class="fa">&#xf014;</i>`;

            // // Add an Event button
            // var editEventButton = document.createElement('button');
            // editEventButton.className = `editEventButtons ${eventId}`;
            // editEventButton.innerHTML = `<i style="font-size:28px" class="far fa-edit"></i>`;

            // $(`.event-container[role='button']`)[0].style.zIndex = 10;

            // // Append the delete and edit buttons to the parent div
            // element.appendChild(deleteButton);
            // element.appendChild(editEventButton);

            // // 
            // element.data('insertButtonAdded', true);
        }
    };

    // Include an add event button 
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
    }

    // --------------------------------------------------------------------------------------------
    // Event Listener to allow functionality to identify booked timeslots on the Calendar
    // --------------------------------------------------------------------------------------------
    document.getElementById('addBtn').onclick = function (e) {
        $('.bookingForm').toggleClass('open');

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
    }


    // const evliContainer = document.querySelector(".event-container"); // Replace with the actual parent element selector
    // eventContainer.addEventListener("click", (event) => {
    //     const clickedButton = event.target.closest(".deleteEventButtons");
    //     if (clickedButton) {
    //         // Handle the clicked button here
    //         console.log("Clicked button:", clickedButton);

    //         // Perform actions specific to the clicked button, such as:
    //         clickedButton.remove(); // Example: Remove the clicked button
    //     }
    //     });


});


// Patch a pre-existing booking
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
    var editForm = $('.bookingForm')[0];
    var formStyle = getComputedStyle(editForm).getPropertyValue("display");
    if (formStyle === 'none') {
        // Hide the form after booking the appointment
        $('.bookingForm').toggleClass('open');
    }
    
    // Attach the event id to the form's dataset
    $('.bookingForm')[0].dataset.event_id =  eventId;

    // Event description that contains first and last names
    var activeEventDesc = activeEvent['description'];

    // Update the prexisting values of the form
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
            console.log(data);
            // Find the index of the previous time slot and remove it from disabled time slots
            previousBookingIndex = data.booked_times.indexOf(activeEvent.time);
            data.booked_times.splice(previousBookingIndex, 1);
            // Update the form options to show only available time slots
            updateFormOptions(data);
            // Define the active option that's available
            document.getElementsByClassName('time_availability')[0].value = activeEvent.time;
        }).catch(error => {
            console.error('Error fetching available times:', error);
        });
    // 
    
});




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

    // Populate options based on availableTimes
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




// --------------------------------------------------------------------------------------------
// Event Listener to allow POST functionality for an event to the Calendar
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
        var eventId = $('.bookingForm')[0].dataset.event_id;
        console.log("editing");
        console.log(eventId);
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
    });

        // After editing, switch off the edit mode
        editMode = false;
    } else {
        // Implement the asynchronous fetch
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
                    id: data.event[0].id,
                    name: data.event[0].name,
                    date: data.event[0].date,
                    color: colorArray[getRandom(colorArray.length)],
                    description: data.event[0].description,
                };
                // Update the calendar with the latest event
                $("#calendar").evoCalendar('addCalendarEvent', [addEvent]);
            }).catch(error => {
                console.error('Error fetching available times:', error);
            });
    }

    // Hide the form after booking the appointment
    $('.bookingForm').toggleClass('open');
    
};



