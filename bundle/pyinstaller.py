#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import platform

from PyInstaller.__main__ import run as run_pyinstaller

OS_NAME, MACHINE, ARCH = (
    sys.platform,
    platform.machine().lower(),
    platform.architecture()[0][:2],
)
if MACHINE in ("x86", "x86_64", "amd64", "i386", "i686"):
    MACHINE = "x86" if ARCH == "32" else ""


def main():
    opts = sys.argv[1:]
    version = "1.0.0"  # デフォルトのバージョン。必要に応じて変更
    script_name = "src/nicodlp/__main__.py" # ビルド対象のスクリプト名。適宜変更

    onedir = "--onedir" in opts or "-D" in opts
    if not onedir and "-F" not in opts and "--onefile" not in opts:
        opts.append("--onefile")

    name, final_file = exe(onedir)
    print(
        f"Building {script_name} v{version} for {OS_NAME} {platform.machine()} with options {opts}"
    )
    print(f"Destination: {final_file}\n")

    opts = [
        f"--name={name}",
        "--upx-exclude=vcruntime140.dll",
        # "--icon=your_icon.ico",  # 必要に応じてアイコンを追加
        "--noconfirm",
        # "--additional-hooks-dir=.", # 必要に応じてフックディレクトリを指定
        *opts,
        script_name, # ビルド対象のスクリプト
    ]

    print(f"Running PyInstaller with {opts}")
    run_pyinstaller(opts)
    set_version_info(final_file, version)


def parse_options():
    # 以前の引数との互換性のためのコードは不要
    return sys.argv[1:]


def exe(onedir):
    """@returns (name, path)"""
    name = "nico_dlp" # アプリケーション名。適宜変更
    return name, "".join(
        filter(
            None,
            (
                "dist/",
                onedir and f"{name}/",
                name,
                OS_NAME == "win32" and ".exe",
            ),
        )
    )


def version_to_list(version):
    version_list = version.split(".")
    return list(map(int, version_list)) + [0] * (4 - len(version_list))


def set_version_info(exe, version):
    if OS_NAME == "win32":
        windows_set_version(exe, version)


def windows_set_version(exe, version):
    # Windowsバージョン情報の記述。必要に応じて修正
    from PyInstaller.utils.win32.versioninfo import (
        FixedFileInfo,
        StringFileInfo,
        StringStruct,
        StringTable,
        VarFileInfo,
        VarStruct,
        VSVersionInfo,
    )

    try:
        from PyInstaller.utils.win32.versioninfo import SetVersion
    except ImportError:  # Pyinstaller >= 5.8
        from PyInstaller.utils.win32.versioninfo import (
            write_version_info_to_executable as SetVersion,
        )


if __name__ == "__main__":
    main()
