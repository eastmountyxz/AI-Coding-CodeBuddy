import cv2
import sys

def rgb_to_gray(input_path: str, output_path: str) -> None:
    # Read the color image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Failed to read image: {input_path}")
        sys.exit(1)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    if not cv2.imwrite(output_path, gray):
        print(f"Failed to write image: {output_path}")
        sys.exit(1)

    print(f"Grayscale image saved to: {output_path}")

if __name__ == "__main__":
    # Input: baby.png in current directory
    input_image = "baby.png"
    output_image = "baby_gray.png"
    rgb_to_gray(input_image, output_image)
