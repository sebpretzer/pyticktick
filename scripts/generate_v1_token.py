#! /usr/bin/env uv run python

"""Script to generate a token for the v1 API.

This script will prompt the user for the necessary information to trigger the OAuth
flow to generate a token for the v1 API. This will require the a web browser to
authenticate.

Once generated, the user has the option of copying the token to the clipboard,
printing it to the console, or saving it to a file.
"""

from pathlib import Path
from time import time

from click import confirm, prompt
from loguru import logger

from pyticktick import Settings


def main() -> None:
    """Generate a token for the v1 API."""
    client_id = prompt("Enter your client_id")
    client_secret = prompt("Enter your client_secret")
    redirect_url = prompt("Enter your OAuth redirect URL")

    logger.info("Launching the OAuth2 flow to generate a token for the v1 API")
    logger.info(f" - client_id: {client_id}")
    logger.info(f" - client_secret: {client_secret}")
    logger.info(f" - redirect_url: {redirect_url}")

    token = Settings.v1_signon(client_id, client_secret, redirect_url)
    token_value = token.access_token
    token_expiration = token.expires_in + int(time())

    logger.info("Token generated successfully.")

    if confirm("Do you want the token to be copied to the clipboard?", default=True):
        # https://github.com/asweigart/pyperclip/issues/210
        import pyperclip  # type: ignore[import-untyped] # noqa: PLC0415

        pyperclip.copy(str(token_value))
        logger.info("Token copied to clipboard.")
        input("Press Enter to continue...")

        pyperclip.copy(str(token_expiration))
        logger.info("Token expiration copied to clipboard.")
    elif confirm("Do you want to print the token and its expiration?", default=True):
        logger.info(f"Token: {token_value}")
        logger.info(f"Token expiration: {token_expiration}")
    else:
        _file_path = prompt("Enter the file path to save the token and expiration: ")
        file_path = Path(_file_path)
        if file_path.exists():
            confirm("File already exists. Overwrite?", abort=True)
        elif not file_path.parent.exists():
            confirm("Parent directory does not exist. Create?", abort=True)
            file_path.parent.mkdir(parents=True)
        _text = f"""
        PYTICKTICK_V1_CLIENT_ID="{client_id}"
        PYTICKTICK_V1_CLIENT_SECRET="{client_secret}"
        PYTICKTICK_V1_TOKEN_VALUE="{token_value}"
        PYTICKTICK_V1_TOKEN_EXPIRATION="{token_expiration}"
        """
        file_path.write_text(_text)
        logger.info(f"Token and expiration saved to `{file_path}`")


if __name__ == "__main__":
    main()
