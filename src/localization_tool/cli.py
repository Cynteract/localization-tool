import argparse
import io
import os
import subprocess
import tarfile
import tempfile

"""Command Line Interface for the localization tool."""


def restore_historic_localization_folder(localization_path: str, temp_dir: str):
    """Creates a folder for historic localization files."""
    # Use git archive to extract the previous version of the localization_path into temp_dir
    archive_proc = subprocess.run(
        ["git", "archive", "HEAD", localization_path],
        stdout=subprocess.PIPE,
        check=True,
    )
    with tarfile.open(fileobj=io.BytesIO(archive_proc.stdout)) as tar:
        tar.extractall(path=temp_dir)
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                print(os.path.relpath(os.path.join(root, file), temp_dir))
    print(f"Restored previous version of {localization_path} to {temp_dir}")


def main():
    """Main entry point for the CLI."""
    try:
        parser = argparse.ArgumentParser(
            prog="python -m localization_tool",
            description="Localization Tool CLI - Version 0.1.0",
        )
        parser.add_argument(
            "--localization-path",
            type=str,
            required=True,
            help="Path to the localization files.",
        )
        args = parser.parse_args()

        print("Localization Tool CLI - Version 0.1.0")
        print("Use --help to see available commands.")

        with tempfile.TemporaryDirectory() as temp_dir:
            if args.localization_path:
                restore_historic_localization_folder(args.localization_path, temp_dir)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
