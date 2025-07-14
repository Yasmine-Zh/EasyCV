/**
 * EasyCV Resume Website JavaScript
 * Provides interactive features for the generated resume website
 */

(function() {
    'use strict';

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeResumeFeatures();
    });

    function initializeResumeFeatures() {
        // Add smooth scrolling for anchor links
        addSmoothScrolling();
        
        // Add print functionality
        addPrintFeature();
        
        // Add contact info copy functionality
        addContactCopyFeature();
        
        // Add theme switcher if multiple themes available
        addThemeSwitcher();
        
        // Add responsive navigation for mobile
        addMobileNavigation();
        
        // Add fade-in animations
        addScrollAnimations();
    }

    function addSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    function addPrintFeature() {
        // Add print button if not present
        const header = document.querySelector('.header');
        if (header && !document.querySelector('.print-button')) {
            const printButton = document.createElement('button');
            printButton.className = 'print-button';
            printButton.innerHTML = '📄 Print Resume';
            printButton.addEventListener('click', function() {
                window.print();
            });
            
            // Style the print button
            printButton.style.cssText = `
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 0.5rem 1rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: background 0.3s ease;
            `;
            
            printButton.addEventListener('mouseover', function() {
                this.style.background = 'rgba(255, 255, 255, 0.3)';
            });
            
            printButton.addEventListener('mouseout', function() {
                this.style.background = 'rgba(255, 255, 255, 0.2)';
            });
            
            header.style.position = 'relative';
            header.appendChild(printButton);
        }
    }

    function addContactCopyFeature() {
        // Add click-to-copy functionality for contact information
        const emailLinks = document.querySelectorAll('.contact-email');
        const phoneElements = document.querySelectorAll('.contact-phone');
        
        [...emailLinks, ...phoneElements].forEach(element => {
            element.style.cursor = 'pointer';
            element.title = 'Click to copy';
            
            element.addEventListener('click', function(e) {
                e.preventDefault();
                
                const text = this.textContent || this.innerText;
                copyToClipboard(text);
                
                // Show temporary feedback
                showCopyFeedback(this);
            });
        });
    }

    function copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            // Use modern clipboard API
            navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
            } catch (err) {
                console.error('Failed to copy text: ', err);
            }
            
            document.body.removeChild(textArea);
        }
    }

    function showCopyFeedback(element) {
        const originalText = element.textContent;
        element.textContent = 'Copied!';
        element.style.opacity = '0.7';
        
        setTimeout(() => {
            element.textContent = originalText;
            element.style.opacity = '1';
        }, 1000);
    }

    function addThemeSwitcher() {
        // Only add if multiple themes are detected or theme classes exist
        const body = document.body;
        const currentTheme = body.className.match(/theme-\w+/);
        
        if (currentTheme) {
            const themes = ['professional', 'modern', 'creative', 'traditional'];
            const currentThemeName = currentTheme[0].replace('theme-', '');
            
            // Create theme switcher
            const switcher = document.createElement('div');
            switcher.className = 'theme-switcher';
            switcher.innerHTML = `
                <select id="theme-select">
                    ${themes.map(theme => 
                        `<option value="${theme}" ${theme === currentThemeName ? 'selected' : ''}>
                            ${theme.charAt(0).toUpperCase() + theme.slice(1)}
                        </option>`
                    ).join('')}
                </select>
            `;
            
            // Style the switcher
            switcher.style.cssText = `
                position: fixed;
                bottom: 1rem;
                right: 1rem;
                background: white;
                padding: 0.5rem;
                border-radius: 4px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 1000;
            `;
            
            document.body.appendChild(switcher);
            
            // Add theme switching functionality
            const select = document.getElementById('theme-select');
            select.addEventListener('change', function() {
                const newTheme = this.value;
                body.className = body.className.replace(/theme-\w+/, `theme-${newTheme}`);
                
                // Save preference to localStorage
                localStorage.setItem('easycv-theme', newTheme);
            });
            
            // Load saved theme preference
            const savedTheme = localStorage.getItem('easycv-theme');
            if (savedTheme && themes.includes(savedTheme)) {
                select.value = savedTheme;
                body.className = body.className.replace(/theme-\w+/, `theme-${savedTheme}`);
            }
        }
    }

    function addMobileNavigation() {
        // Add mobile-friendly navigation for long resumes
        const sections = document.querySelectorAll('h1, h2');
        
        if (sections.length > 3) {
            const nav = document.createElement('nav');
            nav.className = 'mobile-nav';
            nav.innerHTML = `
                <button class="nav-toggle">☰ Sections</button>
                <ul class="nav-list">
                    ${Array.from(sections).map((section, index) => {
                        const text = section.textContent;
                        const id = section.id || `section-${index}`;
                        if (!section.id) section.id = id;
                        
                        return `<li><a href="#${id}">${text}</a></li>`;
                    }).join('')}
                </ul>
            `;
            
            // Style the navigation
            nav.style.cssText = `
                position: fixed;
                top: 1rem;
                left: 1rem;
                z-index: 1000;
                display: none;
            `;
            
            document.body.appendChild(nav);
            
            // Add mobile navigation functionality
            const toggle = nav.querySelector('.nav-toggle');
            const navList = nav.querySelector('.nav-list');
            
            toggle.addEventListener('click', function() {
                navList.style.display = navList.style.display === 'block' ? 'none' : 'block';
            });
            
            // Show navigation on smaller screens
            function checkMobile() {
                if (window.innerWidth <= 768) {
                    nav.style.display = 'block';
                } else {
                    nav.style.display = 'none';
                }
            }
            
            checkMobile();
            window.addEventListener('resize', checkMobile);
        }
    }

    function addScrollAnimations() {
        // Add fade-in animations for sections
        const sections = document.querySelectorAll('h1, h2, .main-content > p, .main-content > ul');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            section.style.cssText += `
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            `;
            observer.observe(section);
        });
    }

    // Utility function to add CSS dynamically
    function addCSS(css) {
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    // Add responsive styles for mobile navigation
    addCSS(`
        .mobile-nav .nav-toggle {
            background: rgba(0,0,0,0.8);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        
        .mobile-nav .nav-list {
            display: none;
            background: white;
            border-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            padding: 0;
            margin: 0.5rem 0 0 0;
            list-style: none;
            min-width: 200px;
        }
        
        .mobile-nav .nav-list li {
            border-bottom: 1px solid #eee;
        }
        
        .mobile-nav .nav-list li:last-child {
            border-bottom: none;
        }
        
        .mobile-nav .nav-list a {
            display: block;
            padding: 0.75rem 1rem;
            color: #333;
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .mobile-nav .nav-list a:hover {
            background: #f5f5f5;
        }
        
        @media print {
            .mobile-nav,
            .theme-switcher,
            .print-button {
                display: none !important;
            }
        }
    `);

})(); 