
        // // Set current date
        // const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        // document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', options);

        // // Password toggle
        // document.getElementById('showPasswordic').addEventListener('click', function () {
        //     const passwordInput = document.getElementById('txtPasswordID');
        //     const icon = this.querySelector('i');

        //     if (passwordInput.type === 'password') {
        //         passwordInput.type = 'text';
        //         icon.classList.remove('fa-eye');
        //         icon.classList.add('fa-eye-slash');
        //     } else {
        //         passwordInput.type = 'password';
        //         icon.classList.remove('fa-eye-slash');
        //         icon.classList.add('fa-eye');
        //     }
        // });

        // // Focus on username field
        // window.onload = function () {
        //     document.getElementById('txtLoginNameID').focus();
        //     window.scrollTo(0, 0);
        // };

        // // Form validation
        // function validate() {
        //     const username = document.getElementById('txtLoginNameID').value.trim();
        //     const password = document.getElementById('txtPasswordID').value.trim();

        //     if (!username || !password) {
        //         alert('Please enter both username and password');
        //         return false;
        //     }

        //     // Additional validation logic can be added here

        //     return true;
        // }

        // // Add animation to notice items on hover
        // document.querySelectorAll('.notice-item').forEach(item => {
        //     item.addEventListener('mouseenter', function () {
        //         this.style.transform = 'translateX(5px)';
        //     });

        //     item.addEventListener('mouseleave', function () {
        //         this.style.transform = 'translateX(0)';
        //     });
        // });

        // --- Set current date ---
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
const dateElement = document.getElementById('current-date');
// Safety check: only set date if element exists
if (dateElement) {
    dateElement.textContent = new Date().toLocaleDateString('en-US', options);
}

// --- Password toggle ---
const showPassBtn = document.getElementById('showPasswordic');
if (showPassBtn) {
    showPassBtn.addEventListener('click', function () {
        const passwordInput = document.getElementById('txtPasswordID');
        const icon = this.querySelector('i');

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
}

// --- Focus on username field on load ---
window.onload = function () {
    const loginInput = document.getElementById('txtLoginNameID');
    if (loginInput) {
        loginInput.focus();
        window.scrollTo(0, 0);
    }
};

// --- NEW VALIDATION & LOGIN FUNCTION ---
function validate() {
    // 1. Get values using the IDs from your HTML
    const username = document.getElementById('txtLoginNameID').value.trim();
    const password = document.getElementById('txtPasswordID').value.trim();

    // 2. Basic Validation
    if (!username || !password) {
        alert('Please enter both username and password');
        return false; // Stop form submission
    }

    // 3. Prepare Data for Python Server
    const formData = new FormData();
    formData.append('txtLoginName', username);
    formData.append('txtPassword', password);

    // 4. Send to Backend (AJAX Request)
    // IMPORTANT: Ensure this URL matches your running Flask app port (3000)
    fetch('http://localhost:3000/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data);

// Inside the .then(data => { ... }) block:

if (data.status === 'success') {
    // --- LOGIN SUCCESS ---
    alert('Login Successful! Redirecting to Dashboard...');
    
    // 1. Save user details to Local Storage (Browser's temporary memory)
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('userName', data.user_name);
    localStorage.setItem('userRollNumber', data.roll_number); // We added this in app.py

    // 2. Redirect to the new dashboard page
    window.location.href = "dashboard.html"; 
    
    // No need to return false here since we are redirecting immediately
} else {
    // --- LOGIN FAILED (Keep this the same) ---
    alert('Login Failed: ' + data.message);
}
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error connecting to server. Is app.py running?');
    });

    // 5. IMPORTANT: Return false to prevent the HTML form from reloading the page
    return false; 
}

// --- Add animation to notice items on hover ---
document.querySelectorAll('.notice-item').forEach(item => {
    item.addEventListener('mouseenter', function () {
        this.style.transform = 'translateX(5px)';
    });

    item.addEventListener('mouseleave', function () {
        this.style.transform = 'translateX(0)';
    });
});