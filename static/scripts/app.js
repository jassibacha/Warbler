// Get liked button element
const likeButton = document.querySelector('.like-button');

console.log('loaded app.js');
// Event Listener
likeButton.addEventListener('click', () => {
    console.log('button clicked');
    // Send AJAX request to server to toggle like status
    fetch('/messages/{{ msg.id }}/like', { method: 'POST' })
        .then((response) => response.json())
        .then((data) => {
            // Update button class based on updated status
            if (data.liked) {
                likeButton.classList.remove('btn-secondary');
                likeButton.classList.add('btn-primary');
            } else {
                likeButton.classList.remove('btn-primary');
                likeButton.classList.add('btn-secondary');
            }
        });
});
