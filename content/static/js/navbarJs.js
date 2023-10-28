window.addEventListener("DOMContentLoaded", event => {
    const toggleBtn = document.querySelector('.toggle_btn')
    const dropDownMenu = document.querySelector('.dropdown_menu')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const toggleCat = document.querySelector('.toggle_cat')
    const MidBar = document.querySelector('.midbar')
    const toggleCatIcon = document.querySelector('.toggle_cat i')

    toggleBtn.onclick = function () {
        dropDownMenu.classList.toggle('open')
        const isOpen = dropDownMenu.classList.contains('open')

        toggleBtnIcon.classList = isOpen
            ? 'fa-solid fa-xmark'
            : 'fa-solid fa-bars'
    }


    toggleCat.onclick = function () {
        MidBar.classList.toggle('open')
        const isOpen = MidBar.classList.contains('open')

        toggleCatIcon.classList = isOpen
            ? 'fa-solid fa-angle-up'
            : 'fa-solid fa-angle-down'
    }

});

// Js для messages
document.addEventListener("DOMContentLoaded", function() {
    let alertBlock = document.getElementById("alert-block");
    // Закрытие блока автоматически через 4 секунды
    setTimeout(function() {
        alertBlock.style.opacity = "0";
        setTimeout(function() {
            alertBlock.style.display = "none";
        }, 1000); // Исчезнет после 0.4 секунды анимации
    }, 3500); // Через 4 секунды
});
