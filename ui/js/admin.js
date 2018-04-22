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

$(document).ready(function() {
  $("#dtable").DataTable({
    responsive: true,
    order: [[0, "desc"]]
  });

  $("#menuDate").datepicker({
    dateFormat: "dd/mm/yy"
  });

  //trigger displaying and closing of a modal
  var modal = document.querySelector(".modal");
  var trigger = document.querySelector(".trigger");
  var closeButton = document.querySelector(".close-button");

  function toggleModal() {
    modal.classList.toggle("show-modal");
  }

  function windowOnClick(event) {
    if (event.target === modal) {
      toggleModal();
    }
  }

  trigger.addEventListener("click", toggleModal);
  closeButton.addEventListener("click", toggleModal);
  window.addEventListener("click", windowOnClick);
});
