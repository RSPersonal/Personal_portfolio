const valuesToCheck = {};
valuesToCheck['mainElements'] = [];
const portfolioOveralReturn = {};
portfolioOveralReturn['item'] = 'portfolioOveralReturn';
portfolioOveralReturn['divID'] = 'overalReturnDiv';
portfolioOveralReturn['value'] = JSON.parse(document.getElementById("portfolioOveralReturn").textContent);
valuesToCheck.mainElements.push(portfolioOveralReturn);

const dailyReturn = {};
dailyReturn['item'] = 'dailyReturn';
dailyReturn['divID'] = 'dailyReturnDiv';
// TODO: Daily return still needs to be calculated and prepared for this value
dailyReturn['value'] = JSON.parse(document.getElementById("portfolioDailyReturn").textContent);
valuesToCheck.mainElements.push(dailyReturn);

valuesToCheck.mainElements.forEach(item => {
    let itemValue = item.value;
    if (itemValue < 0) {
        const element = document.getElementById(item.divID);
        element.style.backgroundColor='red';
    }
})