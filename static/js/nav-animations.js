// Navigation Animations and Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize GSAP animations for navbar items
    initNavAnimations();
    
    // Handle navbar scroll effects
    handleNavbarScroll();
    
    // Initialize hover effects for nav links
    initNavHoverEffects();
    
    // Initialize mobile menu animations
    initMobileMenuAnimations();
    
    // Initialize magnetic buttons
    initMagneticButtons();
    
    // Initialize brand animation
    initBrandAnimation();
    
    // Initialize hero slide animations
    initHeroSlideAnimations();
    
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: false,
        mirror: true
    });
    
    // Initialize counter animations for statistics section
    initCounterAnimations();
    
    // Prevent navbar from collapsing on desktop when clicking links
    // Get all navbar links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    // Only apply this fix on desktop
    function isDesktop() {
        return window.innerWidth >= 992; // Bootstrap lg breakpoint
    }
    
    // Fix for navbar collapse on mobile
    if (navLinks && navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Only prevent collapse on desktop
                if (isDesktop()) {
                    // Prevent the default bootstrap behavior of collapsing
                    e.stopPropagation();
                } else if (navbarCollapse.classList.contains('show')) {
                    // On mobile, we want to close the menu after clicking a link
                    // Use Bootstrap's API to close the navbar
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
        });
    }
    
    // Ensure navbar stays visible on window resize
    window.addEventListener('resize', function() {
        if (isDesktop() && navbarCollapse) {
            navbarCollapse.classList.add('show');
            if (navbarToggler && navbarToggler.getAttribute('aria-expanded') === 'false') {
                navbarToggler.setAttribute('aria-expanded', 'true');
            }
        }
    });
    
    // Make sure navbar is visible on page load for desktop
    if (isDesktop() && navbarCollapse) {
        navbarCollapse.classList.add('show');
        if (navbarToggler) {
            navbarToggler.setAttribute('aria-expanded', 'true');
        }
    }
    
    // Auto-dismiss alerts after specified time
    initAutoDismissAlerts();
});

// Initialize GSAP animations for navbar elements
function initNavAnimations() {
    // Stagger animation for nav items on page load
    gsap.from('.navbar-nav .nav-item', {
        opacity: 0,
        y: -20,
        stagger: 0.1,
        duration: 0.8,
        ease: "power3.out",
        delay: 0.2,
        onComplete: function() {
            // Ensure items remain visible after animation
            gsap.set('.navbar-nav .nav-item', {
                clearProps: "all"
            });
        }
    });
    
    // Animate navbar brand
    gsap.from('.navbar-brand', {
        opacity: 0,
        x: -30,
        duration: 0.8,
        ease: "back.out(1.7)",
        onComplete: function() {
            // Ensure brand remains visible after animation
            gsap.set('.navbar-brand', {
                clearProps: "opacity,x"
            });
        }
    });
    
    // Animate buttons in navbar
    gsap.from('.navbar .btn', {
        opacity: 0,
        scale: 0.8,
        stagger: 0.1,
        duration: 0.8,
        ease: "elastic.out(1, 0.5)",
        delay: 0.5,
        onComplete: function() {
            // Ensure buttons remain visible after animation
            gsap.set('.navbar .btn', {
                clearProps: "opacity,scale"
            });
        }
    });
    
    // Add index attributes to nav items for staggered animations
    document.querySelectorAll('.navbar-nav .nav-item').forEach((item, index) => {
        item.style.setProperty('--item-index', index);
    });
}

// Handle navbar scroll effects
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar-enhanced');
    
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
            
            // Add subtle animation to navbar when scrolled
            gsap.to('.navbar-brand', {
                scale: 0.95,
                duration: 0.3,
                ease: "power2.out"
            });
            
            gsap.to('.navbar-nav', {
                y: -2,
                duration: 0.3,
                ease: "power2.out"
            });
        } else {
            navbar.classList.remove('navbar-scrolled');
            
            // Reset animations when back at top
            gsap.to('.navbar-brand', {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
            
            gsap.to('.navbar-nav', {
                y: 0,
                duration: 0.3,
                ease: "power2.out"
            });
        }
    });
}

// Initialize hover effects for nav links
function initNavHoverEffects() {
    const navLinks = document.querySelectorAll('.navbar-enhanced .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            gsap.to(this, {
                y: -3,
                scale: 1.05,
                duration: 0.3,
                ease: "power2.out"
            });
            
            // Add subtle glow effect
            this.style.textShadow = "0 0 8px rgba(78, 115, 223, 0.3)";
        });
        
        link.addEventListener('mouseleave', function() {
            gsap.to(this, {
                y: 0,
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
            
            // Remove glow effect
            this.style.textShadow = "none";
        });
    });
}

