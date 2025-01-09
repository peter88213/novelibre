#!/usr/bin/python3
"""A novel organizer for writers. 

Version @release
Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.
"""
import os
from pathlib import Path
import sys

from nvlib.configuration.configuration import Configuration
from nvlib.configuration.nv_configuration import NvConfiguration
from nvlib.controller.main_controller import MainController
from nvlib.nv_globals import launchers
from nvlib.nv_globals import prefs

SETTINGS = dict(
    arcs_width=55,
    backup_dir='',
    color_1st_edit='DarkGoldenrod4',
    color_2nd_edit='DarkGoldenrod3',
    color_arc='maroon',
    color_before_schedule='lime green',
    color_behind_schedule='magenta',
    color_chapter='green',
    color_comment_tag='lemon chiffon',
    color_done='DarkGoldenrod2',
    color_draft='black',
    color_locked_bg='dim gray',
    color_locked_fg='light gray',
    color_major='navy',
    color_minor='cornflower blue',
    color_modified_bg='goldenrod1',
    color_modified_fg='maroon',
    color_notes_bg='lemon chiffon',
    color_notes_fg='black',
    color_note_tag='bisque',
    color_on_schedule='black',
    color_outline='dark orchid',
    color_stage='red',
    color_status_error_bg='red',
    color_status_error_fg='white',
    color_status_notification_bg='yellow',
    color_status_notification_fg='black',
    color_status_success_bg='green',
    color_status_success_fg='white',
    color_text_bg='white',
    color_text_fg='black',
    color_unused='gray',
    color_xml_tag='cornflower blue',
    coloring_mode='',
    column_order='wc;vp;sy;st;nt;dt;tm;dr;tg;po;ac;pt;ar',
    date_width=70,
    duration_width=55,
    gco_height=4,
    gui_theme='',
    import_mode='0',
    index_card_height=13,
    last_open='',
    middle_frame_width=400,
    nt_width=20,
    points_width=300,
    prop_win_geometry='299x716+260+260',
    ps_width=50,
    right_frame_width=350,
    root_geometry='1200x800',
    scene_width=40,
    status_width=100,
    tags_width=100,
    time_width=40,
    title_width=400,
    vp_width=100,
    wc_width=50,
)
OPTIONS = dict(
    ask_doc_open=True,
    detach_prop_win=False,
    enable_hovertips=True,
    large_icons=False,
    localize_date=True,
    lock_on_export=False,
    show_auto_numbering=False,
    show_ch_links=False,
    show_contents=True,
    show_cr_bio=True,
    show_cr_goals=True,
    show_cr_links=False,
    show_date_time=False,
    show_it_links=False,
    show_language_settings=False,
    show_lc_links=False,
    show_markup=False,
    show_narrative_time=False,
    show_pl_links=False,
    show_plot=False,
    show_pn_links=False,
    show_pp_links=False,
    show_pr_links=False,
    show_properties=True,
    show_relationships=False,
    show_renamings=False,
    show_sc_links=False,
    show_scene=False,
    show_st_links=False,
    show_writing_progress=False,
)


def set_backup_directory(defaultDir):
    backupDir = prefs['backup_dir']
    if not os.path.isdir(backupDir):
        backupDir = defaultDir
        try:
            os.makedirs(backupDir, exist_ok=True)
        except:
            backupDir = ''
        prefs['backup_dir'] = backupDir


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
    try:
        configuration.read(iniFile)
    except:
        pass
        # skipping the configuraton if faulty
    prefs.update(configuration.settings)
    prefs.update(configuration.options)

    #--- Launchers for opening linked non-standard filetypes.
    launcherConfig = NvConfiguration()
    launcherConfig.read(f'{configDir}/launchers.ini')
    launchers.update(launcherConfig.settings)

    #--- Central backup directory.
    set_backup_directory(f'{installDir}/backup')

    #--- Instantiate the app object.
    app = MainController('novelibre @release', tempDir)
    ui = app.get_view()

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

    #--- Save launchers.
    launcherConfig.settings = launchers
    launcherConfig.write(f'{configDir}/launchers.ini')

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
