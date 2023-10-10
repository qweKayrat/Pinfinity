// elements.forEach(element => {
//     const rect = element.getBoundingClientRect();
//     Примените transform для каждого элемента
// element.style.transform = `translateX(${rect.left}px) translateY(${rect.bottom}px)`;
// });

// $(document).ready(function () {
//     let offset = 20;  // Начальное смещение
//     let limit = 20;   // Количество записей для загрузки
//     let loading = false;
//
//     let contentContainer = $('.main');
//     // let lastCard = $('.card').last();
//
//     // Получаем текущий URL страницы
//     // Разбиваем URL на части, используя '/' в качестве разделителя
//     let urlParts = window.location.href.split('/');
//
//     // Ищем индекс элемента, содержащего cat_slug в URL
//     let catSlugIndex = urlParts.indexOf('category');
//
//     // Извлекаем cat_slug, если он существует
//     let catSlug = null;
//     if (catSlugIndex !== -1 && catSlugIndex < urlParts.length - 1) {
//         catSlug = urlParts[catSlugIndex + 1];
//     }
//
//     // Теперь у вас есть значение cat_slug
//     if (catSlug !== null) {
//         // Вы можете использовать catSlug в вашем AJAX-запросе
//         // Например, добавьте его в data объект:
//         var data = {
//             'cat_slug': catSlug,
//             'offset': offset
//         }
//     } else {
//         var data = {
//             'offset': offset
//         }
//     }
//
//
//     function loadMoreContent() {
//         if (loading) return;
//         loading = true;
//         $.ajax({
//             url: '/load_more_content/',
//             data: data,
//             dataType: 'json',
//             success: function (data) {
//                 // Обработка полученных данных и добавление их на страницу
//                 if (data.length > 0) {
//                     for (let i = 0; i < data.length; i++) {
//                         let item = data[i]
//                         let card = $('<div class="card">');
//
//                         let pict = $('<div class="pict">').appendTo(card);
//                         $('<a>', {
//                             href: '/post/' + item.slug + '/',
//                             html: '<img src="' + item.image_url + '" alt="image ' + item.title + '" class="image">'
//                         }).appendTo(pict);
//
//                         let postOwner = $('<div class="post_owner">').appendTo(card);
//                         $('<img>', {
//                             src: item.owner_img, // Обращаемся по ключу 'owner' и далее по ключу 'img_url'
//                             alt: 'image ' + item.owner_username,
//                             class: 'owner_image'
//                         }).appendTo(postOwner);
//                         $('<p>', {
//                             text: item.owner_username
//                         }).appendTo(postOwner);
//
//                         let details = $('<div class="details" onclick="window.location=\'/post/' + item.slug + '/\'">').appendTo(card);
//                         $('<h2>', {
//                             html: item.title
//                         }).appendTo(details);
//
//
//                         lastCard.after(card)
//                     }
//                     offset += data.length;
//                 } else {
//                 }
//                 loading = false;
//             },
//             error: function () {
//                 loading = false; // Сброс флага при ошибке запроса
//             }
//         });
//     }
//
//     // Отслеживание события прокрутки страницы
//     $(window).scroll(function () {
//         if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
//             loadMoreContent();
//         }
//     });
// });
window.onload = function() {
    let chatContainer = document.querySelector('.chat');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function loadMessages() {
    let contentContainer = $('.chat');
    let urlParts = window.location.href.split('/');

    // Ищем индекс элемента, содержащего cat_slug в URL
    let senderIndex = urlParts.indexOf('chat');

    // Извлекаем cat_slug, если он существует
    let sender = null;
    if (senderIndex !== -1 && senderIndex < urlParts.length - 1) {
        sender = urlParts[senderIndex + 1];
    }

    $.ajax({
            url: '/profile/load_messages/',
            data: {'sender_username': sender},
            dataType: 'json',
            success: function (data) {
                if (data.length > 0) {
                    for (let i = 0; i < data.length; i++) {
                        let item = data[i]
                        if (item.sender === sender) {
                            let card = $('<div class="mess right">');
                        } else {
                            let card = $('<div class="mess left">');
                        }
                        $('<p>', {
                            text: item.body
                        }).appendTo(card);

                        contentContainer.appendTo(card)
                    }
                } else {
                }
            }
        }
    )
    ;
}

// Вызовите функцию loadMessages() при загрузке страницы и через интервал времени для обновления сообщений в реальном времени
$(document).ready(function () {
    loadMessages();
    setInterval(loadMessages, 3000); // каждые 5 секунд
});
