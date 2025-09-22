
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


// FUNCTION TO UPDATE YOUTUBE VIDEO HEIGHT
function updateYouTubeVideoHeight() {
    var videos = document.getElementsByClassName("youTubeVideo");

    for (var i = 0; i < videos.length; i++) {
        var video = videos[i];
        var width = video.clientWidth;
        var height = (width / 16) * 9; // Calculate height for 16:9 aspect ratio

        video.style.height = height + "px";
    }
}

// FUNCTION TO UPDATE YOUTUBE SHORTS HEIGHT
function updateYouTubeShortsHeight() {
    var shortsList = document.getElementsByClassName("youTubeShorts");

    for (var i = 0; i < shortsList.length; i++) {
        var shorts = shortsList[i];
        var width = shorts.clientWidth;
        var height = (width / 9) * 16; // Calculate height for 9:16 aspect ratio

        shorts.style.height = height + "px";
        shorts.style.width = width;
    }
}

// Function to scroll to the bottom of the message container
//function scrollToBottom() {
//    var container = document.querySelector('.scroll-container');
//    container.scrollTop = container.scrollHeight;
//}

// Function to scroll to the bottom on DOMContentLoaded
//function scrollToBottomOnLoad() {
//    scrollToBottom();
//}

// Function to dynamically set the ul-container height
function setUlContainerHeight() {
var headerHeight = document.querySelector('.header').offsetHeight;
var formContainerHeight = document.querySelector('.form-container').offsetHeight;
var windowHeight = window.innerHeight;

var ulContainer = document.querySelector('.ul-container');
var ulContainerHeight = windowHeight - formContainerHeight - headerHeight;
var ulContainerHeight = windowHeight - formContainerHeight - headerHeight;

ulContainer.style.maxHeight = ulContainerHeight + 'px';
}

// Function to dynamically set the max-height of scroll-container
function setScrollContainerMaxHeight() {
var headerHeight = document.querySelector('.header').offsetHeight;
var formContainerHeight = document.querySelector('.form-container').offsetHeight;
var windowHeight = window.innerHeight;

// Add your desired offset here
var offset = 50;

var scrollContainer = document.querySelector('.scroll-container');
var maxScrollContainerHeight = windowHeight - headerHeight - formContainerHeight - offset;

// Adjust for other container heights if needed
// maxScrollContainerHeight -= otherContainerHeight;

scrollContainer.style.maxHeight = maxScrollContainerHeight + 'px';
}

    // Call the functions on DOMContentLoaded, load, and resize events
    document.addEventListener("DOMContentLoaded", function () {
        updateYouTubeVideoHeight();
        updateYouTubeShortsHeight();
        //scrollToBottomOnLoad();
        //setUlContainerHeight(); // Call the function to set ul-container height
        setScrollContainerMaxHeight(); // Call the function to set max-height of scroll-container
    });


    window.addEventListener("load", function () {
        updateYouTubeVideoHeight();
        updateYouTubeShortsHeight();
        //scrollToBottom();
        //setUlContainerHeight(); // Call the function to set ul-container height
        setScrollContainerMaxHeight(); // Call the function to set max-height of scroll-container
    });


    window.addEventListener("resize", function () {
        updateYouTubeVideoHeight();
        updateYouTubeShortsHeight();
        setUlContainerHeight(); // Call the function to set ul-container height
        setScrollContainerMaxHeight(); // Call the function to set max-height of scroll-container
    });