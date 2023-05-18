var today = new Date();
var date = new Date();

function buildCalendar() {
    var doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    var lastDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    var tbCalendar = document.getElementById("calendar");
    var tbCalendarYM = document.getElementById("tbCalendarYM");
    tbCalendarYM.textContent = today.getFullYear() + "년 " + (today.getMonth() + 1) + "월";

    while (tbCalendar.rows.length > 1) {
        tbCalendar.deleteRow(tbCalendar.rows.length - 1);
    }

    var row = tbCalendar.insertRow();
    var cnt = 0;
    var prevMonthLastDate = new Date(today.getFullYear(), today.getMonth(), 0).getDate();

    for (i = doMonth.getDay() - 1; i >= 0; i--) {
        cell = row.insertCell();
        cell.textContent = prevMonthLastDate - i;
        cell.style.color = "#A9A9A9";
        cnt = cnt + 1;
    }

    for (i = 1; i <= lastDate.getDate(); i++) {
        cell = row.insertCell();
        cell.textContent = i;
        cnt = cnt + 1;
        if (cnt % 7 == 1) {
            cell.style.color = "#ed2a61";
        }
        if (cnt % 7 == 0) {
            cell.style.color = "#3c6ffa";
            row = tbCalendar.insertRow();
        }
        if (today.getFullYear() == date.getFullYear() && today.getMonth() == date.getMonth() && i == date.getDate()) {
            cell.style.backgroundColor = "#ddd";
        }
    }

  var nextMonthStartDay = row.cells.length % 7;
    if (nextMonthStartDay < 7) {
        for (i = 1; i <= 7 - nextMonthStartDay; i++) {
          cell = row.insertCell();
          cell.textContent = i;
          cell.style.color = "#A9A9A9";
        }
    }
}

function prevCalendar() {
    today.setMonth(today.getMonth() - 1);
    buildCalendar();
}

function nextCalendar() {
    today.setMonth(today.getMonth() + 1);
    buildCalendar();
}
