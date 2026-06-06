"""
Functions for getting various user folders, such as the sc2 install path.
"""
import glob
import logging
import os

import Utils
from .failable import Error
from .. import SC2World

logger = logging.getLogger("Starcraft2")

SC2_DIRNAME = "StarCraft II"
WINE_PREFIX_TO_SC2_INSTALL = "drive_c/Program Files (x86)/StarCraft II"
DOCUMENTS_SC2_DIRNAME = f"Documents/{SC2_DIRNAME}"
BANKS_DIRNAME = "Banks"
# Note(mm): The case here is important; filepaths are case-sensitive on Linux, but the game searches for a
# path case-insensitively, preferring "backup". So setting "Backup" here when "backup" already exists leads
# to communication failures.
BACKUP_DIRNAME = "backup"

WINE_ENV_VAR = "WINE"
WINE_PREFIX_ENV_VAR = "WINEPREFIX"
SC2_DOCS_ENV_VAR = "SC2_DOCUMENTS_DIR"
SC2_INSTALL_ENV_VAR = "SC2PATH"


def _get_wine_path() -> str:
    # @assume non-windows only
    # host.yaml override
    result: str | None = str(SC2World.settings.wine_path)
    if result:
        result = os.path.expanduser(result)
        if not os.path.isfile(result):
            logger.warning(f"Warning: host.yaml wine_path is not a file: {result}")
        else:
            return result

    # Environment variable override
    result = os.environ.get(WINE_ENV_VAR)
    if result is not None:
        result = os.path.expanduser(result)
        if not os.path.isfile(result):
            logger.warning(f"Warning: Value of env:{WINE_ENV_VAR} is not a file: {result}")
        else:
            return result

    # Default value
    result = "/usr/bin/wine"
    if os.path.isfile(result):
        return result
    logger.warning("Warning: could not find a wine installation to use")
    return ""


_wine_path: str | None = None
def get_wine_path() -> str | Error[str]:
    global _wine_path
    if _wine_path is None:
        _wine_path = _get_wine_path()
    if not _wine_path:
        return Error(
            "Error: Could not find a valid wine executable. "
            f"Set one in host.yaml under sc2_options.wine_path or with environment variable {WINE_ENV_VAR}."
        )
    return _wine_path


def _get_wine_prefix() -> str:
    # @assume non-windows only
    # host.yaml override
    result: str | None = str(SC2World.settings.wine_prefix)
    if result:
        result = os.path.expanduser(result)
        sc2_install_path = os.path.join(result, WINE_PREFIX_TO_SC2_INSTALL)
        if not os.path.isdir(result):
            logger.warning(f"Warning: host.yaml wine_prefix is not a folder: {result}")
        elif not os.path.isdir(sc2_install_path):
            logger.warning(f"Warning: host.yaml wine_prefix does not contain a sc2 install at {sc2_install_path}")
        else:
            return result

    # Environment variable override
    result = os.environ.get(WINE_PREFIX_ENV_VAR)
    if result is not None:
        result = os.path.expanduser(result)
        sc2_install_path = os.path.join(result, WINE_PREFIX_TO_SC2_INSTALL)
        if not os.path.isdir(result):
            logger.warning(f"Warning: Value of env:{WINE_PREFIX_ENV_VAR} is not a folder: {result}")
        elif not os.path.isdir(sc2_install_path):
            logger.warning(
                f"Warning: Value of env:{WINE_PREFIX_ENV_VAR} does not contain a sc2 install at {sc2_install_path}"
            )
        else:
            return result

    # Default value
    result = os.path.expanduser("~/.wine")
    sc2_install_path = os.path.join(result, WINE_PREFIX_TO_SC2_INSTALL)
    if not os.path.isdir(result):
        pass
    elif not os.path.isdir(sc2_install_path):
        logger.warning(f"Warning: wine prefix '{result}' does not contain a sc2 install at {sc2_install_path}")
    else:
        return result
    return ""


_wine_prefix: str | None = None
def get_wine_prefix() -> str | Error[str]:
    global _wine_prefix
    if _wine_prefix is None:
        _wine_prefix = _get_wine_prefix()
    if not _wine_prefix:
        return Error(
            "Error: Could not find a valid wine prefix. "
            "Set one in host.yaml under sc2_options.wine_prefix "
            f"or with environment variable {WINE_PREFIX_ENV_VAR}."
        )
    return _wine_prefix


