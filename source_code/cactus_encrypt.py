#cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
#Copyright 2023,2024 Redcactus5
'''
This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 
'''
#this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)



#this file is basically just a launcher for the main program




import command_line_interface

#set to true for release builds
RELEASEBUILD=False


if(RELEASEBUILD):
    try:
        command_line_interface.start(False)
    except Exception as e:
        print("\n")*50
        print("a serious error occurred. the program has quit to prevent further problems")
        print("detected error: "+str(e))
        input("press enter to finish")
else:
    command_line_interface.start(True)

