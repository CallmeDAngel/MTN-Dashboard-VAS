document.addEventListener('DOMContentLoaded', function () {
    const BarLineNormalUrl = "/dashboard/crbt_bar_line/";
    const sheetNormalUrl = "/dashboard/get_sheets/";
    let myBarLineChart;

    function populateSheetSelector() {
        fetch(sheetNormalUrl)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                const sheetSelector = document.getElementById('sheetBarSelector');
                    
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
        console.log(`Fetching data for sheet: ${sheetName}`);
        const urlWithParams = `${BarLineNormalUrl}?sheet=${sheetName}`;
            
        fetch(urlWithParams)
            .then(response => response.json())
            .then(data => {
                console.log("Data received from server:", data);
                if (data.error) {
                    throw new Error(data.error);
                }
    
                const labels = data.labels;
                const bar_data = data.bar_data;
                const line_data = data.line_data;
    
                console.log("Labels reçus :", labels);
                console.log("Données Bar :", bar_data);
                console.log("Données Line :", line_data);
    
                const ctx = document.getElementById("myBarLineChart").getContext('2d');
    
                if (myBarLineChart) {
                    myBarLineChart.destroy();
                }
    
                myBarLineChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Total',
                                data: bar_data,
                                borderColor: "#4e73df",
                                backgroundColor: "#4e73df",
                                hoverBackgroundColor: "#2e59d9",
                                yAxisID: 'y-axis-1',
                                order: 1
                            },
                            {
                                label: 'Success % without exclusion',
                                data: line_data,
                                borderColor: "#e74a3b",
                                backgroundColor: 'transparent',
                                yAxisID: 'y-axis-2',
                                type: 'line',
                                borderWidth: 2,
                                pointBackgroundColor: "#e74a3b",
                                pointBorderColor: "#fff",
                                pointBorderWidth: 2,
                                pointRadius: 5,
                                tension: 0.1,
                                order: 0
                            }
                        ]
                    },
                });
            })
            .catch(error => {
                console.error("Erreur lors du chargement du graphique :", error);
            });
    }
    

    // Initialiser le sélecteur avec les feuilles disponibles
    populateSheetSelector();

    // Ajout de l'écouteur sur le sélecteur
    const sheetSelector = document.getElementById('sheetBarSelector'); // Utiliser le bon ID ici
    sheetSelector.addEventListener('change', function () {
        const selectedSheet = this.value;
        console.log("Feuille sélectionnée :", selectedSheet);
        fetchDataAndUpdateChart(selectedSheet);
    });
});
