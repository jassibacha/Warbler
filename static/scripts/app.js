// Get liked button element
const likeButtons = document.querySelectorAll('.like-button');

console.log('loaded app.js');
// Event Listener
likeButtons.forEach((likeButton) => {
    likeButton.addEventListener('click', () => {
        const messageId = likeButton.dataset.mid;
        console.log(`Like button clicked, message id: ${messageId}`);
        // Send AJAX request to server to toggle like status
        fetch(`/messages/${messageId}/like`, { method: 'POST' })
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
});
