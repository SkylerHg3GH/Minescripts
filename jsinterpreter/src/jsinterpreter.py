import pythonmonkey as js
import keyboard

from minescript import EventQueue, EventType, append_chat_history, show_chat_screen
from minescript import echo as _echo

def input(prompt=""):
    result = None
    with EventQueue() as q:
        q.register_outgoing_chat_interceptor(prefix=prompt)
        show_chat_screen(True, prompt)
        def on_esc(key):
            show_chat_screen(True, prompt)
        escdetector = keyboard.on_press_key('esc', on_esc)
        while result is None:
            event = q.get()
            if event.type == EventType.OUTGOING_CHAT_INTERCEPT:
                msg = event.message
                if msg.startswith(prompt):
                    result = msg[len(prompt):]
                    append_chat_history(msg)
                    break
        keyboard.unhook_key('esc')
    return result

def echo(*text: str):
    _echo(*tuple([str(thing).replace('&', '§') for thing in text]))
    
echo('&eUse exit() to exit the interpreter.')
def _exit():
    exit()
js.globalThis["exit"] = _exit
while True:
    thing = input('>>> ')
    try:
        echo('&e>> ', js.eval(thing))
    except Exception as e:
        print(e)
