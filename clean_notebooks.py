#!/usr/bin/env python3
"""
Jupyter notebook output cleaner
Usage:
    python clean_notebooks.py           # clean all notebooks in current dir
    python clean_notebooks.py nb1.ipynb # clean specific notebook
"""

from pathlib import Path
import sys
import argparse
import json
import nbformat


def validate_notebook(path: Path) -> tuple[bool, str]:
    """Validate if file is a Jupyter notebook"""
    if not path.exists():
        return False, f"File not found: {path}"
    if path.suffix not in ['.ipynb', '.json']:
        return False, f"Not a notebook file: {path} (must end in .ipynb)"
    try:
        with open(path, encoding='utf-8') as f:
            content = json.load(f)
        if 'cells' not in content:
            return False, f"Not a valid notebook: {path} (no cells found)"
        return True, ""
    except json.JSONDecodeError:
        return False, f"Not a valid JSON file: {path}"
    except Exception as e:  # pylint: disable=broad-except
        return False, f"Error validating {path}: {str(e)}"


def clean_notebook(notebook_path: Path, check_only: bool = False) -> bool:
    """Clean all outputs from a notebook or check if it has outputs"""
    try:
        # Validate first
        is_valid, error_msg = validate_notebook(notebook_path)
        if not is_valid:
            print(f"Error: {error_msg}")
            return None

        print(f"Processing {notebook_path}...")
        with open(notebook_path, encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Track if notebook has outputs
        had_outputs = False

        for cell in nb.cells:
            if cell.cell_type == 'code':
                if cell.get('outputs') or cell.get('execution_count'):
                    had_outputs = True
                    if check_only:
                        break
                if not check_only:
                    cell['outputs'] = []
                    cell['execution_count'] = None

        if check_only:
            if had_outputs:
                print(f"❌ {notebook_path} contains outputs/execution counts")
                return str(notebook_path)
            else:
                print(f"✅ {notebook_path} is clean")
                return None
        else:
            if had_outputs:
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    nbformat.write(nb, f)
                print(f"✓ Cleaned {notebook_path}")
                return str(notebook_path)
            else:
                print(f"- No outputs to clean in {notebook_path}")
                return None

    except Exception as e:  # pylint: disable=broad-except
        print(f"Error processing {notebook_path}: {str(e)}")
        return None


def main():
    """ Main entry point for the script. """
    parser = argparse.ArgumentParser(
        description="Clean Jupyter notebook outputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "notebooks", nargs="*", help="Notebooks to clean (default: all *.ipynb)"
    )
    parser.add_argument(
        "--check", action="store_true", help="Only check for outputs without cleaning"
    )
    args = parser.parse_args()

    # Find notebooks
    if args.notebooks:
        notebooks = [Path(n) for n in args.notebooks]
    else:
        notebooks = list(Path('.').glob('*.ipynb'))

    if not notebooks:
        print("No notebooks found!")
        return 1

    # Process each notebook
    cleaned_files = []
    has_errors = False

    for nb in notebooks:
        result = clean_notebook(nb, check_only=args.check)
        if result:
            cleaned_files.append(result)
        elif result is None:  # Error occurred
            has_errors = True

    # Print summary
    if args.check:
        if cleaned_files:
            print(f"\n🚫 FOUND {len(cleaned_files)} notebooks with outputs!")
            print("Run 'python clean_notebooks.py' to clean them.")
            return 1  # Exit with error code to block commit
        else:
            print("\n✅ All notebooks are clean")
            return 0
    else:
        if cleaned_files:
            print("\nCLEANED_FILES:")
            for f in cleaned_files:
                print(f)

    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
