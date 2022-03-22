let canvas;
let context;

let fpsInterval = 1000 / 30; // the denominator is FPS
let now;
let then = Date.now();


let player = {
    x: 0,
    y: 0,
    width: 60.6666666666666666667,
    height: 61.5,
    frameX: 0,
    frameY: 2,
    xChange: 0,
    yChange: 0,
    in_air: false
};



let floor;

let moveLeft = false;
let moveUp = false;
let moveRight = false;
let moveDown = false;


let background = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,7],
    [14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14]
];

let tilesPerRow = 8;
let tileSize = 16;

let IMAGES = {player: "golden-armor-spritesheet.png", background: "tiles.png"};

document.addEventListener("DOMContentLoaded", init, false);

function init() {
    canvas = document.querySelector("canvas");
    context = canvas.getContext("2d");

    floor = canvas.height - 27;
    player.x = canvas.width / 2;
    player.y = floor - player.height; // This will give the appearance of the player standing on the floor
    
    
    window.addEventListener("keydown", activate, false);
    window.addEventListener("keyup", deactivate, false);

    load_images(draw());
}

function draw() {
    window.requestAnimationFrame(draw);
    let now = Date.now();
    let elapsed = now - then;
    if (elapsed <= fpsInterval) {
        return;
    }
    then = now - (elapsed % fpsInterval);

    // Draw background on canvas
    context.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    context.fillStyle = "#87cefa"; // light sky blue
    context.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grass from tileset
    for (let r = 0; r < 20; r += 1) {
        for(let c = 0; c < 32; c +=1) {
            let tile = background[r][c];
            if (tile >= 0) {
                let tileRow = Math.floor(tile / tilesPerRow);
                let tileCol = Math.floor(tile % tilesPerRow);
                context.drawImage(IMAGES.background,
                    tileCol * tileSize, tileRow * tileSize, tileSize, tileSize,
                    c * tileSize, r * tileSize, tileSize, tileSize);
            }
        }
    }

    // Draw player
    context.fillStyle = "red";
    context.drawImage(IMAGES.player,
        player.frameX * player.width, player.frameY * player.width, player.width, player.height,
        player.x, player.y, player.width, player.height);
    

    /* The chunk below is for animation with a multiple row sprite */
    if ((moveLeft || moveRight) && ! (moveLeft && moveRight) && ! (player.in_air)) {
        player.frameX = (player.frameX + 1) % 9;
    }


    // Draw other objects

    // Handle key presses
    if (moveLeft) {
        player.xChange = player.xChange - 0.5;
        player.frameY = 1;
    }
    if (moveRight) {
        player.xChange = player.xChange + 0.5;
        player.frameY = 3;
    }
    if (moveUp && ! player.in_air) { // If the player presses upArrow and they aren't in the air already
        player.yChange = player.yChange - 20;
        player.in_air = true;
    }
    
    // Update the player
    player.x = player.x + player.xChange;
    player.y = player.y + player.yChange;

    // Update the other objects

    // Physics
    player.yChange = player.yChange + 1.5; // gravity
    player.xChange = player.xChange * 0.9; // friction
    player.yChange = player.yChange * 0.9; // friction

    // Collisions
    if (player.y + player.height > floor) { // Check if player is in contact with the floor
        player.in_air = false;
        player.y = floor - player.height;
        player.yChange = 0;
    }

    // Going off left or right
    if (player.x + player.width < 0) {
        player.x = canvas.width;
    } else if (player.x > canvas.width) {
        player.x = - player.width;
    }

}



function activate(event) {
    let key = event.key;
    if (key === "ArrowLeft") {
        moveLeft = true;
    } else if (key === "ArrowUp") {
        moveUp = true;
    } else if (key === "ArrowRight") {
        moveRight = true;
    } else if (key === "ArrowDown") {
        moveDown = true;
    }
}

function deactivate(event) {
    let key = event.key;
    if (key === "ArrowLeft") {
        moveLeft = false;
    } else if (key === "ArrowUp") {
        moveUp = false;
    } else if (key === "ArrowRight") {
        moveRight = false;
    } else if (key === "ArrowDown") {
        moveDown = false;
    }
}

// function player_collides(a) {
//     if (player.x + player.size < a.x ||
//         a.x + a.size < player.x ||
//         player.y > a.y + a.size ||
//         a.y > player.y + player.size) {
//         return false; // the above if statement checks if you are NOT colliding and returns false
//     } else {
//         return true; // else they are colliding so return true
//     }
// }

function stop() {
    window.removeEventListener("keydown", activate, false);
    window.removeEventListener("keyup", deactivate, false);
    window.cancelAnimationFrame(request_id);
}

// function to load images
function load_images(callback) {
    let num_images = Object.keys(IMAGES).length;
    let loaded = function() {
        num_images = num_images - 1;
        if (num_images === 0) {
            callback();
        }
    };
    for (let name of Object.keys(IMAGES)) {
        let img = new Image();
        img.addEventListener("load", loaded, false);
        img.src = IMAGES[name];
        IMAGES[name] = img;
    }
}