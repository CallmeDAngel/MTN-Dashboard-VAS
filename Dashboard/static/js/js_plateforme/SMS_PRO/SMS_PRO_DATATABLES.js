// $(document).ready(function() {
//     if (typeof moment !== 'undefined') {
//         $.fn.dataTable.moment('DD/MM/YYYY'); // Assure-toi que ce format correspond à celui utilisé dans les données
//     }

//     $('#dataTable').DataTable({
//         "ajax": {
//             "url": "/dashboard/sms_pro_datatable/",  // Remplace par l'URL de ta vue Django qui renvoie les données JSON
//             "type": "GET",
//             "dataSrc": "data"  // La clé où se trouvent les données dans la réponse JSON
//         },
//         "pageLength": 10,  // Nombre d'éléments par page
//         "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Tous"]],
//         "language": {
//             "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json"
//         },
//         "columns": [
//             { "data": "Date" },  // Nom de la colonne dans les données JSON (ajuste en fonction de tes champs)
//             { "data": "Success" },
//             { "data": "Error" },
//             { "data": "Total" },  // Nom de la colonne dans les données JSON (ajuste en fonction de tes champs)
//             { "data": "Success % without exclusion" },
//             { "data": "Success % with exclusion" },
//             // Ajoute autant de colonnes que nécessaire
//         ],
//         "columnDefs": [
//             { 
//                 "targets": 0, // Assure-toi que l'index est correct pour la colonne date
//                 "type": "date"
//             }
//         ]
//     });
// });
