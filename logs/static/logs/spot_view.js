

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
        document.getElementById("lower_header").innerHTML = "Sessions";
    }
    else {
        document.getElementById("session_table").style.display = "none";
        document.getElementById("report_table").style.display = "block";
        document.getElementById("lower_header").innerHTML = "Reports";
    }
}
