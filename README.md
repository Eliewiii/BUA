### Installation Instructions

#### 1. Standard Installation (With Setup Script)

By default, the package will run the setup script during installation to configure necessary files.
To install the package with the setup script:

```bash
pip install .
```

This will execute the pre-installation setup script, which may include downloading required files or performing other
configurations.

#### 2. Skip Setup Script During Installation

If you want to install the package without running the setup script (for example, during development), you can skip the
script by setting the SKIP_SETUP_SCRIPT environment variable to true:

* Linux/macOS:

```bash
SKIP_SETUP_SCRIPT=true pip install .
```
* Windows (Command Prompt):

```cmd
set SKIP_SETUP_SCRIPT=true
pip install .
```

* Windows (PowerShell):

```powershell
$env:SKIP_SETUP_SCRIPT="true"
pip install .
```
This will install the package without running the setup script. You can later run the setup script manually if
needed.

