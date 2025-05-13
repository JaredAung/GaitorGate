console.log('clearHistory.js loaded'); // Debug loading

function clearHistory() {
    console.log('clearHistory function called'); // Debug function call
    
    if (confirm('Are you sure you want to clear your entire history?')) {
        console.log('User confirmed clear history'); // Debug confirmation
        
        // Get the current domain
        const baseUrl = window.location.origin;
        console.log('Base URL:', baseUrl); // Debug base URL
        
        fetch(`${baseUrl}/clear_history`, {
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
                // Reload the page to show empty history
                window.location.reload();
            } else {
                alert('Failed to clear history: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
            console.error('Error details:', {
                message: error.message,
                stack: error.stack
            });
            alert('Failed to clear history. Please try again. Error: ' + error.message);
        });
    }
} 