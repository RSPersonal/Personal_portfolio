const valuesToCheck = {};

// We first want to get the daily return data before we check on values to make the corresponding colors 
const portfolioID = JSON.parse(document.getElementById("portfolioID").textContent);
let fetchedLatestPrice;

fetch(`http://127.0.0.1:8000/api/v1/daily-return/${portfolioID}`)
    .then((response) => response.json())
    .then((data) => {
        fetchedLatestPrice = -100;// data.data[0].last_price;
        if (fetchedLatestPrice) {
            document.getElementById("dailyReturnItem").innerHTML = `€ ${fetchedLatestPrice.toLocaleString()}`;
        }
    })
    .catch((error) => {
        console.warn(error);
    });    

// Portfolio overal return
valuesToCheck['mainElements'] = [];
const portfolioOveralReturn = {};
portfolioOveralReturn['item'] = 'portfolioOveralReturn';
portfolioOveralReturn['divID'] = 'overalReturnDiv';
portfolioOveralReturn['value'] = JSON.parse(document.getElementById("portfolioOveralReturn").textContent);
valuesToCheck.mainElements.push(portfolioOveralReturn);

// Portfolio daily return
// TODO daily return div is to slow from api call which results in async checking of negative value
// Meaning the call is to slow and the value gets checked to fast for positive or negative
const dailyReturn = {};
dailyReturn['item'] = 'dailyReturn';
dailyReturn['divID'] = 'dailyReturnDiv';
dailyReturn['value'] = JSON.parse(document.getElementById("portfolioDailyReturn").textContent);
valuesToCheck.mainElements.push(dailyReturn);

valuesToCheck.mainElements.forEach(item => {
    let itemValue = item.value;
    if (itemValue < 0) {
        const element = document.getElementById(item.divID);
        element.style.backgroundColor='red';
        element.style.borderRadius= "5px";
    }
})