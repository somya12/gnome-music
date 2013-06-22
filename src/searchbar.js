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
        this.view = null;

        let frame = new Gtk.Frame({ shadow_type: Gtk.ShadowType.IN,
                                    opacity: 0.9 });
        frame.get_style_context().add_class('documents-dropdown');

        this._grid = new Gtk.Grid({ orientation: Gtk.Orientation.HORIZONTAL });
        frame.add(this._grid);

        this._searchEntry = new Gd.TaggedEntry();
        this._searchEntry.connect("changed", Lang.bind(this, this.search_entry_changed));
        this._grid.add(this._searchEntry)

        this.widget = new Gtk.Revealer({ halign: Gtk.Align.CENTER,
                                         valign: Gtk.Align.START });
        this.widget.add(frame);

        this.hide();
        this.widget.show_all();
    },

    setViewFilter: function(model, iter, user_data) {
        if(this._searchEntry.visible){
            let search_string = this._searchEntry.text.toLowerCase();
            let media = model.get_value(iter, 5);
            let searchable_fields = [];
            if (media && media.get_artist){
                searchable_fields = [media.get_artist(), media.get_album(), media.get_title()]
            } else {
                searchable_fields = [model.get_value(iter, 2), model.get_value(iter, 3)]
            }
            for each(let field in searchable_fields){
                if (field && field.toLowerCase().indexOf(search_string) > -1)
                    return true;
            }
            return false;
        }
        return true;
    },

    _onItemActivated: function() {
        this.emit('item-activated');
    },

    show: function() {
        this.widget.reveal_child = true;
    },

    hide: function() {
        this.widget.reveal_child = false;
    },

    search_entry_changed: function() {
        this.search_term = this._searchEntry.text;
        if (this.view) {
            this.view.filter.refilter();
        }
    },

});
Signals.addSignalMethods(Searchbar.prototype);
