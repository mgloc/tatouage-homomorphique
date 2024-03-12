import phe as paillier
print("Generating paillier keypair")
public_key, private_key = paillier.generate_paillier_keypair()
