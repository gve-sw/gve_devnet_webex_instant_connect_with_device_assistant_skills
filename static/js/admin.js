function logout() {
    console.log("logging out..");
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/login'
        }
    }
    var url = "/admin/logout";
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}

function login() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = '/admin/home'
        }

        if (this.readyState == 4 && this.status == 401) {
            var error = document.getElementById("error-text");
            error.innerText = JSON.parse(xmlHttp.responseText)['error'];
        }
    }
    var url = "/admin/login";
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    }));
}

function dashboard() {
    var date = document.getElementById("dateTime");

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();

    today = mm + '/' + dd + '/' + yyyy;
    date.innerHTML = today;
}