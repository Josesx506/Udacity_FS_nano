var today = new Date();

var active_events = [];

// let events = [
//     {
//         id: 'event-1',
//         name: 'Event 1',
//         datetime: '2023-12-31T10:30:00', // ISO 8601 format (replace with your desired date and time)
//     },
//     {
//         id: 'event-2',
//         name: 'Event 2',
//         datetime: '2023-12-31T15:45:00', // ISO 8601 format (replace with your desired date and time)
//     },
// ];

var events = [ {
    id: "imwyx6S",
    name: "Event #3",
    description: "Lorem ipsum dolor sit amet.",
    date: today.getMonth() + 1 + "/18/" + today.getFullYear(),
    type: "event"
}, {
    id: "9jU6g6f",
    name: "Holiday #1",
    description: "Lorem ipsum dolor sit amet.",
    date: today.getMonth() + 1 + "/10/" + today.getFullYear(),
    time: '2023-12-31T10:30:00',
    type: "holiday"
}, {
    id: "d8jai7s",
    name: "Author's Birthday",
    description: "Author's note: Thank you for using EvoCalendar! :)",
    date: "December/25/2023",
    type: "birthday",
    everyYear: !0
}, {
    id: "in8bha4",
    name: "Holiday #2 " + today.getFullYear(),
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    date: today,
    type: "holiday"
}, {
    id: "in8bha4",
    name: "Event #2",
    date: today,
    type: "event"
}];

$(document).ready(function() {
    $("#calendar").evoCalendar({
        format: "mm/dd/yyyy",//"MM dd, yyyy",
        theme: 'default',
        language: 'en',
        titleFormat: "MM",
        todayHighlight: true,
        sidebarToggler: true,
        eventListToggler: true,
        canAddEvent: true,
        calendarEvents: events
    })

    // $("#addBtn").click(function(a) {
    //     curAdd = getRandom(events.length);
    //     $("#calendar").evoCalendar("addCalendarEvent", events[curAdd]);
    //     active_events.push(events[curAdd]);
    //     events.splice(curAdd, 1);
    //     if (0 === events.length) {
    //         a.target.disabled = true;
    //     }
    //     if (active_events.length > 0) {
    //         $("#removeBtn").prop("disabled", false);
    //     }
    // });
    $("#removeBtn").click(function(a) {
        curRmv = getRandom(active_events.length);
        $("#calendar").evoCalendar("removeCalendarEvent", active_events[curRmv].id);
        events.push(active_events[curRmv]);
        active_events.splice(curRmv, 1);
        if (0 === active_events.length) {
            a.target.disabled = true;
        }
        if (events.length > 0) {
            $("#addBtn").prop("disabled", false);
        }
    });

    function getRandom(a) {
        return Math.floor(Math.random() * a);
    }

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

document.getElementById('addBtn').onclick = function(e) {
    // Use this line to prevent the default page refresh each time there is an update
    e.preventDefault();

    // Show the booking form
    showPopupForm();
};

document.getElementsByClassName('bookingForm').onsubmit = function(e) {
    e.preventDefault();

    // Implement the asynchronous fetch
    fetch("/appointments/book", {
        // method type
        method: 'POST',
        // json formatted string from the form input
        body: JSON.stringify({'first': document.getElementById('firstName').value,
                                'last': document.getElementById('lastName').value,
                                'phone': document.getElementsByClassName('bookPhoneNum')[0].value,
                                'email': document.getElementsByClassName('bookEmail')[0].value,
                                'date_time': document.getElementsByClassName('bookDateTime')[0].value}),
        // specify the data type as json so the server understands how to read it
        headers: {'Content-Type': 'application/json'}
    })

    // Process form submission logic here
    hidePopupForm();
};

function showPopupForm() {
    document.getElementById('popupForm').style.display = 'block';
    var curDate = $("#calendar").evoCalendar('getActiveDate').split("/"); // date format is mm/dd/yyyy
    var fillDatetime = curDate[2] + "-" + curDate[0] + "-" + curDate[1] + "T" + "09:00:00";
    // Get the first item of from the class
    document.getElementsByClassName('bookDateTime')[0].value = fillDatetime;
}

function hidePopupForm() {
    document.getElementById('popupForm').style.display = 'none';
}