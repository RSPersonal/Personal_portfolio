let autocomplete;
let address1Field;
let streetField;
let houseNumberField;
let postalField;
let cityField;
const scriptOn = true;

if (scriptOn) {
    function initAutocomplete() {
        address1Field = document.querySelector("#addressSearchBar");
        streetField = document.querySelector("#street")
        houseNumberField = document.querySelector("#houseNumber");
        cityField = document.querySelector("#city");
        postalField = document.querySelector("#postcode");
        autocomplete = new google.maps.places.Autocomplete(
            document.getElementById('addressSearchBar'),
            {
                types: ['address'],
                componentRestrictions: { 'country': ['NL'] },
                fields: ['formatted_address', 'address_components'],
            });
        address1Field.focus();
        autocomplete.addListener("place_changed", fillInAddress);
    }


    function fillInAddress() {
        const place = autocomplete.getPlace();
        // returns Meestersweg 4, 7951 BS Staphorst, Netherlands
        let address1 = "";
        let postcode = "";
        for (const component of place.address_components) {
            const componentType = component.types[0];
            switch (componentType) {
                case "street_number": {
                    address1 = `${component.long_name} ${address1}`;
                    document.querySelector("#houseNumber").value = component.long_name;
                    break;
                }
                case "route": {
                    address1 += component.short_name;
                    document.querySelector("#street").value = component.long_name;
                    break;
                }
                case "postal_code": {
                    postcode = `${component.long_name}${postcode}`;
                    break;
                }
                case "postal_code_suffix": {
                    postcode = `${postcode}- ${component.long_name}`;
                    break;
                }
                case "locality": {
                    document.querySelector("#locality").value = component.long_name;
                    break;
                }
            }
            postalField.value = postcode;
        }
    }
};
