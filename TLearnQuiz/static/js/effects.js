class Coord {
    constructor(x = 0, y = 0,) {
        this.x = x;
        this.y = y;
    }
}

const COORD_CENTER = new Coord(window.innerWidth / 2, window.innerHeight / 2);
let  COORD_MOUSE = new Coord(0, 0);

document.addEventListener("mousemove", (event) => {
    COORD_MOUSE.x = event.clientX;
    COORD_MOUSE.y = event.clientY;
});

class ParticleDieProcess {
    constructor(resize, opacity, delay) {
        this.resize = resize;
        this.fade = opacity;
        this.delay = delay;
    }
}

const DIE_SMALL = new ParticleDieProcess(0, 0, 0);

const TARGET_FPS = 59;
const FRAME_RATE = 1000 / TARGET_FPS;

const GRAVITY_G = -9.8;

class Vector {
    constructor(x, y) {
        this.x = x
        this.y = y
    }

    randomize () {
        this.x = Math.random() * 2 - 1;
        this.y = Math.random() * 2 - 1;
    }

    awayFrom (coord) {

    }

    down() {
        return new Vector(0, -1);
    }
}

class Particle {
    constructor(pos, width, height, lifetime = 2, sprite = null, rotation = 0, die = new ParticleDieProcess(1, 1, 0), acceleration = 0, useGravity = false, gravityScale = 1, debug = false) {
        this.pos = new Coord(pos.x, pos.y);
        this.width = width;
        this.height = height;
        this.moveVector = new Vector(0, 0);
        this.speed = 0;
        this.lifetime = lifetime;
        this.aliveTime = 0;
        this.representSprite = null;
        this.scale = 1;
        this.dieProcess = new ParticleDieProcess(1, 1, 0);
        this.resizeSpeed = 0;
        this.acceleration = acceleration;
        this.useGravity = useGravity
        this.gravityScale = gravityScale;
        this.debug = debug;

        setTimeout(() => {
            this.resizeSpeed = (die.resize - 1) / (this.lifetime - this.aliveTime / 1000);
            // alert ("Resize " + this.resizeSpeed + " lt: " + this.lifetime + " at: " + this.aliveTime / 1000);
        }, die.delay * 1000);

        let represent = document.createElement("particle");

        // represent.style.transformOrigin = "center";
        represent.style.position = "fixed";

        if (sprite == null) represent.style.background = "black";
        else {
            this.representSprite = document.createElement('img');
            this.representSprite.src = sprite;
        }


        represent.id = this.generateId();

        document.body.append(represent);

        this.representation = document.getElementById(represent.id);
        if (sprite != null) this.representation.appendChild(this.representSprite);

        if (this.debug) {
            this.representation.classList.add ('debug-particle');
        }

        this.setPosition(this.pos);
        this.setSize(width, height);
        this.setRotation(rotation);

        let updateTimer = setInterval(() => {
            this.aliveTime += 10;

            this.scale += this.resizeSpeed / 1000 * FRAME_RATE;
            if (this.speed < 0) {
                this.speed = 0;
            }
            else {
                this.speed += this.acceleration / 1000 * 10;
            }

            this.move(this.moveVector);
            if (this.useGravity) {
                this.move(new Vector().down(), (GRAVITY_G * this.gravityScale * Math.pow(this.aliveTime / 1000, 2)) / 2);
            }


            this.updateParticle();
        }, FRAME_RATE);

        setTimeout(() => {
            this.representation.remove();
            clearInterval(updateTimer);
            delete this;
        }, this.lifetime * 1000);
    }

    generateId() {
        let abc = 'qwertyuiopasdfghjklzxcvbnm';
        let id = 'm';
        while (id === 'm' && document.querySelector(`#${id}`) == null) {
            id = '';
            while (id.length < 10) {
                id += abc[Math.round(Math.random() * (abc.length - 1))]
            }
        }
        return id;
    }

    setPosition(pos) {
        this.representation.style.top = String(pos.y - this.height/2) + "px";
        this.representation.style.left = String(pos.x - this.width/2) + "px";
    }

    setRotation(rotate) {
        this.representation.style.rotate = rotate + 'deg';
    }

