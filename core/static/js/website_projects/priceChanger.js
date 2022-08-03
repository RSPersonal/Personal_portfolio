let meanPriceField;
let percentageField;
let timesClicked = 0;

const percentageButton = document.getElementById("bidPercentageButton");
percentageField = document.getElementById("biddingPercentage");
meanPrice = JSON.parse(document.getElementById("meanPriceJson").textContent);

if (percentageButton) {
    percentageButton.addEventListener("click", () => {
        changePriceBasedOnPercentage();
    })
}

function changePriceBasedOnPercentage() {
    const convertedInputToPercentage = percentageField.value / 100
    const newPriceFromCalculation = Math.floor(meanPrice * convertedInputToPercentage) + meanPrice;
    document.getElementById("meanPrice").innerHTML = "€ " + newPriceFromCalculation.toLocaleString();
}
