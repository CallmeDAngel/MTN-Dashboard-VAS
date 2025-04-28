document.addEventListener('DOMContentLoaded', function () {
    const BarLineErrorurl = "/dashboard/sms_bar_line_error/";
    const sheetErrorsUrl = "/dashboard/get_sheets_error/";
    let myBarLineChartError;
    
    function populateSheetSelector() {
        fetch(sheetErrorsUrl)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
    
                const sheetSelector = document.getElementById('sheetErrorSelector');
                    
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
        const urlWithParams = `${BarLineErrorurl}?sheet=${sheetName}`;
            
        fetch(urlWithParams)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
    
                const labels = data.labels;
                const barline_data = data.line_data;
    
                console.log("Labels reçus :", labels);
                console.log("Données reçues :", barline_data);
    
                const ctx = document.getElementById("myBarLineChartError").getContext('2d');
    
                if (myBarLineChartError) {
                    myBarLineChartError.destroy();
                }
    
                myBarLineChartError = new Chart(ctx, {
                    type: 'bar', // Le type principal du graphique est 'bar'
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Nombre',
                                data: data.bar_data,
                                borderColor: "#4e73df",
                                backgroundColor: "#4e73df",
                                hoverBackgroundColor: "#2e59d9",
                                yAxisID: 'y-axis-1', // Associe cet ensemble à l'axe 'y-axis-1'
                                order: 1
                            },
                            {
                                label: '%',
                                data: data.line_data,
                                borderColor: "#e74a3b",
                                backgroundColor: 'transparent',
                                yAxisID: 'y-axis-2', // Associe cet ensemble à l'axe 'y-axis-2'
                                type: 'line',
                                borderWidth: 2,
                                pointBackgroundColor: "#e74a3b",
                                pointBorderColor: "#fff",
                                pointBorderWidth: 2,
                                pointRadius: 5,
                                tension: 0.1, // Ajuste la courbure de la ligne
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
    const sheetSelector = document.getElementById('sheetErrorSelector');
    sheetSelector.addEventListener('change', function () {
        const selectedSheet = this.value;
        console.log("Feuille sélectionnée :", selectedSheet);
        fetchDataAndUpdateChart(selectedSheet);
    });
});
