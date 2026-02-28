try:
    import asyncio
    import system.lib.minescript as m
    import shlex
    import os
    import sys
    import threading
    import time
    import subprocess
    import json
    from pathlib import Path
except ModuleNotFoundError as e:
    print(f"Error while importing: {e}")
    exit()

HOST = '127.0.0.1'
PORT = 19133

folder = Path(__file__)
folder = folder.parent
folder = folder.__str__()
if not os.path.exists(r'C:\\Program Files\\nodejs\\node.exe'):
    m.echo(f"§7[§cMinescript-JS§7] §cError: You need nodejs installed! Please install it on §e'C:\\Program Files\\nodejs\\node.exe'")
    exit()
def run_node():
    subprocess.run(f'"C:\\Program Files\\nodejs\\node.exe" {folder}\\{sys.argv[1]}', cwd=folder, shell=True)

async def handle_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')

        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            args = shlex.split(message)
            if not args:
                continue

            job = args[0]
            if job != '.':
                break

            cmd = args[1] if len(args) > 1 else 'nop'
            next_args = " ".join(args[2:]) if len(args) > 2 else ""

            if cmd == 'echo':
                m.echo(next_args)
                writer.write(b'success')
                await writer.drain()
            if cmd == 'query_args':
                # print("QUERY_ARGS:", sys.argv[1:])
                writer.write(json.dumps(sys.argv[1:]).encode())
                await writer.drain()
            elif cmd == 'player_press_forward':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_forward(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_set_orientation':
                if len(args) > 3:
                    m.player_set_orientation(float(args[2]), float(args[3]))
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'chat':
                if len(args) > 2:
                    writer.write(b'success')
                    m.chat(args[2])
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'chat_input':
                if len(args) > 2:
                    writer.write(b'success')
                    m.set_chat_input(args[2], True)
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'close_chat_input':
                writer.write(b'success')
                m.set_chat_input('', True)
                await writer.drain()
            elif cmd == 'player_press_backward':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_backward(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_left':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_left(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_right':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_right(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_jump':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_jump(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_use':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_use(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_sprint':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_sprint(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_drop':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_drop(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_pick_item':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_pick_item(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'query_all_entities':
                entities = m.entities()
                out = json.dumps([e.__dict__ for e in entities])
                writer.write(out.encode())
                await writer.drain()
            elif cmd == 'player_press_swap_hands':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_swap_hands(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'player_press_sneak':
                if len(args) > 2:
                    writer.write(b'success')
                    m.player_press_sneak(args[2].lower() == 'true')
                else:
                    writer.write(b'err')
                await writer.drain()
            elif cmd == 'eval':
                try:
                    writer.write(bytes(eval(next_args)))
                except Exception as e:
                    writer.write(str(f'error: {e}').encode())
                await writer.drain()
            elif cmd == 'exit':
                writer.close()
                await writer.wait_closed()
                server.close()
                m.echo(f'§eScript stopped: {sys.argv[1]}')
                return
            else:
                writer.write(b'unknown_command')
                await writer.drain()

        # print(f"Connection closed from {addr}")
        writer.close()
        await writer.wait_closed()
    except asyncio.exceptions.CancelledError:
        pass

async def main():
    try:
        global server
        server = await asyncio.start_server(handle_client, HOST, PORT)
        addr = server.sockets[0].getsockname()
        threading.Thread(target=run_node, daemon=True).start()

        async with server:
            await server.serve_forever()
    except asyncio.exceptions.CancelledError:
        pass

asyncio.run(main())
