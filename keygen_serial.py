import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

fixed_part = "00X0X00"

print("keygen serial android moment\n")
for _ in range(10):
    random_part = generate_random_string(6)
    result = random_part + fixed_part
    print(result)
