
// User Search Functionality
document.getElementById('userSearchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const searchBy = document.getElementById('userSearchBy').value;
    const userCards = document.querySelectorAll('.user-card');
    
    userCards.forEach(card => {
        let searchText = '';
        if (searchBy === 'name') {
            searchText = card.dataset.name;
        } else if (searchBy === 'email') {
            searchText = card.dataset.email;
        } else if (searchBy === 'user_id') {
            searchText = card.dataset.userid;
        }
        
        if (searchText.includes(searchTerm) || searchTerm === '') {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
// Form validation can be added here if needed
// The forms will now submit directly to your backend endpoints

// Optional: Add client-side password confirmation validation
document.addEventListener('DOMContentLoaded', function() {
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
});




document.addEventListener('DOMContentLoaded', function() {
    // Auto-update placeholder text based on search selection
    const searchBy = document.getElementById('searchBy');
    const searchInput = document.getElementById('searchInput');
    
    if (searchBy && searchInput) {
        searchBy.addEventListener('change', function() {
            const placeholders = {
                'location': 'Enter city or area name...',
                'lot_name': 'Enter parking lot name...',
                'area': 'Enter area or landmark...'
            };
            searchInput.placeholder = placeholders[this.value] || 'search . . .';
        });
    }
    
    // Form validation before submission
    const bookingForms = document.querySelectorAll('.booking-form');
    bookingForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const spotSelect = this.querySelector('select[name="spot_id"]');
            const hoursInput = this.querySelector('input[name="hours"]');
            
            if (!spotSelect.value) {
                e.preventDefault();
                alert('Please select a parking spot first!');
                spotSelect.focus();
                return false;
            }
            
            if (!hoursInput.value || hoursInput.value < 1) {
                e.preventDefault();
                alert('Please enter valid hours (minimum 1 hour)!');
                hoursInput.focus();
                return false;
            }
            
            // Show confirmation
            const spotId = spotSelect.value;
            const hours = hoursInput.value;
            const totalCost = document.getElementById('totalCost').textContent;
            
            const confirmMessage = `Confirm booking?\n\nSpot: ${spotId}\nDuration: ${hours} hour(s)\nTotal Cost: ${totalCost}`;
            
            if (!confirm(confirmMessage)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Auto-calculate total cost when hours change
    calculateTotal();
});

// Function to select spot by clicking on visual spot
function selectSpot(spotId) {
    // Update dropdown
    const spotSelect = document.getElementById('selected_spot');
    if (spotSelect) {
        spotSelect.value = spotId;
        
        // Remove previous selection styling
        document.querySelectorAll('.spot.available').forEach(spot => {
            spot.classList.remove('selected');
        });
        
        // Add selection styling to clicked spot
        const clickedSpot = document.querySelector(`[data-spot="${spotId}"]`);
        if (clickedSpot && clickedSpot.classList.contains('available')) {
            clickedSpot.classList.add('selected');
        }
        
        // Show success message
        showNotification(`Spot ${spotId} selected!`, 'success');
    }
}

// Function to calculate total booking cost
function calculateTotal() {
    const hoursInput = document.getElementById('booking_hours');
    const totalCostDiv = document.getElementById('totalCost');
    const ratePerHour = 50; // ₹50 per hour
    
    if (hoursInput && totalCostDiv) {
        const hours = parseInt(hoursInput.value) || 1;
        const total = hours * ratePerHour;
        totalCostDiv.textContent = `₹${total}`;
    }
}