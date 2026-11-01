"""Exchange an EmbeddedSetup oauth_token cookie for a gkeepapi master token.

Run this once with `uv run python scripts/get_master_token.py`. The cookie is
read with hidden input and is not stored. Protect the printed master token
like a password.
"""

import getpass
import secrets

import gpsoauth


def main() -> None:
    email = input("Google account email: ").strip()
    oauth_token = getpass.getpass("EmbeddedSetup oauth_token cookie (input hidden): ").strip()
    if not email or not oauth_token:
        raise SystemExit("Email and oauth_token cookie are required.")
    device_id = secrets.token_hex(8)

    response = gpsoauth.exchange_token(email, oauth_token, device_id)
    master_token = response.get("Token")
    if not master_token:
        raise SystemExit(
            f"Token exchange failed: {response.get('Error', 'unknown error')}. "
            "Check the account email and obtain a fresh oauth_token cookie."
        )

    print("\nSuccess. Set these in the MCP server's environment:\n")
    print(f"GOOGLE_KEEP_EMAIL={email}")
    print(f"GOOGLE_KEEP_MASTER_TOKEN={master_token}")
    print(f"GOOGLE_KEEP_DEVICE_ID={device_id}")
    print(
        "\nThe device ID is pinned so future logins look like the same "
        "device — keep it paired with this master token."
    )


if __name__ == "__main__":
    main()
