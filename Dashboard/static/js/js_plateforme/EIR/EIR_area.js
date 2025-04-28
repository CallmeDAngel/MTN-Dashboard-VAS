document.addEventListener('DOMContentLoaded', function () {
    const areaUrl = "/dashboard/eir_area/";
    const sheetsUrl = "/dashboard/get_sheets/";
    let myLineChart;

    function populateSheetSelector() {
        fetch(sheetsUrl)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                const sheetSelector = document.getElementById('sheetSelector');
                
                // Vider le sélecteur avant d'ajouter de nouvelles options
                sheetSelector.innerHTML = '';

                // Ajouter chaque feuille comme option
                data.sheets.forEach(sheet => {
                    const option = document.createElement('option');
                    option.value = sheet;
                    option.textContent = sheet;
                    sheetSelector.appendChild(option);
                });

                // Charger la première feuille par défaut
                if (data.sheets.length > 0) {
                    fetchDataAndUpdateChart(data.sheets[0]);
                }
            })
            .catch(error => {
                console.error("Erreur lors du chargement des feuilles :", error);
            });
    }

    function fetchDataAndUpdateChart(sheetName) {
        const urlWithParams = `${areaUrl}?sheet=${sheetName}`;
        
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

    // Initialiser le sélecteur avec les feuilles disponibles
    populateSheetSelector();

    // Ajout de l'écouteur sur le sélecteur
    const sheetSelector = document.getElementById('sheetSelector');
    sheetSelector.addEventListener('change', function () {
        const selectedSheet = this.value;
        console.log("Feuille sélectionnée :", selectedSheet);
        fetchDataAndUpdateChart(selectedSheet);
    });
});
