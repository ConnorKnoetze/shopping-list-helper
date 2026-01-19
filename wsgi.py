"""App entry point."""

import os

from pantry import create_app
from dotenv import load_dotenv

app = create_app()

if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=5000, threaded=True)
