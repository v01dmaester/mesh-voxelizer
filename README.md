# mesh-voxelizer
Maya 2014-15 plugin. Works on any closed mesh to 'voxelize' it based on given resolution.

Start Maya 2014/2015 and load the voxelPlugin.py file into the script editor.
Ensure that ‘voxelize.png’ is located in the same directory as the Python script before loading the script into Maya.

Load the plugin. Go to Windows > Settings/Preferences > Plug-in Manager.
Browse to the file named VoxelMesh.mll (for Windows) or libvoxelMesh.so (for Linux).
For Maya 2015 use voxelMesh2015.mll.

Run the Python script from the script editor and the plugin should be ready for use.

//===================================================================================================

This plugin is supported for Autodesk Maya 2014 and requires Visual Studio 2010 redistributables to work on Windows
and Qt redistributables to work on Linux.

This plugin now supports Autodesk Maya 2015 for Windows and requires Visual Studio 2012 redistributables to work.

Code for the actual C++ plugin cannot be disclosed at this time.
