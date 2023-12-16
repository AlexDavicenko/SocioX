from bcryptCPP import bcrypt



for _ in range(100):
    print(bcrypt(b'mypassword', b"c5c31e2f7ea847b9797040158b64377a", 5))