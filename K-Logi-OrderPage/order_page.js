// Order Page JavaScript
let currentStep = 1;
const totalSteps = 4;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the order page
    initOrderPage();
});

function initOrderPage() {
    // Mobile menu toggle
    initMobileMenu();
    
    // Form step navigation
    initStepNavigation();
    
    // Form validation
    initFormValidation();
    
    // Pincode autofill
    initPincodeAutofill();
    
    // Price calculation
    initPriceCalculation();
    
    // Form submission
    initFormSubmission();
}

// Mobile Menu
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

// Step Navigation
function initStepNavigation() {
    const form = document.getElementById('orderForm');
    const steps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.progress-step');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    function showStep(stepNumber) {
        // Hide all steps
        steps.forEach(step => step.classList.remove('active'));
        progressSteps.forEach(step => step.classList.remove('active'));
        
        // Show current step
        const currentStepElement = document.querySelector(`[data-step="${stepNumber}"]`);
        const currentProgressStep = document.querySelector(`.progress-step[data-step="${stepNumber}"]`);
        
        if (currentStepElement) currentStepElement.classList.add('active');
        if (currentProgressStep) currentProgressStep.classList.add('active');
        
        // Update navigation buttons
        updateNavigationButtons(stepNumber);
    }
    
    function updateNavigationButtons(stepNumber) {
        if (stepNumber === 1) {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        } else if (stepNumber === totalSteps) {
            prevBtn.style.display = 'inline-flex';
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            prevBtn.style.display = 'inline-flex';
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }
    }
    
    function nextStep() {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        }
    }
    
    function prevStep() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    }
    
    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', nextStep);
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', prevStep);
    }
    
    // Progress step click navigation
    progressSteps.forEach(step => {
        step.addEventListener('click', () => {
            const stepNumber = parseInt(step.dataset.step);
            if (stepNumber <= currentStep || validateAllPreviousSteps(stepNumber)) {
                currentStep = stepNumber;
                showStep(currentStep);
            }
        });
    });
}

// Form Validation - Global functions
function validateCurrentStep() {
    const currentStepElement = document.querySelector(`.form-step[data-step="${currentStep}"]`);
    const requiredFields = currentStepElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Additional validation for specific fields
    if (currentStep === 1) {
        isValid = validateCustomerInfo() && isValid;
    } else if (currentStep === 2) {
        isValid = validateAddresses() && isValid;
    } else if (currentStep === 3) {
        isValid = validatePackageDetails() && isValid;
    } else if (currentStep === 4) {
        isValid = validatePayment() && isValid;
    }
    
    return isValid;
}

function validateAllPreviousSteps(targetStep) {
    for (let i = 1; i < targetStep; i++) {
        const stepElement = document.querySelector(`.form-step[data-step="${i}"]`);
        const requiredFields = stepElement.querySelectorAll('[required]');
        
        for (let field of requiredFields) {
            if (!field.value.trim()) {
                return false;
            }
        }
    }
    return true;
}

function validateCustomerInfo() {
    const phone = document.getElementById('customer_phone');
    const email = document.getElementById('customer_email');
    let isValid = true;
    
    // Phone validation
    if (phone.value && !/^[6-9]\d{9}$/.test(phone.value)) {
        showFieldError(phone, 'Please enter a valid 10-digit mobile number');
        isValid = false;
    }
    
    // Email validation
    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showFieldError(email, 'Please enter a valid email address');
        isValid = false;
    }
    
    return isValid;
}

function validateAddresses() {
    const pickupPincode = document.getElementById('pickup_pincode');
    const deliveryPincode = document.getElementById('delivery_pincode');
    let isValid = true;
    
    // Pincode validation
    if (pickupPincode.value && !/^\d{6}$/.test(pickupPincode.value)) {
        showFieldError(pickupPincode, 'Please enter a valid 6-digit pincode');
        isValid = false;
    }
    
    if (deliveryPincode.value && !/^\d{6}$/.test(deliveryPincode.value)) {
        showFieldError(deliveryPincode, 'Please enter a valid 6-digit pincode');
        isValid = false;
    }
    
    return isValid;
}

function validatePackageDetails() {
    const weight = document.getElementById('weight');
    const length = document.getElementById('length');
    const width = document.getElementById('width');
    const height = document.getElementById('height');
    let isValid = true;
    
    // Weight validation
    if (weight.value && parseFloat(weight.value) <= 0) {
        showFieldError(weight, 'Weight must be greater than 0');
        isValid = false;
    }
    
    // Dimensions validation
    [length, width, height].forEach(field => {
        if (field.value && parseFloat(field.value) <= 0) {
            showFieldError(field, 'Dimension must be greater than 0');
            isValid = false;
        }
    });
    
    return isValid;
}

function validatePayment() {
    const gstBill = document.getElementById('gst_bill');
    let isValid = true;
    
    // File validation
    if (gstBill.files.length > 0) {
        const file = gstBill.files[0];
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        const maxSize = 5 * 1024 * 1024; // 5MB
        
        if (!allowedTypes.includes(file.type)) {
            showFieldError(gstBill, 'Please upload a valid file (PDF, JPG, PNG)');
            isValid = false;
        } else if (file.size > maxSize) {
            showFieldError(gstBill, 'File size must be less than 5MB');
            isValid = false;
        }
    }
    
    return isValid;
}

