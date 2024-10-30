# get_constants.py
import sys
import constants

def get_constant(constant_name):
    return getattr(constants, constant_name, None)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_constants.py <CONSTANT_NAME>")
        sys.exit(1)
    
    constant_name = sys.argv[1]
    value = get_constant(constant_name)
    
    if value is not None:
        print(value)
    else:
        print(f"Constant '{constant_name}' not found.")