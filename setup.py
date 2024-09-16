from setuptools import setup
from setuptools.command.install import install as _install
import subprocess
import sys
import os



# class InstallCommand(_install):
#     """Custom install command to run post-installation tasks."""
#
#     def run(self):
#         # Run the standard install process
#         _install.run(self)
#         # os.makedirs(r"C:\Users\eliem\AppData\Local\BUA", exist_ok=True)
#         setup_dot_py_dir = os.path.dirname(__file__)
#         package_dir = os.path.abspath(os.path.join(setup_dot_py_dir, 'src','bua'))
#         # Define the path to the post-installation script
#         script_path = os.path.join(setup_dot_py_dir, 'src/bua/config/bua_config_structure.py')
#         print(f"Running post-installation script: {script_path}")
#         sys.stdout.flush()
#
#         # Check if the script exists before running it
#         if os.path.exists(script_path):
#             # Run the post-installation script
#             subprocess.check_call([sys.executable, script_path, 'setup','--version', version_tag])
#         else:
#             print(f"Post-installation script not found: {script_path}")`


def run_setup_script_and_get_version():
    version_tag = "0.0.0"  # Default version tag or fetch from another source
    # os.makedirs(r"C:\Users\eliem\AppData\Local\BUA", exist_ok=True)
    setup_dot_py_dir = os.path.dirname(__file__)
    # Define the path to the post-installation script
    script_path = os.path.join(setup_dot_py_dir, 'src/bua/config/bua_config_structure.py')

    # Run the setup script with the version tag
    subprocess.check_call(['python', script_path, '--version', version_tag, '--setup',"true"])


    return version_tag

version_tag = run_setup_script_and_get_version()

setup(
    version=version_tag
)