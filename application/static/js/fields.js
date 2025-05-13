document.addEventListener('DOMContentLoaded', function() {
    const accountTypeSelect = document.getElementById('account_type');
    const studentFields = document.getElementById('student_fields');
    const companyFields = document.getElementById('company_fields');
    
    function toggleFields() {
        if (accountTypeSelect.value === 'Student') {
            studentFields.style.display = 'block';
            companyFields.style.display = 'none';
        } else if (accountTypeSelect.value === 'Company') {
            studentFields.style.display = 'none';
            companyFields.style.display = 'block';
        } else {
            // For General account type
            studentFields.style.display = 'none';
            companyFields.style.display = 'none';
        }
    }
    
    // Initial toggle based on default selection
    toggleFields();
    
    // Add event listener for changes
    accountTypeSelect.addEventListener('change', toggleFields);
});