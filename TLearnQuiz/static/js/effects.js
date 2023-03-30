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
}

class Particle {
    constructor(pos, width, height, lifetime = 2, sprite = null, rotation = 0, die = new ParticleDieProcess(1, 1, 0), acceleration = 0, useGravity = false, gravityScale = 1) {
        this.pos = new Coord(pos.x, pos.y);
        this.width = width;
        this.height = height;
        this.radialVector = 90;
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

        setTimeout(() => {
            this.resizeSpeed = (die.resize - 1) / (this.lifetime - this.aliveTime / 1000);
            // alert ("Resize " + this.resizeSpeed + " lt: " + this.lifetime + " at: " + this.aliveTime / 1000);
        }, die.delay * 1000);

        let represent = document.createElement("particle");

        represent.style.transformOrigin = "center";
        represent.style.position = "fixed";

        if (sprite == null) represent.style.background = "black";
        else {
            this.representSprite = document.createElement('img');
            this.representSprite.src = sprite;
        }


        represent.id = this.generateId();

        document.body.append(represent);

        this.representation = document.getElementById(represent.id);
        this.representation.appendChild(this.representSprite);
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

            this.move(this.radialVector);
            if (this.useGravity) {
                this.move(-90, (GRAVITY_G * this.gravityScale * Math.pow(this.aliveTime / 1000, 2)) / 2);
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
        this.representation.style.top = String(pos.y) + "px";
        this.representation.style.left = String(pos.x) + "px";
    }

    setRotation(rotate) {
        this.representation.style.rotate = rotate + 'deg';
    }

    setSize(width, height) {
        this.representation.style.width = String(width * this.scale) + "px";
        this.representation.style.height = String(height * this.scale) + "px";
    }

    move(radial, speed = this.speed) {
        let rad = (Math.PI / 180) * radial;

        this.pos.x += Math.cos(rad) * speed;
        this.pos.y += Math.sin(rad) * speed;

    }

    updateParticle() {
        this.setPosition(this.pos);
        this.setSize(this.width, this.height);
    }
}

class Emitter {
    constructor(data) {
        this.data = data;
    }

    play() {
        let lifecycle = setInterval(() => {
            let particle = new Particle(this.data.particle.pos, this.data.particle.width,
                 this.data.particle.height, this.data.particle.lifetime, this.data.particle.sprite,
                this.data.particle.rotation, this.data.particle.die, this.data.particle.acceleration,
                this.data.particle.gravity, this.data.particle.gravityScale);
            particle.radialVector = Math.random() * 360;
            particle.speed = this.data.particle.speed;
        }, 1000 / this.data.amount);

        setTimeout(() => {
            clearInterval(lifecycle);
            delete this;
        }, this.data.duration * 1000);
    }
}

function CreateWrongAnswerEffect(id) {
    let source = document.querySelector(id);
    let sourceRect = source.rect
}