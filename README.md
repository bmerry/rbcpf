Rhythmbox Custom Playlist Format
================================
This is a Rhythmbox plugin that allows the format of the playlist sidepane to
be customized. For example, it can be used to show the genre instead of the
artist.

Installation
------------
Simply copy the entire directory tree to the Rhythmbox plugins directory. For
a local user on a UNIX-like system, this is ~/.local/share/rhythmbox/plugins.

Configuration
-------------
At present the new format is hard-coded into the plugin. Edit `rbcpf.py` to
change it.

Caveats
-------
Limitations in GTK+ make it impossible to completely deactivate the plugin.
After deactiviting the plugin through the API, it is recommended to close and
restart Rhythmbox.

This has only be tested with Rhythmbox 2.99, which uses Python 2. Your mileage
may vary with Rhythmbox 3.x, which uses Python 3. At a minimum you may need
to change the Loader in `rbcpf.plugin` from `python` to `python3`.

License
-------
Copyright © 2014 Bruce Merry

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
