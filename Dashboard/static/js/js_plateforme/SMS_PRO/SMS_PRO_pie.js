// Premier graphique
const doughnutdmc = "/dashboard/sms_pro_pie/";
const updateRequestNew = new Request(doughnutdmc, { method: 'GET' });

fetch(updateRequestNew)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        var ctx1 = document.getElementById('myPieChart1').getContext('2d');

        function generateColors(numColors) {
            var colors = [];
            for (var i = 0; i < numColors; i++) {
                colors.push('#' + Math.floor(Math.random() * 16777215).toString(16));
            }
            return colors;
        }

        var backgroundColor = generateColors(data.labels.length);

        var myPieChart1 = new Chart(ctx1, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: backgroundColor,
                    hoverBackgroundColor: backgroundColor.map(color => color + 'CC'),
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                var label = context.label;
                                var value = context.raw;

                                // Calculer le pourcentage
                                var total = context.chart.data.datasets[0].data.reduce((acc, curr) => acc + curr, 0);
                                var percentage = ((value / total) * 100).toFixed(2);

                                return `${label}: ${percentage}% (${value})`;
                            }
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                    },
                },
                cutout: '80%',
            },
        });
    })
    .catch(error => {
        console.error("Erreur:", error);
        document.getElementById('myPieChart1').innerHTML = "Erreur lors du chargement des données: " + error.message;
    });

// Deuxième graphique
const doughnutErrorDmc = "/dashboard/sms_pro_pie_error/";
const updateRequestError = new Request(doughnutErrorDmc, { method: 'GET' });

fetch(updateRequestError)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        var ctx2 = document.getElementById('myPieChart2').getContext('2d');

        function generateColors(numColors) {
            var colors = [];
            for (var i = 0; i < numColors; i++) {
                colors.push('#' + Math.floor(Math.random() * 16777215).toString(16));
            }
            return colors;
        }

        var backgroundColor = generateColors(data.labels.length);

        var myPieChart2 = new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: backgroundColor,
                    hoverBackgroundColor: backgroundColor.map(color => color + 'CC'),
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                var label = context.label;
                                var value = context.raw;

                                // Calculer le pourcentage
                                var total = context.chart.data.datasets[0].data.reduce((acc, curr) => acc + curr, 0);
                                var percentage = ((value / total) * 100).toFixed(2);

                                return `${label}: ${percentage}% (${value})`;
                            }
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                    },
                },
                cutout: '80%',
            },
        });
    })
    .catch(error => {
        console.error("Erreur:", error);
        document.getElementById('myPieChart2').innerHTML = "Erreur lors du chargement des données: " + error.message;
    });
