// Fixed Search Functionality for Parking Dashboard

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
            searchInput.placeholder = placeholders[this.value] || 'search parking lots...';
        });
    }

    // FIXED: Search functionality for parking lots
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            const searchBy = document.getElementById('searchBy').value;
            
            // Get the select dropdown and its options
            const parkingSelect = document.getElementById('parking_lot_id');
            if (!parkingSelect) {
                console.error('Parking lot select element not found');
                return;
            }
            
            const options = parkingSelect.querySelectorAll('option:not(:first-child)');
            let hasVisibleResults = false;
            
            // Reset all options to visible first
            options.forEach(option => {
                option.style.display = 'block';
            });
            
            // If search term is empty, show all options
            if (searchTerm === '') {
                hasVisibleResults = true;
            } else {
                // Filter options based on search criteria
                options.forEach(option => {
                    let searchText = '';
                    
                    if (searchBy === 'location') {
                        searchText = (option.dataset.location || option.getAttribute('data-location') || '').toLowerCase();
                    } else if (searchBy === 'lot_name') {
                        searchText = (option.dataset.name || option.getAttribute('data-name') || option.textContent || '').toLowerCase();
                    }
                    
                    if (searchText.includes(searchTerm)) {
                        option.style.display = 'block';
                        hasVisibleResults = true;
                    } else {
                        option.style.display = 'none';
                    }
                });
            }
            
            // Show feedback if no results found
            showSearchFeedback(hasVisibleResults, searchTerm);
        });
    }

    // NEW: Booking Search Functionality
    initializeBookingSearch();

    // Form validation before submission
    const bookingForms = document.querySelectorAll('.booking-form');
    bookingForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const spotSelect = this.querySelector('select[name="spot_id"]');
            const durationInput = this.querySelector('input[name="duration"]');
            
            if (!spotSelect || !spotSelect.value) {
                e.preventDefault();
                alert('Please select a parking location first!');
                if (spotSelect) spotSelect.focus();
                return false;
            }
            
            if (!durationInput || !durationInput.value || durationInput.value < 1) {
                e.preventDefault();
                alert('Please enter valid duration (minimum 1 hour)!');
                if (durationInput) durationInput.focus();
                return false;
            }
        });
    });
});

