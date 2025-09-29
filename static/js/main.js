// Ladies Collections - Shared JavaScript

document.addEventListener('DOMContentLoaded', function() {
  
  // Initialize Hero Carousel
  initializeCarousel();
  
  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Header scroll effect
  window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
      header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
      header.style.backdropFilter = 'blur(10px)';
    } else {
      header.style.backgroundColor = '#fff';
      header.style.backdropFilter = 'none';
    }
  });

  // Active navigation highlighting
  function setActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
      link.classList.remove('active');
      const linkPath = link.getAttribute('href');
      
      if (currentPath === '/' || currentPath.includes('index.html')) {
        if (linkPath === 'index.html' || linkPath === '/') {
          link.classList.add('active');
        }
      } else if (currentPath.includes(linkPath.replace('.html', ''))) {
        link.classList.add('active');
      }
    });
  }
  
  setActiveNav();

  // Simple loading animation for images
  const images = document.querySelectorAll('img');
  images.forEach(img => {
    img.addEventListener('load', function() {
      this.style.opacity = '1';
    });
    
    // Set initial opacity
    img.style.opacity = '0';
    img.style.transition = 'opacity 0.3s ease';
  });

  // Mobile menu toggle (if needed)
  function setupMobileMenu() {
    const header = document.querySelector('.header-content');
    const nav = document.querySelector('.nav-menu');
    
    // Add mobile menu button if screen is small
    if (window.innerWidth <= 768) {
      let mobileMenuBtn = document.querySelector('.mobile-menu-btn');
      if (!mobileMenuBtn) {
        mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.className = 'mobile-menu-btn';
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        mobileMenuBtn.style.cssText = `
          background: none;
          border: none;
          color: #a10649;
          font-size: 1.5rem;
          cursor: pointer;
          display: block;
        `;
        
        header.appendChild(mobileMenuBtn);
        
        mobileMenuBtn.addEventListener('click', () => {
          nav.classList.toggle('mobile-active');
        });
      }
    }
  }
  
  // Setup mobile menu on load and resize
  setupMobileMenu();
  window.addEventListener('resize', setupMobileMenu);

  // Contact form handling (if contact form exists)
  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Simple form validation and submission
      const formData = new FormData(this);
      const name = formData.get('name');
      const email = formData.get('email');
      const message = formData.get('message');
      
      if (name && email && message) {
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
      } else {
        alert('Please fill in all required fields.');
      }
    });
  }

  // WhatsApp click tracking
  const whatsappLinks = document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]');
  whatsappLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Track WhatsApp clicks (you can integrate with analytics here)
      console.log('WhatsApp contact initiated');
    });
  });

  // Phone call tracking
  const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
  phoneLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Track phone calls (you can integrate with analytics here)
      console.log('Phone call initiated');
    });
  });

});

// Utility functions
window.LadiesCollections = {
  // Format price function
  formatPrice: function(price) {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0
    }).format(price);
  },

  // Show notification
  showNotification: function(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 100px;
      right: 20px;
      background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 5px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      z-index: 1000;
      animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 5000);
  },

  // Scroll to top
  scrollToTop: function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }
};

// Hero Carousel Functionality
let currentSlideIndex = 0;
let carouselInterval;

function initializeCarousel() {
  const slides = document.querySelectorAll('.carousel-slide');
  if (slides.length === 0) return; // Exit if no carousel exists
  
  // Ensure first slide is active
  slides[0].classList.add('active');
  const firstDot = document.querySelector('.dot');
  if (firstDot) firstDot.classList.add('active');
  
  // Start automatic rotation after a short delay
  setTimeout(() => {
    startCarousel();
  }, 1000);
  
  // Pause on hover
  const carousel = document.querySelector('.hero-carousel');
  if (carousel) {
    carousel.addEventListener('mouseenter', stopCarousel);
    carousel.addEventListener('mouseleave', startCarousel);
  }
}

function startCarousel() {
  stopCarousel(); // Clear any existing interval
  carouselInterval = setInterval(() => {
    changeSlide(1);
  }, 4000); // Change slide every 4 seconds (faster)
}

function stopCarousel() {
  clearInterval(carouselInterval);
}

function changeSlide(direction) {
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.dot');
  
  if (slides.length === 0) return;
  
  // Remove active class from current slide and dot
  slides[currentSlideIndex].classList.remove('active');
  dots[currentSlideIndex].classList.remove('active');
  
  // Calculate next slide
  currentSlideIndex += direction;
  
  if (currentSlideIndex >= slides.length) {
    currentSlideIndex = 0;
  } else if (currentSlideIndex < 0) {
    currentSlideIndex = slides.length - 1;
  }
  
  // Add active class to new slide and dot
  slides[currentSlideIndex].classList.add('active');
  dots[currentSlideIndex].classList.add('active');
}

function currentSlide(slideNumber) {
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.dot');
  
  if (slides.length === 0) return;
  
  // Remove active class from current slide and dot
  slides[currentSlideIndex].classList.remove('active');
  dots[currentSlideIndex].classList.remove('active');
  
  // Set new current slide
  currentSlideIndex = slideNumber - 1;
  
  // Add active class to new slide and dot
  slides[currentSlideIndex].classList.add('active');
  dots[currentSlideIndex].classList.add('active');
  
  // Restart automatic rotation
  stopCarousel();
  startCarousel();
}

// Add CSS for animations
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
  
  .mobile-active {
    display: flex !important;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    padding: 1rem;
  }
  
  @media (max-width: 768px) {
    .nav-menu {
      display: none;
    }
  }
`;
document.head.appendChild(style);