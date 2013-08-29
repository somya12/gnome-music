# Copyright (c) 2013 Vadim Rutkovsky <vrutkovs@redhat.com>
# Copyright (c) 2013 Arnel A. Borja <kyoushuu@yahoo.com>
# Copyright (c) 2013 Seif Lotfy <seif@lotfy.com>
# Copyright (c) 2013 Guillaume Quintard <guillaume.quintard@gmail.com>
#
# GNOME Music is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# GNOME Music is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with GNOME Music; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# The GNOME Music authors hereby grant permission for non-GPL compatible
# GStreamer plugins to be used and distributed together with GStreamer
# and GNOME Music.  This permission is above and beyond the permissions
# granted by the GPL license by which GNOME Music is covered.  If you
# modify this code, you may extend this exception to your version of the
# code, but you are not obligated to do so.  If you do not wish to do so,
# delete this exception statement from your version.


from gi.repository import Grl, GLib, GObject

from gnomemusic.query import Query


class Grilo(GObject.GObject):

    __gsignals__ = {
        'ready': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    # Note that we ask for thumbnail in the first query too,
    # but since we don't pass the Grl.ResolutionFlags.FULL,
    # we only get a result if tracker has it readily available
    # (usually it's not, because it requires tracker compiled
    # with UPnP support)
    # In any case, we'll proceed to fetch the thumbnail later
    # by resolving the item, through grl-local-metadata or
    # grl-lastfm-albumart
    METADATA_KEYS = [
        Grl.METADATA_KEY_ID, Grl.METADATA_KEY_TITLE,
        Grl.METADATA_KEY_ARTIST, Grl.METADATA_KEY_ALBUM,
        Grl.METADATA_KEY_DURATION,
        Grl.METADATA_KEY_CREATION_DATE,
        Grl.METADATA_KEY_THUMBNAIL
    ]

    METADATA_THUMBNAIL_KEYS = [
        Grl.METADATA_KEY_ID,
        Grl.METADATA_KEY_THUMBNAIL
    ]

    def __init__(self):
        GObject.GObject.__init__(self)

        self.fast_options = Grl.OperationOptions()
        self.fast_options.set_flags(Grl.ResolutionFlags.IDLE_RELAY)
        self.full_options = Grl.OperationOptions()
        self.full_options.set_flags(Grl.ResolutionFlags.FULL |
                                    Grl.ResolutionFlags.IDLE_RELAY)

        self.registry = Grl.Registry.get_default()
        try:
            self.registry.load_all_plugins()
        except GLib.GError:
            print('Failed to load plugins.')

        self.sources = {}
        self.tracker = None

        self.registry.connect('source_added', self._on_source_added)
        self.registry.connect('source_removed', self._on_source_removed)

    def _on_source_added(self, pluginRegistry, mediaSource):
        id = mediaSource.get_id()
        if id == 'grl-tracker-source':
            ops = mediaSource.supported_operations()
            if ops & Grl.SupportedOps.SEARCH:
                print('Detected new source available: \'%s\' and it supports search' %
                      mediaSource.get_name())

                self.sources[id] = mediaSource
                self.tracker = mediaSource

                if self.tracker is not None:
                    self.emit('ready')

    def _on_source_removed(self, pluginRegistry, mediaSource):
        print('source removed')

    def populate_artists(self, offset, callback):
        self.populate_items(Query.ARTISTS, offset, callback)

    def populate_albums(self, offset, callback):
        self.populate_items(Query.ALBUMS, offset, callback)

    def populate_songs(self, offset, callback):
        self.populate_items(Query.SONGS, offset, callback)

    def populate_album_songs(self, album_id, callback):
        self.populate_items(Query.album_songs(album_id), 0, callback)

    def populate_items(self, query, offset, callback, count=50):
        options = self.fast_options.copy()
        options.set_skip(offset)

        def _callback(source, param, item, count, data, offset):
            callback(source, param, item)
        self.tracker.query(query, self.METADATA_KEYS, options, _callback, None)

    def _search_callback(self):
        print('yeah')

    def search(self, q):
        for source in self.sources:
            print(source.get_name() + ' - ' + q)
            source.search(q, [Grl.METADATA_KEY_ID], 0, 10,
                          self.fast_options, self._search_callback, source)

    def get_album_art_for_album(self, album, _callback, data):
        self.tracker.resolve(album, self.METADATA_THUMBNAIL_KEYS,
                             self.full_options, _callback, data)

Grl.init(None)

grilo = Grilo()
