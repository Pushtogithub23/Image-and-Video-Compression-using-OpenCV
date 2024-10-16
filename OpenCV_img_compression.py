import cv2 as cv
import numpy as np
import os
import requests
import matplotlib.pyplot as plt

def fetch_image(image_path):
    """Fetch an image from a URL or local path and return it along with its size in KB or MB."""
    if image_path.startswith(('http', 'https')):
        try:
            response = requests.get(image_path)
            response.raise_for_status()
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv.imdecode(image_array, cv.IMREAD_COLOR)
            size_kb = int(response.headers.get('Content-Length', 0)) / 1024
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from URL: {e}")
            return None, None
    else:
        img = cv.imread(image_path)
        if img is None:
            print("Couldn't read the image. Check the file path.")
            return None, None
        size_kb = os.path.getsize(image_path) / 1024

    if img is None:
        print("Failed to decode the image.")
        return None, None

    return img, size_kb

def compress_and_save_image(img, save_path, quality):
    """Compress the image with the specified quality and save it. Returns compressed image and size."""
    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
    success, encoded_img = cv.imencode('.jpg', img, encode_param)
    if success:
        compressed_img = cv.imdecode(encoded_img, cv.IMREAD_COLOR)
        cv.imwrite(save_path, compressed_img)
        compressed_size_kb = os.path.getsize(save_path) / 1024
        return compressed_img, compressed_size_kb
    else:
        print("Failed to compress and save the image.")
        return None, None

def calculate_metrics(original_img, compressed_img):
    """Calculate MSE and PSNR between the original and compressed images."""
    mse = np.mean((original_img - compressed_img) ** 2)
    psnr = float('inf') if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))
    return mse, psnr

def format_size(size_kb):
    """Format size in KB or MB."""
    if size_kb > 1024:
        return f"{size_kb / 1024:.2f} MB"
    return f"{size_kb:.2f} KB"

def display_images(original_img, compressed_img, original_size_kb, compressed_size_kb, mse, psnr):
    """Display the original and compressed images with sizes, MSE, and PSNR."""
    dpi = 100
    fig_w, fig_h = int(original_img.shape[1]/dpi), int(original_img.shape[0]/dpi)
    fig, axs = plt.subplots(1, 2, figsize=(fig_w, fig_h))
    original_size_label = format_size(original_size_kb)
    compressed_size_label = format_size(compressed_size_kb)
    axs[0].imshow(cv.cvtColor(original_img, cv.COLOR_BGR2RGB))
    axs[0].set_title(f"Original Image: {original_size_label}", fontsize = 20)
    axs[0].axis('off')
    axs[1].imshow(cv.cvtColor(compressed_img, cv.COLOR_BGR2RGB))
    axs[1].set_title(f"Compressed Image: {compressed_size_label}\nMSE: {mse:.2f}, PSNR: {psnr:.2f} dB", fontsize = 20)
    axs[1].axis('off')
    plt.tight_layout()
    plt.show()

def compress_image(image_path, filename, quality, show_image=True):
    """Compress an image from a URL or local path and optionally display it."""
    img, original_size_kb = fetch_image(image_path)
    if img is None:
        return

    save_path = os.path.join("IMAGES/COMPRESSED_IMAGES", filename)
    compressed_img, compressed_size_kb = compress_and_save_image(img, save_path, quality)
    if compressed_img is None:
        return

    mse, psnr = calculate_metrics(img, compressed_img)
    
    if show_image:
        display_images(img, compressed_img, original_size_kb, compressed_size_kb, mse, psnr)

# Example usage for a local image
compress_image("IMAGES/ORIGINAL_IMAGES/BMW.jpg", 'BMW_Compressed.jpg', 10)
# compress_image(r"D:\VS CODE FILES\OpenCV\IMAGES\deer.jpg", 'deer_Compressed.jpg', 10)

# Example usage for a web image
# compress_image("https://images.pexels.com/photos/6133952/pexels-photo-6133952.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", 'pelican_compressed.jpg', 10)
