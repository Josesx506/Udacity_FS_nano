var today = new Date();

var active_events = [];

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

function getRandom(a) {
    return Math.floor(Math.random() * a);
}

$(document).ready(function() {
    $("#calendar").evoCalendar({
        format: "mm/dd/yyyy",//"MM dd, yyyy",
        theme: 'default',
        language: 'en',
        titleFormat: "MM",
        todayHighlight: false,
        sidebarToggler: false,
        eventListToggler: false,
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

// Modify the dropdown of available times to exclude booked slots.
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
  }

document.getElementById('addBtn').onclick = function(e) {
    // Use this line to prevent the default page refresh each time there is an update
    e.preventDefault();

    // Show the booking form
    $('.bookingForm').toggleClass('open');

    // Select the date of interest - Perform get request to blank out times that have been selected for that day
    var doi = $("#calendar").evoCalendar('getActiveDate').replace("/","-").replace("/","-")
    fetch("/appointments/"+doi, {
        // method type
        method: 'GET',
        // specify the data type as json so the server understands how to read it
        headers: {'Content-Type': 'application/json'}
    }).then(response => response.json())
    .then(data => {
        // Update the form options to show only available time slots
        updateFormOptions(data);
    }).catch(error => {
      console.error('Error fetching available times:', error);
    });

    // Fill the date with the active date
    // var curDate = $("#calendar").evoCalendar('getActiveDate').split("/"); // date format is mm/dd/yyyy
    // var fillDatetime = curDate[2] + "-" + curDate[0] + "-" + curDate[1] + "T" + "09:00:00";
    // Get the first item of from the class
    // document.getElementsByClassName('bookDateTime')[0].value = fillDatetime;
    // showPopupForm();
};

document.getElementsByClassName('bookingForm')[0].onsubmit = function(e) {
    e.preventDefault();
    // Extract the items from the form
    var firstName =  document.getElementById('firstName').value
    var lastName = document.getElementById('lastName').value
    var phoneNum = document.getElementsByClassName('bookPhoneNum')[0].value
    var emailAdd = document.getElementsByClassName('bookEmail')[0].value
    var actDate = $("#calendar").evoCalendar('getActiveDate').replace("/","-").replace("/","-")
    var selectedTime = document.getElementsByClassName('time_availability')[0].value
    var dateTime = actDate + " " + selectedTime;
    console.log()

    // Implement the asynchronous fetch
    fetch("/appointments/book", {
        // method type
        method: 'POST',
        // json formatted string from the form input
        body: JSON.stringify({'first': firstName,
                                'last': lastName,
                                'phone': phoneNum,
                                'email': emailAdd,
                                'date_time': dateTime}),
        // specify the data type as json so the server understands how to read it
        headers: {'Content-Type': 'application/json'}
    })

    // Update the frontend with a new booking
    var apptTitle = "Hair Appointment";
    // var splitDateTime = dateTime.split('T') // Split the dates
    // var splitDate = splitDateTime[0].split('-');
    // var rearrangedDate = splitDate[1]+"/"+splitDate[2]+"/"+splitDate[0];
    var description = "<b>Time:</b> "+selectedTime+"\n"+"<b>Name:</b> "+firstName +" "+ lastName

    $("#calendar").evoCalendar('addCalendarEvent', [
        {
          id: 'skibo',
          name: apptTitle,
          date: actDate,
          color: colorArray[getRandom(colorArray.length)],
          description: description,
        }
    ]);
    
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