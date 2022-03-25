    let config = {
      type: 'pie',
      data: {
        datasets: [{
          data: {{ data|safe }},
          backgroundColor: [

          ],
          label: 'Stock ticker'
        }],
        labels: {{ labels|safe }}
      },
      options: {
        responsive: true
      }
    };

    window.onload = function() {
      let ctx = document.getElementById('pie-chart').getContext('2d');
      window.myPie = new Chart(ctx, config);
    };