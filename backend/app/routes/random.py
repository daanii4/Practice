import random
import string

def generate_random_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

state_string = generate_random_state()
print(state_string)
