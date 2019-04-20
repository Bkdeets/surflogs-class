
function filter_click(id) {
    if(id=="session") {
        filter(true)
    }
    else{
        filter(false)
    }
}

function filter(isSession) {
    if(isSession) {
        document.getElementById("session_table").style.display = "block";
        document.getElementById("report_table").style.display = "none";
        document.getElementById("session_button").style.backgroundColor = "lightgray";
        document.getElementById("report_button").style.backgroundColor = "white";
    }
    else {
        document.getElementById("session_table").style.display = "none";
        document.getElementById("report_table").style.display = "block";
        document.getElementById("report_button").style.backgroundColor = "lightgray";
        document.getElementById("session_button").style.backgroundColor = "white";

    }
}
