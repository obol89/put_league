let selectedRow = null

function getMaxTeams() {
    let val = parseInt($('#teams_number').val());
    return isNaN(val) ? 16 : val;
}

function onFormSubmit() {
      if (validate()) {
        let formData = readFormData();
        if (selectedRow == null)
            insertNewRecord(formData);
        else
            updateRecord(formData);
        resetForm();
    }
  }

function readFormData() {
    let formData = [];
    formData["teamName"] = document.getElementById("teamName").value;
    return formData;
}

function insertNewRecord(data) {
    let table = document.getElementById("allTeams").getElementsByTagName('tbody')[0];
    let teamCount = document.getElementById("allTeams").rows.length;
    let newRow = table.insertRow(table.length);
    let cell1 = newRow.insertCell(0);
    cell1.innerHTML = teamCount;
    let cell2 = newRow.insertCell(1);
    cell2.innerHTML = data.teamName;
    let cell3 = newRow.insertCell(2);
    cell3.innerHTML = `<a onClick="onEdit(this)">Edit</a>
                       <a onClick="onDelete(this)">Delete</a>`;
}

function resetForm() {
    document.getElementById("teamName").value = "";
    selectedRow = null;
}

function onEdit(td) {
    selectedRow = td.parentElement.parentElement;
    document.getElementById("teamName").value = selectedRow.cells[1].innerHTML;
}
function updateRecord(formData) {
    selectedRow.cells[1].innerHTML = formData.teamName;
}

function onDelete(td) {
    if (confirm('Are you sure to delete this record ?')) {
        let row = td.parentElement.parentElement;
        let table = document.getElementById("allTeams").getElementsByTagName('tbody')[0];
        document.getElementById("allTeams").deleteRow(row.rowIndex);
        for (let i = 0, row; row = table.rows[i]; i++) {
            table.rows[i].cells[0].innerHTML = i+1;
           }
        resetForm();
    }
}

function validate() {
    let isValid = true;
    let maxTeams = getMaxTeams();
    let teamsColumn = $("#allTeams tr").find("td:eq(1)");
    let teamValues = [];
    $.each(teamsColumn, function(key, el){
         teamValues.push($(el).text());
    });
    let enteredTeam = document.getElementById("teamName").value;
    if (enteredTeam == "") {
        isValid = false;
    } else if (document.getElementById("allTeams").getElementsByTagName('tbody')[0].rows.length >= maxTeams) {
      isValid = false;
      alert('Table is full (' + maxTeams + ' teams).');
    } else if (teamValues.includes(enteredTeam)) {
      isValid = false;
      alert('Team was added. Please enter another name.');
      resetForm();
    }
    return isValid;
}


$('#Split').click( function(event) {
  let maxTeams = getMaxTeams();
  let currentCount = document.getElementById("allTeams").getElementsByTagName('tbody')[0].rows.length;
  if (currentCount < maxTeams) {
    alert('Please enter ' + maxTeams + ' teams. Currently: ' + currentCount + '.');
    event.preventDefault();
  } else {
    event.preventDefault();
    let splitBtn = $('#Split');
    splitBtn.addClass('disabled').css('pointer-events', 'none');

    let arr = [];
    $("#allTeams tr").each(function(){
        arr.push($(this).find("td:eq(1)").text());
    });
    let myJsonString = JSON.stringify(arr);
    let groupCount = $('#group_count').val();
    $.ajax({
      type: 'POST',
      data: {'teams': myJsonString, 'group_count': groupCount},
    }).done(function() {
      window.location.href = 'teams';
    }).fail(function(xhr) {
      let msg = 'An error occurred while submitting teams.';
      if (xhr.responseJSON && xhr.responseJSON.error) {
        msg = xhr.responseJSON.error;
      }
      alert(msg);
      splitBtn.removeClass('disabled').css('pointer-events', 'auto');
    });
  }});
