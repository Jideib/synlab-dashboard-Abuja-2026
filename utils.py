# utils.py
import base64
import os


def get_logo_b64(logo_filename="synlab_logo.png"):
    """Search for the logo inside the assets directory across root and subpages."""
    possible_paths = [
        os.path.join("assets", logo_filename),
        os.path.join("..", "assets", logo_filename),
        logo_filename,
        os.path.join("..", logo_filename),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")

    return None


def render_hero_logo(height=65, style="margin-bottom: 12px;"):
    """Return an HTML <img> tag with the Base64 encoded logo image."""
    b64_str = get_logo_b64()
    if b64_str:
        return f'<img src="data:image/png;base64,{b64_str}" style="height: {height}px; {style} filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.15));" />'
    # Fallback emoji if logo file is not found
    return '<span style="font-size: 48px;">🔬</span>'