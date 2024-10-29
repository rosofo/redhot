from pathlib import Path
from tempfile import TemporaryDirectory


CustomParHelper: CustomParHelper = (
    next(d for d in me.docked if "ExtUtils" in d.tags)
    .mod("CustomParHelper")
    .CustomParHelper
)  # import
NoNode: NoNode = (
    next(d for d in me.docked if "ExtUtils" in d.tags).mod("NoNode").NoNode
)  # import
###


class RedhotReleaseExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        CustomParHelper.Init(
            self, ownerComp, enable_properties=True, enable_callbacks=True
        )
        NoNode.Init(
            ownerComp,
            enable_chopexec=True,
            enable_datexec=True,
            enable_parexec=True,
            enable_keyboard_shortcuts=True,
        )
        self.td_pip = ownerComp.op("td_pip")
        self.Status = tdu.Dependency(val="Not Installed")

        if len(self.wheels) == 0:
            self.Status.val = "Nothing Prepared for Install"
            return

        is_present = self.td_pip.TestModule(self.evalModule, silent=True)
        if is_present:
            self.Status.val = "Installed"
            return
        if self.evalInstalloncreate:
            self.Install()
        else:
            self.Status.val = "Not Installed"

    @property
    def wheels(self):
        return self.ownerComp.op("virtualFile").vfs.find(pattern="*.whl")

    def onParInstall(self, val):
        self.Install()

    def onParPreparerelease(self, val):
        self.Status.val = "Preparing"
        path = self.evalWheel
        if not path:
            self.Status.val = "No Wheel Selected"
            return
        try:
            self.ownerComp.op("virtualFile").AddFile(path)
        except Exception as e:
            self.Status.val = "Failed to bundle wheel: See Textport"
            debug(f"Failed to prepare {path}: {e}")
            return
        self.parInstalloncreate.val = True
        self.Status.val = "Ready to release; set Module to the name of the top-level import and include this COMP in your .tox"

    def Install(self):
        try:
            wheels = self.ownerComp.op("virtualFile").vfs
            with TemporaryDirectory() as tempdir:
                wheels.export(tempdir)
                tempdir = Path(tempdir)
                paths = list(tempdir.glob("*"))
                for path in paths:
                    self.td_pip.InstallPackage(str(path))
        except Exception as e:
            self.Status.val = "Failed: See Textport"
            debug(f"Failed to install {self.evalModule}: {e}")
            return
