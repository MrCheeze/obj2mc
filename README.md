obj2mc
======

Converts a 3d model from .obj format into the json form recognized by Minecraft. Usage:

`python obj2mc.py myobject.obj [growthfactor]`

growthfactor is an optional argument that increases or decreases the overall size of the model. For example, growthfactor of 2 will double all three dimensions, and 0.5 will halve them.

Note that for high-resolution models, you might want to lower the poly count using [some other tool](http://www.blender.org/download/) first, at least if you want Minecraft to be able to render it without crashing.

At the moment, only the format used in 16w06b is supported, not later versions.