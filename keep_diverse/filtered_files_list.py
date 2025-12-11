from .knee import Knee


class FilteredFilesList:
    def __init__(self, kept_files_path: str):
        self.kept_files_path = kept_files_path

    def save(self, knee: Knee):
        content = "\n".join(knee.good_files())
        with open(self.kept_files_path, "w") as f:
            f.write(content)
