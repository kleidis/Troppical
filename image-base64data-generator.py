import base64
import os

# Define the directory containing the images
image_dir = "icons/logos"
output_dir = "."

# List of image files to convert
image_files = ["LimeLogo.png", "CitraEnhanced.png", "Citra_Logo.svg", "installer_logo.svg", "yuzu.svg"]
# Loop through each file and generate a corresponding base64 .py file
for image_file in image_files:
    # Construct the full file path
    file_path = os.path.join(image_dir, image_file)
    # Create a base64 .py filename
    base64_filename = os.path.splitext(image_file)[0] + "_base64.py"
    base64_file_path = os.path.join(output_dir, base64_filename)

    # Read the image and encode it
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')

    # Write the encoded data to a .py file in the working directory
    with open(base64_file_path, "w") as text_file:
        text_file.write(f"image_data = '{encoded_string}'")
