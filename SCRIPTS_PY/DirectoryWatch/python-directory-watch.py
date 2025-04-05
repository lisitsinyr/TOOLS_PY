"""Watch.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     Watch.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil
import filecmp
import psutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import random
import string
import tkinter as tk
import pyperclip

import random
from tkinter import *
from tkinter import messagebox
import pyperclip

import os
import shutil
from datetime import datetime

from pathlib import Path
from contextlib import contextmanager
from typing import Generator
from os import PathLike
from traceback import print_exc
import time
import os
from dataclasses import dataclass

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUos as LUos
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

#------------------------------------------
# process () -> None:
#------------------------------------------
def process () -> None:
    """process"""
#beginfunction
    pass
#endfunction

#------------------------------------------
# 
#------------------------------------------
@dataclass
class FileInfo:
    path: Path
    inode: tuple[int, int]

    @classmethod
    def from_path(cls, path: os.PathLike):
        st = os.stat(path)
        return cls(Path(path), (st.st_ino, st.st_dev))

    def __hash__(self):
        return hash(self.inode)

    def __eq__(self, __value: object) -> bool:
        if self.inode == __value.inode:
            return True
        else:
            return self == __value

#------------------------------------------
# 
#------------------------------------------
@contextmanager
def mangage_history(history_file: Path) -> Generator[set[str], None, None]:
    """Context manager which reads and writes to file with newline delimited strings.
    Yeilds a set of the strings contained in the file or an empty set,
    any items added to the set will be written to the file when the context manager exits.
    Creates a file if the history_file argument is not an existing filepath.

    Parameters
    ----------
    history_file : Path
        Path to history file location

    Yields
    ------
    Generator[set[str], None, None]
        A set containing items from newline delimited file.
    """
    history_file.touch()

    try:
        with open(history_file, mode="r") as f:
            initial = set([x.strip() for x in f.readlines()])
            yield initial

    finally:
        with open(history_file, mode="w") as f:
            for file in initial:
                f.write(f"{file}\n")

#------------------------------------------
# 
#------------------------------------------
def listen(
    path: Path,
    *,
    history_paths: set[PathLike] = set(),
    pattern: str = "*",
    resolve_paths: bool = True,
    polling_rate=10,
) -> Generator[Path, None, None]:
    """Generator which polls for new files in a directory and yeilds when new files are found. Will block unless new file is found.

    Parameters
    ----------
    path : Path
        The directory which should be watched for new files.
    history_paths : set[PathLike], optional
        set of path objects which should be ignored (usually because they were already processed), by default empty set()
    pattern : str, optional
        Unix glob patterns to filter new paths found. Conforms to patterns allowed in pathlib.Path.glob. , by default "*"
    resolve_paths : bool, optional
        All paths found will be resolved to absolute using pathlib.Path.resolve, by default True

    Yields
    ------
    Generator[Path, None, None]
        Will yield paths to new files found in the directory. Blocks until new file is found.

    Raises
    ------
    ValueError
        Check that path parameter is valid directory & pathlib.Path object
    ValueError
        Check that history_paths is valid python set
    ValueError
        Check that pattern is a string.

    """
    if not isinstance(pattern, str):
        raise ValueError("Input pattern must be a str object. ")

    if not isinstance(path, Path):
        raise ValueError("Input path must be a pathlib.Path object")

    if not isinstance(history_paths, set):
        raise ValueError(
            f"history_paths object must be a python set. Object provided is of type {type(history_paths)}"
        )

    if not path.is_dir():
        raise ValueError(f"Input path must be a directory '{path}' is not a directory.")

    history_paths_converted = set()
    for hist_path in history_paths:
        history_paths_converted.add(Path(hist_path))

    yield from _listen(
        path,
        history_paths=history_paths_converted,
        pattern=pattern,
        resolve_paths=resolve_paths,
        polling_rate=polling_rate,
    )


#------------------------------------------
# 
#------------------------------------------
def _listen(
    path: Path,
    *,
    history_paths: set[PathLike] = set(),
    pattern: str = "*",
    resolve_paths=True,
    polling_rate=10,
) -> Generator[Path, None, None]:
    history_info = set([FileInfo.from_path(p) for p in history_paths])

    while True:
        time.sleep(1 / polling_rate)
        if resolve_paths:
            items = set([FileInfo.from_path((p.resolve())) for p in path.glob(pattern)])
        else:
            items = set([FileInfo.from_path(p) for p in path.glob(pattern)])

        new_items = items.difference(history_info)

        if new_items:
            for item in new_items:
                yield item.path

                history_info.add(item)

#------------------------------------------
# 
#------------------------------------------
def listen_with_history(
    path,
    *,
    pattern="*",
    resolve_paths=True,
    history_filepath=Path("~pydirwatch_history.tmp"),
    errors="raise",
    polling_rate=10,
):
    """Generator which polls for new files in a directory and yeilds when new files are found. Will block unless new file is found.
    When generator exits it will save history of files read to disk. Restarting the generator with the same history file will
    skip any files found in the directory which match those found in the history file.

    Parameters
    ----------
    path : Path
        The directory which should be watched for new files.
    history_paths : set[PathLike], optional
        set of path objects which should be ignored (usually because they were already processed), by default empty set()
    pattern : str, optional
        Unix glob patterns to filter new paths found. Conforms to patterns allowed in pathlib.Path.glob. , by default "*"
    resolve_paths : bool, optional
        All paths found will be resolved to absolute using pathlib.Path.resolve, by default True
    history_filepath : pathlib.Path, optional
        filepath for the history file to store persistent history of files read on disk. File will be created if it does not exist.
        , by default Path("~pydirwatch_history.tmp")

    Yields
    ------
    Generator[Path, None, None]
        Will yield paths to new files found in the directory. Blocks until new file is found.

    """
    with mangage_history(history_filepath) as h:
        for path in listen(
            path=path,
            history_paths=h,
            resolve_paths=resolve_paths,
            pattern=pattern,
            polling_rate=polling_rate,
        ):
            try:
                yield path
                h.add(path)

            except:
                if errors == "suppress":
                    pass
                elif errors == "warn":
                    print_exc()
                else:
                    raise

#------------------------------------------
def main ():
    """main"""
#beginfunction
    pass
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
# endif

# endmodule
