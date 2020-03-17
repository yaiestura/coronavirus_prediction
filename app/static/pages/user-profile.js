$(document).ready(function() {
    $('#edit-cancel').on('click', function() {
        var icon = $('#edit-btn').find("i");
        icon.removeClass('icofont-close');
        icon.addClass('icofont-edit');
        $('.view-info').show();
        $('.edit-info').hide();
    });

    $('.edit-info').hide();

    $('#edit-btn').on('click', function() {
        var icon = $(this).find("i");
        var edit_class = icon.attr('class');
        if (edit_class == 'icofont icofont-edit') {
            icon.removeClass('icofont-edit');
            icon.addClass('icofont-close');
            $('.view-info').hide();
            $('.edit-info').show();
        } else {
            icon.removeClass('icofont-close');
            icon.addClass('icofont-edit');
            $('.view-info').show();
            $('.edit-info').hide();
        }
    });

    //edit user description
    $('#edit-cancel-btn').on('click', function() {

        var icon = $('#edit-info-btn').find("i");
        icon.removeClass('icofont-close');
        icon.addClass('icofont-edit');
        $('.view-desc').show();
        $('.edit-desc').hide();
    });
});
