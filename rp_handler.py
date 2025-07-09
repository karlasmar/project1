import runpod
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

# Load the model globally
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def handler(event):
    prompt = event['input'].get('prompt', 'a futuristic robot in Tokyo at night')

    image = pipe(prompt).images[0]

    # Convert image to base64 string
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {
        "image_base64": img_base64
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
