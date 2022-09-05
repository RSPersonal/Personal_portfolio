const portfolioID = JSON.parse(document.getElementById("portfolioID").textContent);
let fetchedLatestPrice;

fetch(`http://127.0.0.1:8000/api/v1/daily-return/${portfolioID}`)
.then(function (response) {
    return response.json();
})
.then(function (data) {
    fetchedLatestPrice = data.data[0].last_price;
    if (fetchedLatestPrice) {
        document.getElementById("dailyReturnItem").innerHTML = `€ ${fetchedLatestPrice}`);
        }
    }
}).catch(function (error) {
    console.warn(error);
});
