// static/script.js
document.getElementById('waitlist-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Stop the normal form submission

    const email = document.querySelector('input[name="email"]').value;
    const fullName = document.querySelector('input[name="fullName"]').value;
    const messageDiv = document.getElementById('message');

    fetch('/join', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Or 'application/x-www-form-urlencoded'
        },
        // If using 'application/json'
        body: JSON.stringify({ email: email, fullName: fullName })

        // If using application/x-www-form-urlencoded
        // body: `email=${email}&fullName=${fullName}`

    })
    .then(response => {
        if (!response.ok) {
            throw new Error(response.statusText);  // Handle errors properly
        }
        return response.json();
    })
    .then(data => {
        messageDiv.textContent = data.message;
        messageDiv.style.color = 'green'; // Indicate success
        // You could optionally reset the form here
        document.getElementById('waitlist-form').reset();

    })
    .catch(error => {
        messageDiv.textContent = "An error occurred. Please try again." + error;
        messageDiv.style.color = 'red';  // Indicate error
        console.error('Error:', error);
    });
});