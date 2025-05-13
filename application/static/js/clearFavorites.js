console.log('clearFavorites.js loaded'); // Debug loading

function clearFavorites() {
    console.log('clearFavorites function called'); // Debug function call
    
    if (confirm('Are you sure you want to clear all your favorites?')) {
        console.log('User confirmed clear favorites'); // Debug confirmation
        
        // Get the current domain
        const baseUrl = window.location.origin;
        console.log('Base URL:', baseUrl); // Debug base URL
        
        fetch(`${baseUrl}/clear_favorites`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            console.log('Response status:', response.status); // Debug response status
            console.log('Response headers:', response.headers); // Debug headers
            return response.text().then(text => {
                try {
                    return text ? JSON.parse(text) : {}
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                    console.log('Raw response:', text);
                    throw e;
                }
            });
        })
        .then(data => {
            console.log('Data received:', data); // Debug data
            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert('Failed to clear favorites: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
            console.error('Error details:', {
                message: error.message,
                stack: error.stack
            });
            alert('Failed to clear favorites. Please try again. Error: ' + error.message);
        });
    }
} 