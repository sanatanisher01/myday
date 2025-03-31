/**
 * MyDay - Event Memory Management Platform
 * Main JavaScript file for animations and interactivity
 */

document.addEventListener('DOMContentLoaded', function() {
    // Register GSAP ScrollTrigger Plugin
    gsap.registerPlugin(ScrollTrigger);
    
    // Initialize animations
    initAnimations();
    
    // Initialize event filters
    initEventFilters();
    
    // Initialize rating input
    initRatingInput();
    
    // Initialize modals
    initModals();
    
    // Initialize price calculator
    initPriceCalculator();
});

/**
 * Initialize GSAP animations
 */
function initAnimations() {
    // Hero section animation
    gsap.from('.hero-section .carousel-caption', {
        opacity: 0,
        y: 50,
        duration: 1,
        delay: 0.5
    });
    
    // Welcome section animation
    gsap.from('.welcome-text', {
        scrollTrigger: {
            trigger: '.welcome-section',
            start: 'top 80%',
        },
        opacity: 0,
        y: 30,
        duration: 0.8
    });
    
    gsap.from('.welcome-image', {
        scrollTrigger: {
            trigger: '.welcome-section',
            start: 'top 80%',
        },
        opacity: 0,
        x: 30,
        duration: 0.8,
        delay: 0.3
    });
    
    // Event cards animation
    gsap.utils.toArray('.event-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 90%',
            },
            opacity: 0,
            y: 30,
            duration: 0.6,
            delay: i * 0.1
        });
    });
    
    // Featured event animation
    gsap.from('.featured-image', {
        scrollTrigger: {
            trigger: '.featured-event',
            start: 'top 80%',
        },
        opacity: 0,
        x: -30,
        duration: 0.8
    });
    
    gsap.from('.featured-content', {
        scrollTrigger: {
            trigger: '.featured-event',
            start: 'top 80%',
        },
        opacity: 0,
        x: 30,
        duration: 0.8,
        delay: 0.3
    });
    
    // Stats animation
    gsap.utils.toArray('.stat-item').forEach((stat, i) => {
        gsap.from(stat, {
            scrollTrigger: {
                trigger: '.stats-section',
                start: 'top 80%',
            },
            opacity: 0,
            y: 30,
            duration: 0.6,
            delay: i * 0.2
        });
    });
    
    // Review carousel item animation
    const reviewItems = document.querySelectorAll('.carousel-item');
    reviewItems.forEach(item => {
        if (!item.classList.contains('active')) {
            gsap.set(item, { opacity: 0 });
        }
    });
    
    // Animate stars in reviews
    animateStars();
}

/**
 * Animate star ratings
 */
function animateStars() {
    const ratings = document.querySelectorAll('.rating');
    
    ratings.forEach(rating => {
        const stars = rating.querySelectorAll('.fa-star');
        gsap.from(stars, {
            scrollTrigger: {
                trigger: rating,
                start: 'top 90%',
            },
            opacity: 0,
            scale: 0.5,
            duration: 0.3,
            stagger: 0.1
        });
    });
}

/**
 * Initialize event category filters
 */
function initEventFilters() {
    const filterButtons = document.querySelectorAll('.filter-bar button');
    const eventCards = document.querySelectorAll('.event-card-wrapper');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            const filter = button.dataset.filter;
            
            eventCards.forEach(card => {
                if (filter === 'all') {
                    gsap.to(card, { opacity: 1, y: 0, duration: 0.4, display: 'block' });
                } else if (card.dataset.category === filter) {
                    gsap.to(card, { opacity: 1, y: 0, duration: 0.4, display: 'block' });
                } else {
                    gsap.to(card, { opacity: 0, y: 20, duration: 0.4, display: 'none' });
                }
            });
        });
    });
}

/**
 * Initialize rating input
 */
function initRatingInput() {
    const ratingInput = document.getElementById('rating');
    const ratingStars = document.querySelectorAll('.rating-stars .fa-star');
    
    if (ratingInput && ratingStars.length) {
        ratingInput.addEventListener('input', () => {
            const value = parseInt(ratingInput.value);
            
            ratingStars.forEach((star, index) => {
                if (index < value) {
                    star.classList.add('text-warning');
                } else {
                    star.classList.remove('text-warning');
                }
            });
        });
    }
}

