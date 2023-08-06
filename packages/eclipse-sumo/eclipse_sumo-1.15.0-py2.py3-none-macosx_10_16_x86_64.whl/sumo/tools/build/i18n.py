#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2011-2022 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    i18n.py
# @author  Michael Behrisch
# @date    2022-10-08

"""
Prepare gettext pot and po files for all languages.
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import subprocess
import difflib
from glob import glob
from argparse import ArgumentParser


SUMO_HOME = os.environ.get("SUMO_HOME", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SUMO_LIBRARIES = os.environ.get("SUMO_LIBRARIES", os.path.join(os.path.dirname(SUMO_HOME), "SUMOLibraries"))


def get_args(args=None):
    existing_langs = [os.path.basename(p)[:2] for p in glob(SUMO_HOME + "/data/po/*_sumo.po")]
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-l", "--lang", nargs='*', default=existing_langs,
                            help="languages to process")
    return arg_parser.parse_args(args)


def main(args=None):
    path = ""
    if os.name == "nt":
        paths = glob(os.path.join(SUMO_LIBRARIES, "gettext-*", "tools", "gettext", "bin"))
        if paths:
            path = paths[0] + os.path.sep
    options = get_args(args)
    pot_file = SUMO_HOME + "/data/po/sumo.pot"
    gui_pot_file = SUMO_HOME + "/data/po/gui.pot"
    pots = {pot_file: open(pot_file + ".txt", "w"), gui_pot_file: open(gui_pot_file + ".txt", "w")}
    for f in glob(SUMO_HOME + "/src/*.cpp") + glob(SUMO_HOME + "/src/*/*.cpp") + glob(SUMO_HOME + "/src/*/*/*.cpp"):
        if "gui" in f[len(SUMO_HOME):] or "netedit" in f[len(SUMO_HOME):]:
            print(f, file=pots[gui_pot_file])
        else:
            print(f, file=pots[pot_file])
    for pot, sources in pots.items():
        sources.close()
        subprocess.check_call([path + "xgettext", "--files-from=" + sources.name, "--from-code=UTF-8",
                              "--keyword=TL", "--keyword=TLF", "--output=" + pot + ".new", "--package-name=sumo",
                               "--msgid-bugs-address=sumo-dev@eclipse.org"])
        os.remove(sources.name)
        has_diff = True
        if os.path.exists(pot):
            with open(pot) as old, open(pot + ".new") as new:
                a = [s for s in old.readlines() if not s.startswith(("#", '"POT-Creation-Date:'))]
                b = [s for s in new.readlines() if not s.startswith(("#", '"POT-Creation-Date:'))]
                has_diff = list(difflib.unified_diff(a, b))
            if has_diff:
                os.remove(pot)
        if has_diff:
            os.rename(pot + ".new", pot)
        else:
            os.remove(pot + ".new")
        for lang in options.lang:
            po_file = "%s/data/po/%s_%s" % (SUMO_HOME, lang, os.path.basename(pot)[:-1])
            if os.path.exists(po_file):
                subprocess.check_call([path + "msgmerge", po_file, pot, "--output-file=" + po_file])
            else:
                subprocess.check_call([path + "msginit", "--input=" + pot, "--output=" + po_file,
                                       "--no-translator", "--locale=" + lang])
    for lang in options.lang:
        po_files = ["%s/data/po/%s_%s" % (SUMO_HOME, lang, os.path.basename(pot)[:-1]) for pot in pots]
        merged_po_file = "%s/data/po/%s.po" % (SUMO_HOME, lang)
        subprocess.check_call([path + "msgcat"] + po_files + ["--output-file=" + merged_po_file])
        d = "%s/data/locale/%s/LC_MESSAGES" % (SUMO_HOME, lang)
        os.makedirs(d, exist_ok=True)
        subprocess.check_call([path + "msgfmt", merged_po_file, "--output-file=%s/sumo.mo" % d])
        os.remove(merged_po_file)


if __name__ == "__main__":
    main()
