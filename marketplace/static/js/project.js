/* Project specific Javascript goes here. */
const navbar_toggle = document.querySelector('.navbar-burger')
const navbar_menu = document.querySelector('.navbar-menu')

navbar_toggle.addEventListener('click', () => {
    navbar_toggle.classList.toggle('is-active')
    navbar_menu.classList.toggle('is-active')
})
