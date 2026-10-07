import subprocess
import tempfile
import shutil
from pathlib import Path


def run_tests():
    """Run the existing test suite on the original sample project."""

    result = subprocess.run(
        ["python", "-m", "pytest", "tests"],
        cwd="sample_project",
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "output": result.stdout + result.stderr
    }


def validate_proposed_changes(changes):
    """
    Apply Gemini's proposed changes to a temporary copy
    of the sample project and run the test suite.
    """

    original_project = Path("sample_project").resolve()

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_project = Path(temp_dir) / "sample_project"

        # Copy the complete sample project
        shutil.copytree(
            original_project,
            temp_project
        )

        for change in changes:

            file_path = change.get("file")
            updated_code = change.get("updated_code")

            if not file_path or updated_code is None:
                return {
                    "success": False,
                    "output": "Invalid change format returned by Gemini."
                }

            # Convert Gemini path to a normal Path
            relative_path = Path(file_path)

            # Remove sample_project/ prefix
            if relative_path.parts and relative_path.parts[0] == "sample_project":
                relative_path = Path(*relative_path.parts[1:])

            target_file = (temp_project / relative_path).resolve()

            # Security check: prevent path traversal
            try:
                target_file.relative_to(temp_project.resolve())
            except ValueError:
                return {
                    "success": False,
                    "output": f"Unsafe file path rejected: {file_path}"
                }

            # Only allow Python files
            if target_file.suffix != ".py":
                return {
                    "success": False,
                    "output": f"Only Python files can be modified: {file_path}"
                }

            # Only modify files that already exist
            if not target_file.exists():
                return {
                    "success": False,
                    "output": f"File does not exist: {file_path}"
                }

            # Apply proposed code to temporary copy
            target_file.write_text(
                updated_code,
                encoding="utf-8"
            )

        # Run tests against the modified temporary project
        result = subprocess.run(
            ["python", "-m", "pytest", "tests"],
            cwd=temp_project,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr
        }  