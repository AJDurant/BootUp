/*
    This provides JS for the app


 */


// Add exists function to jQuery
$.fn.exists = function () {
    return this.length !== 0;
};

// Enables clicking on a category label to search
$('.project-category').click(function () {
    cat = $( this );
    $('input[name="search"]').val(cat.text());
    $('form[role="search"]').submit();
});

// Shows the character count limit on project creation
$('input#project_sdesc').keyup(function () {
    desc = $( this ).next();
    len = $( this ).val().length;

    if ($('#sdesc-len').exists()) {
        $('#sdesc-len').text('' + len + ' / 120');
    } else {
        desc.append(' <span id="sdesc-len">' + len + ' / 120</span>');
    }

});
