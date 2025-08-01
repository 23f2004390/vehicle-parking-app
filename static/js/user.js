// User-specific JavaScript functionality
// Only keeping essential functions that are specific to user.html template

document.addEventListener('DOMContentLoaded', function() {
    // Password confirmation validation for user profile
    const passwordForm = document.querySelector('form[action="/change-password"]');
    
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (newPassword !== confirmPassword) {
                e.preventDefault();
                alert('New passwords do not match!');
                return false;
            }
        });
    }
    
    // Debug booking status and show release buttons
    const bookingCards = document.querySelectorAll('.booking-card');
    bookingCards.forEach(card => {
        const statusElement = card.querySelector('.booking-status');
        const status = statusElement ? statusElement.textContent.toLowerCase() : '';
        const dataStatus = card.dataset.status;
        
        console.log('Booking status:', status, 'Data status:', dataStatus);
        
        // Show release button for active bookings
        if (status.includes('active') || dataStatus === 'active' || dataStatus === 'ACTIVE') {
            const actionsDiv = card.querySelector('.booking-actions');
            if (actionsDiv) {
                actionsDiv.style.display = 'block';
            }
        }
    });
});


