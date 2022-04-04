let randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);

function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}
countPositions =

let barColors = [];
for (let i = 0; i < countPositions; i++) {
    randomGeneratedColor = rgbToHex(randomNum(), randomNum(), randomNum());
    while (barColors.includes(randomGeneratedColor)) {
        randomGeneratedColor = rgbToHex(randomNum(), randomNum(), randomNum());
    }
    barColors.push(randomGeneratedColor);
}

let config = {
    type: 'pie',
    data: {
        datasets: [{
            data: [20, 30, 30],
            backgroundColor: barColors,
            label: 'Stock ticker'
        }],
        labels: ['APPL']
    },
    options: {
        responsive: true
    }
};

window.onload = function() {
    let ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
};