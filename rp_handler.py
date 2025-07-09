import runpod
import torch
from diffusers import AutoPipelineForText2Image
import base64
from io import BytesIO

# --- Model Loading ---
# We use AutoPipelineForText2Image to automatically load the correct pipeline for SDXL-Turbo.
# This part runs only once when the worker starts up.
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda") # Move the model to the GPU

# --- Handler Function ---
# This function will run for every API request.
def handler(event):
    """
    The handler function for the serverless worker.
    """
    # Get the 'prompt' from the input, with a default value.
    prompt = event['input'].get('prompt', 'a cinematic shot of a baby raccoon wearing an intricate italian mafioso suit')

    # SDXL-Turbo is designed for speed and works best with fewer steps.
    # We generate the image using the loaded pipeline.
    # guidance_scale=0.0 tells the model to stick closely to the prompt.
    # num_inference_steps=1 is all that's needed for a quality image with this model.
    image = pipe(
        prompt=prompt,
        guidance_scale=0.0,
        num_inference_steps=1
    ).images[0]

    # --- Image Conversion ---
    # Convert the generated image to a base64 string so we can send it in the JSON response.
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # --- Return Response ---
    # The return value must be a JSON-serializable dictionary.
    return {
        "image_base64": img_base64
    }


# --- Start Serverless Worker ---
# This line starts the worker and points it to our handler function.
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})