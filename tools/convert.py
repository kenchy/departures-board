import sys
import os

def convert_htm_to_h(input_filepath):
    # Ensure the input file exists
    if not os.path.isfile(input_filepath):
        print(f"Error: File '{input_filepath}' not found.")
        sys.exit(1)

    # Extract filenames and derive variables
    filename = os.path.basename(input_filepath)
    name, _ = os.path.splitext(filename)
    
    output_filepath = f"{name}.h"
    array_name = filename.replace(".", "")

    hex_values = []
    
    with open(input_filepath, 'rb') as f:
        for line in f:

            # Trim lines
            stripped_line = line.strip()
            
            # Skip empty lines
            if not stripped_line:
                continue
                
            # Skip comment lines
            if stripped_line.startswith(b'//'):
                continue
            
            # Re-append \r\n as a byte string to the trimmed line
            processed_line = stripped_line + b'\r\n'
            
            for byte in processed_line:
                hex_values.append(f"0x{byte:02X}")

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("#include <Arduino.h>\n\n")
        f.write(f"static const uint8_t {array_name}[] PROGMEM={{\n")
        
        for i in range(0, len(hex_values), 21):
            chunk = hex_values[i:i+21]
            f.write(", ".join(chunk))
            
            if i + 21 < len(hex_values):
                f.write(",\n")
            else:
                f.write("\n};\n")
                
    print(f"Successfully created '{output_filepath}' from '{input_filepath}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py <input_file.htm>")
        sys.exit(1)
        
    convert_htm_to_h(sys.argv[1])