// Initialize mobile menu animations
function initMobileMenuAnimations() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (!navbarToggler || !navbarCollapse) return;
    
    // Only apply mobile animations on mobile devices
    function isMobile() {
        return window.innerWidth < 992; // Bootstrap lg breakpoint
    }
    
    navbarToggler.addEventListener('click', function() {
        // Only apply animations on mobile
        if (!isMobile()) return;
        
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        if (!isExpanded) {
            // Opening the menu
            gsap.fromTo(navbarCollapse, 
                { opacity: 0, height: 0 },
                { opacity: 1, height: 'auto', duration: 0.4, ease: "power3.out" }
            );
            
            // Stagger the nav items
            gsap.fromTo('.navbar-collapse .nav-item',
                { opacity: 0, x: -20 },
                { opacity: 1, x: 0, stagger: 0.1, duration: 0.4, delay: 0.2, ease: "power2.out" }
            );
        } else {
            // Closing the menu - add subtle animation
            gsap.to('.navbar-collapse .nav-item', {
                opacity: 0,
                x: -10,
                stagger: 0.05,
                duration: 0.2,
                ease: "power2.in"
            });
            
            gsap.to(navbarCollapse, {
                opacity: 0,
                duration: 0.3,
                ease: "power2.in",
                onComplete: function() {
                    // Let Bootstrap handle the actual collapse
                }
            });
        }
    });
    
    // Reset animations on window resize
    window.addEventListener('resize', function() {
        if (!isMobile() && navbarCollapse) {
            // Reset all GSAP animations for navbar on desktop
            gsap.set(navbarCollapse, { clearProps: "all" });
            gsap.set('.navbar-collapse .nav-item', { clearProps: "all" });
        }
    });
}

// Add magnetic effect to navbar buttons
function initMagneticButtons() {
    const buttons = document.querySelectorAll('[data-magnetic="true"]');
    
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const moveX = (x - centerX) * 0.1;
            const moveY = (y - centerY) * 0.1;
            
            gsap.to(this, {
                x: moveX,
                y: moveY,
                duration: 0.3,
                ease: "power3.out"
            });
        });
        
        btn.addEventListener('mouseleave', function() {
            gsap.to(this, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: "elastic.out(1, 0.5)"
            });
        });
    });
}

// Initialize brand animation
function initBrandAnimation() {
    const brandElements = document.querySelectorAll('.brand-text-animated');
    const brandDot = document.querySelector('.brand-dot');
    
    if (brandElements.length === 0) return;
    
    // Initial animation
    gsap.from(brandElements, {
        y: -30,
        opacity: 0,
        stagger: 0.1,
        duration: 1,
        ease: "elastic.out(1, 0.5)"
    });
    
    if (brandDot) {
        gsap.from(brandDot, {
            scale: 0,
            opacity: 0,
            duration: 0.8,
            delay: 0.5,
            ease: "back.out(2)"
        });
    }
    
    // Hover animation for navbar brand
    const navbarBrand = document.querySelector('.navbar-brand');
    if (navbarBrand) {
        navbarBrand.addEventListener('mouseenter', function() {
            gsap.to(brandElements[0], {
                y: -5,
                rotation: -5,
                duration: 0.3,
                ease: "power2.out"
            });
            
            gsap.to(brandElements[1], {
                y: -5,
                rotation: 5,
                duration: 0.3,
                ease: "power2.out"
            });
            
            if (brandDot) {
                gsap.to(brandDot, {
                    scale: 1.5,
                    duration: 0.3,
                    ease: "power2.out"
                });
            }
        });
        
        navbarBrand.addEventListener('mouseleave', function() {
            gsap.to(brandElements, {
                y: 0,
                rotation: 0,
                duration: 0.5,
                ease: "elastic.out(1, 0.5)"
            });
            
            if (brandDot) {
                gsap.to(brandDot, {
                    scale: 1,
                    duration: 0.5,
                    ease: "elastic.out(1, 0.5)"
                });
            }
        });
    }
}

