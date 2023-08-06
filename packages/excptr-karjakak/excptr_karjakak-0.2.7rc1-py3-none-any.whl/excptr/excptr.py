# -*- coding: utf-8 -*-
# Copyright (c) 2022, KarjaKAK
# All rights reserved.

from functools import wraps
from textwrap import fill
from contextlib import redirect_stdout
from datetime import datetime as dt
import io, inspect, os, sys


__all__ = ['']


DIRPATH = (
    os.environ["USERPROFILE"] if sys.platform.startswith("win") else os.environ["HOME"]
)
DEFAULTDIR = os.path.join(DIRPATH, "EXCPTR")
DEFAULTFILE = os.path.join(
    DEFAULTDIR, f"{int(dt.timestamp(dt.today().replace(microsecond=0)))}_EXCPTR.log"
)


def defd():
    """Create default directory"""

    if not os.path.isdir(DEFAULTDIR):
        os.mkdir(DEFAULTDIR)
    else:
        raise Exception(f"{DEFAULTDIR} is already exist!")


def prex(details, exc_tr, fc_name):
    """Printing Exception"""

    print(f"\nFilename caller: {details[0].filename.upper()}\n")
    print(f"ERROR - <{fc_name}>:")
    print(f"{'-' * 70}", end="\n")
    print("Start at:\n")

    filenm = details[0].filename
    for detail in details:
        if "excptr.py" not in detail.filename:
            if filenm != detail.filename:
                print(f"Filename: {detail.filename.upper()}\n")
            cc = fill(
                "".join(detail.code_context).strip(),
                initial_indent=" " * 4,
                subsequent_indent=" " * 4,
            )
            print(f"line {detail.lineno} in {detail.function}:\n" f"{cc}\n")
            err = None
            for li in cc.splitlines():
                if fc_name in li:
                    err = li
                    break
            del cc
            if err:
                print(f"Detecting ERROR:\n{err}")
                print(f"{err.index(fc_name)*' '}{len(fc_name)*'^'}")
            del err
        del detail

    tot = f">>>- Exception raise: {exc_tr.__class__.__name__} ->"
    print("~" * len(tot))
    print(tot)
    print("~" * len(tot) + "\n")

    allextr = inspect.getinnerframes(exc_tr.__traceback__)[1:]
    for extr in allextr:
        if "excptr.py" not in extr.filename:
            if filenm != extr.filename:
                print(f"Filename: {extr.filename.upper()}\n")
            cc = fill(
                "".join(extr.code_context).strip(),
                initial_indent=" " * 4,
                subsequent_indent=" " * 4,
            )
            print(f"line {extr.lineno} in {extr.function}:\n" f"{cc}\n")
            del cc
        del extr
    print(f"{exc_tr.__class__.__name__}: {exc_tr.args[0]}")
    print(f"{'-' * 70}", end="\n")
    del tot, allextr, filenm, details, exc_tr, fc_name


def crtk(v: str):
    """Tkinter gui display"""

    import tkinter as tk
    from tkinter import messagebox as msg

    root = tk.Tk()
    root.title("Exception Error Messages")
    root.attributes("-topmost", 1)
    text = tk.Listbox(root, relief=tk.FLAT, width=70, selectbackground="light green")
    text.pack(side="left", expand=1, fill=tk.BOTH, pady=2, padx=(2, 0))
    scr = tk.Scrollbar(root, orient=tk.VERTICAL)
    scr.pack(side="right", fill=tk.BOTH)
    scr.config(command=text.yview)
    text.config(yscrollcommand=scr.set)
    val = v.splitlines()
    for v in val:
        text.insert(tk.END, v)
    text.config(
        state=tk.DISABLED,
        bg="grey97",
        disabledforeground="black",
        font="courier 12",
        height=len(val),
    )
    del val, v
    scnd = 5000

    def viewing():
        nonlocal scnd
        scnd += scnd if scnd < 20000 else 5000
        match scnd:
            case sec if sec <= 25000:
                ans = msg.askyesno(
                    "Viewing",
                    f"Still viewing for another {scnd//1000} seconds?",
                    parent=root,
                )
                if ans:
                    root.after(scnd, viewing)
                else:
                    root.destroy()
            case sec if sec > 25000:
                msg.showinfo(
                    "Viewing", "Viewing cannot exceed more than 1 minute!", parent=root
                )
                root.destroy()

    root.after(5000, viewing)
    root.mainloop()
    del root, text, scr, scnd


def ckrflex(filenm: str) -> bool:
    """Checking file existence or an empty file"""

    if os.path.exists(filenm):
        with open(filenm) as rd:
            if rd.readline():
                return False
            else:
                return True
    else:
        return True


def excp(m: int = -1, filenm: str = None):
    """Decorator for function"""

    match m:
        case m if not isinstance(m, int):
            raise ValueError(f'm = "{m}" Need to be int instead!')
        case m if m not in [-1, 0, 1, 2]:
            raise ValueError(
                f'm = "{m}" Need to be either one of them, [-1 or 0 or 1 or 2]!'
            )

    def ckerr(f):
        ckb = m

        @wraps(f)
        def trac(*args, **kwargs):
            try:
                if fn := f(*args, **kwargs):
                    return fn
                del fn
            except Exception as e:
                details = inspect.stack()[1:][::-1]
                match ckb:
                    case -1:
                        raise
                    case 0:
                        prex(details, e, f.__name__)
                    case 1:
                        v = io.StringIO()
                        with redirect_stdout(v):
                            prex(details, e, f.__name__)
                        crtk(v.getvalue())
                        v.flush()
                    case 2:
                        if filenm:
                            v = io.StringIO()
                            with redirect_stdout(v):
                                prex(details, e, f.__name__)
                            wrm = (
                                str(dt.today()).rpartition(".")[0]
                                + ": TRACING EXCEPTION\n"
                                if ckrflex(filenm)
                                else "\n"
                                + str(dt.today()).rpartition(".")[0]
                                + ": TRACING EXCEPTION\n"
                            )
                            with open(filenm, "a") as log:
                                log.write(wrm)
                                log.write(v.getvalue())
                            v.flush()
                            del v, wrm
                        else:
                            raise

                del details, e

        return trac

    return ckerr


def excpcls(m: int = -1, filenm: str = None):
    """Decorator for class (for functions only)"""

    match m:
        case m if not isinstance(m, int):
            raise ValueError(f'm = "{m}" Need to be int instead!')
        case m if m not in [-1, 0, 1, 2]:
            raise ValueError(
                f'm = "{m}" Need to be either one of them, [-1 or 0 or 1 or 2]!'
            )

    def catchcall(cls):
        ckb = m
        match cls:
            case cls if not inspect.isclass(cls):
                raise TypeError("Type error, suppose to be a class!")
            case _:
                for name, obj in vars(cls).items():
                    if inspect.isfunction(obj):
                        setattr(cls, name, excp(ckb, filenm)(obj))

        return cls

    return catchcall
