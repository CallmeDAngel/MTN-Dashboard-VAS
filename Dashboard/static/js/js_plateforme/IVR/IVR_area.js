// Définition de l'URL de l'API
const areaUrl = "/dashboard/ivr_area/";

// Envoi de la requête fetch à l'API
fetch(areaUrl)
    .then(response => response.json())
    .then(data => {
        // Vérification s'il y a une erreur dans les données reçues
        if (data.error) {
            throw new Error(data.error);
        }

        // Extraction des données depuis la réponse
        const labels = data.labels;
        const line_data = data.line_data;

        // Vérification et affichage des données extraites pour le débogage
        console.log("Labels reçus :", labels);
        console.log("Données reçues :", line_data);

        // Obtention du contexte du canvas où le graphique sera dessiné
        const ctx = document.getElementById("myAreaChart").getContext('2d');

        // Création du graphique Chart.js
        const myLineChart = new Chart(ctx, {
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

            // options: {
            //     maintainAspectRatio: false,
            //     layout: {
            //         padding: {
            //             left: 10,
            //             right: 25,
            //             top: 25,
            //             bottom: 0
            //         }
            //     },
            //     scales: {
            //         x: {
            //             type: 'time',
            //             time: {
            //                 unit: 'date',
            //                 tooltipFormat: 'DD/MM/YYYY',  // Ajustez ce format à vos besoins
            //             },
            //             grid: {
            //                 display: false,
            //                 drawBorder: false
            //             },
            //             ticks: {
            //                 maxTicksLimit: 7
            //             }
            //         },
            //         y: {
            //             ticks: {
            //                 maxTicksLimit: 5,
            //                 padding: 10,
            //             },
            //             grid: {
            //                 color: "rgb(234, 236, 244)",
            //                 zeroLineColor: "rgb(234, 236, 244)",
            //                 drawBorder: false,
            //                 borderDash: [2],
            //                 zeroLineBorderDash: [2]
            //             }
            //         },
            //     },
            //     plugins: {
            //         legend: {
            //             display: true,
            //             position: 'top'
            //         },
            //         tooltip: {
            //             backgroundColor: "rgb(255,255,255)",
            //             bodyColor: "#858796",
            //             titleMarginBottom: 10,
            //             titleColor: '#6e707e',
            //             titleFont: {
            //                 size: 14
            //             },
            //             borderColor: '#dddfeb',
            //             borderWidth: 1,
            //             padding: 15,
            //             displayColors: false,
            //             intersect: false,
            //             mode: 'index',
            //             caretPadding: 10,
            //             callbacks: {
            //                 label: function(context) {
            //                     const label = context.dataset.label || '';
            //                     const value = context.parsed.y || 0;
            //                     return `${label}: ${value}%`;
            //                 }
            //             }
            //         }
            //     }
            // }
        });
    })
    .catch(error => {
        console.error("Erreur lors du chargement du graphique :", error);
        // Afficher un message d'erreur à l'utilisateur si nécessaire
    });
