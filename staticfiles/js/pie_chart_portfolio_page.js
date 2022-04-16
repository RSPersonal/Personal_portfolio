const config = {
    type: 'pie',
    data: {
        datasets: [{
            data: {
                {
                    data | safe
                }
            },
            backgroundColor: [

            ],
            label: 'Stock ticker'
        }],
        labels: {
            {
                labels | safe
            }
        }
    },
    options: {
        responsive: true
    }
};

window.onload = function() {
    let ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
};
helpers.each(dataset.data, function(dataPoint, index) {
    //Add a new point for each piece of data, passing any required data to draw.

    datasetObject.bars.push(new this.BarClass({
        value: dataPoint,
        label: data.labels[index],
        datasetLabel: dataset.label,
        strokeColor: dataset.strokeColor,
        fillColor: getRandomColor(),
        highlightFill: dataset.highlightFill || dataset.fillColor,
        highlightStroke: dataset.highlightStroke || dataset.strokeColor
    }));
}, this);