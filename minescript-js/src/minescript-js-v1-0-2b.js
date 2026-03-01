const net = require('net');

const ver = 'v1.0.2b'

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
    /**
     * Echoes something to chat
     * @param {string} message the thing to echo
     */
    return send(`. echo ${message}`);
}

function exit() {
    /**
     * Exits the program
     */
    return send(`. exit`);
}

function eval_python_expr(expr) {
    /**
     * Evaluates a python expression.
     * @param {any} text the thing to evaluate
     */
    return send(`. eval ${expr}`);
}

class Chat {
    static send(thing) {
        /**
         * Sends something to chat.
         * @param {string} text the thing to send
         */
        return send(`. chat ${thing}`);
    }
    static set_chat_input(thing) {
        /**
         * Sets the chat input.
         * @param {string} text the thing to set the chat input to
         */
        return send(`. set_chat_input ${thing}`);
    }
    static set_ci = this.set_chat_input
    static close_chat_input(thing) {
        /**
         * Closes the chat input.
         */
        return send(`. close_chat_input`);
    }
    static close_ci = this.close_chat_input
    static chat_input() {
        /**
         * Queries the chat input.
         * @returns {Array} An array of [text in chat input, cursor position]
         */
        return send(`. query_ci`);
    }
    static ci = this.chat_input
}
class Entity {
    static async qall() {
        /**
         * Queries all entites as a JSON.
         * @returns {Array} An array representing all entites (Python object directly converted to JS)
         */
        const thing = JSON.parse(await send(`. query_all_entities`))
        return thing
    }

    static list_found(thing) {
        /**
         * Returns all things found in your entity data
         * @returns {Array} the things
         */
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
    /**
     * Queries all arguments passed to the script
     * @returns {Array} the arguments
     */
    const out = await send(`. query_args`);
    const things = JSON.parse(out);
    return things;
}

async function argv() {
    /**
     * Queries all arguments passed to the script excluding the script name
     * Equivalent to `argr().slice(1)`
     * @returns {Array} the arguments
     */
    const things = await argr();
    return things.slice(1);
}

async function name() {
    /**
     * Queries all arguments passed to the script and only gets the script name
     * Equivalent to `argr()[0]`
     */
    const args = await argr();
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
