#!/usr/bin/python3
"""A novel organizer for writers. 

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
from pathlib import Path
import sys

from nvlib.configuration.nv_configuration import NvConfiguration
from nvlib.controller.nv_controller import NvController
from nvlib.nv_globals import prefs
from novxlib.config.configuration import Configuration

SETTINGS = dict(
    last_open='',
    root_geometry='1200x800',
    gui_theme='',
    button_context_menu='<Button-3>',
    middle_frame_width=400,
    right_frame_width=350,
    index_card_height=13,
    gco_height=4,
    prop_win_geometry='299x716+260+260',
    color_chapter='green',
    color_arc='maroon',
    color_stage='red',
    color_unused='gray',
    color_major='navy',
    color_minor='cornflower blue',
    color_outline='dark orchid',
    color_draft='black',
    color_1st_edit='DarkGoldenrod4',
    color_2nd_edit='DarkGoldenrod3',
    color_done='DarkGoldenrod2',
    color_behind_schedule='magenta',
    color_before_schedule='lime green',
    color_on_schedule='black',
    color_locked_bg='dim gray',
    color_locked_fg='light gray',
    color_modified_bg='goldenrod1',
    color_modified_fg='maroon',
    color_text_bg='white',
    color_text_fg='black',
    color_notes_bg='lemon chiffon',
    color_notes_fg='black',
    coloring_mode='',
    title_width=400,
    ps_width=50,
    wc_width=50,
    status_width=100,
    nt_width=20,
    vp_width=100,
    tags_width=100,
    scene_width=40,
    date_width=70,
    time_width=40,
    duration_width=55,
    arcs_width=55,
    points_width=300,
    column_order='wc;vp;sy;st;nt;dt;tm;dr;tg;po;ac;pt;ar',
    import_mode='0',
    )
OPTIONS = dict(
    show_contents=True,
    show_properties=True,
    show_markup=False,
    show_language_settings=False,
    show_auto_numbering=False,
    show_renamings=False,
    show_writing_progress=False,
    show_narrative_time=False,
    show_sc_arcs=False,
    show_date_time=False,
    show_action_reaction=False,
    show_relationships=False,
    show_cr_links=False,
    show_lc_links=False,
    show_it_links=False,
    show_pr_links=False,
    show_ch_links=False,
    show_sc_links=False,
    show_st_links=False,
    show_pl_links=False,
    show_pp_links=False,
    show_pn_links=False,
    show_cr_bio=True,
    show_cr_goals=True,
    detach_prop_win=False,
    large_icons=False,
    lock_on_export=False,
    ask_doc_open=True,
    )


def main():
    #--- Set up the directories for configuration and temporary files.
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.novx'
    except:
        installDir = '.'
    os.makedirs(installDir, exist_ok=True)
    configDir = f'{installDir}/config'
    os.makedirs(configDir, exist_ok=True)
    tempDir = f'{installDir}/temp'
    os.makedirs(tempDir, exist_ok=True)

    #--- Load configuration.
    iniFile = f'{configDir}/novx.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    prefs.update(configuration.settings)
    prefs.update(configuration.options)

    #--- Instantiate the app object.
    app = NvController('novelibre @release', tempDir)
    ui = app.get_view()

    #--- Launchers for opening linked non-standard filetypes.
    launcherConfig = NvConfiguration()
    launcherConfig.read(f'{configDir}/launchers.ini')
    app.launchers = launcherConfig.settings

    #--- Load a project, if specified.
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = prefs['last_open']
    if sourcePath and os.path.isfile(sourcePath):
        app.open_project(filePath=sourcePath)

    #--- Run the GUI application.
    ui.start()

    #--- Save project specific configuration
    for keyword in prefs:
        if keyword in configuration.options:
            configuration.options[keyword] = prefs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = prefs[keyword]
    configuration.write(iniFile)

    #--- Delete the temporary files.
    # Note: Do not remove the temp directory itself,
    # because other novelibre instances might be running and using it.
    # However, temporary files of other running instances are deleted
    # if not protected e.g. by a read-only flag.
    for file in os.scandir(tempDir):
        try:
            os.remove(file)
        except:
            pass


if __name__ == '__main__':
    main()
