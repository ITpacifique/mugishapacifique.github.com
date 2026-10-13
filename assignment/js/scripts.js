/*!
* Start Bootstrap - Creative v7.0.2 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });

    const profilePhotoInput = document.querySelector('#profilePhotoInput');
    const profilePhoto = document.querySelector('.profile-photo');
    const profilePhotoPlaceholder = document.querySelector('.profile-photo-placeholder');
    const profilePhotoStatus = document.querySelector('#profilePhotoStatus');
    const chooseProfilePhoto = document.querySelector('#chooseProfilePhoto');

    if (profilePhotoInput && profilePhoto && profilePhotoPlaceholder && profilePhotoStatus && chooseProfilePhoto) {
        const maxProfilePhotoSize = 5 * 1024 * 1024;

        chooseProfilePhoto.addEventListener('click', () => profilePhotoInput.click());

        const showProfilePhotoPlaceholder = () => {
            profilePhoto.hidden = true;
            profilePhotoPlaceholder.hidden = false;
        };

        profilePhoto.addEventListener('load', () => {
            profilePhoto.hidden = false;
            profilePhotoPlaceholder.hidden = true;
        });

        profilePhoto.addEventListener('error', () => {
            showProfilePhotoPlaceholder();
            profilePhotoStatus.textContent = 'Default portrait not found. Choose a photo to preview it here.';
        });

        if (profilePhoto.complete && profilePhoto.naturalWidth > 0) {
            profilePhotoPlaceholder.hidden = true;
        } else if (profilePhoto.complete) {
            showProfilePhotoPlaceholder();
        }

        profilePhotoInput.addEventListener('change', () => {
            const selectedPhoto = profilePhotoInput.files[0];
            profilePhotoInput.value = '';

            if (!selectedPhoto) {
                return;
            }

            if (!selectedPhoto.type.startsWith('image/')) {
                profilePhotoStatus.textContent = 'Choose an image file to preview your portrait.';
                return;
            }

            if (selectedPhoto.size > maxProfilePhotoSize) {
                profilePhotoStatus.textContent = 'Choose an image smaller than 5 MB.';
                return;
            }

            const photoReader = new FileReader();
            photoReader.addEventListener('load', () => {
                profilePhoto.src = photoReader.result;
                profilePhotoStatus.textContent = 'Photo preview active in this browser. Add it as assets/img/profile.jpg to publish it.';
            });
            photoReader.addEventListener('error', () => {
                profilePhotoStatus.textContent = 'This photo could not be opened. Please choose another image.';
            });
            photoReader.readAsDataURL(selectedPhoto);
        });
    }

});
