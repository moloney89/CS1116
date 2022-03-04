let canvas;
let context;

let fpsInterval = 1000/30; // the denominator is FPS
let now;
let then = Date.now();

let particles = [];


// Variable statements that aren't in a function are global

document.addEventListener("DOMContentLoaded", init, false); // the js will wait for the page to fully load then run the init function

function init() {
    canvas = document.querySelector("canvas");
    context = canvas.getContext("2d"); // This variable will do the "drawing" on the canvas

    

    draw();
}

function draw() {
    window.requestAnimationFrame(draw);
    let now = Date.now();
    let elapsed = now-then;
    if (elapsed <= fpsInterval) {
        return;
    }
    then = now - (elapsed % fpsInterval);

    for (let i = 0; i < 30; i += 1) {
        let p = {
            x : 250,
            y : 150,
            size : 10,
            xChange : randint(-10,10),
            yChange : randint(-10,10)
        };
        particles.push(p);
    }

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "yellow";

    for (let p of particles){
        context.fillRect(p.x, p.y, p.size, p.size); 
    }
    for (let p of particles){
        p.x = p.x + p.xChange;
        p.y = p.y + p.yChange;
        p.yChange = p.yChange + 1.5; // This gives a visual effect similar to gravity
    }

    
    
    

}

function randint(min, max) {
    return Math.round(Math.random() * (max-min))+ min;
}