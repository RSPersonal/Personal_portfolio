let meanPriceField: number | HTMLElement;
let percentageField: number | HTMLElement;
let timesClicked = 0;

const percentageButton = document.getElementById("bidPercentageButton") as HTMLElement | null;
inferface percentageField {
    new (): HTMLElement | null;
}
percentageField = document.getElementById("biddingPercentage") as HTMLElement | null;
let meanPrice = JSON.parse(document.getElementById("meanPriceJson").textContent);

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
