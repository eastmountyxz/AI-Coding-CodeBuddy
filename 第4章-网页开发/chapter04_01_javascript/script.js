document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registration-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const confirmPasswordError = document.getElementById('confirm-password-error');
    const successMessage = document.getElementById('success-message');

    // Email validation function
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Password validation function
    function validatePassword(password) {
        // Password must be at least 8 characters with at least one number and one letter
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        return passwordRegex.test(password);
    }

    // Real-time email validation
    emailInput.addEventListener('input', function() {
        if (emailInput.value.trim() === '') {
            emailError.textContent = 'Email is required';
            emailInput.classList.add('error');
        } else if (!validateEmail(emailInput.value)) {
            emailError.textContent = 'Please enter a valid email address';
            emailInput.classList.add('error');
        } else {
            emailError.textContent = '';
            emailInput.classList.remove('error');
        }
    });

    // Real-time password validation
    passwordInput.addEventListener('input', function() {
        if (passwordInput.value.trim() === '') {
            passwordError.textContent = 'Password is required';
            passwordInput.classList.add('error');
        } else if (!validatePassword(passwordInput.value)) {
            passwordError.textContent = 'Password must be at least 8 characters with at least one letter and one number';
            passwordInput.classList.add('error');
        } else {
            passwordError.textContent = '';
            passwordInput.classList.remove('error');
        }
        
        // Check confirm password match if it has a value
        if (confirmPasswordInput.value.trim() !== '') {
            if (confirmPasswordInput.value !== passwordInput.value) {
                confirmPasswordError.textContent = 'Passwords do not match';
                confirmPasswordInput.classList.add('error');
            } else {
                confirmPasswordError.textContent = '';
                confirmPasswordInput.classList.remove('error');
            }
        }
    });

    // Real-time confirm password validation
    confirmPasswordInput.addEventListener('input', function() {
        if (confirmPasswordInput.value.trim() === '') {
            confirmPasswordError.textContent = 'Please confirm your password';
            confirmPasswordInput.classList.add('error');
        } else if (confirmPasswordInput.value !== passwordInput.value) {
            confirmPasswordError.textContent = 'Passwords do not match';
            confirmPasswordInput.classList.add('error');
        } else {
            confirmPasswordError.textContent = '';
            confirmPasswordInput.classList.remove('error');
        }
    });

    // Form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Validate all fields
        let isValid = true;
        
        // Email validation
        if (emailInput.value.trim() === '') {
            emailError.textContent = 'Email is required';
            emailInput.classList.add('error');
            isValid = false;
        } else if (!validateEmail(emailInput.value)) {
            emailError.textContent = 'Please enter a valid email address';
            emailInput.classList.add('error');
            isValid = false;
        }
        
        // Password validation
        if (passwordInput.value.trim() === '') {
            passwordError.textContent = 'Password is required';
            passwordInput.classList.add('error');
            isValid = false;
        } else if (!validatePassword(passwordInput.value)) {
            passwordError.textContent = 'Password must be at least 8 characters with at least one letter and one number';
            passwordInput.classList.add('error');
            isValid = false;
        }
        
        // Confirm password validation
        if (confirmPasswordInput.value.trim() === '') {
            confirmPasswordError.textContent = 'Please confirm your password';
            confirmPasswordInput.classList.add('error');
            isValid = false;
        } else if (confirmPasswordInput.value !== passwordInput.value) {
            confirmPasswordError.textContent = 'Passwords do not match';
            confirmPasswordInput.classList.add('error');
            isValid = false;
        }
        
        // If all validations pass
        if (isValid) {
            // Hide the form and show success message
            form.style.display = 'none';
            successMessage.style.display = 'block';
            
            // In a real application, you would send the form data to a server here
            console.log('Form submitted successfully');
            console.log('Email:', emailInput.value);
            console.log('Password:', passwordInput.value);
        }
    });
});