// NEW: Initialize booking search functionality
function initializeBookingSearch() {
    const bookingSearchInput = document.getElementById('bookingSearchInput');
    const bookingSearchBy = document.getElementById('bookingSearchBy');
    const clearBookingSearchBtn = document.getElementById('clearBookingSearch');
    
    if (!bookingSearchInput || !bookingSearchBy) return;
    
    // Update placeholder based on search type
    bookingSearchBy.addEventListener('change', function() {
        const placeholders = {
            'vehicle_number': 'Enter vehicle number...',
            'status': 'Enter status (active, completed, cancelled)...',
            'date': 'Enter date (YYYY-MM-DD)...',
            'location': 'Enter location name...'
        };
        bookingSearchInput.placeholder = placeholders[this.value] || 'Search your bookings...';
    });
    
    // Search functionality
    bookingSearchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const searchBy = bookingSearchBy.value;
        
        const bookingCards = document.querySelectorAll('.booking-card');
        const noResultsMessage = document.getElementById('noBookingsMessage');
        let hasVisibleResults = false;
        
        bookingCards.forEach(card => {
            let searchText = '';
            
            switch(searchBy) {
                case 'vehicle_number':
                    searchText = card.dataset.vehicle || '';
                    break;
                case 'status':
                    searchText = card.dataset.status || '';
                    break;
                case 'date':
                    searchText = card.dataset.date || '';
                    break;
                case 'location':
                    searchText = card.dataset.location || '';
                    break;
            }
            
            if (searchText.toLowerCase().includes(searchTerm) || searchTerm === '') {
                card.style.display = 'block';
                hasVisibleResults = true;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show/hide no results message
        if (noResultsMessage) {
            if (!hasVisibleResults && searchTerm !== '') {
                noResultsMessage.style.display = 'block';
            } else {
                noResultsMessage.style.display = 'none';
            }
        }
        
        // Update search count
        updateBookingSearchCount();
    });
    
    // Clear search functionality
    if (clearBookingSearchBtn) {
        clearBookingSearchBtn.addEventListener('click', function() {
            bookingSearchInput.value = '';
            bookingSearchInput.dispatchEvent(new Event('input'));
            bookingSearchInput.focus();
        });
    }
}

// NEW: Update booking search count
function updateBookingSearchCount() {
    const visibleCards = document.querySelectorAll('.booking-card[style*="display: block"], .booking-card:not([style*="display: none"])');
    const searchInput = document.getElementById('bookingSearchInput');
    
    if (searchInput && searchInput.value.trim() !== '') {
        // You can add a counter display here if needed
        console.log(`Showing ${visibleCards.length} bookings`);
    }
}

// Function to show search feedback
function showSearchFeedback(hasResults, searchTerm) {
    // Remove existing feedback
    const existingFeedback = document.querySelector('.search-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Create feedback element
    const feedback = document.createElement('div');
    feedback.className = 'search-feedback';
    feedback.style.cssText = `
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
        font-size: 0.9rem;
    `;
    
    if (!hasResults && searchTerm) {
        feedback.textContent = `No parking lots found for "${searchTerm}". Try a different search term.`;
        feedback.style.backgroundColor = '#fff3cd';
        feedback.style.color = '#856404';
        feedback.style.border = '1px solid #ffeaa7';
    } else if (hasResults && searchTerm) {
        feedback.textContent = `Found parking lots matching "${searchTerm}"`;
        feedback.style.backgroundColor = '#d4edda';
        feedback.style.color = '#155724';
        feedback.style.border = '1px solid #c3e6cb';
    }
    
    // Insert feedback after search controls
    const searchControls = document.querySelector('.search-controls');
    if (searchControls && (searchTerm && (!hasResults || hasResults))) {
        searchControls.insertAdjacentElement('afterend', feedback);
    }
}

// Alternative search method for real-time filtering of visible results
function alternativeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBy = document.getElementById('searchBy');
    
    if (!searchInput || !searchBy) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const searchType = searchBy.value;
        
        // Create or update results display
        let resultsContainer = document.querySelector('.search-results');
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.className = 'search-results';
            resultsContainer.style.cssText = `
                background: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin: 10px 0;
                max-height: 200px;
                overflow-y: auto;
            `;
            
            const searchContainer = document.querySelector('.search-container');
            if (searchContainer) {
                searchContainer.appendChild(resultsContainer);
            }
        }
        
        if (searchTerm === '') {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
            return;
        }
        
        // Get parking lots data (this should come from your backend)
        const parkingSelect = document.getElementById('parking_lot_id');
        const options = parkingSelect ? parkingSelect.querySelectorAll('option:not(:first-child)') : [];
        
        let results = [];
        options.forEach(option => {
            let searchText = '';
            if (searchType === 'location') {
                searchText = option.getAttribute('data-location') || '';
            } else if (searchType === 'lot_name') {
                searchText = option.getAttribute('data-name') || option.textContent || '';
            }
            
            if (searchText.toLowerCase().includes(searchTerm)) {
                results.push({
                    id: option.value,
                    name: option.getAttribute('data-name') || option.textContent,
                    location: option.getAttribute('data-location') || ''
                });
            }
        });
        
        // Display results
        if (results.length > 0) {
            resultsContainer.innerHTML = results.map(result => `
                <div class="search-result-item" style="padding: 10px; border-bottom: 1px solid #eee; cursor: pointer;" 
                     onclick="selectParkingLot('${result.id}')">
                    <strong>${result.name}</strong><br>
                    <small style="color: #666;">${result.location}</small>
                </div>
            `).join('');
            resultsContainer.style.display = 'block';
        } else {
            resultsContainer.innerHTML = '<div style="padding: 15px; text-align: center; color: #666;">No results found</div>';
            resultsContainer.style.display = 'block';
        }
    });
}

// Function to select a parking lot from search results
function selectParkingLot(lotId) {
    const parkingSelect = document.getElementById('parking_lot_id');
    if (parkingSelect) {
        parkingSelect.value = lotId;
        
        // Hide search results
        const resultsContainer = document.querySelector('.search-results');
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
        
        // Clear search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = '';
        }
        
        // Show selection confirmation
        const selectedOption = parkingSelect.querySelector(`option[value="${lotId}"]`);
        if (selectedOption) {
            showNotification(`Selected: ${selectedOption.textContent}`, 'success');
        }
    }
}

// Utility function for notifications
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .search-result-item:hover {
        background-color: #f8f9fa;
    }
`;
document.head.appendChild(style);

// Initialize alternative search if needed
// alternativeSearch();