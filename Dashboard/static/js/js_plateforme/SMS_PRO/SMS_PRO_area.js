document.addEventListener('DOMContentLoaded', function () {
    const areaUrl = "/dashboard/sms_pro_area/";
    const sheetsUrl = "/dashboard/get_sheets/";
    let myLineChart;

    const filterButton = document.getElementById('filterButton');
    filterButton.addEventListener('click', function () {
        const dateDebut = document.getElementById('date_debut').value;
        const dateFin = document.getElementById('date_fin').value;

        if (dateDebut && dateFin) {
            // Envoyez les dates au format ISO pour éviter les problèmes de formatage
            console.log("Filtrage avec dates :", dateDebut, dateFin);
            fetchDataAndUpdateChart(dateDebut, dateFin);
        } else {
            console.log("Veuillez sélectionner une plage de dates valide");
        }
    });

    function populateSheetSelector() {
        fetch(sheetsUrl)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                const sheetSelector = document.getElementById('sheetSelector');
                sheetSelector.innerHTML = '';

                data.sheets.forEach(sheet => {
                    const option = document.createElement('option');
                    option.value = sheet;
                    option.textContent = sheet;
                    sheetSelector.appendChild(option);
                });

                if (data.sheets.length > 0) {
                    fetchDataAndUpdateChart(data.sheets[0]);
                }
            })
            .catch(error => {
                console.error("Erreur lors du chargement des feuilles :", error);
            });
    }

    function fetchDataAndUpdateChart(dateDebut = null, dateFin = null) {
        let urlWithParams = `${areaUrl}`;
        
        if (dateDebut && dateFin) {
            urlWithParams += `?date_debut=${encodeURIComponent(dateDebut)}&date_fin=${encodeURIComponent(dateFin)}`;
        }
        
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

                updateChart(labels, line_data);
            })
            .catch(error => {
                console.error("Erreur lors du chargement du graphique :", error);
            });
    }

    function updateChart(labels, data) {
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
                    data: data,
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
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
});