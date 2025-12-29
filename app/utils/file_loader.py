from pathlib import Path

def load_text_files(directory: Path):
    for file_path in directory.glob('*.md'):
        yield {
            "id": file_path.stem,
            "source": str(file_path),
            "text": file_path.read_text(encoding="utf-8")
        }