/**
 * Initialize modal animations
 */
function initModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', () => {
            gsap.fromTo(
                modal.querySelector('.modal-dialog'),
                { scale: 0.8, opacity: 0 },
                { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(1.7)' }
            );
        });
    });
}

/**
 * Handle Bootstrap carousel animation
 */
document.addEventListener('slide.bs.carousel', function(e) {
    const nextItem = e.relatedTarget;
    const activeItem = document.querySelector('.carousel-item.active');
    
    // Animate out the current item
    gsap.to(activeItem.querySelector('.carousel-caption'), {
        opacity: 0,
        y: 30,
        duration: 0.3
    });
    
    // Animate in the next item
    gsap.fromTo(
        nextItem.querySelector('.carousel-caption'),
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.5, delay: 0.3 }
    );
});

/**
 * Parallax effect for hero section
 */
window.addEventListener('scroll', function() {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const scrollPosition = window.scrollY;
        const heroSlides = document.querySelectorAll('.hero-slide');
        
        heroSlides.forEach(slide => {
            const yPos = -scrollPosition * 0.2;
            slide.style.backgroundPosition = `center ${yPos}px`;
        });
    }
});

/**
 * Notification bell animation 
 * Used in user dashboard when there are new notifications
 */
function animateNotificationBell() {
    const bell = document.querySelector('.notification-bell');
    if (bell && bell.dataset.hasNotifications === 'true') {
        gsap.timeline({ repeat: -1, repeatDelay: 5 })
            .to(bell, { rotation: 15, duration: 0.1 })
            .to(bell, { rotation: -15, duration: 0.1 })
            .to(bell, { rotation: 10, duration: 0.1 })
            .to(bell, { rotation: -10, duration: 0.1 })
            .to(bell, { rotation: 0, duration: 0.1 });
    }
}

/**
 * Handle drag-and-drop file uploads
 * Used in admin dashboard for image uploads
 */
function initDragDropUpload() {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.querySelector('.drop-zone input[type="file"]');
    
    if (dropZone && fileInput) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drop-zone--over');
        });
        
        ['dragleave', 'dragend'].forEach(type => {
            dropZone.addEventListener(type, () => {
                dropZone.classList.remove('drop-zone--over');
            });
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateThumbnail(dropZone, e.dataTransfer.files[0]);
            }
            
            dropZone.classList.remove('drop-zone--over');
        });
        
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updateThumbnail(dropZone, fileInput.files[0]);
            }
        });
    }
}

/**
 * Update thumbnail for drag-and-drop uploads
 */
function updateThumbnail(dropZone, file) {
    let thumbnailElement = dropZone.querySelector('.drop-zone__thumb');
    
    // First time - create thumbnail element
    if (!thumbnailElement) {
        thumbnailElement = document.createElement('div');
        thumbnailElement.classList.add('drop-zone__thumb');
        dropZone.appendChild(thumbnailElement);
    }
    
    thumbnailElement.dataset.label = file.name;
    
    // Show thumbnail for image files
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        
        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        };
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}

/**
 * Initialize price calculator
 */
function initPriceCalculator() {
    const servicePrice = document.getElementById('service_price');
    const taxAmount = document.getElementById('tax_amount');
    const totalAmount = document.getElementById('total_amount');
    const subeventPrice = parseFloat('{{ subevent.price }}');
    
    // Update prices in Rupees
    function updatePrices() {
        // Convert to Rupees (assuming $1 = ₹82.50)
        const rupeesRate = 82.50;
        const priceInRupees = (subeventPrice * rupeesRate).toFixed(2);
        const taxInRupees = (priceInRupees * 0.1).toFixed(2);
        const totalInRupees = (parseFloat(priceInRupees) + parseFloat(taxInRupees)).toFixed(2);
        
        // Update the display
        servicePrice.textContent = `₹${priceInRupees}`;
        taxAmount.textContent = `₹${taxInRupees}`;
        totalAmount.textContent = `₹${totalInRupees}`;
    }
    
    // Update prices when the page loads
    updatePrices();
}
