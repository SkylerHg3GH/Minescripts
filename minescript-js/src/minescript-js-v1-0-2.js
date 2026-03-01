const net = require('net');

const ver = 'v1.0.2'

let client = null;
let queue = [];
let buffer = '';

function ensureConnection() {
    if (client) return;

    client = net.createConnection({ port: 19133, host: '127.0.0.1' });

    client.on('data', data => {
        buffer += data.toString();

        if (buffer.includes('\n') || buffer.length > 0) {
            const resolve = queue.shift();
            if (resolve) resolve(buffer.trim());
            buffer = '';
        }
    });

    client.on('close', () => {
        client = null;
    });

    client.on('error', err => {
        const reject = queue.shift();
        if (reject) reject(err);
    });
}

function send(text) {
    return new Promise((resolve, reject) => {
        ensureConnection();
        queue.push(resolve);
        client.write(text + '\n');
    });
}
function echo(message) {
    return send(`. echo ${message}`);
}

function exit() {
    return send(`. exit`);
}

function eval_python_expr(expr) {
    return send(`. eval ${expr}`);
}

class Chat {
    static send(thing) {
        return send(`. chat ${thing}`);
    }
    static set_chat_input(thing) {
        return send(`. set_chat_input ${thing}`);
    }
    static set_ci = this.set_chat_input
    static close_chat_input(thing) {
        return send(`. close_chat_input`);
    }
    static close_ci = this.close_chat_input
    static chat_input() {
        return send(`. chat_input`);
    }
    static ci = this.chat_input
}
class Entity {
    static async qall() {
        const thing = JSON.parse(await send(`. query_all_entities`))
        return thing
    }

    static list_found(thing) {
        if (typeof thing === "object") {
            return Object.keys(thing)
        }
        throw new TypeError('Input must be json')
    }
    static queryall = this.qall
}

class Player {
    static Orientation(pitch, yaw) { return [pitch, yaw] }
    static press_use(v){ send(`. player_press_use ${v}`); }
    static gpress_use(v){ return send(`. player_press_use ${v}`); }

    static press_forward(v){ send(`. player_press_forward ${v}`); }
    static gpress_forward(v){ return send(`. player_press_forward ${v}`); }

    static press_backward(v){ send(`. player_press_backward ${v}`); }
    static gpress_backward(v){ return send(`. player_press_backward ${v}`); }

    static press_left(v){ send(`. player_press_left ${v}`); }
    static gpress_left(v){ return send(`. player_press_left ${v}`); }

    static press_right(v){ send(`. player_press_right ${v}`); }
    static gpress_right(v){ return send(`. player_press_right ${v}`); }

    static press_jump(v){ send(`. player_press_jump ${v}`); }
    static gpress_jump(v){ return send(`. player_press_jump ${v}`); }

    static press_sprint(v){ send(`. player_press_sprint ${v}`); }
    static gpress_sprint(v){ return send(`. player_press_sprint ${v}`); }

    static press_drop(v){ send(`. player_press_drop ${v}`); }
    static gpress_drop(v){ return send(`. player_press_drop ${v}`); }

    static press_pick_item(v){ send(`. player_press_pick_item ${v}`); }
    static gpress_pick_item(v){ return send(`. player_press_pick_item ${v}`); }

    static press_swap_hands(v){ send(`. player_press_swap_hands ${v}`); }
    static gpress_swap_hands(v){ return send(`. player_press_swap_hands ${v}`); }

    static press_sneak(v){ send(`. player_press_sneak ${v}`); }
    static gpress_sneak(v){ return send(`. player_press_sneak ${v}`); }

    static set_orientation(v, y){ send(`. player_set_orientation ${v} ${y}`); }
    static gset_orientation(v, y){ return send(`. player_set_orientation ${v} ${y}`); }
}

async function argr() {
    const out = await send(`. query_args`);
    const things = JSON.parse(out);
    return things;
}

async function argv() {
    const things = await argr();
    return things.slice(1);
}

async function name() {
    const args = await argv();
    return args[0];
}
module.exports = {
    send,
    echo, 
    exit,
    eval,
    name,
    argr,
    argv,
    eval_python_expr,
    Entity,
    Player,
    Chat
};
