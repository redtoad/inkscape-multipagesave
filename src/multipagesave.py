#!/usr/bin/env python

# This extension to Inkscape will export SVG layers independently to PDFs
# Copyright (C) 2018 Sebastian Rahlf
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

import collections
import os
import tempfile

import inkex


class InkscapeLayer(object):

    def __init__(self, root):
        self.root = root

        def _parse_style(txt):
            attrs = [attr.split(":") for attr in txt.split(";")]
            return {
                key.strip(): val.strip()
                for key, val in attrs
                if key.strip()
            } if txt and attrs else {}

        self.id = root.get("id")
        self.label = root.xpath("string(./@inkscape:label)", namespaces=inkex.NSS)
        self.style = _parse_style(root.get("style", ""))
        self.visible = self.style.get("display") != "none"
        self.locked = root.xpath("string(./@sodipodi:insensitive)", namespaces=inkex.NSS).lower() == "true"

    def __repr__(self):
        return "<Layer id={0.id} label={0.label!r} visible={0.visible}>".format(self)

    def find_parent_id(self):
        """
        Return ID of parent layer element or ``None`` if already top layer.
        """
        parents = self.root.xpath('ancestor::svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        return parents[-1].get("id") if len(parents) > 0 else None

    @staticmethod
    def from_document(document):
        layers = document.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        for layer in layers:
            yield InkscapeLayer(layer)

    def hide(self):
        self.root.set("style", "display:none")
        self.visible = False

    def show(self):
        self.root.set("style", "")
        self.visible = True


class MultipageSave(inkex.Effect):

    def effect(self):
        """Apply some effects on the document. Extensions subclassing Effect
        must override this function and define the transformations
        in it."""
        layers = self.find_layers()
        for no, layer in enumerate(layers, start=1):
            map(lambda l: l.hide(), layers)
            layer.show()
            tmp_svg = os.path.abspath(tempfile.mktemp("page_%i.svg" % no))
            tmp_pdf = os.path.abspath("page_%i.pdf" % no)

            with open(tmp_svg, 'w') as fp:
                fp.write(inkex.etree.tostring(self.document.getroot()))
                fp.close()
                cmd = 'inkscape -f "{0}" -A "{1}"'.format(tmp_svg, tmp_pdf)
                print(cmd)
                os.system(cmd)

    def find_layers(self):
        layers = collections.OrderedDict([
            (layer.id, layer) for layer in InkscapeLayer.from_document(self.document)
        ])
        for layer in layers.values():
            print("[{1}] {0}".format(layer, "x" if layer.visible else " "))
        return layers.values()


if __name__ == '__main__':  # pragma: no cover
    e = MultipageSave()
    e.affect()