def _get_sc2_docs_folder() -> str:
    # host.yaml override
    result: str | None = str(SC2World.settings.sc2_documents_path)
    if result:
        result = os.path.expanduser(result)
        if not os.path.isdir(result):
            logger.warning(f"Warning: host.yaml sc2_documents_path is not a folder: {result}")
        else:
            return result

    # Environment variable override
    result = os.environ.get(SC2_DOCS_ENV_VAR)
    if result is not None:
        result = os.path.expanduser(result)
        if not os.path.isdir(result):
            logger.warning(f"Warning: Value of env:{SC2_DOCS_ENV_VAR} is not a folder: {result}")
        else:
            return result

    # Windows handling
    if Utils.is_windows:
        # Get location of user's Documents/ folder even if it's been moved.
        # The next five lines of utterly inscrutable code are brought to you by copy-paste from Stack Overflow.
        # https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path/30924555#
        import ctypes.wintypes
        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        documents_path: str = buf.value
        result = os.path.join(documents_path, SC2_DIRNAME)
        if os.path.isdir(result):
            return result

        # Handle documents folder backed up by cloud service (OneDrive)
        sc2_docs_folders = glob.glob(os.path.expanduser(f"~/*/{DOCUMENTS_SC2_DIRNAME}"))
        if len(sc2_docs_folders) > 0:
            result = sc2_docs_folders[0]
        else:
            result = os.path.expanduser(f"~/{DOCUMENTS_SC2_DIRNAME}")
        if not os.path.isdir(result):
            logger.warning("StarCraft II documents folder not found")
            return ""
        return result

    # Linux handling
    wine_prefix = get_wine_prefix()
    if not isinstance(wine_prefix, Error):
        user_folder_name = os.path.basename(os.path.expanduser("~"))
        result = os.path.join(wine_prefix, f"drive_c/users/{user_folder_name}/{DOCUMENTS_SC2_DIRNAME}")
        if not os.path.isdir(result):
            logger.warning(f"Warning: sc2 documents dir within specified wine prefix is not a folder: {result}")
        else:
            return result
    result = os.path.expanduser(f"~/{DOCUMENTS_SC2_DIRNAME}")
    if os.path.isdir(result):
        return result
    return ""


_sc2_docs_folder: str | None = None
def get_sc2_docs_folder() -> str | Error[str]:
    global _sc2_docs_folder
    if _sc2_docs_folder is None:
        _sc2_docs_folder = _get_sc2_docs_folder()
    if not _sc2_docs_folder:
        return Error(
            f"Error: Could not find the {DOCUMENTS_SC2_DIRNAME} folder. "
            "Set one in host.yaml under sc2_options.sc2_documents_path "
            f"or with environment variable {SC2_DOCS_ENV_VAR}."
        )
    return _sc2_docs_folder


def _get_bank_folder() -> str | Error[str]:
    docs_folder = get_sc2_docs_folder()
    if isinstance(docs_folder, Error):
        return docs_folder
    result = os.path.join(docs_folder, BANKS_DIRNAME)
    if os.path.isfile(result):
        return Error(f"Encountered a file instead of a folder at Banks folder location: {result}")
    if not os.path.isdir(result):
        os.makedirs(result)
    return result


_sc2_bank_folder: str | Error[str] | None = None
def get_bank_folder() -> str | Error[str]:
    global _sc2_bank_folder
    if _sc2_bank_folder is None:
        _sc2_bank_folder = _get_bank_folder()
    return _sc2_bank_folder


