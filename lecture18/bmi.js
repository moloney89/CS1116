let weight;
let weight_errors;
let height;
let height_errors;
let bmi;
let form;

document.addEventListener("DOMContentLoaded", init, false)

/* 
We have now written this program where all of the work is done server-side, and where all of the work is done cleint-side.
There are benefits to each approach, but what are the tradeoffs?
While it may seem like there are less requests required for the JS approach, for the first use, there is the same amount of requests performed. 
However, if you want to run the program multiple times, javascript is better (assuming there is a cache) as the browser only needs to request the program once.

When must we use a server-side approach?
-- When there is a database, broadly speaking, there should only be one copy of a database.

*/

function init() {
    // The querySelectors below use CSS selectors to "find" items within the document
    weight = document.querySelector("#weight");
    weight_errors = document.querySelector("#weight_errors");
    height = document.querySelector("#height");
    height_errors = document.querySelector("#height_errors");
    bmi = document.querySelector("#bmi");
    form = document.querySelector("form");
    form.addEventListener("submit", calculate_bmi, false); // This line is event driven programming, it is telling the form to listen for
                                                           // the submit button being pressed.
}

function check_for_float(text, minimum, maximum) {
    let trimmed_text = text.trim(); // trim() works the same as the strip method in Python.
    if (trimmed_text === "") {
        return "Required";
    }
    let number = parseFloat(trimmed_text); // If you use parseFloat on something that is not a number, it becomes NaN (Not a Number)
    if (isNaN(number)) { // isNaN is a built-in function to check if something is NaN
        return "Must be a number";
    }
    if (number < minimum) {
        return "Must be no less than " + minimum;
    }
    if (number > maximum) {
        return "Must be no greater than " + maximum;
    }
    return ""; // i.e. No errors
}

function calculate_bmi(event) {
    // Validate user input
    let weight_error_message = check_for_float(weight.value, 10, 200);
    let height_error_message = check_for_float(height.value, 0.5, 2.5);
    if (weight_error_message || height_error_message) {
        weight_errors.innerHTML = weight_error_message; // These lines add the contents of weight_error_message/height_error_message to the corresponding span
        height_errors.innerHTML = height_error_message; // in the HTML.
    } else { // both are empty string -> valid input
        bmi.value = weight.value / (height.value * height.value); // .value gets the text value from the variable, e.g. weight.value = users weight input
    } 
    event.preventDefault(); // Normally, when submit is pressed, the data is sent to the server; This line prevents that behaviour
}