import shutil
import platform


# Try to find tesseract in PATH first
def set_tesseract_cmd():
    print(f"Platform: {platform.system()}")
    tesseract_path = shutil.which("tesseract")
    print(f"Tesseract found at: {tesseract_path}")

    if tesseract_path:
        return tesseract_path
    else:
        # Fallback to common installation paths
        if platform.system() == "Windows":
            return r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # On Linux/Mac, it's usually in PATH, but you can add fallbacks if needed
