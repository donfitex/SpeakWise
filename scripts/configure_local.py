"""Create local development settings once; never overwrite existing configuration."""

import os
import secrets
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    destination = root / ".env"
    if destination.exists():
        print("Existing .env preserved.")
        return
    template = (root / ".env.example").read_text()
    template = template.replace(
        "DJANGO_SECRET_KEY=\n", "DJANGO_SECRET_KEY=" + secrets.token_urlsafe(48) + "\n"
    ).replace("POSTGRES_PASSWORD=\n", "POSTGRES_PASSWORD=" + secrets.token_urlsafe(32) + "\n")
    # Exclusive creation protects concurrent setup and existing user files.
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as handle:
        handle.write(template)
    destination.chmod(0o600)
    print("Created private local .env. No secret values were printed.")


if __name__ == "__main__":
    main()
