$(document).ready(function() {

    var ambient = [
        {
            x: ambient_dates,
            y: ambient_data,
            mode: 'lines+markers',
            type: 'scatter',
            name: "Ambient",
            marker: {
                size: 2,
                color: 'blue'
            },
            opacity: 0.4
        }
    ];

    var cowling = [
        {
            x: cowling_dates,
            y: cowling_data,
            mode: 'lines+markers',
            type: 'scatter',
            name: "Cowl",
            marker: {
                size: 2,
                color: 'red'
            },
            opacity: 0.4
        }
    ];

    var layout = {
        showlegend: false,
        xaxis: {
            autorange: true,
            showgrid: false,
            zeroline: false,
            showline: false,
            autotick: true,
            ticks: '',
            showticklabels: false
        },
        yaxis: {
            autorange: true,
            showgrid: false,
            zeroline: false,
            showline: false,
            autotick: true,
            ticks: '',
            showticklabels: false
        },
        margin: {
            l: 0,
            r: 0,
            t: 0,
            b: 0
        },
        height: 200,
    };

    Plotly.newPlot('chart', ambient, layout);
    Plotly.addTraces('chart', cowling)

});
