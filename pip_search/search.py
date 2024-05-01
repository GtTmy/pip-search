import requests
import argparse
from typing import List
from packaging import version

from packaging.specifiers import SpecifierSet


def is_python_version_compatible(specifier: str, python_version: str) -> bool:
    """
    指定された Python バージョンが、指定されたバージョン条件に合致するかどうかを判断します。

    Args:
        specifier (str): バージョン条件を示す文字列。
        python_version (str): チェックする Python バージョン。

    Returns:
        bool: バージョンが条件に合致する場合は True、そうでない場合は False。
    """
    try:
        return version.parse(python_version) in SpecifierSet(specifier)
    except Exception as e:
        print(f"Error checking Python version compatibility: {e}")
        raise


def search_package_versions(python_version: str, package_name: str) -> List[str]:
    """
    指定された Python バージョンに対応するパッケージのバージョンを検索します。

    Args:
        python_version (str): 対象の Python バージョン。
        package_name (str): 検索するパッケージ名。

    Returns:
        List[str]: 対応するバージョンのリスト。
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        versions = package_data.get("releases", {})
        compatible_versions = []
        for version_string, releases in versions.items():
            if releases:  # リリースが存在する場合のみチェック
                release = releases[-1]  # 最新のリリース情報を使用
                requires_python = release.get("requires_python", "")
                if requires_python is None:
                    # requires_python fieldがNoneの場合は判定できないのでスキップ
                    # 最近のライブラリでは指定されているが、古いライブラリでは指定されていないことがある
                    continue
                if is_python_version_compatible(requires_python, python_version):
                    compatible_versions.append(version_string)
        return compatible_versions
    else:
        print(f"{package_name} のパッケージデータの取得に失敗しました。")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="指定された Python バージョンに対応するパッケージのバージョンを検索します。"
    )
    parser.add_argument("python_version", help="Python バージョン")
    parser.add_argument("package_name", help="パッケージ名")
    parser.add_argument(
        "-a", "--all", action="store_true", help="利用可能な全バージョンを表示"
    )

    args = parser.parse_args()

    python_version = args.python_version
    package_name = args.package_name

    compatible_versions = search_package_versions(python_version, package_name)

    if compatible_versions:
        if args.all:
            print(f"{package_name} の {python_version} 用の全利用可能バージョン:")
            sorted_versions = sorted(
                compatible_versions, key=lambda x: version.parse(x)
            )
            for version in sorted_versions:
                print(version)
        else:
            max_version = max(compatible_versions, key=lambda x: version.parse(x))
            print(f"{package_name} の {python_version} 用の最大互換バージョン:")
            print(max_version)
    else:
        print(
            f"{package_name} の {python_version} 用の互換バージョンは見つかりませんでした。"
        )
