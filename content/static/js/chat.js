// var sender_id = {{ request.user.id} };
// var recipient_id = {{ recipient.id }};
//
//
// // Функция для получения сообщений
// function getMessages() {
//     $.ajax({
//         type: 'GET',
//         url: '/chat/' + recipient_id + '/',
//         success: function (response) {
//             for (var i = 0; i < response.length; i++) {
//                 var message = response[i];
//                 var messageHtml = '<div>' + message.content + '</div>';
//                 $('#messages').append(messageHtml);
//             }
//             // Прокручиваем страницу к последнему сообщению
//             $('html, body').animate({scrollTop: $(document).height()}, 1000);
//         }
//     });
// }
//
// // Вызываем функцию для получения сообщений каждые 3 секунды
// setInterval(getMessages, 3000);