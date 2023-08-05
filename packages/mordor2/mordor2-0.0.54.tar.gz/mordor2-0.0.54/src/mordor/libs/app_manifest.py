from typing import List, Optional


class AppManifest:
    """Represent application manifest
    """

    manifest: dict  # the manifest of the application

    def __init__(self, manifest: dict):
        self.manifest = manifest

    @property
    def version(self) -> str:
        return self.manifest["version"]

    @property
    def exclude_dirs(self) -> List[str]:
        return self.manifest.get("exclude_dirs", [])

    @property
    def stage(self) -> Optional[str]:
        return self.manifest.get("stage")
