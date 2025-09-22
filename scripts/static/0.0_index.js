/*
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
*/

document.addEventListener("DOMContentLoaded", function () {
    // Function to scroll to the last message element with a 1-second delay
    function scrollToLastMessage() {
        var scrollContainer = document.querySelector(".scroll-container");
        var lastMessageElement = scrollContainer.lastElementChild;

        // Check if the lastMessageElement exists
        if (lastMessageElement) {
            lastMessageElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    }

    // Scroll to the last message when the page loads
    scrollToLastMessage();
});


