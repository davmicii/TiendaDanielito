$(document).ready(function() {
    // Redirigir a una subcategoría
    $('.category-card').on('click', function() {
        var categoryName = $(this).data('category-name');
         window.location.href = '/erp/subcategorias/' + encodeURIComponent(categoryName) + '/';
    });


    // Redirigir a productos de una subcategoría
    $('.sub-category-card').on('click', function() {
        var subcategoryName = $(this).data('subcategory-name');
         window.location.href = '/erp/productos/' + encodeURIComponent(subcategoryName) + '/';
    });

    // Redirigir a detalle de un producto
    $('.list-product-card').on('click', function() {
        var productName = $(this).data('product-name');
        var productId = $(this).data('product-id');
        window.location.href = '/erp/detalle_producto/' + encodeURIComponent(productName) + '/' + productId + '/';
    });



    // Redirigir a la creación de subcategoría
    $('#create-subcategoria-btn').on('click', function() {
        var categoryId = $(this).data('category-id');
        var categoryName = "{{ category_name }}";
        window.location.href = '/erp/subcategorias/create/' + categoryId + '/' + encodeURIComponent(categoryName) + '/';
    });
});


