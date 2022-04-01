let canvas;
let context;

let request_id;
let fpsInterval = 1000/30; // the denominator is FPS
let now;
let then = Date.now();

let asteroids = [];

let player = {
    x : 0,
    y : 150,
    size : 10
}

let moveLeft = false;
let moveUp = false;
let moveRight = false;
let moveDown = false;


// Variable statements that aren't in a function are global

document.addEventListener("DOMContentLoaded", init, false); // the js will wait for the page to fully load then run the init function

function init() {
    canvas = document.querySelector("canvas");
    context = canvas.getContext("2d"); // This variable will do the "drawing" on the canvas

    window.addEventListener("keydown", activate, false); // when a key is pressed, run the function 'activate'
    window.addEventListener("keyup", deactivate, false); // when a key is depressed, run the function 'deactivate
    draw();
}

function draw() {
    request_id = window.requestAnimationFrame(draw);
    let now = Date.now();
    let elapsed = now-then;
    if (elapsed <= fpsInterval) {
        return;
    }
    then = now - (elapsed % fpsInterval);

    if (asteroids.length < 10) {
        let a = {
            x : canvas.width, // asteroid will generate off the edge of the canvas
            y : randint(0, canvas.height),
            size : randint(5, 15),
            xChange : randint(-10,-1), // asteroid can only move from right to left
            yChange : 0
        };
        asteroids.push(a);
    }
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "yellow";
    for (let a of asteroids){
        context.fillRect(a.x, a.y, a.size, a.size); 
    }
    context.fillStyle = "cyan";
    context.fillRect(player.x, player.y, player.size, player.size); // Draw the player in cyan

    // Game ending conditions: 
    // // Reaching the right edge
    if (player.x + player.size >= canvas.width) {
        stop("You've Won!");
        return;
    }
    // // Colliding with an asteroid
    for (let a of asteroids) {
        if (player_collides(a)) {
            stop("You've Lost. Loser!")
            return;
        }
    }

    for (let a of asteroids){
        if (a.x + a.size < 0) { // if the top right (x + width) of the particle is off the left of the screen
            a.x=canvas.width // put the particle on the right side
            a.y=randint(0, canvas.height) // at a random height
        } else {
            a.x = a.x + a.xChange;
            a.y = a.y + a.yChange;
        }
    }
    if (moveRight) {
        player.x = player.x + player.size;
    }
    if (moveUp) {
        player.y = player.y - player.size;
    }
    if (moveDown) {
        player.y = player.y + player.size;
    }
    if (moveLeft) {                          // Game objective is to get to the right of the screen, therefore you shouldn't be able to go back
        player.x = player.x - player.size;
    }
}

function randint(min, max) {
    return Math.round(Math.random() * (max-min))+ min;
}

function activate(event) {
    let key = event.key;
    if (key === "ArrowUp") {
        moveUp = true;
    } else if (key === "ArrowRight") {
        moveRight = true;
    } else if (key === "ArrowDown") {
        moveDown = true;
    }
}

function deactivate(event) {
    let key = event.key;  
    if (key === "ArrowUp") {
        moveUp = false;
    } else if (key === "ArrowRight") {
        moveRight = false;
    } else if (key === "ArrowDown") {
        moveDown = false;
    }     
}

function player_collides(a) {
    if (player.x + player.size < a.x ||
        a.x + a.size < player.x ||
        player.y > a.y + a.size ||
        a.y > player.y + player.size) {
            return false; // the above if statement checks if you are NOT colliding and returns false
        } else {
            return true; // else they are colliding so return true
        }
}

function stop(message) {
    window.removeEventListener("keydown", activate, false);
    window.removeEventListener("keyup", deactivate, false);
    window.cancelAnimationFrame(request_id);
    let outcome_element = document.querySelector("#outcome");
    outcome_element.innerHTML = message; 
    // takes text from stop outcome and appends to paragraph with ID 'outcome'
}

