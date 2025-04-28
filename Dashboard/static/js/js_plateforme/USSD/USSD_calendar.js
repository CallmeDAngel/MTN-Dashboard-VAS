$(function() {
    $('#dateRangePicker').daterangepicker({
        locale: {
            format: 'DD/MM/YYYY'
        },
        startDate: moment().subtract(29, 'days'),
        endDate: moment()
    }, function(start, end, label) {
        console.log("Plage de dates sélectionnée : " + start.format('DD/MM/YYYY') + ' au ' + end.format('DD/MM/YYYY'));

        // Envoyer une requête AJAX avec les dates sélectionnées
        $.ajax({
            url: '/ussd_area/',  // URL de la vue Django
            data: {
                start_date: start.format('DD/MM/YYYY'),
                end_date: end.format('DD/MM/YYYY'),
                sheet: 'Aug 24'  // Tu peux changer cela pour la feuille sélectionnée dynamiquement
            },
            success: function(response) {
                // Actualiser le diagramme avec les nouvelles données
                updateChart(response.labels, response.line_data);
            },
            error: function(xhr) {
                alert('Erreur lors de la récupération des données.');
            }
        });
    });
});

function updateChart(labels, data) {
    // Met à jour le diagramme ici (par exemple avec Chart.js)
    // Remplacer ceci par ton code pour mettre à jour le graphique avec les nouvelles données
    console.log(labels, data);
}
