let canvas;
let context;

let fpsInterval = 1000/30; // the denominator is FPS
// FINISH FROM SLIDES

let x = 250;
let y = 150;
let size = 10;
let xChange = randint(-10,10);
let yChange = randint(-10,10);
// Variable statements that aren't in a function are global

document.addEventListener("DOMContentLoaded", init, false); // the js will wait for the page to fully load then run the init function

function init() {
    canvas = document.querySelector("canvas");
    context = canvas.getContext("2d"); // This variable will do the "drawing" on the canvas

    draw();
}

function draw() {
    window.requestAnimationFrame(draw);
    context.clearRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = "yellow";
    context.fillRect(x, y, size, size); // In CompSci, co-ords function differently, the top left is (0,0)
    if (x >= canvas.width || x <= 0){
        xChange = xChange * -1;
    }

    if (y >= canvas.height || y <= 0){
        yChange = yChange * -1;
    }
    x = x + xChange;
    y = y + yChange;
    context.fillRect(x, y, size, size);
}

function randint(min, max) {
    return Math.round(Math.random() * (max-min))+ min;
}