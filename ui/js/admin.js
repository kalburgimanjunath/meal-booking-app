function showMenu() {
  var x = document.getElementById("myNavbar");
  if (x.className === "navbar") {
    x.className += " responsive";
  } else {
    x.className = "navbar";
  }
}

function deleteItem() {
  alert("Are you sure you want to delete this meal option.");
}
