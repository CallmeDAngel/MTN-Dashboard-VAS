document.addEventListener('DOMContentLoaded', function () {
    const areaUrl = "/dashboard/ussd_area/";
    let myLineChart;

    // Fonction pour mettre à jour le graphique
    function fetchDataAndUpdateChart(startDate, endDate) {
        const urlWithParams = `/dashboard/ussd_area/?start_date=${startDate}&end_date=${endDate}`;
        
        fetch(urlWithParams)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
    
                const labels = data.labels;
                const line_data = data.line_data;
    
                console.log("Labels reçus :", labels);
                console.log("Données reçues :", line_data);
    
                const ctx = document.getElementById("myAreaChart").getContext('2d');
    
                if (myLineChart) {
                    myLineChart.destroy();
                }
    
                myLineChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: "Success % with exclusion",
                            data: line_data,
                            lineTension: 0.3,
                            backgroundColor: "rgba(78, 115, 223, 0.05)",
                            borderColor: "rgba(78, 115, 223, 1)",
                            pointRadius: 3,
                            pointBackgroundColor: "rgba(78, 115, 223, 1)",
                            pointBorderColor: "rgba(78, 115, 223, 1)",
                            pointHoverRadius: 3,
                            pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                            pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                        }],
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                            },
                        }
                    }
                });
            })
            .catch(error => {
                console.error("Erreur lors du chargement du graphique :", error);
            });
    }    

    // Ajouter l'écouteur d'événement pour le bouton
    document.getElementById('updateChart').addEventListener('click', function () {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        if (startDate && endDate) {
            fetchDataAndUpdateChart(startDate, endDate);
        } else {
            alert('Veuillez sélectionner une plage de dates.');
        }
    });

    // Charger les données initiales avec une plage de dates par défaut (par exemple, le mois dernier)
    const start = new Date();
    start.setMonth(start.getMonth() - 1);
    const end = new Date();

    document.getElementById('startDate').value = start.toISOString().split('T')[0];
    document.getElementById('endDate').value = end.toISOString().split('T')[0];

    fetchDataAndUpdateChart(start.toISOString().split('T')[0], end.toISOString().split('T')[0]);
});
