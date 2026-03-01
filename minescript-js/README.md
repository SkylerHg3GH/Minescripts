# minescript-js
Minescript-js is a Minescript script that allows you to run Javascript scripts in Minecraft using interprocess communication.
It is very limited but i personally want my settimeout and setinterval in python 

## Documentation
### `ensureConnection()`
Ensures the connection of the IPC

### `send(text)`
Sends text to the IPC to execute commands

### `echo(text)`
Echoes text to Minecraft

### `exit()`
Exits the script.
**NOTE: You must include this in all your scripts because without it your script will not exit at all!**

### `eval_python_expr(thing)`
Evaluates a python expression

### `argr()`
Gets all arguments passed to the script.  
**Returns:** `Promise<Array>` of all arguments.

### `argv()`
Gets all arguments **except the first one**.  
**Returns:** `Promise<Array>` of arguments starting from index 1.

### `name()`
Gets the first argument **after the script itself**.  
**Returns:** `Promise<String>` — the “name” argument.

### `Entity`
#### `Entity.qall()` / `Entity.queryall()`
Queries all entities in the Minecraft world.  
**Returns:** `Promise<Array<Object>>` of entities.

#### `Entity.list_found(thing)`
Gets the keys of an object returned from entity queries.  
**Input:** JSON object.  
**Returns:** `Array<String>` of keys.  
**Throws:** `TypeError` if input is not an object.
-# this was used for debugging 

### `Player`
#### `Player.Orientation(pitch, yaw)`
Creates a simple `[pitch, yaw]` array for orientation.

#### `Player.press_*` / `Player.gpress_*`
Simulates pressing a key. All `press_*` functions send the command without waiting; `gpress_*` returns a Promise.

- `press_forward(v)` / `gpress_forward(v)` – Move forward
- `press_backward(v)` / `gpress_backward(v)` – Move backward
- `press_left(v)` / `gpress_left(v)` – Move left
- `press_right(v)` / `gpress_right(v)` – Move right
- `press_jump(v)` / `gpress_jump(v)` – Jump
- `press_sprint(v)` / `gpress_sprint(v)` – Sprint
- `press_drop(v)` / `gpress_drop(v)` – Drop item
- `press_pick_item(v)` / `gpress_pick_item(v)` – Pick item
- `press_swap_hands(v)` / `gpress_swap_hands(v)` – Swap hands
- `press_sneak(v)` / `gpress_sneak(v)` – Sneak
- `set_orientation(v, y)` / `gset_orientation(v, y)` – Set player orientation

### `Chat`
#### `Chat.send(thing)`
Sends something to Minecraft chat.

#### `Chat.set_chat_input(thing)` / `Chat.set_ci(thing)`
Sets chat input.

#### `Chat.close_chat_input()` / `Chat.close_ci()`
Closes chat input.

#### `Chat.ci()` / `Chat.chat_input()`
Reads the chat input,
Returns: `[text, cursor position]`

## Usage
`\runjs <script name> <args>`

## Requirements
- NodeJS
- Minescript (I only tested it for Minescript 5.0b10 Neoforge on win11 but it might work on other versions)
