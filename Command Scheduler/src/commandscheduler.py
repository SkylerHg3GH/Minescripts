import time
import minescript as ms
import sys

def echo(text):
    ms.echo(str(text).replace("&", "§").replace('§§', '&'))

if len(sys.argv) < 3 or len(sys.argv) > 4:
    echo('&eUsage: &7commandscheduler &8<&ecommand&8> &8<&eTime, in seconds&8> &8[&efalse &7(to show message or not)&8]')
    exit()

command = sys.argv[1]

try:
    interval = float(sys.argv[2])
except ValueError:
    echo('&cError: the amount of time is not a float')
    exit()

silent = sys.argv[3].lower() == 'false' if len(sys.argv) == 4 else False

echo('&eUse killjob to remove the scheduler!')
is_command = command.startswith('/') or command.startswith('\\')
while True:
    if not silent:
        echo(f'&8[&eCommandScheduler&8] &eExecuted command &a{command.replace("&", "&&")} &ein intervals of &a{interval}&e seconds')
    if is_command:
        ms.execute(command)
    else:
        ms.chat(command)
    time.sleep(interval)
