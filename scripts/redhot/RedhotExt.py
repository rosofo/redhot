op("td_pip").PrepareModule("maturin_import_hook")
import logging

logging.basicConfig(format="%(name)s [%(levelname)s] %(message)s", level=logging.DEBUG)
import sys
from pathlib import Path
from maturin_import_hook.project_importer import MaturinProjectImporter


class CustomImporter(MaturinProjectImporter):
    def find_maturin(self) -> Path:
        return Path(".venv/bin/maturin").resolve()


CustomParHelper: CustomParHelper = (
    next(d for d in me.docked if "ExtUtils" in d.tags)
    .mod("CustomParHelper")
    .CustomParHelper
)  # import
NoNode: NoNode = (
    next(d for d in me.docked if "ExtUtils" in d.tags).mod("NoNode").NoNode
)  # import
###


class RedhotExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        CustomParHelper.Init(
            self, ownerComp, enable_properties=True, enable_callbacks=True
        )
        NoNode.Init(
            enable_chopexec=False, enable_datexec=False, enable_keyboard_shortcuts=False
        )

    @staticmethod
    def InstallHook():
        import maturin_import_hook

        maturin_import_hook.reset_logger()
        importer = CustomImporter(
            enable_reloading=True,
            enable_automatic_installation=True,
        )
        sys.meta_path.insert(0, importer)

    @staticmethod
    def UninstallHook():
        import maturin_import_hook

        maturin_import_hook.uninstall()
