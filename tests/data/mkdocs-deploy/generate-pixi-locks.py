#!/usr/bin/env python3
"""Generate pixi.lock files for test fixtures that need them."""

import subprocess
import sys
from pathlib import Path

# Directories that need pixi.lock files
PIXI_DIRS = [
    "test-pull-request-pixi",
    "test-release-trigger-pixi",
    "test-package-manager-commands",
]

def main():
    base_dir = Path(__file__).parent

    for dir_name in PIXI_DIRS:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            print(f"Directory not found: {dir_path}")
            continue

        print(f"\nGenerating pixi.lock for {dir_name}...")
        try:
            # Run pixi install to generate lock file
            result = subprocess.run(
                ["pixi", "install"],
                cwd=dir_path,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✓ Successfully generated pixi.lock in {dir_name}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to generate pixi.lock in {dir_name}")
            print(f"Error: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print("✗ pixi command not found. Please install pixi first:")
            print("  curl -fsSL https://pixi.sh/install.sh | bash")
            sys.exit(1)

    print("\n✓ All pixi.lock files generated successfully!")

if __name__ == "__main__":
    main()

