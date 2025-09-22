
document.getElementById("resetButton").addEventListener("click", function() {
            // Send an AJAX request to reset the counter
            fetch('/reset_counter', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    // Update the counter value on the page
                    //document.querySelector('span#counterValue').textContent = data.counter;
                    // Refresh the page
                    location.reload();
                })
                .catch(error => {
                    console.error('Error resetting the counter:', error);
                });
        });


document.addEventListener("DOMContentLoaded", function () {
 // After adding a new message to the container
var container = document.querySelector('.scroll-container');
container.scrollTop = container.scrollHeight;
});










