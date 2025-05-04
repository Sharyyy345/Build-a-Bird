# Build-a-Bird
Final project for COSC365 at IUP.

## Setup (Linux)
1. Clone the repository and change into its directory.
2. Install Poetry for dependency management (see [docs](https://python-poetry.org/docs/)) and activate your virtual environment.
3. Run `poetry install` in terminal to install dependencies from `pyproject.toml`.
4. Create `.env` file outside `src` directory. 

    At a minimum, you'll need to specify the `APP_EMAIL` (expects gmail.com address) and `APP_EMAIL_PASSWORD` variables in order to send receipt emails. See https://stackoverflow.com/a/27515833/ for more info on `APP_EMAIL_PASSWORD` setup.

    Image generation should work without specifying the `DIFFUSERS_MODEL_ID` variable. By default [Stable Diffusion v1-5](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5) is used but you can use any model from Hugging Face.

    `MODEL_DEVICE` is the name of the hardware component to run the image generation model on. If you have an NVIDIA GPU, set it to cuda. If you don't have a GPU, use CPU. The default is cpu.

    `IMG_SIZE` is the width and height (in pixels) of the generated image. This is 128x128 by default.

    Sample `.env` configuration:
    ```
    APP_EMAIL = noreply@gmail.com
    APP_EMAIL_PASSWORD = iuzr jmsb tgpr tpq
    DIFFUSERS_MODEL_ID = stabilityai/sdxl-turbo
    MODEL_DEVICE = cuda
    IMG_SIZE = 128
    ```
5. Run `flask --app src/build_a_bird/app/launch run --debug` in terminal to start serving the Flask app in debug mode. **Do not use this in a production environment!**
6. Open browser and navigate to `localhost:5000` - you should see the home page :)
