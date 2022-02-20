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

"""
This script exports an Inkscape drawing to multiple PDF documents, one 
for each layer. This works by showing just one layer after the other 
(while hiding all others) and exporting the document to a PDF file.
"""

import collections
import os
import tempfile

import inkex
from inkex.command import inkscape
from lxml import etree


class Layer(object):

    """
    A single layer in the document.
    """

    def __init__(self, root):
        self.root = root
        self.id = root.get("id")
        self.label = root.xpath("string(./@inkscape:label)", namespaces=inkex.NSS)
        self.style = root.attrib.get("style", default="")
        self.visible = "display:none" in self.style
        self.locked = root.xpath(
            "string(./@sodipodi:insensitive)", namespaces=inkex.NSS).lower() == "true"

    def __repr__(self):
        return "<Layer id={0.id} label={0.label!r} visible={0.visible} locked={0.locked}>".format(self)

    def find_parent_id(self):
        """
        Return ID of parent layer element or ``None`` if already top layer.
        """
        parents = self.root.xpath(
            'ancestor::svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        return parents[-1].get("id") if len(parents) > 0 else None

    @staticmethod
    def from_document(document):
        # TODO detect layer hierarchy
        layers = document.xpath(
            '//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        for layer in layers:
            yield Layer(layer)

    def hide(self):
        self.root.set("style", "display:none")
        self.visible = False

    def show(self):
        # TODO Don't overwrite existing style!
        self.root.set("style", "")
        self.visible = True


class MultipageSave(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--directory", type=str, dest="directory", help="Directory where PDFs are stored.")
        pars.add_argument("--hide-locked-layers", type=inkex.Boolean, dest="hide_locked_layers", help="Hide locked layers during rendering.")

    def effect(self):

        #self.debug(self.options)

        layers = self.find_layers().values()

        #inkex.errormsg(f"--directory={self.options.directory} --hide-locked-layers={self.options.hide_locked_layers}")
        #inkex.errormsg("\n".join("[{1}] {0}".format(layer, "x" if layer.visible else " ") for layer in layers))
        #inkex.errormsg(f"--directory={self.options.directory} --hide-locked-layers={self.options.hide_locked_layers}")

        for no, layer in enumerate(layers, start=1):
            map(lambda l: l.hide(), layers)
            layer.show()

            tmp_svg = os.path.abspath(tempfile.mktemp("page_%i.svg" % no))
            tmp_pdf = os.path.abspath(os.path.expanduser(os.path.join(self.options.directory, "page_%i.pdf" % no)))

            with open(tmp_svg, 'w') as fp:
                root = self.document.getroot()
                fp.write(etree.tostring(root).decode('utf-8'))
                fp.close()
                #self.debug(f"{tmp_svg} -> {tmp_pdf}")
                inkscape(tmp_svg, export_filename=tmp_pdf)

    def find_layers(self):
        layers = collections.OrderedDict([
            (layer.id, layer) for layer in Layer.from_document(self.svg)
        ])
        #for layer in layers.values():
        #    self.debug("[{1}] {0}".format(layer, "x" if layer.visible else " "))
        return layers


if __name__ == '__main__':  # pragma: no cover
    MultipageSave().run()
