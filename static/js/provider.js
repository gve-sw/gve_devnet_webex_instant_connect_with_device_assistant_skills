function logout() {
    console.log("logging out..");
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/login'
        }
    }
    var url = "/provider/logout";
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}

function login() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/provider/home'
        }

        if (this.readyState == 4 && this.status == 401) {
            var error = document.getElementById("error-text");
            error.innerText = JSON.parse(xmlHttp.responseText)['error'];
        }
    }
    var url = "/provider/login";
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    }));
}

function schedule() {
    document.getElementById("schedule-button").disabled = true;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/provider/appointments';
        }
    }
    var url = "/teleconsultCreate";
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        type: "provider",
        patient: document.getElementById("patient").value,
        appointment_time: document.getElementById("time").value,
        date: document.getElementById("date").value
    }));
}

function allPatients() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var select = document.getElementById("patient");
            var data = JSON.parse(this.responseText);
            var length = Object.keys(data).length;

            for (var i = 0; i < length; i++) {
                var option = document.createElement("option");
                var name = data[i]['first_name'] + ' ' + data[i]['last_name'];
                option.text = name;
                option.value = data[i]['_id'];
                select.appendChild(option);
            }
        }
    }
    var url = "/patient/all";
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}

function appointmentTimes() {
    var time = document.getElementById("time");

    for (var i = 9; i < 12; i++) {
        var option = document.createElement("option");
        option.text = String(i) + ':00 AM EST';
        option.value = i;
        time.appendChild(option);
    }
    var noon = document.createElement("option");
    noon.text = String(12) + ':00 PM EST';
    noon.value = 12;
    time.appendChild(noon);
    for (var i = 1; i <= 5; i++) {
        var option = document.createElement("option");
        option.text = String(i) + ':00 PM EST';
        option.value = i+12;
        time.appendChild(option);
    }
}