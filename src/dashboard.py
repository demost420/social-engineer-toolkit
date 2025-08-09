"""Simple dashboard interface for the Social-Engineer Toolkit.

This module provides a minimal text-based control panel for exploring
available SET modules. It lists sub-packages within ``src`` and allows the
user to attempt execution of a selected module if it exposes a ``main``
function. The dashboard is intended as a lightweight convenience utility
and does not replace the full ``setoolkit`` interactive menu.
"""

from __future__ import annotations

import importlib
import os
from typing import List

MODULE_DIR = os.path.dirname(__file__)


def list_modules() -> List[str]:
    """Return a list of available modules under :data:`MODULE_DIR`.

    Only directories that are not private (do not start with ``_``) are
    considered modules. The order of modules is alphabetical.
    """

    modules = []
    for name in sorted(os.listdir(MODULE_DIR)):
        path = os.path.join(MODULE_DIR, name)
        if os.path.isdir(path) and not name.startswith("__"):
            modules.append(name)
    return modules


def display_menu(modules: List[str]) -> None:
    """Print the dashboard menu to stdout."""

    print("SET Dashboard - Control Panel")
    print("=" * 30)
    for index, name in enumerate(modules, start=1):
        print(f"{index}. {name}")
    print("0. Exit")


def run_module(module_name: str) -> None:
    """Attempt to run the chosen module.

    The function imports ``src.<module_name>.main`` and executes its
    ``main`` function. If the module cannot be imported or does not expose
    a ``main`` function, the error is printed to the user.
    """

    try:
        module = importlib.import_module(f"src.{module_name}.main")
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Module '{module_name}' does not define a main() function.")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to execute module '{module_name}': {exc}")


def main() -> None:
    """Entry point for the dashboard utility."""

    modules = list_modules()
    while True:
        display_menu(modules)
        choice = input("Select module: ").strip()
        if choice == "0":
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(modules):
                run_module(modules[idx])
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number corresponding to the module.")
        print()


if __name__ == "__main__":  # pragma: no cover
    main()
