from pathlib import Path
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


BASE_DIR = Path.home() / "Desktop"


# ---------------------------
# Path Resolver (Secure)
# ---------------------------
def resolve_pdf_path(user_input: str) -> Path:
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


# ---------------------------
# MCP Tools
# ---------------------------
def pdf_tools_func(mcp):

    # ---------------------------
    # READ PDF
    # ---------------------------
    @mcp.tool()
    def read_pdf(file: str) -> str:
        """Read full text of a PDF file from Desktop."""

        file_path = resolve_pdf_path(file)

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError("Only .pdf files allowed")

        reader = PdfReader(file_path)

        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return text


    # ---------------------------
    # SEARCH PDF
    # ---------------------------
    @mcp.tool()
    def search_pdf(file: str, query: str) -> str:
        """Search for a keyword inside a PDF."""

        file_path = resolve_pdf_path(file)

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        reader = PdfReader(file_path)

        matches = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if query.lower() in text.lower():
                matches.append(f"Page {i+1}:\n{text[:800]}")

        if not matches:
            return "No matches found."

        return "\n\n".join(matches[:5])


    # ---------------------------
    # DELETE PDF (STRICT CONFIRM)
    # ---------------------------
    @mcp.tool()
    def delete_pdf(file: str, confirm: str = "") -> str:
        """
        Delete a PDF file.
        Requires confirm="DELETE filename.pdf"
        """

        file_path = resolve_pdf_path(file)

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        expected = f"DELETE {file_path.name}"

        if confirm.strip().upper() != expected.upper():
            return (
                "❌ Deletion cancelled.\n\n"
                f'To delete this file, call again with:\n'
                f'confirm="{expected}"'
            )

        file_path.unlink()

        return f"✅ Deleted: {file_path.name}"


    # ---------------------------
    # RENAME PDF (STRICT CONFIRM)
    # ---------------------------
    @mcp.tool()
    def rename_pdf(file: str, new_name: str, confirm: str = "") -> str:
        """
        Rename a PDF file.
        
        """

        file_path = resolve_pdf_path(file)

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        if not new_name.lower().endswith(".pdf"):
            raise ValueError("New name must end with .pdf")

        expected = f"RENAME {file_path.name}"

        if confirm.strip().upper() != expected.upper():
            return (
                "❌ Rename cancelled.\n\n"
                f'To rename this file, call again with:\n'
                f'confirm="{expected}"'
            )

        new_path = file_path.parent / new_name
        file_path.rename(new_path)

        return f"✅ Renamed to: {new_name}"


    # ---------------------------
    # CREATE PDF (STRICT CONFIRM)
    # # ---------------------------

    

    @mcp.tool()
    def create_pdf(file: str, content: str) -> str:
        """
        Create a new PDF file on Desktop.
        If file already exists, ask for a different name.
        """

        file_path = resolve_pdf_path(file)

        # Force .pdf extension
        if not file_path.name.lower().endswith(".pdf"):
            file_path = file_path.with_suffix(".pdf")

        # ✅ DO NOT RAISE — RETURN MESSAGE INSTEAD
        if file_path.exists():
            return (
                f"⚠️ A file named '{file_path.name}' already exists on your Desktop.\n\n"
                f"Please provide a different file name."
            )

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(str(file_path))
        styles = getSampleStyleSheet()
        elements = []

        if not content.strip():
            content = "Empty Document"

        for line in content.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))

        doc.build(elements)

        return f"✅ Created: {file_path.name}"
    

    @mcp.tool
    def find_relevant_pdfs_on_desktop(query: str) -> str:
        """
        Search all PDF files on the Desktop and return those
        that contain information related to the given query.
        """

        import os
        from pypdf import PdfReader

        desktop = os.path.expanduser("~/Desktop")

        results = []

        for file in os.listdir(desktop):

            if not file.lower().endswith(".pdf"):
                continue

            path = os.path.join(desktop, file)

            try:
                reader = PdfReader(path)

                text = ""

                for page in reader.pages:
                    text += page.extract_text() or ""

                if query.lower() in text.lower():
                    results.append(file)

            except Exception:
                pass

        if not results:
            return "No relevant PDF files found."

        return "Relevant PDFs:\n" + "\n".join(results)
