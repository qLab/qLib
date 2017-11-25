#!/bin/bash
#
#		@file		install.sh
#		@author		Imre Tuske
#		@since		2014-11-14
#
#		@brief		Simple install script for the menu items (linux-only).
#
#		Requires the "houdini_setup_bash" or equivalent to be sourced first
#		(so variables like $HIH would be available).
#
#


echo Installing/updating menu scripts...
echo -- location: $HIH

rm -fv $HIH/MainMenuMaster.xml
rm -fv $HIH/PARMmenu.xml
rm -fv $HIH/MVexport

# NOTE: this might need to be edited
SRC=./qLib/menu

ln -sfv $SRC/MainMenuMaster.xml $HIH/MainMenuMaster.xml
ln -sfv $SRC/PARMmenu.xml $HIH/PARMmenu.xml
ln -sfv $SRC/MVexport $HIH/MVexport


echo ...done.

