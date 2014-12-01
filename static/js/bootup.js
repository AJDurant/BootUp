
// Add exists function to jQuery
$.fn.exists = function () {
    return this.length !== 0;
};

$('.project-category').click(function () {
    cat = $( this );
    $('input[name="search"]').val(cat.text());
    $('form[role="search"]').submit();
});

$('input#project_sdesc').keyup(function () {
    desc = $( this ).next();
    len = $( this ).val().length;

    if ($('#sdesc-len').exists()) {
        $('#sdesc-len').text('' + len + ' / 120');
    } else {
        desc.append(' <span id="sdesc-len">' + len + ' / 120</span>');
    }

});
