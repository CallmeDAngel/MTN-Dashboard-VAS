$(document).ready(function() {
    if (typeof moment !== 'undefined') {
        $.fn.dataTable.moment('DD/MM/YYYY'); // Assure-toi que ce format correspond à celui utilisé dans les données
    }

    $('#dataTable_error').DataTable({
        "pageLength": 10,  // Nombre d'éléments par page
        "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Tous"]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json"
        },
        "columnDefs": [
            { 
                "targets": 0, // Assure-toi que l'index est correct
                "type": "date"
            }
        ]
    });

    $('#dataTable').DataTable({
        "pageLength": 10,  // Nombre d'éléments par page
        "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Tous"]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json"
        },
        "columnDefs": [
            { 
                "targets": 0, // Assure-toi que l'index est correct
                "type": "date"
            }
        ]
});
});
