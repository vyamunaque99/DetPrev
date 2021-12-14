$('td').on('click', function() {
    var $currentTable = $(this).closest('table');
    var index = $(this).index();
    $currentTable.find('td').removeClass('selected');
    $currentTable.find('tr').each(function() {
        $(this).find('td').eq(index).addClass('selected');
    });
});