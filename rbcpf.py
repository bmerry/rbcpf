# rbcpf: customizes the playlist sidepane in Rhythmbox
# Copyright (C) 2014  Bruce Merry <bmerry@users.sourceforge.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from gi.repository import GObject, GLib, Gtk, RB, Peas
import gettext
gettext.install('rhythmbox', RB.locale_dir())

format_str = '{title}\n<span size="smaller"><i>{genre}</i></span>'

# The format string equivalent to the Rhythmbox built-in
original_format_str = '{title}\n<span size="smaller">{from} <i>{album}</i>\n{by} <i>{artist}</i></span>'

def format_time(seconds):
    '''
    Converts a number of seconds into a human-readable format
    '''
    if seconds >= 3600:
        return "{}:{:02d}:{:02d}".format(seconds // 3600, (seconds % 3600) // 60, seconds % 60)
    else:
        return "{}:{:02d}".format(seconds // 60, seconds % 60)

class RBCPFPlugin(GObject.Object, Peas.Activatable):
    '''
    Plugin class

    :var RB.Shell object: Reference to the Rhythmbox shell
    :ivar boolean replaced: Whether our print function has been installed
    :ivar str format_str: The current format string
    '''

    object = GObject.property(type = GObject.Object)

    def __init__(self):
        super(RBCPFPlugin, self).__init__()
        self.replaced = False
        self.format_str = original_format_str

    def play_queue_data_func(self, cell_layout, cell, model, it, data):
        entry = model.get_value(it, 0)

        fields = {
            'title': entry.get_string(RB.RhythmDBPropType.TITLE),
            'genre': entry.get_string(RB.RhythmDBPropType.GENRE),
            'artist': entry.get_string(RB.RhythmDBPropType.ARTIST),
            'album': entry.get_string(RB.RhythmDBPropType.ALBUM),
            'track_number': str(entry.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)),
            'duration': format_time(entry.get_ulong(RB.RhythmDBPropType.DURATION)),
            'from': _("from"),
            'by': _("by")
        }
        for key in fields:
            fields[key] = GLib.markup_escape_text(fields[key])

        markup = self.format_str.format(**fields)
        cell.props.markup = markup

    def get_treeview(self):
        shell = self.object
        queue = shell.props.queue_source
        view = queue.props.sidebar
        treeview = view.get_child()
        return treeview

    def set_format(self, format_str):
        self.format_str = format_str
        treeview = self.get_treeview()
        model = treeview.get_model()

        # Force treeview to redraw and recompute heights
        treeview.set_fixed_height_mode(False)
        treeview.set_fixed_height_mode(True)
        it = model.get_iter_first()
        while it != None:
            path = model.get_path(it)
            model.row_changed(path, it)
            it = model.iter_next(it)

    def replace_sidebar(self):
        treeview = self.get_treeview()
        column = treeview.get_column(1)
        renderer = column.get_cells()[0]

        column.set_cell_data_func(renderer, self.play_queue_data_func)

    def do_activate(self):
        '''
        Plugin activation
        '''
        shell = self.object

        if not self.replaced:
            self.replace_sidebar()
            self.set_format(format_str)
            self.replaced = True

    def do_deactivate(self):
        '''
        Plugin deactivation
        '''
        self.set_format(original_format_str)
