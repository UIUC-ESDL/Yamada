"""
Most tests are written in Jupyter Notebooks to include explanations and visualizations.
To run these tests with pytest, we must extract the test cells from the notebooks.
"""

import pytest
import nbformat
from pathlib import Path


def pytest_collect_file(file_path, parent):
    """
    Automatically discover and include Jupyter Notebooks (.ipynb) in pytest.
    """
    # Ensure the path is a pathlib.Path object
    path = Path(file_path)
    if path.suffix == ".ipynb":
        return NotebookFile.from_parent(parent, path=path)


class NotebookFile(pytest.File):
    """
    Custom Pytest collector for Jupyter Notebooks.
    """
    def __init__(self, path: Path, parent, **kwargs):
        super().__init__(path=path, parent=parent, **kwargs)
        self.path = path

    def collect(self):
        """
        Collect test cells from the Jupyter notebook.
        """
        with self.path.open("r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        for i, cell in enumerate(notebook.cells):
            if cell.cell_type == "code" and "def test_" in cell.source:
                yield NotebookTest.from_parent(self, name=f"cell_{i}", cell=cell)


class NotebookTest(pytest.Item):
    """
    Pytest item representing an individual test cell from a notebook.
    """
    def __init__(self, name, parent, cell, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)
        self.cell = cell

    def runtest(self):
        """
        Execute the test cell in a global namespace.
        """
        exec(self.cell.source, globals())

    def repr_failure(self, excinfo):
        """
        Customize the error message when a test fails.
        """
        return f"Test failed in notebook cell:\n{self.cell.source}\n{excinfo.value}"

    def reportinfo(self):
        """
        Return information for reporting test results.
        """
        return self.path, 0, f"notebook test: {self.name}"
