

document.getElementById('searchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const searchBy = document.getElementById('searchBy').value;
    const cards = document.querySelectorAll('.parking-lot-card');
    
    cards.forEach(card => {
        let searchText = '';
        if (searchBy === 'location') {
            searchText = card.dataset.location;
        } else if (searchBy === 'lot_name') {
            searchText = card.dataset.name;
        } else if (searchBy === 'user_id') {
            searchText = card.querySelector('.lot-title').textContent;
        }
        
        if (searchText.includes(searchTerm) || searchTerm === '') {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bars on load
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
});
// User Edit Functions
function openUserEditPopup(userId, name, email, password,address) {
    document.getElementById('editUserId').value = userId;
    document.getElementById('editUserName').value = name;
    document.getElementById('editUserEmail').value = email;
    // document.getElementById('editUserAddress').value = address || '';

    document.getElementById('userEditPopup').classList.add('active');
}

// Parking Lot Edit Functions
function openLotEditPopup(lotId, lotName, location, totalSpaces, occupiedSpaces) {
    document.getElementById('editLotId').value = lotId;
    document.getElementById('editLotName').value = lotName;
    document.getElementById('editLotLocation').value = location
    document.getElementById('editTotalSpaces').value = totalSpaces
    document.getElementById('editOccupiedSpaces').value = occupiedSpaces;
    
    document.getElementById('lotEditPopup').classList.add('active');
}

// Close popup function
function closePopup(popupId) {
    document.getElementById(popupId).classList.remove('active');
}

// Close popup when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('popup-overlay')) {
        e.target.classList.remove('active')
    }
});
// Create Parking Lot Functions
function openCreateLotPopup() {
    document.getElementById('createLotForm').reset();
document.getElementById('createLotPopup').classList.add('active');
}

document.getElementById('createLotForm').addEventListener('submit', function(e) {
    // You can add validation here if needed
    const totalSpaces = document.getElementById('createTotalSpaces').value
    const pricePerHour = document.getElementById('createPricePerHour').value;
    
    if (totalSpaces < 1) {
        alert('Total spaces must be at least 1');
        e.preventDefault();
        return;
    }
    
    if (pricePerHour < 10) {
        alert('Price per hour must be at least ₹10');
        e.preventDefault();
        return;
    }
    
    // Form will submit to /lot_create route
});

// Open Users Popup
function openUsersPopup() {
    document.getElementById('usersPopup').classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close Users Popup
function closeUsersPopup() {
    document.getElementById('usersPopup').classList.remove('active')
    document.body.style.overflow = 'auto';
}

// Create User Functions
function openCreateUserPopup() {
    document.getElementById('createUserForm').reset();
    document.getElementById('createUserPopup').classList.add('active');
}

// Delete User Functions
function deleteUser(userId, userName) {
    document.getElementById('deleteUserId').value = userId
    document.getElementById('deleteUserName').textContent = userName
    document.getElementById('deleteUserPopup').classList.add('active')
}

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

// Close popup when clicking outside content area
document.getElementById('usersPopup').addEventListener('click', function(e) {
    if (e.target === this) {
        closeUsersPopup();
    }
});

// Close popup with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && document.getElementById('usersPopup').classList.contains('active')) {
        closeUsersPopup();
    }
});
// Open Booking Popup
function openBookingPopup() {
    document.getElementById('bookingPopup').classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close Booking Popup
function closeBookingPopup() {
    document.getElementById('bookingPopup').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Create Booking Functions
function openCreateBookingPopup() {
    document.getElementById('createBookingForm').reset();
    document.getElementById('createBookingPopup').classList.add('active');
}

// Booking Action Functions
function editBooking(bookingId) {
    alert('Edit booking: ' + bookingId + '\n(This would open an edit form)');
}

function completeBooking(bookingId) {
    if (confirm('Mark booking ' + bookingId + ' as completed?')) {
        alert('Booking ' + bookingId + ' marked as completed!');
        // Here you would update the booking status
    }
}

function cancelBooking(bookingId) {
    if (confirm('Cancel booking ' + bookingId + '? This will refund the user.')) {
        alert('Booking ' + bookingId + ' cancelled and refund processed!');
        // Here you would cancel the booking
    }
}

function deleteBooking(bookingId) {
    if (confirm('Delete booking ' + bookingId + '? This action cannot be undone.')) {
        alert('Booking ' + bookingId + ' deleted!');
        // Here you would delete the booking record
    }
}

function viewBookingDetails(bookingId) {
    alert('Viewing details for booking: ' + bookingId + '\n(This would open a detailed view)');
}

// Booking Search Functionality
document.getElementById('bookingSearchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const statusFilter = document.getElementById('bookingSearchBy').value;
    const bookingCards = document.querySelectorAll('.booking-card');
    
    bookingCards.forEach(card => {
        let shouldShow = false;
        
        // Filter by status
        if (statusFilter === 'all') {
            shouldShow = true;
        } else {
            shouldShow = card.dataset.status === statusFilter;
        }
        
        // Filter by search term
        if (shouldShow && searchTerm !== '') {
            const cardText = card.textContent.toLowerCase();
            shouldShow = cardText.includes(searchTerm);
        }
        
        card.style.display = shouldShow ? 'block' : 'none';
    });
});

// Close booking popup when clicking outside content area
document.getElementById('bookingPopup').addEventListener('click', function(e) {
    if (e.target === this) {
        closeBookingPopup();
    }
});

// Close booking popup with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && document.getElementById('bookingPopup').classList.contains('active')) {
        closeBookingPopup();
    }
});
        // // Toggle between available and occupied spots
        // document.querySelectorAll('.spot').forEach(spot => {
        //     spot.addEventListener('click', function() {
        //         if (this.classList.contains('available')) {
        //             this.classList.remove('available');
        //             this.classList.add('occupied');
        //         } else {
        //             this.classList.remove('occupied');
        //             this.classList.add('available');
        //         }
        //     });
        // });



