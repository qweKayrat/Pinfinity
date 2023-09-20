const toggleContent = document.querySelector('.toggle_content')
const AddContent = document.querySelector('.add_content')

toggleContent.onclick = function () {
    toggleContent.classList.add('close')
    AddContent.classList.add('open')
};

document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("id_cat");

    select.addEventListener("mousedown", function (e) {
        e.preventDefault();
        const option = e.target;

        if (option.value !== "") {
            option.selected = !option.selected;
        }
    });
});
