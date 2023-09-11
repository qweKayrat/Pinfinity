const CreateBtn = document.querySelector('.create')
const SavedBtn = document.querySelector('.saved')
const CreatedContent = document.querySelector('.content-c')
const SavedContent = document.querySelector('.content-s')

CreateBtn.onclick = function () {
    SavedBtn.classList.remove('active')
    SavedContent.classList.remove('active')
    CreateBtn.classList.add('active')
    CreatedContent.classList.add('active')
}

SavedBtn.onclick = function () {
    CreateBtn.classList.remove('active')
    CreatedContent.classList.remove('active')
    SavedBtn.classList.add('active')
    SavedContent.classList.add('active')
}
