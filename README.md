# Build-a-Bird
Final project for COSC365 at IUP.

## Setup (Linux)
1. Clone the repository and change into its directory.
2. Install Poetry for dependency management (see [docs](https://python-poetry.org/docs/)) and activate your virtual environment.
3. Run `poetry install` in terminal to install dependencies from `pyproject.toml`.
4. Run `flask --app src/build_a_bird/app/launch run --debug` in terminal to start serving the Flask app in debug mode. **Do not use this in a production environment!**
5. Open browser and navigate to `localhost:5000` - you should see the home page :)
