import requests
import argparse
from typing import List
from packaging import version

from packaging.specifiers import SpecifierSet


def is_python_version_compatible(specifier: str, python_version: str) -> bool:
    """
    Determines if the specified Python version matches the given version specifier.

    Args:
        specifier (str): A string representing the version specifier.
        python_version (str): The Python version to check.

    Returns:
        bool: True if the version matches the specifier, False otherwise.
    """
    try:
        return version.parse(python_version) in SpecifierSet(specifier)
    except Exception as e:
        print(f"Error checking Python version compatibility: {e}")
        raise


def search_package_versions(python_version: str, package_name: str) -> List[str]:
    """
    Searches for package versions compatible with the specified Python version.

    Args:
        python_version (str): The target Python version.
        package_name (str): The package name to search.

    Returns:
        List[str]: A list of compatible versions.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        versions = package_data.get("releases", {})
        compatible_versions = []
        for version_string, releases in versions.items():
            if releases:  # Only check if there are releases
                release = releases[-1]  # Use the latest release information
                requires_python = release.get("requires_python", "")
                if requires_python is None:
                    # Skip if requires_python field is None
                    # It's specified in recent libraries but may be missing in older ones
                    continue
                if is_python_version_compatible(requires_python, python_version):
                    compatible_versions.append(version_string)
        return compatible_versions
    else:
        print(f"Failed to retrieve package data for {package_name}.")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Searches for package versions compatible with a specified Python version."
    )
    parser.add_argument("python_version", help="Python version")
    parser.add_argument("package_name", help="Package name")
    parser.add_argument(
        "-a", "--all", action="store_true", help="Display all available versions"
    )

    args = parser.parse_args()

    python_version = args.python_version
    package_name = args.package_name

    compatible_versions = search_package_versions(python_version, package_name)

    if compatible_versions:
        if args.all:
            print(
                f"All available versions for {package_name} compatible with Python {python_version}:"
            )
            sorted_versions = sorted(
                compatible_versions, key=lambda x: version.parse(x)
            )
            for version in sorted_versions:
                print(version)
        else:
            max_version = max(compatible_versions, key=lambda x: version.parse(x))
            print(
                f"Maximum compatible version for {package_name} with Python {python_version}:"
            )
            print(max_version)
    else:
        print(
            f"No compatible versions found for {package_name} with Python {python_version}."
        )