    setSize(width, height) {
        this.representation.style.width = String(width * this.scale) + "px";
        this.representation.style.height = String(height * this.scale) + "px";
    }

    move(vector, speed = this.speed) {
        this.pos.x += vector.x * speed;
        this.pos.y += vector.y * speed;
    }

    updateParticle() {
        this.setPosition(this.pos);
        this.setSize(this.width, this.height);
    }
}

class Emitter {
    constructor(data) {
        this.data = data;
        this.debug = data.debug;
        this.scale = 1;
        this.pos = data.pos;



        let represent = document.createElement("emitter");
        represent.id = 'emitter-' + this.generateId();
        document.body.append(represent);
        this.representation = document.querySelector(`#${represent.id}`);

        if (data.shape.form === 'circle') {
            this.width = data.shape.radius;
            this.height = data.shape.radius;
        }

        this.setSize(this.width, this.height);

        let updateTimer = setInterval(() => {

            this.updateEmitter();
        }, FRAME_RATE);

        if (this.debug) {
            this.representation.classList.add('emitter-debug-circle');
        }
    }

    setSize(width, height) {
        this.representation.style.width = String(width * this.scale) + "px";
        this.representation.style.height = String(height * this.scale) + "px";
    }

    setPosition(pos) {
        this.representation.style.top = String(pos.y) + "px";
        this.representation.style.left = String(pos.x) + "px";
    }

    generateId() {
        let abc = 'qwertyuiopasdfghjklzxcvbnm';
        let id = 'm';
        while (id === 'm' && document.querySelector(`#emitter-${id}`) == null) {
            id = '';
            while (id.length < 10) {
                id += abc[Math.round(Math.random() * (abc.length - 1))]
            }
        }
        return id;
    }

    getParticleSpawnPoint() {
        switch (this.data.shape.form) {
            case 'circle':
                let x = Math.random() * 2 - 1;
                let modY = Math.abs(Math.sqrt(1 - Math.acos(x) * Math.PI / 180));
                if (this.data.shape.spawnArea === "allSurface") {
                    let y = Math.random() * modY * 2 - modY;
                    console.log (`x: ${x}, acos(${x}): ${Math.acos(x)}, modY: ${modY}`);
                    return new Coord(this.pos.x + x * this.data.shape.radius / 2, this.pos.y + y * this.data.shape.radius / 2);
                }
                if (this.data.shape.spawnArea === "borders") {
                    let m = Math.round(Math.random() * 2 - 1);
                    if (m <= 0) m = -1;
                    else m = 1;
                    let y = modY * m;
                    console.log (`x: ${x}, acos(${x}): ${Math.acos(x)}, modY: ${modY}`);
                    return new Coord(this.pos.x + x * this.data.shape.radius / 2, this.pos.y + y * this.data.shape.radius / 2);
                }
        }
    }

    play() {
        let lifecycle = setInterval(() => {
            let spawn = this.getParticleSpawnPoint();
            let particle = new Particle(spawn, this.data.particle.width,
                 this.data.particle.height, this.data.particle.lifetime, this.data.particle.sprite,
                0, this.data.particle.die, this.data.particle.acceleration,
                this.data.particle.gravity, this.data.particle.gravityScale, this.data.particle.debug);
            if (this.data.particle.rotation === "random") {
                particle.setRotation(Math.random() * 360);
            }
            else {
                particle.setRotation(this.data.particle.rotation);
            }

            let movementVector = new Vector(0, 0);
            switch (this.data.particle.speedDirection) {
                case 'fromCenter':
                    movementVector.x = ((spawn.x - this.pos.x) * 2) / this.data.shape.radius;
                    movementVector.y = ((spawn.y - this.pos.y) * 2) / this.data.shape.radius;
                    break
                case 'random':
                    movementVector.randomize();
                    break
            }
            particle.moveVector = movementVector;

            particle.speed = this.data.particle.speed;
        }, 1000 / this.data.amount);

        setTimeout(() => {
            clearInterval(lifecycle);
            delete this;
        }, this.data.duration * 1000);
    }

    updateEmitter() {
        this.setPosition(this.pos);
        this.setSize(this.width, this.height);
    }
}

function CreateWrongAnswerEffect(id) {
    let source = document.querySelector(id);
    let sourceRect = source.rect
}