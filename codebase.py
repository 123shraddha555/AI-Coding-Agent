from pathlib import Path

RELEVANT_FILES = [
    "config.py",
    "models.py",
    "validators.py",
    "services.py",
    "routers.py",
    "tests/test_validators.py",
    "tests/test_services.py",
    "tests/test_routes.py",
]

def get_codebase_files(codebase_path):
    """
    Find relevant Python files inside the sample project.
    """

    codebase = Path(codebase_path)

    files = []

    for relative_file in RELEVANT_FILES:

        file_path = codebase / relative_file

        if file_path.exists() and file_path.suffix == ".py":
            files.append(file_path)

    return files


def read_file(file_path):
    """
    Read a Python file.
    """

    return Path(file_path).read_text(
        encoding="utf-8"
    )


def build_codebase_context(codebase_path):
    """
    Build a compact codebase context for Gemini.

    Only relevant source and test files are included
    to reduce prompt size and improve response speed.
    """

    files = get_codebase_files(
        codebase_path
    )

    context = []

    for file in files:

        content = read_file(file)

        context.append(
            f"FILE: {file}\n"
            f"{content}\n"
            f"{'-' * 60}"
        )

    return "\n".join(context)