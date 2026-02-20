import base64

# --- Explanation ---
# Why do we convert images to Base64 text?
# 1. Large Language Models (LLMs) like Llama were originally designed to process "Text".
# 2. Internet protocols (like HTTP/JSON) handle text/strings natively and reliably.
# 3. Converting an image to Base64 transforms the "Binary Data" (raw bytes) into a readable "String".
# 4. The model reads this string as a digital signal representing the image pixels.
# -------------------

def demonstrate_conversion(image_path="kl_div.png"):
    try:
        # Read the image file content
        # Keyword: open(path, 'rb') - 'rb' stands for read binary
        with open(image_path, "rb") as image_file:
            sample_data = image_file.read()
        
        print(f"✅ Successfully opened: {image_path}")
    except FileNotFoundError:
        print(f"❌ Image not found: {image_path}")
        print("Using dummy data for demonstration purposes...")
        sample_data = b"Simple math image data" 
    
    print("-" * 30)
    print("1. Raw Binary Data (50 bytes):")
    print(sample_data[:50], "...") 
    print("-" * 30)

    # Encode binary data to Base64 bytes
    # Keyword: base64.b64encode
    encoded_bytes = base64.b64encode(sample_data)
    
    # Decode Base64 bytes to a standard UTF-8 string
    # Keyword: .decode('utf-8')
    encoded_string = encoded_bytes.decode('utf-8')

    print("2. Image converted to Base64 String (First 100 characters):")
    print(encoded_string[:100], "...")
    print("-" * 30)
    
    # This URL is what we actually send in the JSON body to Groq/Llama API
    print("3. Data URL format sent to the Model:")
    data_url = f"data:image/png;base64,{encoded_string[:100]}..."
    print(data_url)
    print("-" * 30)
    print("Note: The real text string will be very long (thousands of characters) depending on image size.")

if __name__ == "__main__":
    # You can change the filename here to match your image
    demonstrate_conversion("kl_div.png")
