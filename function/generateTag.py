import os
from dotenv import load_dotenv
load_dotenv()

def generate_img_tags(container, imgs):
    """
    Generate image tags for the given images.
    """
    source = os.getenv('CDN_URL')
    img_tags = []
    for path in imgs:
        img_tags.append(f'<img src="{source}/{container}/{path}" alt="{path}">')
    
    return '\n'.join(img_tags)