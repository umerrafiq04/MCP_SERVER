from fastmcp import FastMCP
from pathlib import Path

# mcp = FastMCP("desktop_control")

BASE_DIR = Path.home() / "Desktop"

def resolve_path(user_input: str) -> Path:
    cleaned = user_input.strip()

    for token in ["desktop", "Desktop", "on my desktop", "in desktop"]:
        cleaned = cleaned.replace(token, "")

    cleaned = cleaned.strip("/\\ ")

    if ".." in cleaned:
        raise ValueError("Invalid path")

    target = (BASE_DIR / cleaned).resolve()

    if not str(target).startswith(str(BASE_DIR)):
        raise ValueError("Access outside Desktop is not allowed")

    return target

def read_text(file_path: Path) -> str:
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")
def detect_mode(instruction: str) -> str:
    """
    Decide whether to append or overwrite based on user intent.
    """
    instruction = instruction.lower()

    overwrite_keywords = [
        "overwrite",
        "replace",
        "remove previous",
        "clear",
        "delete content",
        "reset file",
        "replace all"
    ]

    for word in overwrite_keywords:
        if word in instruction:
            return "overwrite"

    return "append"  # safe default

def desktop_tools_func(mcp):

    @mcp.tool()
    def read_file(path: str) -> str:
        """Read a .txt file from Desktop or subfolders."""
        file_path = resolve_path(path)

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are allowed")

        return read_text(file_path)
    
    # list files
    @mcp.tool()
    def list_files(path: str="")->list[str]:
        """List files in a Desktop folder."""
        target = resolve_path(path)

        if not target.exists():
            raise FileNotFoundError("Folder not found")

        if not target.is_dir():
            raise ValueError("Path is not a directory")

        return [p.name for p in target.iterdir()]  
    
# bydefault append --user can request to overwrite
# if file is not present python will create automatically
    @mcp.tool()
    def write_file(
        path: str,
        content: str = "",
        instruction: str = ""
    ) -> str:
        """
        Write to a .txt file.

        - Appends by default
        - Overwrites ONLY if user instruction explicitly says so
        """
        file_path = resolve_path(path)

        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are allowed")

        if not content.strip():
            raise ValueError("No content provided")

        mode = detect_mode(instruction)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        if mode == "overwrite":
            file_path.write_text(content, encoding="utf-8")
            action = "Overwritten"
        else:
            previous = read_text(file_path)
            new_text = (
                previous + ("\n" if previous and not previous.endswith("\n") else "") + content
            )
            file_path.write_text(new_text, encoding="utf-8")
            action = "Appended"

        final_content = read_text(file_path)

        return (
            f"✅ {action} file: {file_path.name}\n\n"
            f"📄 Current content:\n"
            f"{final_content}"
        )
    

    @mcp.tool()
    def delete_file(path: str, confirm: str = "") -> str:
        """
        Delete a file from Desktop ONLY.
        Requires explicit confirmation by typing YES.
        """

        if not path.strip():
            raise ValueError("No file path provided")

        file_path = resolve_path(path)

        if not file_path.exists():
            raise FileNotFoundError("File does not exist")

        if not file_path.is_file():
            raise ValueError("Only files can be deleted (folders are blocked)")

        if confirm.strip().upper() != "YES":
            return (
                "❌ Deletion cancelled.\n\n"
                f"To delete this file, call again with:\n"
                f'confirm="YES"\n\n'
                f"File: {file_path.name}"
            )

        file_path.unlink()

        return (
            "✅ File deleted successfully.\n\n"
            f"🗑️ Deleted file: {file_path.name}"
        )



      

        

    




