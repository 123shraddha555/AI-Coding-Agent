import difflib


def generate_diff(original, updated, filename):
    diff = difflib.unified_diff(
        original.splitlines(),
        updated.splitlines(),
        fromfile=f"{filename} (before)",
        tofile=f"{filename} (after)",
        lineterm="")

    return "\n".join(diff)