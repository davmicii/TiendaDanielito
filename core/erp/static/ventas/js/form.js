var tblProductos;

// Función para la venta
var vents = {
    // Items de mi factura
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    // Cálculo de los valores de mi factura
    calculate_invoice: function(){
        var subtotal = 0.00
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function(pos, dict){
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;
        $("input[name='subtotal']").val(this.items.subtotal.toFixed(2));
        $("input[name='ivacalc']").val(this.items.iva.toFixed(2));
        $("input[name='total']").val(this.items.total.toFixed(2));
    },
    add: function(item){
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProductos = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "subcategoria"},
                {"data": "precio"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cant+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
              $(row).find('input[name="cant"]').TouchSpin({
                  min: 1,
                  max: 10000000,
                  step: 1
              });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

// Propiedades y formatos
$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    // $("input[name='iva']").TouchSpin({
    //     min: 0,
    //     max: 100,
    //     step: 0.01,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     postfix: '%'
    // }).on('change', function(){
    //     vents.calculate_invoice();
    // }).val('0.00');

    // Buscar productos
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,        
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            //console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });



    // Remover todos los items
    $('.btnRemoveAll').on('click', function(){
        if(vents.items.products.length === 0) return false;
        alert_action('¡Notificación!', '¿Estás seguro de eliminar todos los items de tu detalle?',
    function(){
                vents.items.products = [];
                vents.list();
        }, function(){
        });
    });

    // Calcular cantidades modificadas en la factura y botón eliminar
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function(){
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            alert_action('¡Notificación!', '¿Está seguro de eliminar el producto de su detalle?',function(){
                vents.items.products.splice(tr.row, 1);
                vents.list();
                }, function() {
            });
        })
        .on('change keyup', 'input[name="cant"]', function(){
        var cant = parseInt($(this).val());
        var tr = tblProductos.cell($(this).closest('td, li')).index();
        var data = tblProductos.row(tr.row).node();
        vents.items.products[tr.row].cant = cant;
        vents.calculate_invoice();
        $('td:eq(5)', tblProductos.row(tr.row).node()).html('$ ' + vents.items.products[tr.row].subtotal.toFixed(2));
    });


    // Evento submit para guardar venta
    $('form').on('submit', function(e){
        e.preventDefault();

        if(vents.items.products.length===0){
            message('Debe tener al menos un producto en la factura');
            return false;
        }

        // Obtener fecha y cliente
        vents.items.date_joined = $('input[name="fecha_venta"]').val();
        vents.items.cli = $('select[name="cliente"]').val();


        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
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
                            url: window.location.pathname,
                            type: 'POST',
                            data: parameters,
                            dataType: 'json',
                            processData: false,
                            contentType: false,
                        }).done(function (data) {
                            if (!data.hasOwnProperty('error')) {
                                alert_action('¡Notificación!', '¿Desea guardar la factura de la venta?', function(){
                                    window.open('/erp/ventas/invoice/pdf/'+data.id+'/', '_blank');
                                    location.href = '/erp/ventas/list/';
                                }, function (){
                                    location.href = '/erp/ventas/list/';
                                });
                                return false;
                            }
                            message(data.error);
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            var errorMessage = textStatus + ': ' + errorThrown;
                            message(errorMessage);
                        }).always(function (data) {
                            // Se puede agregar acciones adicionales aquí si es necesario
                        });
                    }
                },
                danger: {
                    text: 'No',
                    btnClass: 'btn-red',
                    action: function () {
                        // Se puede agregar acciones adicionales aquí si es necesario
                    }
                },
            }
        });
    })


    // Limpiar el input de búsqueda
    $('.btnClearSearch').on('click', function(){
        $('input[name="search"]').val('').focus();
    })
});


// Preguntar antes de guardar si desea generar el PDF
function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
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
                    callback();
                }
            },
            danger: {
                text: 'No',
                btnClass: 'btn-red',
                action: function () {
                    // Agregar acciones adicionales aquí si es necesario
                    cancel();
                }
            },
        }
    });
}