from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

project_dir = Path(__file__).resolve().parents[1]
notebook_path = project_dir / "entregables" / "segunda_entrega.ipynb"

with notebook_path.open(encoding="utf-8") as stream:
    notebook = nbformat.read(stream, as_version=4)

executor = ExecutePreprocessor(timeout=600, kernel_name="python3")
print(f"Executing {notebook_path.name} ...")
executor.preprocess(notebook, {"metadata": {"path": str(project_dir)}})

with notebook_path.open("w", encoding="utf-8") as stream:
    nbformat.write(notebook, stream)

print("Notebook executed and saved with outputs.")
