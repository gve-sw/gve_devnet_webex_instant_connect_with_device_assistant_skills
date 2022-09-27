window.onload = function() {
    getAppointments("/patient/my-appointments")
};

// GET the appointments stored in the DB and build a table to display
function getAppointments(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    console.log(xmlHttp.responseText);
    var data = JSON.parse(xmlHttp.responseText);
    var length = Object.keys(data).length;
    var tbody = document.getElementById("table-body");

    for (var i = 0; i < length; i++) {
        var row = document.createElement('tr');

        var appointment = data[i]["baseSubject"];
        var appointmentTd = document.createElement('td');
        appointmentTd.innerHTML = appointment;

        var date = data[i]["date"];
        var dateTd = document.createElement('td');
        dateTd.innerHTML = date;

        var time = data[i]["appointmentTime"];
        var timeVal = parseInt(time);
        if (timeVal > 12) {
            timeVal -= 12
            time = timeVal.toString();
            time += ":00 PM EST";
        } else if (timeVal == 12) {
            time += ":00 PM EST";
        } else {
            time += ":00 AM EST";
        }
        var timeTd = document.createElement('td');
        timeTd.innerHTML = time;

        var provider = data[i]["providerName"];
        var providerTd = document.createElement('td');
        providerTd.innerHTML = provider;

        var guestUrl = data[i]["guestUrl"];
        var guestJoinTd = document.createElement('td');
        var link = document.createElement('a');
        link.setAttribute("href", guestUrl);
        link.innerHTML = "Join Now";
        link.classList.add("btn");
        link.classList.add("btn--success");
        link.setAttribute('target', '_blank');
        guestJoinTd.appendChild(link);

        guestJoinTd.appendChild(link);

        row.appendChild(appointmentTd);
        row.appendChild(dateTd);
        row.appendChild(timeTd);
        row.appendChild(providerTd);
        row.appendChild(guestJoinTd);

        tbody.appendChild(row);
    }
}