// Initialize hero slide animations
function initHeroSlideAnimations() {
    const heroSlides = document.querySelectorAll('.hero-slide');
    
    if (heroSlides.length === 0) return;
    
    heroSlides.forEach(slide => {
        const caption = slide.querySelector('.carousel-caption');
        const heading = caption?.querySelector('h1');
        const paragraph = caption?.querySelector('p');
        const button = caption?.querySelector('.btn');
        
        if (!caption) return;
        
        // Create a timeline for each slide
        const tl = gsap.timeline({paused: true});
        
        // Add animations to the timeline
        if (heading) {
            tl.from(heading, {
                y: 50,
                opacity: 0,
                duration: 0.8,
                ease: "power3.out"
            }, 0);
        }
        
        if (paragraph) {
            tl.from(paragraph, {
                y: 30,
                opacity: 0,
                duration: 0.8,
                ease: "power3.out"
            }, 0.2);
        }
        
        if (button) {
            tl.from(button, {
                y: 20,
                opacity: 0,
                scale: 0.9,
                duration: 0.8,
                ease: "back.out(1.7)"
            }, 0.4);
            
            // Add hover animation for the button
            button.addEventListener('mouseenter', function() {
                gsap.to(this, {
                    scale: 1.05,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
            
            button.addEventListener('mouseleave', function() {
                gsap.to(this, {
                    scale: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
        }
        
        // Play the timeline when the slide is visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    tl.play();
                } else {
                    tl.progress(0).pause();
                }
            });
        }, {threshold: 0.3});
        
        observer.observe(slide);
    });
}

// Initialize counter animations for statistics section
function initCounterAnimations() {
    const statsSection = document.querySelector('.stats-section');
    if (!statsSection) return;
    
    const statNumbers = statsSection.querySelectorAll('.stat-number');
    
    // Create a timeline for the counter animations
    const countersTimeline = gsap.timeline({
        paused: true,
        onComplete: function() {
            // Ensure the final values are set correctly
            statNumbers.forEach(statNumber => {
                const finalValue = statNumber.getAttribute('data-final-value') || statNumber.textContent;
                statNumber.textContent = finalValue;
            });
        }
    });
    
    // Process each stat number
    statNumbers.forEach(statNumber => {
        // Store the final value as an attribute
        const originalText = statNumber.textContent;
        statNumber.setAttribute('data-final-value', originalText);
        
        // Determine if the value has a suffix like '+' or '%'
        let numericValue = originalText;
        let suffix = '';
        
        if (originalText.includes('+')) {
            numericValue = originalText.replace('+', '');
            suffix = '+';
        } else if (originalText.includes('%')) {
            numericValue = originalText.replace('%', '');
            suffix = '%';
        }
        
        // Convert to a number for the animation
        let endValue = parseFloat(numericValue);
        
        // Set initial value to 0
        statNumber.textContent = '0' + suffix;
        
        // Add to the timeline
        countersTimeline.to(statNumber, {
            duration: 2.5,
            ease: "power2.out",
            onUpdate: function() {
                const progress = this.progress();
                let currentValue = Math.round(endValue * progress);
                
                // Handle special case for 100%
                if (suffix === '%' && endValue === 100 && progress > 0.9) {
                    currentValue = 100;
                }
                
                statNumber.textContent = currentValue + suffix;
            }
        }, 0);
    });
    
    // Use Intersection Observer to trigger the animation when the section is visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                countersTimeline.play();
                observer.unobserve(entry.target); // Only play once
            }
        });
    }, {threshold: 0.2});
    
    observer.observe(statsSection);
}

// Auto-dismiss alerts after specified time
function initAutoDismissAlerts() {
    // Find all alert messages with auto-dismiss class
    const alerts = document.querySelectorAll('.alert-enhanced');
    
    alerts.forEach(alert => {
        // Set timeout to dismiss the alert after 5 seconds
        setTimeout(() => {
            // Use Bootstrap's alert dismiss functionality
            const bsAlert = new bootstrap.Alert(alert);
            
            // Add fade out animation
            alert.classList.add('fade-out');
            
            // Dismiss after animation completes
            setTimeout(() => {
                bsAlert.close();
            }, 500); // Fade out animation duration
        }, 5000); // 5 seconds
    });
}

// Add active link highlighting with scroll
document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('section[id]');
    
    if (sections.length > 0) {
        window.addEventListener('scroll', function() {
            let current = '';
            const scrollY = window.pageYOffset;
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');
                
                if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                    current = sectionId;
                }
            });
            
            document.querySelectorAll('.navbar-enhanced .nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });
    }
});
