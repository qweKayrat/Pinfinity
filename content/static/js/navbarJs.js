const toggleBtn = document.querySelector('.toggle_btn')
const dropDownMenu = document.querySelector('.dropdown_menu')
const toggleBtnIcon = document.querySelector('.toggle_btn i')
// const  = document.querySelector('')
// const  = document.querySelector('')


toggleBtn.onclick = function () {
    dropDownMenu.classList.toggle('open')
    const isOpen = dropDownMenu.classList.contains('open')

    toggleBtnIcon.classList = isOpen
        ? 'fa-solid fa-xmark'
        : 'fa-solid fa-bars'
}


const toggleCat = document.querySelector('.toggle_cat')
const MidBar = document.querySelector('.midbar')
const toggleCatIcon = document.querySelector('.toggle_cat i')

toggleCat.onclick = function () {
    MidBar.classList.toggle('open')
    const isOpen = MidBar.classList.contains('open')

    toggleCatIcon.classList = isOpen
        ? 'fa-solid fa-angle-up'
        : 'fa-solid fa-angle-down'
}

