import os
from pathlib import Path
import logging

logging.basicConfig(format="%(name)s [%(levelname)s] %(message)s", level=logging.DEBUG)
op("td_pip").PrepareModule("maturin_import_hook")
import maturin_import_hook

maturin_import_hook.reset_logger()


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
        RedhotExt.addPathEntries()
        maturin_import_hook.install(
            enable_automatic_installation=True,
            enable_project_importer=True,
            enable_reloading=True,
        )

    @staticmethod
    def addPathEntries():
        path = os.environ["PATH"]
        cargo_bin = Path.home() / ".cargo" / "bin"
        venv_bin = Path(".venv/bin").resolve()
        if str(cargo_bin) not in path:
            os.environ["PATH"] += f":{cargo_bin}"
        if str(venv_bin) not in path:
            os.environ["PATH"] += f":{venv_bin}"

    @staticmethod
    def UninstallHook():
        import maturin_import_hook

        maturin_import_hook.uninstall()
