/**
 * Created by adagio on 2018-09-04.
 */

/* PCA implementation */

//##################################################################
all_data = JSON.parse(pca_all);

var ctx = document.getElementById("myChart2").getContext('2d');

var scatterChart2 = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'zero',
            borderColor: '#DAA2DA',
            backgroundColor: 'white',
            data: all_data['zero']
        },{
            label: 'one',
            borderColor: '#BED905',
            backgroundColor: 'white',
            data: all_data['one']
        },{
            label: 'two',
            borderColor: '#0ba804',
            backgroundColor: 'white',
            data: all_data['two']
        },{
            label: 'three',
            borderColor: '#C0334D',
            backgroundColor: 'white',
            data: all_data['three']
        },{
            label: 'four',
            borderColor: '#16235A',
            backgroundColor: 'white',
            data: all_data['four']
        },{
            label: 'five',
            borderColor: '#888C46',
            backgroundColor: 'white',
            data: all_data['five']
        },{
            label: 'six',
            borderColor: '#F3B05A',
            backgroundColor: 'white',
            data: all_data['six']
        },{
            label: 'seven',
            borderColor: '#F46A4E',
            backgroundColor: 'white',
            data: all_data['seven']
        },{
            label: 'eight',
            borderColor: '#BF9D7A',
            backgroundColor: 'white',
            data: all_data['eight']
        },{
            label: 'nine',
            borderColor: '#A4A4BF',
            backgroundColor: 'white',
            data: all_data['nine']
        }
        ]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                ticks: {
                    max: 40,
                    min: -40
                }
            }],
            yAxes: [{
                type: 'linear',
                position: 'left',
                ticks: {
                    max: 40,
                    min: -40
                }
            }]
        },
        legend: {
          position: 'bottom',
          labels: {
            fontSize: 12,
            boxWidth: 10,
            usePointStyle: true
          }
        },
        tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
                label: function(tooltipItems, data) {
                    return data.datasets[tooltipItems.datasetIndex].label;
                    //return data.datasets[tooltipItems.datasetIndex].label;
                }
            }
        }
    }
});










