
$('.project-category').click(function () {
    cat = $( this );
    $('input[name="search"]').val(cat.text());
    $('form[role="search"]').submit();
});
