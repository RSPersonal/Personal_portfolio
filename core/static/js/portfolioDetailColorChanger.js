const valuesToCheck = {};

// We first want to get the daily return data before we check on values to make the corresponding colors
const portfolioID = JSON.parse(document.getElementById("portfolioID").textContent);
const apiHost = JSON.parse(document.getElementById("apiHost").textContent);
console.log(apiHost);



fetch(`${apiHost}api/v1/daily-return/${portfolioID}`)
    .then((response) => response.json())
    .then((data) => {
        let fetchedLatestPrice;
        if (data.data[0]) {
            fetchedLatestPrice = data.data[0].last_price;
            console.log(fetchedLatestPrice);
        } else {
            fetchedLatestPrice = 0;
        }
        document.getElementById("dailyReturnItem").innerHTML = `€ ${fetchedLatestPrice.toLocaleString()}`;
        
        // Portfolio overal return
        valuesToCheck['mainElements'] = [];
        const portfolioOveralReturn = {};
        portfolioOveralReturn['item'] = 'portfolioOveralReturn';
        portfolioOveralReturn['divID'] = 'overalReturnDiv';
        portfolioOveralReturn['value'] = JSON.parse(document.getElementById("portfolioOveralReturn").textContent);
        valuesToCheck.mainElements.push(portfolioOveralReturn);

        // Portfolio daily return
        const dailyReturn = {};
        dailyReturn['item'] = 'dailyReturn';
        dailyReturn['divID'] = 'dailyReturnDiv';
        dailyReturn['value'] = fetchedLatestPrice;
        valuesToCheck.mainElements.push(dailyReturn);

        valuesToCheck.mainElements.forEach(item => {
            let itemValue = parseFloat(item.value);
            console.log(itemValue);
            if (itemValue < 0) {
                const element = document.getElementById(item.divID);
                console.log(element, itemValue, itemValue < 0);
                element.style.backgroundColor = 'red';
                element.style.borderRadius = "5px";
            }
        })
    })
    .catch((error) => {
        console.warn(error);
    });
