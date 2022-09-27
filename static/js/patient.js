function logout() {
    console.log("logging out..");
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/login'
        }
    }
    var url = "/patient/logout";
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}

function login() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/patient/home'
        }

        if (this.readyState == 4 && this.status == 401) {
            var error = document.getElementById("error-text");
            error.innerText = JSON.parse(xmlHttp.responseText)['error'];
        }
    }
    var url = "/patient/login";
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
            window.location = '/patient/appointments';
        } else {
            console.log(this.status)
        }
    }
    var url = "/teleconsultCreate";
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        type: 'patient',
        provider: document.getElementById("provider").value,
        appointment_time: document.getElementById("time").value,
        date: document.getElementById("date").value
    }));
}

function allProviders() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var select = document.getElementById("provider");
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
    var url = "/provider/all";
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}

function addNotes() {
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var success = document.getElementById("success-text");
            success.innerText = JSON.parse(xmlHttp.responseText)['success'];
        }
    }

    patient = document.getElementById("patient");
    var url = "/patient/notes/" + patient.textContent;

    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        notes: document.getElementById("patient_notes").value
    }));
}

function appointmentTimes() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("schedule-button").disabled = false;

            var time = document.getElementById("time");
            time.textContent = ''

            var data = JSON.parse(this.responseText);
            var length = Object.keys(data).length;

            if (length == 0) {
                document.getElementById("schedule-button").disabled = true;

                var option = document.createElement("option");
                option.text = 'No Available Appointments';
                option.value = -1;
                time.appendChild(option);

                return
            }

            console.log(data)

            for (var i = 0; i < length; i++){
                startTimeArr = data[i][0].split(':')
                endTimeArr = data[i][1].split(':')

                console.log(startTimeArr)
                console.log(endTimeArr)

                startHour = parseInt(startTimeArr[0])
                endHour = parseInt(endTimeArr[0])
    
                for (var j = startHour; j < endHour; j++) {
                    var option = document.createElement("option");

                    console.log(j)

                    if (j < 12) {
                        option.text = String(j) + ':00 AM EST';
                    } else if (j == 12) {
                        option.text = String(j) + ':00 PM EST';
                    } else {
                        option.text = String(j-12) + ':00 PM EST';
                    }

                    console.log(option)

                    option.value = j;
                    time.appendChild(option);
                }
            }
        }
    }

    var url = "/provider/free-time";
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        provider: document.getElementById("provider").value,
        date: document.getElementById("date").value
    }));
}