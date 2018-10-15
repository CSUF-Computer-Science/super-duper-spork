'use strict';

function hideAddItem() {
        var addItemDiv = document.getElementById("add_item").style;
    addItemDiv.display = (addItemDiv.display === "none") ? "block" : "none";
}