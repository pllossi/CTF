from base64 import b64decode
import binascii

def is_base64(s):
    """Check if string is valid base64"""
    try:
        if isinstance(s, str):
            s = s.encode('ascii')
        decoded = b64decode(s, validate=True)
        return True
    except Exception:
        return False

def is_hex(s):
    """Check if string is valid hex"""
    try:
        if isinstance(s, str):
            bytes.fromhex(s)
            return True
        else:
            s.decode('ascii')
            bytes.fromhex(s.decode('ascii'))
            return True
    except Exception:
        return False

def decode_step(data):
    """Try to decode one step - either base64 or hex"""
    results = []
    
    # Try base64 decode
    if is_base64(data):
        try:
            decoded_b64 = b64decode(data)
            results.append(('base64', decoded_b64))
        except Exception as e:
            pass
    
    # Try hex decode
    if is_hex(data):
        try:
            if isinstance(data, bytes):
                decoded_hex = bytes.fromhex(data.decode('ascii'))
            else:
                decoded_hex = bytes.fromhex(data)
            results.append(('hex', decoded_hex))
        except Exception as e:
            pass
    
    return results

def decode_recursively(data, step=0, path=""):
    """Recursively decode the data trying all possible paths"""
    if step > 15:  # Prevent infinite recursion
        return []
    
    print(f"Step {step}: Trying to decode ({len(data)} bytes)")
    if isinstance(data, bytes):
        try:
            data_str = data.decode('ascii', errors='ignore')
            print(f"  Data preview: {data_str[:100]}...")
        except:
            print(f"  Data preview: {data[:100]}...")
    else:
        print(f"  Data preview: {data[:100]}...")
    
    # Check if we found the flag
    if isinstance(data, bytes):
        try:
            decoded_str = data.decode('ascii', errors='ignore')
            if decoded_str.startswith('pascalCTF{') and decoded_str.endswith('}'):
                print(f"\n🎉 FOUND FLAG!")
                print(f"Path: {path}")
                print(f"Flag: {decoded_str}")
                return [decoded_str]
        except:
            pass
    elif isinstance(data, str):
        if data.startswith('pascalCTF{') and data.endswith('}'):
            print(f"\n🎉 FOUND FLAG!")
            print(f"Path: {path}")
            print(f"Flag: {data}")
            return [data]
    
    # Try to decode further
    possible_decodings = decode_step(data)
    results = []
    
    for method, decoded_data in possible_decodings:
        new_path = f"{path} -> {method}"
        print(f"  Trying {method} decode...")
        
        # Recursively try to decode the result
        recursive_results = decode_recursively(decoded_data, step + 1, new_path)
        results.extend(recursive_results)
    
    return results

if __name__ == "__main__":
    # Read the encoded output
    with open('output.txt', 'r') as f:
        encoded_data = f.read().strip()
    
    print(f"Starting decode process...")
    print(f"Input length: {len(encoded_data)} characters")
    print("="*60)
    
    flags = decode_recursively(encoded_data, 0, "start")
    
    if not flags:
        print("\n❌ No valid flag found!")
    else:
        print(f"\n✅ Found {len(flags)} potential flag(s):")
        for flag in flags:
            print(f"  {flag}")