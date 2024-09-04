function message(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align:left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: 'Confirmación',
        icon: 'fa fa-info',
        content: '¿Estás seguro de completar la acción?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        var errorMessage = textStatus + ': ' + errorThrown;
                        message(errorMessage);
                    }).always(function (data) {
                        // Puedes agregar acciones adicionales aquí si es necesario
                    });
                }
            },
            danger: {
                text: 'No',
                btnClass: 'btn-red',
                action: function () {
                    // Puedes agregar acciones adicionales aquí si es necesario
                }
            },
        }
    });
}

// function alert_action(title, content, callback) {
//     $.confirm({
//         theme: 'material',
//         title: title,
//         icon: 'fa fa-info',
//         content: content,
//         columnClass: 'small',
//         typeAnimated: true,
//         cancelButtonClass: 'btn-primary',
//         draggable: true,
//         dragWindowBorder: false,
//         buttons: {
//             info: {
//                 text: 'Si',
//                 btnClass: 'btn-primary',
//                 action: function () {
//                     callback();
//                 }
//             },
//             danger: {
//                 text: 'No',
//                 btnClass: 'btn-red',
//                 action: function () {
//                     // Agregar acciones adicionales aquí si es necesario
//                 }
//             },
//         }
//     });
// }