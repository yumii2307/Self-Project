var today = new Date();
var date = new Date();

function buildCalendar() {
    var doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    var lastDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    var tbCalendar = document.getElementById("calendar");
    var tbCalendarYM = document.getElementById("tbCalendarYM");
    tbCalendarYM.innerHTML = today.getFullYear() + "년 " + (today.getMonth() + 1) + "월";

    while (tbCalendar.rows.length > 1) {
        tbCalendar.deleteRow(tbCalendar.rows.length - 1);
    }

    var row = null;
    row = tbCalendar.insertRow();

    var cnt = 0;

    var prevMonthLastDate = new Date(today.getFullYear(), today.getMonth(), 0).getDate();
    for (i = doMonth.getDay() - 1; i >= 0; i--) {
        cell = row.insertCell();
        cell.innerHTML = prevMonthLastDate - i;
        cell.style.color = "#A9A9A9";
        cnt = cnt + 1;
    }

    for (i = 1; i <= lastDate.getDate(); i++) {
        cell = row.insertCell();
        cell.innerHTML = i;
        cnt = cnt + 1;
        if (cnt % 7 == 1) {
        cell.innerHTML = "<font color=#ed2a61>" + i;
        }
        if (cnt % 7 == 0) {
        cell.innerHTML = "<font color=#3c6ffa>" + i;
        row = tbCalendar.insertRow();
        }
        if (today.getFullYear() == date.getFullYear() && today.getMonth() == date.getMonth() && i == date.getDate()) {
        cell.bgColor = "#ddd";
        }
    }

    var nextMonthStartDay = row.cells.length % 7;
    if (nextMonthStartDay < 7) {
        for (i = 1; i <= 7 - nextMonthStartDay; i++) {
        cell = row.insertCell();
        cell.innerHTML = i;
        cell.style.color = "#A9A9A9";
        }
    }
}

function prevCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    buildCalendar();
}

function nextCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
    buildCalendar();
}