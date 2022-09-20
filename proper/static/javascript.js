var login = async function() {
    console.log("hei")

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    let request = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            password: password

        }),
    });
    if (request.status === 200) {
        document.getElementById('appdiv').style.display = "block"
        document.getElementById('loginform').style.display = "none"

        getData();
    }

}
var logout = async function() {
    let response = await fetch("/logout", { method: "GET" });
    document.getElementById('appdiv').style.display = "none"
    document.getElementById('loginform').style.display = "block"

}

var getData = async function() {
    console.log("her")
    let request = await fetch("/contacts")
    if (request.status === 200) {
        let data = await request.json();
        console.log(data);
        listContacts2(data)
    }
}

var Contact = function(name, email, phone) {
    this.name = name;
    this.email = email;
    this.phone = phone;
}



var contacts = [];
//contacts.push(new Contact("Petter", "Petter@gmail.com", "472 489 01"));
//contacts.push(new Contact("Thomas", "Thomas@gmail.com", "472 489 02"));

var listContacts2 = function(data) {
    document.getElementById('displayContacts').innerHTML = " ";
    for (var i = 0; i < data.length; i++) {
        document.getElementById('displayContacts').innerHTML += '<tr id=' + data[i].id + '><td>' + data[i].name + '</td><td><a href="mailto:' + data[i].email + '">' + data[i].email + '</a></td><td>' + data[i].phone + '</td><td><button onclick=editContact(' + i + ')>Edit</button></div><button onclick=deleteContact(' + i + ')>Delete</button></td></tr>';
    }
}

var listContacts = function() {
    document.getElementById('displayContacts').innerHTML = " ";
    for (var i = 0; i < contacts.length; i++) {
        document.getElementById('displayContacts').innerHTML += '<tr><td id="name' + i + '">' + contacts[i].name + '</td><td id="email' + i + '"><a href="mailto:' + contacts[i].email + '">' + contacts[i].email + '</a></td><td id="phone' + i + '">' + contacts[i].phone + '</td><td><button onclick=editContact(' + i + ')>Edit</button></div><button onclick=deleteContact(' + i + ')>Delete</button></td></tr>';
    }
}

var addNewContact = async function() {
    var name = document.getElementById('inputName').value;
    var email = document.getElementById('inputEmail').value;
    var phone = document.getElementById('inputPhone').value;
    var validateionPatternEmail = /^[^ ]+@[^ ]+.[a-z]{2,3}$/;
    var validateionPatternTel = /^[0-9 ()+-]+$/;

    if (!(name == "") && email.match(validateionPatternEmail) || phone.match(validateionPatternTel)) {

        let request = await fetch("/contacts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name,
                email: email,
                phone: phone,

            }),
        });
        if (request.status === 200) {
            document.getElementById('appdiv').style.display = "block"

            getData();
        }

    } else if (name == "") {
        window.alert("Input name")
    } else if (!(email.match(validateionPatternEmail)) && (!(email == ""))) {
        window.alert("Input valid email")

    } else if (!(phone.match(validateionPatternTel)) && (!(phone == ""))) {
        window.alert("Input valid phonenumber")
    } else {
        window.alert("Input either email or phone number")
    }

}

var deleteContact = async function(i) {
    if (confirm("Are you sure you want to delete?") == true) {

        let table = document.getElementById("displayContacts");
        console.log(table.children[i].firstChild);
        let contactid = table.children[i].firstChild.id
        let url = ("/contacts/" + contactid)
        let response = await fetch(url, {
            method: "DELETE"
        });
        if (response.status === 200) {


            getData();
        }
        //contacts.splice(i, 1);
        //listContacts();
    }
}

var editContact = async function(i) {
        let table = document.getElementById("displayContacts");


        var name = document.getElementById('inputName').value;
        var email = document.getElementById('inputEmail').value;
        var phone = document.getElementById('inputPhone').value;
        console.log("yo");

        console.log(table.children[i].firstChild);

        let contactid = table.children[i].firstChild.id

        let url = ("/contacts/" + contactid)
        let request = await fetch("url", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name,
                email: email,
                phone: phone,

            }),
        });
    }
    /*
    contactId = i;
    document.getElementById("inputName").value = contacts[i].name;
    document.getElementById("inputEmail").value = contacts[i].email;
    document.getElementById("inputPhone").value = contacts[i].phone;
    document.getElementById("submitButtons").innerHTML = '<button id="updateButton" onclick=submitEditedContact(contactId)>Submit</button>';
    */


var submitEditedContact = function(i) {
    contacts[i].name = document.getElementById("inputName").value;
    contacts[i].email = document.getElementById("inputEmail").value;
    contacts[i].phone = document.getElementById("inputPhone").value;

    document.getElementById("inputName").value = "";
    document.getElementById("inputEmail").value = "";
    document.getElementById("inputPhone").value = "";

    listContacts2();
}

function inputValidation() {

    var name = document.getElementById('inputName').value;
    var email = document.getElementById('inputEmail').value;
    var phone = document.getElementById('inputPhone').value;
    var validateionPatternEmail = /^[^ ]+@[^ ]+.[a-z]{2,3}$/;
    var validateionPatternTel = /^[0-9 ()+-]+$/;

    if (!(name == "") && email.match(validateionPatternEmail) || phone.match(validateionPatternTel)) {

    }
}


function searchFun() {
    var input, filter, found, table, tr, td, i, j;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("displayContacts");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
                found = true;
            }
        }
        if (found) {
            tr[i].style.display = "";
            found = false;
        } else {
            tr[i].style.display = "none";
        }
    }
}



listContacts();