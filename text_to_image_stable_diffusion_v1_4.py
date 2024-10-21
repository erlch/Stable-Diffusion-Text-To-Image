# -*- coding: utf-8 -*-
"""text_to_image_stable_diffusion_v1_4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YL0lHhsjMyLDEWoV5R59AAiUrsL5-1Us

# **Import Required Packages**
You'll need Python (3.7+) and the following libraries:
* `torch`
* `transformers`
* `diffusers`
* `Pillow` (image display)
* `gradio` (simple UI)
"""

import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gradio'])
# For simple UI
import gradio

import torch
import transformers
# For displaying image
from PIL import Image
from diffusers import StableDiffusionPipeline

"""# **Set Up Model**

Load the `stable-diffusion-v-1-4-original` Stable Diffusion model from Hugging Face. Note: Internet connection is required to download the model weights.

Floating-point precision (FP16) can reduce computation time by halving the number of bits used for model weights. Many modern GPUs (like RTX 30xx and A100) handle FP16 operations very efficiently.

We also want to move to using a GPU as it will make Stable Diffusion significantly faster than CPU. Thus, if you are using Google Colab, go to `Runtime -> Change Runtime Type` and select `T4 GPU`.
"""

# Load the pre-trained Stable Diffusion model: https://huggingface.co/CompVis/stable-diffusion-v1-4
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

# Move model to GPU (if possible)
if torch.cuda.is_available():
    print("CUDA is available. Using GPU.")
    pipe = pipe.to("cuda")
else:
    print("CUDA is not available. Using CPU.")
    pipe = pipe.to("cpu")

# Generate an image from a text prompt
def generate_image(prompt, num_inference_steps=100, height=512, width=512):
    with torch.no_grad():
        image = pipe(prompt, num_inference_steps=num_inference_steps, height=height, width=width).images[0]
    return image

"""# **Test Image Generation**

Let's test the image generation by passing a random text prompt to the `generate_image` function.
"""

# Test image generation
prompt = "A serene landscape with a crystal-clear lake surrounded by towering snow-capped mountains, under a sky filled with soft pink and purple hues during sunset."
# Generate an image
image = generate_image(prompt)

# Display the generated image
display(image)

"""# **Create a Web Interface (using Gradio)**

To allow users to input text prompts via a simple web interface, we will use Gradio.
"""

# Define a function for Gradio UI
def generate_image_gradio(prompt):
    image = generate_image(prompt)
    return image

# Create a Gradio interface
interface = gradio.Interface(
    fn=generate_image_gradio,
    inputs=gradio.Textbox(label="Enter your prompt", placeholder="A detailed description of the image..."),
    outputs=gradio.Image(label="Generated Image"),
    title="Text-to-Image Generator",
    description="Generate images from text prompts using stable diffusion v1.4."
)

# Launch the Gradio app
interface.launch(share=True)

