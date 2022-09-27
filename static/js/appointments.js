window.onload = function() {
    getAppointments("/getAppointments")
};

// GET the appointments stored in the DB and build a table to display
function getAppointments(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    
    var data = JSON.parse(xmlHttp.responseText);
    var length = Object.keys(data).length;
    var tbody = document.getElementById("table-body");

    console.log(data);

    for (var i = 0; i < length; i++) {
        var row = document.createElement('tr');

        var subject = data[i]['baseSubject'];
        var subjectTd = document.createElement('td');
        subjectTd.innerHTML = subject;

        var hostUrl = data[i]['hostUrl'];
        var hostTd = document.createElement('td');
        var aTagHost = document.createElement('a');
        aTagHost.setAttribute('href', hostUrl);
        aTagHost.innerText = "Host URL";
        aTagHost.setAttribute('target', '_blank');
        hostTd.appendChild(aTagHost);

        var agentUrl = data[i]['agentUrl'];
        var agentTd = document.createElement('td');
        var aTagAgent = document.createElement('a');
        aTagAgent.setAttribute('href', agentUrl);
        aTagAgent.innerText = "Host with forced login";
        aTagAgent.setAttribute('target', '_blank');
        agentTd.appendChild(aTagAgent);

        var guestUrl = data[i]['guestUrl'];
        var guestTd = document.createElement('td');
        var aTagGuest = document.createElement('a');
        aTagGuest.setAttribute('href', guestUrl);
        aTagGuest.innerText = "Guest URL";
        aTagGuest.setAttribute('target', '_blank');
        guestTd.appendChild(aTagGuest);

        var spaceUrl = data[i]['spaceUri'];
        var spaceTd = document.createElement('td');
        spaceTd.innerHTML = spaceUrl;

        var provider = data[i]['providerName'];
        var providerTd = document.createElement('td');
        providerTd.innerHTML = provider;

        var startTime = data[i]['appointmentTime'];
        var startTimeVal = parseInt(startTime);
        if (startTimeVal < 12) {
            startTime += ":00 AM EST";
        } else if (startTimeVal == 12) {
            startTime += ":00 PM EST";
        } else if (startTimeVal > 12) {
            startTimeVal -= 12;
            startTime = startTimeVal.toString() + ":00 PM EST";
        }
        var startTimeTd = document.createElement('td');
        startTimeTd.innerHTML = startTime;

        var patientId = data[i]['patientId'];
        var patientIdTd = document.createElement('td');
        patientIdTd.innerHTML = patientId;

        row.appendChild(subjectTd);
        row.appendChild(hostTd);
        row.appendChild(agentTd);
        row.appendChild(guestTd);
        row.appendChild(spaceTd);
        row.appendChild(providerTd);
        row.appendChild(startTimeTd);
        // row.appendChild(endTimeTd);
        row.appendChild(patientIdTd);

        tbody.appendChild(row);
    }
}