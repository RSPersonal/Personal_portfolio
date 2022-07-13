let priceField;
let percentageField;
let timesClicked = 0;

percentageButton = document.getElementById("bidPercentageButton")
percentageField = document.getElementById("biddingPercentage");

percentageButton.addEventListener("click", () => {
    changePriceBasedOnPercentage();
})


function changePriceBasedOnPercentage() {
    priceField = document.getElementById("meanPrice").innerHTML = percentageField.value;
}