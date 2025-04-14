// Enhanced Reviews Section JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize review cards with animation
    initReviewCards();
    
    // Initialize star rating inputs
    initStarRating();
    
    // Initialize load more functionality
    initLoadMore();
    
    // Initialize review image lightbox
    initReviewImageLightbox();
});

// Initialize review cards with animation
function initReviewCards() {
    const reviewCards = document.querySelectorAll('.review-card');
    
    // Add wrapper class for animation if not already present
    reviewCards.forEach(card => {
        if (!card.parentElement.classList.contains('review-card-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'review-card-wrapper col-lg-4 col-md-6';
            card.parentNode.insertBefore(wrapper, card);
            wrapper.appendChild(card);
        }
    });
    
    // Add hover effect for review images
    const reviewImages = document.querySelectorAll('.review-image');
    reviewImages.forEach(img => {
        const wrapper = document.createElement('div');
        wrapper.className = 'review-image-wrapper';
        img.parentNode.insertBefore(wrapper, img);
        wrapper.appendChild(img);
    });
}

// Initialize star rating inputs
function initStarRating() {
    const ratingInputs = document.querySelectorAll('.rating-input');
    
    ratingInputs.forEach(input => {
        // Check if it's already enhanced
        if (input.querySelector('.star-rating-input')) return;
        
        const rangeInput = input.querySelector('input[type="range"]');
        if (!rangeInput) return;
        
        // Create star rating UI
        const starContainer = document.createElement('div');
        starContainer.className = 'star-rating-input';
        
        // Create 5 star inputs
        for (let i = 5; i >= 1; i--) {
            const radioInput = document.createElement('input');
            radioInput.type = 'radio';
            radioInput.name = rangeInput.name;
            radioInput.value = i;
            radioInput.id = `star${i}`;
            if (i == rangeInput.value) {
                radioInput.checked = true;
            }
            
            const label = document.createElement('label');
            label.htmlFor = `star${i}`;
            label.innerHTML = '<i class="fas fa-star"></i>';
            
            starContainer.appendChild(radioInput);
            starContainer.appendChild(label);
        }
        
        // Replace range input with star rating
        rangeInput.style.display = 'none';
        input.appendChild(starContainer);
        
        // Add event listeners to update the range input value
        starContainer.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', function() {
                rangeInput.value = this.value;
                // Trigger change event on range input
                const event = new Event('change');
                rangeInput.dispatchEvent(event);
            });
        });
    });
}

// Initialize load more functionality
function initLoadMore() {
    const loadMoreBtn = document.querySelector('.load-more-btn');
    if (!loadMoreBtn) return;
    
    const reviewCards = document.querySelectorAll('.review-card-wrapper');
    const cardsPerPage = 6;
    let currentlyShown = cardsPerPage;
    
    // Hide cards beyond initial limit
    reviewCards.forEach((card, index) => {
        if (index >= cardsPerPage) {
            card.style.display = 'none';
        }
    });
    
    // Update button visibility
    if (reviewCards.length <= cardsPerPage) {
        loadMoreBtn.style.display = 'none';
    }
    
    // Add click event to load more button
    loadMoreBtn.addEventListener('click', function() {
        // Show next batch of cards
        for (let i = currentlyShown; i < currentlyShown + cardsPerPage && i < reviewCards.length; i++) {
            reviewCards[i].style.display = 'block';
            // Trigger animation by removing and adding the class
            reviewCards[i].classList.remove('review-card-wrapper');
            setTimeout(() => {
                reviewCards[i].classList.add('review-card-wrapper');
            }, 10);
        }
        
        currentlyShown += cardsPerPage;
        
        // Hide button if all cards are shown
        if (currentlyShown >= reviewCards.length) {
            loadMoreBtn.style.display = 'none';
        }
    });
}

// Initialize review image lightbox
function initReviewImageLightbox() {
    const reviewImages = document.querySelectorAll('.review-image');
    
    reviewImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create lightbox elements
            const lightbox = document.createElement('div');
            lightbox.className = 'review-lightbox';
            lightbox.style.position = 'fixed';
            lightbox.style.top = '0';
            lightbox.style.left = '0';
            lightbox.style.width = '100%';
            lightbox.style.height = '100%';
            lightbox.style.backgroundColor = 'rgba(0,0,0,0.9)';
            lightbox.style.display = 'flex';
            lightbox.style.alignItems = 'center';
            lightbox.style.justifyContent = 'center';
            lightbox.style.zIndex = '9999';
            lightbox.style.opacity = '0';
            lightbox.style.transition = 'opacity 0.3s ease';
            
            const lightboxImg = document.createElement('img');
            lightboxImg.src = this.src;
            lightboxImg.style.maxWidth = '90%';
            lightboxImg.style.maxHeight = '90%';
            lightboxImg.style.borderRadius = '5px';
            lightboxImg.style.boxShadow = '0 5px 30px rgba(0,0,0,0.3)';
            lightboxImg.style.transform = 'scale(0.9)';
            lightboxImg.style.transition = 'transform 0.3s ease';
            
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '&times;';
            closeBtn.style.position = 'absolute';
            closeBtn.style.top = '20px';
            closeBtn.style.right = '20px';
            closeBtn.style.backgroundColor = 'transparent';
            closeBtn.style.border = 'none';
            closeBtn.style.color = 'white';
            closeBtn.style.fontSize = '2rem';
            closeBtn.style.cursor = 'pointer';
            
            // Add elements to DOM
            lightbox.appendChild(lightboxImg);
            lightbox.appendChild(closeBtn);
            document.body.appendChild(lightbox);
            
            // Animate in
            setTimeout(() => {
                lightbox.style.opacity = '1';
                lightboxImg.style.transform = 'scale(1)';
            }, 10);
            
            // Close on button click or background click
            closeBtn.addEventListener('click', closeLightbox);
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox) {
                    closeLightbox();
                }
            });
            
            function closeLightbox() {
                lightbox.style.opacity = '0';
                lightboxImg.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    document.body.removeChild(lightbox);
                }, 300);
            }
        });
    });
}
