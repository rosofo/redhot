# redhot - pyo3 (python + rust) auto-reloading for TouchDesigner

This is a little COMP to make your life easier when integrating Rust into your extensions

## tl;dr

Let's assume you've got:

- A TouchDesigner project with a project folder
- A Python venv under `$PROJECT/.venv`
- A Rust installation

And you want:

- To develop a Rust extension with Python bindings usable in TD
- Have it automatically *rebuild* and *reload* when you re-init your TD extensions, scripts, etc
  
Then follow these steps:

- With the venv activated run `pip install maturin maturin-import-hook`
  - This installs [maturin](https://www.maturin.rs/) (the pyo3 build tool) and [maturin-import-hook](https://github.com/PyO3/maturin-import-hook)
- Run `maturin new <name>` inside your project folder
  - Creates a pyo3 package which will contain your Rust code
  - This name is what you'll be importing in Python-land
- Run `cd <name>; maturin develop --release`
  - Builds and installs the package into the venv
  - Should only be necessary once
- Grab `redhot.tox` and drop it into TouchDesigner
  - Sets up the environment and some magic hooks
- Import your package like so
  
  ```python
  import importlib
  import <name>  # careful: your Rust module will be exposed under `<name>.<name>`
  importlib.reload(<name>)
  ```

  The `reload` call normally has no effect on native code, but now it will rebuild and reinstall your package if there were any changes, and force the Python interpreter to actually reload it from disk!

  - check for output in the Textport
  - note that while a rebuild is happening the TD process will hang. This should only happen when you've edited Rust code and then enabled/disabled your COMP/script, re-inited, etc


## Motivation

[pyo3](https://pyo3.rs/) is great and gives us an easy way to integrate Rust into Python projects. The only catch is that CPython can't reload native extensions, requiring you to restart the interpreter when you make changes. Bad news for TouchDesigner - you'd have to restart the whole app as part of your feedback loop!

More background on this can be found at [maturin-import-hook/docs/reloading.md](https://github.com/PyO3/maturin-import-hook/blob/main/docs/reloading.md), if you're interested.

## Solution

This COMP uses [maturin-import-hook](https://github.com/PyO3/maturin-import-hook) which includes some clever tricks to force the Python interpreter into reloading pyo3 extensions properly. The hook also provides conveniences for auto-building etc, so it makes sense to try to use it.

## How It Works

On `RedhotExt` init we do some preliminary setup of the environment:

- TouchDesigner doesn't inherit the system path, at least on MacOS, so we need to add `$HOME/.cargo/bin` to the `PATH` so that the `rustc` command is available
- We need to ensure the venv you're using (which is assumed to be in the project folder under `.venv` and to have `maturin` and `maturin-import-hook` installed!) is also in the `PATH`
- The venv also needs to be added to the Python search path, which is done by appending to `sys.path`

After that it's just a call to `maturin_import_hook.install()` and the hook handles everything
