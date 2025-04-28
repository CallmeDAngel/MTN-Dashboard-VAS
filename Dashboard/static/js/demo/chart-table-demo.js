$(function() {
    const table = $('#dataTable').DataTable({
        paging: true,
        info: false,
        searching: false,
        pageLength: 10 // longueur de page initiale
    });

    const rowCount = table.data().count();
    let displayLength = 10;

    $('#loadMore').on('click', function() {
        if (displayLength < rowCount) {
            displayLength = Math.min(displayLength + 10, rowCount);
            table.page.len(displayLength).draw();
            if (displayLength >= rowCount) {
            $(this).hide();
            }
        }
    });
});