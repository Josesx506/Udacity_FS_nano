var today = new Date();


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
                    id: slotEvent.id,
                    name: slotEvent.name,
                    date: slotEvent.date,
                    color: colorArray[getRandom(colorArray.length)],
                    description: slotEvent.description,
                    type: slotEvent.type,
                    everyYear: false
                };
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

$(document).ready(function () {
    $("#calendar").evoCalendar({
        format: "mm/dd/yyyy",//"MM dd, yyyy",
        theme: 'default',
        language: 'en',
        titleFormat: "MM",
        todayHighlight: false,
        sidebarToggler: false,
        eventListToggler: true,
        canAddEvent: true,
        // calendarEvents: []
    })

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
})


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



// --------------------------------------------------------------------------------------------
// Event Listener to enable functionality that will include dynamic add, edit, and delete buttons to the Calendar
// --------------------------------------------------------------------------------------------
$("#calendar").on('selectDate', function (event, newDate, oldDate) {

    // Check if an event-container exists for the selected date
    const eventContainer = $(`.event-container[role='button']`);
    
    if (eventContainer.length > 0) {
        
        // Your logic for handling the existence of an event-container goes here
        for (i=0;i<eventContainer.length; i++) {
            var element = eventContainer[i];

            // var eventId = element.getAttribute('data-event-index');
            
            // Add a Delete button
            var deleteButton = document.createElement('button');
            deleteButton.className = `deleteEventButtons`;
            // You can replace this with an "x-icon" HTML or use an image
            deleteButton.innerHTML =  `<i style="font-size:24px" class="fa">&#xf014;</i>`;

            // Add an Event button
            var editEventButton = document.createElement('button');
            editEventButton.className = `editEventButtons`;
            editEventButton.innerHTML = `<i style="font-size:24px" class="far fa-edit"></i>`;

            // Append the delete and edit buttons to the parent div
            element.appendChild(deleteButton);
            element.appendChild(editEventButton);
        }
    };

    // Include an add event button 
    var eventHeaderContainer =  $(`.calendar-events`);
    // Flag for checking the button exists
    var addButtonAdded = eventHeaderContainer.data('addButtonAdded'); 

    if (!addButtonAdded) {

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
    console.log()

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

    // Hide the form after booking the appointment
    $('.bookingForm').toggleClass('open');
};


// function showPopupForm() {
//     // document.getElementById('popupForm').style.display = 'block';
//     var curDate = $("#calendar").evoCalendar('getActiveDate').split("/"); // date format is mm/dd/yyyy
//     var fillDatetime = curDate[2] + "-" + curDate[0] + "-" + curDate[1] + "T" + "09:00:00";
//     // Get the first item of from the class
//     document.getElementsByClassName('bookDateTime')[0].value = fillDatetime;
// }

// function hidePopupForm() {
//     document.getElementById('popupForm').style.display = 'none';
// }