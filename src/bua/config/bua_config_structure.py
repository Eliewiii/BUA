import os
import platform


def ensure_directory_exists(directory):
    """Ensure that the specified directory exists. Create it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def get_root_folders():
    """Return the root and user folders for the package's additional data based on the operating system."""
    os_name = platform.system().lower()

    if os_name == "windows":
        root_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'your_package_data')  # For machine-specific data
        user_folder = os.path.join(os.getenv('APPDATA'), 'your_package_data')  # For user-specific data
    elif os_name == "linux":
        root_folder = os.path.join(os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share")),
                                   'your_package_data')
        user_folder = os.path.join(os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config")), 'your_package_data')
    elif os_name == "darwin":
        root_folder = os.path.join(os.path.expanduser("~"), 'Library', 'Application Support', 'your_package_data')
        user_folder = os.path.join(os.path.expanduser("~"), 'Library', 'Preferences', 'your_package_data')
    else:
        raise OSError("Unsupported operating system")

    # Ensure the directories exist
    ensure_directory_exists(root_folder)
    ensure_directory_exists(user_folder)

    return root_folder, user_folder


# Define paths using the root folder
root_folder,user_folder = get_root_folders()

simulation_data_path = os.path.join(root_folder, 'simulation_data')
weather_data_path = os.path.join(root_folder, 'weather_data')

# Optional: Ensure these directories exist
ensure_directory_exists(simulation_data_path)
ensure_directory_exists(weather_data_path)

# Example usage within the module (for debugging or setup)
if __name__ == "__main__":
    print("Configuration settings:")
    print(f"Root folder: {root_folder}")
    print(f"Simulation data path: {simulation_data_path}")
    print(f"Weather data path: {weather_data_path}")
