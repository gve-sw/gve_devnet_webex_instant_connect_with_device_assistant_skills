window.onload = function() {
    getPatients("/admin/allPatients");
};

// GET the appointments stored in the DB and build a table to display
function getPatients(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    
    var data = JSON.parse(xmlHttp.responseText);
    var length = Object.keys(data).length;
    var tbody = document.getElementById("table-body");

    for (var i = 0; i < length; i++) {
        var row = document.createElement('tr');

        var firstName = data[i]['first_name'];
        var lastName = data[i]['last_name'];
        var nameTd = document.createElement('td');
        nameTd.innerHTML = firstName + ' ' + lastName;

        var email = data[i]['email'];
        var emailTd = document.createElement('td');
        emailTd.innerHTML = email;

        var phone = data[i]['phone_number'];
        var phoneTd = document.createElement('td');
        phoneTd.innerHTML = phone;

        var record = data[i]['record_number'];
        var recordTd = document.createElement('td');
        recordTd.innerHTML = record;


        row.appendChild(nameTd);
        row.appendChild(emailTd);
        row.appendChild(phoneTd);
        row.appendChild(recordTd);

        tbody.appendChild(row);
    }
}