// Get the dropdown button element
const dropdownMenuButton = document.querySelector('#dropdownMenuButton');
const dropdownMenuButtonDay = document.querySelector('#dropdownMenuButtonDay');
const dropdownMenuButtonTime = document.querySelector('#dropdownMenuButtonTime');

// Add an event listener for the 'click' event
document.querySelector('#dropdownMenu').addEventListener('click', function(event) {
  // Get the selected dropdown item
  const selectedItem = event.target;

  // Get the text of the selected dropdown item
  const selectedItemText = selectedItem.textContent;

  // Set the text of the dropdown button to the selected item text
  dropdownMenuButton.textContent = selectedItemText;
});

document.querySelector('#dropdownMenuDay').addEventListener('click', function(event) {
    const selectedItem = event.target;
    const selectedItemText = selectedItem.textContent;
  
    dropdownMenuButtonDay.textContent = selectedItemText;
});

document.querySelector('#dropdownMenuTime').addEventListener('click', function(event) {
    const selectedItem = event.target;
    const selectedItemText = selectedItem.textContent;
  
    dropdownMenuButtonTime.textContent = selectedItemText;
});