def _get_sc2_install_dir() -> str:
    # Resolution order:
    # 1. host.yaml setting
    # 2. SC2PATH environment variable
    # 3. contents of Documents/StarCraft II/ExecuteInfo.txt
    # 4. Hardcoded path based on platform

    # host.yaml override
    result: str | None = str(SC2World.settings.sc2_install_path)
    if result:
        result = os.path.expanduser(result)
        if not os.path.isdir(result):
            logger.warning(f"Warning: host.yaml sc2_install_path is not a folder: {result}")
        else:
            return result

    # Environment variable override
    result = os.environ.get(SC2_INSTALL_ENV_VAR)
    if result is not None:
        result = os.path.expanduser(result)
        if not os.path.isdir(result):
            logger.warning(f"Warning: Value of env:{SC2_INSTALL_ENV_VAR} is not a folder: {result}")
        else:
            return result


    # Try reading from docs path/ExecuteInfo.txt
    def read_execute_info() -> str:
        docs_path = get_sc2_docs_folder()
        if isinstance(docs_path, Error):
            return ""
        execute_info_path = os.path.join(docs_path, "ExecuteInfo.txt")
        if not os.path.isfile(execute_info_path):
            return ""
        with open(execute_info_path, "rb") as fp:
            contents = fp.read()
        if b'executable = ' not in contents:
            return ""
        contents = contents.split(b'executable = ', 1)[1]
        if b'Versions' not in contents:
            return ""
        contents = contents.split(b'Versions', 1)[0]
        result = contents.decode("utf-8")
        if not Utils.is_windows:
            wine_prefix = get_wine_prefix()
            if isinstance(wine_prefix, Error):
                return ""
            result = result.replace("\\", "/")
            if len(result) > 2 and result[1:3] == ':/':
                result = os.path.join(wine_prefix, f"drive_{result[0].lower()}", result[3:])
        if os.path.isdir(result):
            return result
        else:
            # Note(mm): I would be surprised if this warning ever trips, but better safe than sorry
            logger.warning(
                f"Executable information in {execute_info_path} "
                f"doesn't point to a valid folder: {result}"
            )
            return ""


    result = read_execute_info()
    if result and os.path.isdir(result):
        return result

    # Windows default handling
    if Utils.is_windows:
        result = r"C:\Program Files (x86)\StarCraft II"
        if os.path.isdir(result):
            return result
        logger.warning(f"Could not find sc2 install path at {result}")
        return ""

    # Linux handling
    wine_prefix = get_wine_prefix()
    if not isinstance(wine_prefix, Error):
        result = os.path.join(wine_prefix, f"drive_c/Program Files (x86)/StarCraft II")
        if not os.path.isdir(result):
            logger.warning(f"Warning: sc2 is not installed within wine prefix: {result}")
        else:
            return result
    result = os.path.expanduser(f"~/Games/StarCraft II")
    if os.path.isdir(result):
        return result
    return ""


_sc2_install_dir: str | None = None
def get_sc2_install_dir() -> str | Error[str]:
    global _sc2_install_dir
    if _sc2_install_dir is None:
        _sc2_install_dir = _get_sc2_install_dir()
    if not _sc2_install_dir:
        return Error(
            f"Error: Could not find the Starcraft 2 install folder. "
            "Ensure sc2 is installed, and has been launched through the Blizzard launcher. "
            "If issues persist, set the path in host.yaml under sc2_options.sc2_install_path "
            f"or with environment variable {SC2_INSTALL_ENV_VAR}."
        )
    return _sc2_install_dir


def _get_sc2_exe_path() -> str | Error[str]:
    sc2_install_dir = get_sc2_install_dir()
    if isinstance(sc2_install_dir, Error):
        return sc2_install_dir
    candidates = glob.glob(os.path.join(sc2_install_dir, 'Versions', 'Base*', 'SC2_x64.exe'))
    if not candidates:
        return Error(f"No SC2_x64.exe present in any subdirectory of {sc2_install_dir}/Versions")
    sorted_candidates = sorted(candidates)
    return sorted_candidates[-1]


_sc2_exe_path: str | Error[str] | None = None
def get_sc2_exe_path() -> str | Error[str]:
    global _sc2_exe_path
    if _sc2_exe_path is None:
        _sc2_exe_path = _get_sc2_exe_path()
    return _sc2_exe_path


def reset_cache() -> None:
    global _wine_path
    global _wine_prefix
    global _sc2_install_dir
    global _sc2_docs_folder
    global _sc2_bank_folder
    global _sc2_exe_path
    _wine_path = None
    _wine_prefix = None
    _sc2_install_dir = None
    _sc2_docs_folder = None
    _sc2_bank_folder = None
    _sc2_exe_path = None
