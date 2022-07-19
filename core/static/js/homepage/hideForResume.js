let hideButton = document.getElementById("hideButton");

hideButton.onclick = function () {
    const listOfDivs = ["navBarHomepageRs", "visitorCount", "nLButton"]
    for (const div of listOfDivs) {
        console.log(div);
        toHideDiv = document.getElementById(div);
        if (toHideDiv.style.display !== 'none') {
            toHideDiv.style.display = 'none';
        } else {
            toHideDiv.style.display = 'block';
        }
    }
};
