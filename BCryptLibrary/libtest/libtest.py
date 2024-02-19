from collections import Counter
from bcryptCPP import bcrypt, generate_random_salt


results = set()
print("Tests started")
for _ in range(100):

    hash_res = bcrypt('mypassword', "c5c31e2f7ea847b9797040158b64377a", 2)
    results.add(hash_res)


print(len(results) == 1)

results = []
salts = []
salt = generate_random_salt()
print(f"SALT: {salt}")
for _ in range(1000):
    hash_res = bcrypt('asdasd1231231231231hghttnefeq', '2c4e5daab3745d62603393a6803fae27', 4)
    results.append(hash_res)
    salts.append(salt)

#Counter({'426e6165537265647462756f':
print(Counter(results))

print(Counter(salts))


print(len(generate_random_salt()) == 32)

print("Tested passed")

