import string

alphabet = string.ascii_letters + string.digits + "{}_-.,/%?$!@#"

def reverse_romanize(encrypted_string, key):
    """Reverse the romanize function with a given key"""
    result = [""] * len(encrypted_string)
    for i, c in enumerate(encrypted_string):
        # Subtract the key instead of adding it
        result[i] = alphabet[(alphabet.index(c) - key) % len(alphabet)]
    return "".join(result)

def find_flag(encrypted_output):
    """Try all possible keys to find the original flag"""
    print(f"Encrypted output: {encrypted_output}")
    print(f"Alphabet length: {len(alphabet)}")
    print(f"Trying keys 1 to {len(alphabet) - 1}...")
    print()
    
    for key in range(1, len(alphabet)):
        decrypted = reverse_romanize(encrypted_output, key)
        
        # Check if it looks like a valid flag
        if decrypted.startswith("pascalCTF{") and decrypted.endswith("}"):
            print(f"🎉 FOUND FLAG with key {key}:")
            print(f"Flag: {decrypted}")
            return decrypted
        else:
            print(f"Key {key:2d}: {decrypted}")
    
    print("❌ No valid flag found!")
    return None

if __name__ == "__main__":
    # Read the encrypted output
    with open("output.txt", "r") as f:
        encrypted_output = f.read().strip()
    
    flag = find_flag(encrypted_output)