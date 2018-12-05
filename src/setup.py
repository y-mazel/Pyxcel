# -*- coding: utf8 -*-
"""
Created on 20 nov. 2014

@author: GP243515
"""
import sys
from cx_Freeze import setup, Executable

# INCLUDEFILES = ["C:\\Windows\\System32\\libxrl-7.dll", "libxrl-7.dll", "../i18n/en.qm", "../i18n/en.ts", "../i18n/fr.qm", "../i18n/fr.ts"]
INCLUDEFILES = [(r"C:/Windows/System32/libxrl-7.dll"                    ,"libxrl-7.dll"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/i18n/en.qm"   ,"./i18n/en.qm"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/i18n/en.ts"   ,"./i18n/en.ts"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/i18n/fr.qm"   ,"./i18n/fr.qm"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/i18n/fr.ts"   ,"./i18n/fr.ts"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/pyxcel.ico"   ,"./ui/pyxcel.ico"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/create_instrument.ui"   ,"./ui/create_instrument.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/add_data.ui"   ,"./ui/add_data.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/analysis_window.ui"   ,"./ui/analysis_window.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/data_treatment.ui"   ,"./ui/data_treatment.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/full_analysis_windows.ui"   ,"./ui/full_analysis_windows.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/modeling_window.ui"   ,"./ui/modeling_window.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/op_graph.ui"   ,"./ui/op_graph.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/op_io.ui"   ,"./ui/op_io.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/op_parameter_lite.ui"   ,"./ui/op_parameter_lite.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/op_parameter.ui"   ,"./ui/op_parameter.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/param_evol.ui"   ,"./ui/param_evol.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/profile_func.ui"   ,"./ui/profile_func.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/profile.ui"   ,"./ui/profile.ui"),
                (r"C:/Python27/Pyxcel_instalation_pack/Medepy_V2/ui/xrf_tool_box.ui"   ,"./ui/xrf_tool_box.ui")                              
                ]

# unnecessary libraries exlusion
# might alternatively be done by removing unneeded libs post compilation via a script
EXCLUDES = []

# Dependencies are automatically detected, but it might need fine tuning.
BUILD_EXE_OPTIONS = {
                    "packages": ["os", "pyxcel", "paf", 
                                 "scipy",
                                 'xraylib', "numpy", "quantities"],
                     "includes": ["scipy.special._ufuncs_cxx",
                                  "scipy.special._ufuncs_cxx", "scipy.linalg",
                                  "matplotlib.backends.backend_tkagg", 'six',
                                  'FileDialog'],
                     "excludes": EXCLUDES,
                     "include_files": INCLUDEFILES,
                     "optimize": 2}

# GUI applications require a different base on Windows (the default is for a
# console application).
BASE = None
if sys.platform == "win32":
    BASE = "Win32GUI"

setup(
    name="Medepy", 
    version="0.7", 
    description="Medepy",
    options={"build_exe": BUILD_EXE_OPTIONS},
    executables=[Executable("main.py", base=BASE, targetName = "PyXCEL.exe", icon = "pyxcel.ico")]
    )
