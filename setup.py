from setuptools import setup
from setuptools.command.install import install as _install
import subprocess
import sys
import os


class InstallCommand(_install):
    """Custom install command to run post-installation tasks."""

    def run(self):
        # Run the standard install process
        _install.run(self)

        # Define the path to the post-installation script
        script_path = os.path.join(os.path.dirname(__file__), 'your_package/_setup/setup_script.py')

        # Check if the script exists before running it
        if os.path.exists(script_path):
            # Run the post-installation script
            subprocess.check_call([sys.executable, script_path, 'setup'])
        else:
            print(f"Post-installation script not found: {script_path}")


setup(
    cmdclass={
        'install': InstallCommand,
    },
)