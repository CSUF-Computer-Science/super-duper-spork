

function validateForm() {
    'use strict';
    
    var password = document.getElementById('pwordInput').value;
    var pwordRegex = /test/;
    
    if (pwordRegex.test(password)) {
        var message = document.getElementById('incorrect_pword_msg');    
        message.style.color = "green";
        message.innerHTML = "Correct password format";  
        return true;
    } else {
        var message = document.getElementById('incorrect_pword_msg');    
        message.style.color = "red";
        message.innerHTML = "Incorrect password format";  
        return false;
    }
}