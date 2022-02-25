API_KEY = "7666b7a2889d6bd686dc";

function convertCurrency(fromCurrency, toCurrency, amount) {
    if (amount = ""){
        amount = null;
    }

    let query = fromCurrency + "_" + toCurrency + "," + toCurrency + "_" + fromCurrency;
    query = query.toUpperCase();
    fetch(`https://free.currconv.com/api/v7/convert?q=${query}&compact=ultra&apiKey=${API_KEY}`)
    .then(response => response.json())
    .then(data => console.log(data));
}
