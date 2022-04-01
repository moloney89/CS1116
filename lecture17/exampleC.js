let img_element;

document.addEventListener("DOMContentLoaded", init, false);

function init() {
    img_element = document.querySelector("img");
    img_element.src = "frown.jpg";
    img_element.addEventListener("mouseover", make_it_smile, false);
    img_element.addEventListener("mouseout", make_it_frown, false);
}

function make_it_smile() {
    img_element.src = "smile.jpg";
}

function make_it_frown() {
    img_element.src = "frown.jpg";
}

