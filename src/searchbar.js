/*
 * Copyright (c) 2013 Eslam Mostafa<cseslam@gmail.com>.
 *
 * Gnome Music is free software; you can Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * Gnome Music is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with Gnome Music; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * Author: Eslam Mostafa <cseslam@gmail.com>
 *
 */

const Lang = imports.lang;
const Gtk = imports.gi.Gtk;
const Gdk = imports.gi.Gdk;
const Gd = imports.gi.Gd;
const Signals = imports.signals;

const Searchbar = new Lang.Class({
    Name: "Searchbar",

    _init: function() {
        let frame = new Gtk.Frame({ shadow_type: Gtk.ShadowType.IN,
                                    opacity: 0.9 });
        frame.get_style_context().add_class('documents-dropdown');

        this._grid = new Gtk.Grid({ orientation: Gtk.Orientation.HORIZONTAL });
        frame.add(this._grid);

        this._searchEntry = new Gd.TaggedEntry();
        this._grid.add(this._searchEntry)

        this.widget = new Gtk.Revealer({ halign: Gtk.Align.CENTER,
                                         valign: Gtk.Align.START });
        this.widget.add(frame);

        this.hide();
        this.widget.show_all();
    },

    _onItemActivated: function() {
        this.emit('item-activated');
    },

    show: function() {
        this.widget.reveal_child = true;
    },

    hide: function() {
        this.widget.reveal_child = false;
    }
});
Signals.addSignalMethods(Searchbar.prototype);