function showFieldError(field, message) {
    const formGroup = field.closest('.form-group');
    let errorElement = formGroup.querySelector('.error-message');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        formGroup.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    formGroup.classList.add('error');
}

function clearFieldError(field) {
    const formGroup = field.closest('.form-group');
    const errorElement = formGroup.querySelector('.error-message');
    
    if (errorElement) {
        errorElement.style.display = 'none';
    }
    formGroup.classList.remove('error');
}

// Form Validation Initialization
function initFormValidation() {
    // Add real-time validation for specific fields
    const phoneField = document.getElementById('customer_phone');
    const emailField = document.getElementById('customer_email');
    
    if (phoneField) {
        phoneField.addEventListener('blur', () => {
            if (phoneField.value && !/^[6-9]\d{9}$/.test(phoneField.value)) {
                showFieldError(phoneField, 'Please enter a valid 10-digit mobile number');
            } else {
                clearFieldError(phoneField);
            }
        });
    }
    
    if (emailField) {
        emailField.addEventListener('blur', () => {
            if (emailField.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value)) {
                showFieldError(emailField, 'Please enter a valid email address');
            } else {
                clearFieldError(emailField);
            }
        });
    }
}

// Pincode Autofill
function initPincodeAutofill() {
    const pickupPincode = document.getElementById('pickup_pincode');
    const deliveryPincode = document.getElementById('delivery_pincode');
    
    function fetchPincodeInfo(pincode, type) {
        if (pincode.length === 6) {
            fetch(`/api/pincode/${pincode}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const districtField = document.getElementById(`${type}_district`);
                        const stateField = document.getElementById(`${type}_state`);
                        
                        if (districtField) districtField.value = data.district || '';
                        if (stateField) stateField.value = data.state || '';
                        
                        // Add success styling
                        const pincodeField = document.getElementById(`${type}_pincode`);
                        const formGroup = pincodeField.closest('.form-group');
                        formGroup.classList.add('success');
                        formGroup.classList.remove('error');
                    } else {
                        showFieldError(document.getElementById(`${type}_pincode`), 'Pincode not found');
                    }
                })
                .catch(error => {
                    console.error('Error fetching pincode info:', error);
                    showFieldError(document.getElementById(`${type}_pincode`), 'Error fetching pincode information');
                });
        }
    }
    
    if (pickupPincode) {
        pickupPincode.addEventListener('blur', () => {
            fetchPincodeInfo(pickupPincode.value, 'pickup');
        });
    }
    
    if (deliveryPincode) {
        deliveryPincode.addEventListener('blur', () => {
            fetchPincodeInfo(deliveryPincode.value, 'delivery');
        });
    }
}

// Price Calculation
function initPriceCalculation() {
    const calculateBtn = document.getElementById('calculatePrice');
    const zoneSelect = document.getElementById('zone_id');
    const weightInput = document.getElementById('weight');
    const quantityInput = document.getElementById('quantity');
    
    function calculatePrice() {
        const zone = zoneSelect.value;
        const weight = parseFloat(weightInput.value) || 0;
        const quantity = parseInt(quantityInput.value) || 1;
        
        if (!zone || weight <= 0) {
            alert('Please select a zone and enter a valid weight');
            return;
        }
        
        const selectedOption = zoneSelect.options[zoneSelect.selectedIndex];
        const baseRate = parseFloat(selectedOption.dataset.rate) || 0;
        
        const weightCharge = baseRate * weight;
        const subtotal = weightCharge * quantity;
        const gstAmount = subtotal * 0.18;
        const totalAmount = subtotal + gstAmount;
        
        // Update price display
        document.getElementById('baseRate').textContent = `₹${baseRate.toFixed(2)}`;
        document.getElementById('weightCharge').textContent = `₹${weightCharge.toFixed(2)}`;
        document.getElementById('gstAmount').textContent = `₹${gstAmount.toFixed(2)}`;
        document.getElementById('totalAmount').textContent = `₹${totalAmount.toFixed(2)}`;
        
        // Add animation
        const priceElements = document.querySelectorAll('.price-value');
        priceElements.forEach(element => {
            element.style.animation = 'pulse 0.5s ease-in-out';
            setTimeout(() => {
                element.style.animation = '';
            }, 500);
        });
    }
    
    if (calculateBtn) {
        calculateBtn.addEventListener('click', calculatePrice);
    }
    
    // Auto-calculate when zone or weight changes
    if (zoneSelect) {
        zoneSelect.addEventListener('change', calculatePrice);
    }
    
    if (weightInput) {
        weightInput.addEventListener('input', calculatePrice);
    }
    
    if (quantityInput) {
        quantityInput.addEventListener('input', calculatePrice);
    }
}

// Form Submission
function initFormSubmission() {
    const form = document.getElementById('orderForm');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!validateCurrentStep()) {
                return;
            }
            
            // Show loading overlay
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }
            
            // Create FormData
            const formData = new FormData(form);
            
            // Submit form
            fetch('/new-order', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.success) {
                    // Redirect to booking confirmation
                    window.location.href = `/booking-confirmation/${data.order_id}`;
                } else if (data && data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('Error submitting form:', error);
                alert('An error occurred while submitting your order. Please try again.');
            })
            .finally(() => {
                // Hide loading overlay
                if (loadingOverlay) {
                    loadingOverlay.style.display = 'none';
                }
            });
        });
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#10b981',
        error: '#dc2626',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 