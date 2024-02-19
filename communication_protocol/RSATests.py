import random
import string

def gcd(x, y):
    while x != 0:
        x, y = y % x, x
    return y

def extended_gcd(x: int, y: int) -> (int, int, int):
    prev_u = 1
    prev_v = 0
    u = 0
    v = 1

    while y != 0:
        q = x // y
        x, y = y, x % y

        u_new = prev_u - q * u
        v_new = prev_v - q * v


        prev_u, prev_v = u, v
        u, v = u_new, v_new

    return x, prev_u, prev_v


def generate_keys_fast(p, q):
    N = p*q 

    # phi(x) evaluated at N
    phiN = (p-1)*(q-1)

    e = 0 
    while True:
        potential_e = random.randint(2, phiN-1)
        #Use Euclidian Algorithm for GCD 
        if gcd(phiN,potential_e) == 1:
            e = potential_e
            break
    assert e != 0

    public_key = (e, N)    

    
    _, _, y = extended_gcd(phiN, e)


    private_key = (y, N)    

    return public_key, private_key

def encrypt(plain_text: bytes, public_key, size) -> bytes:
    e, N = public_key

    plain_int = int.from_bytes(plain_text, byteorder= 'little')
    cypher_int = pow(plain_int, e, N)
    cypher_text = cypher_int.to_bytes(size, byteorder="little")

    return cypher_text

def decrypt(cypher_text: bytes, private_key, size) -> bytes:
    
    d, N = private_key

    cypher_int = int.from_bytes(cypher_text, byteorder = 'little')
    plain_int = pow(cypher_int, d, N)
    plain_text = plain_int.to_bytes(size, byteorder = "little")

    return plain_text

def get_2_primes():
    with open("communication_protocol\primes_for_rsa.txt", "r") as f:
        primes = f.read().splitlines()

        return map(int, random.sample(primes, 2))

for _ in range(10):
    while True:
        #Ensure that the product of the primes is 2048 bits
        p, q = get_2_primes()
        prod_len = (p * q).bit_length()
        if prod_len == 2048:
            break
    
    public_key, private_key = generate_keys_fast(int(p),int(q))
    CHUNK_SIZE = 256
    size = random.randint(10,300)
    plain_text = ''.join(random.choice(string.ascii_letters) for i in range(size))
    
    encoded_text = plain_text.encode()
    
    encrypted_chunks = []
    header = str(f"{size:<{CHUNK_SIZE}}").encode()
    encrypted_chunks.append(encrypt(header, public_key, CHUNK_SIZE)) 
    
    for i in range(0, size, CHUNK_SIZE):
        chunk = encoded_text[i:i+CHUNK_SIZE]
        encrypted_chunks.append(encrypt(chunk, public_key, CHUNK_SIZE))
    
    # -- MESSAGE IS SENT --


    received_header = encrypted_chunks.pop(0)
    received_size = int(decrypt(received_header, private_key, CHUNK_SIZE))
    ptext = b''
    for echunk in encrypted_chunks:
        ptext += decrypt(echunk, private_key, CHUNK_SIZE)

    ptext = ptext[:received_size].decode()
    print(ptext)
    print(plain_text)
    print(size, received_size)

    assert ptext == plain_text