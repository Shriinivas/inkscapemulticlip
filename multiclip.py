#!/usr/bin/env python
"""
Inkscape extension to create clip an objects with objects placed above
Tested with Inkscape version 1.3

Author: Shrinivas Kulkarni (khemadeva@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import inkex, random
from lxml import etree  # type: ignore


class MulticlipEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        arg = self.arg_parser.add_argument
        arg("--tab", help="Select Options")
        arg(
            "--delete_original",
            type=inkex.Boolean,
            help="Delete selected paths",
        )
        arg(
            "--position",
            type=str,
            help="Add clipped part below or above shape (ignored if 'Delete Selection' is checked)",
        )
        arg(
            "--grouping",
            type=str,
            help="Whether to group clipped part with its clipping object (ignored if 'Delete Clipping Objects' is checked)",
        )
        arg(
            "--animate",
            type=inkex.Boolean,
            help="Add simple animation",
        )

    def add_clip_path(self, clipping_elem):
        clip_path_elem = self.svg.defs.add(inkex.ClipPath())
        path_elem = clip_path_elem.add(inkex.PathElement())
        path_elem.path = clipping_elem.path.transform(
            clipping_elem.composed_transform()
        )
        return clip_path_elem

    def add_translate_anim(self, anim_parent, extent_min, extent_max, anim_dur):
        anim_trans = etree.SubElement(
            anim_parent, inkex.addNS("animateTransform", "svg")
        )
        anim_trans.set("attributeName", "transform")
        anim_trans.set("attributeType", "XML")
        anim_trans.set("type", "translate")
        anim_trans.set(
            "from",
            f"{random.randint(extent_min, extent_max)} "
            + f"{random.randint(extent_min, extent_max)}",
        )
        anim_trans.set("to", "0 0")
        anim_trans.set("dur", f"{anim_dur}")
        anim_trans.set("repeatCount", "1")
        return anim_trans

    def effect(self):
        delete_original = self.options.delete_original
        grouping = self.options.grouping
        animate = self.options.animate
        position = self.options.position

        # Constants for animation bounds and duration
        anim_extent_min = -150
        anim_extent_max = 150
        anim_dur = 1

        to_remove = set()
        layer = self.svg.get_current_layer()

        elems = self.svg.selection.rendering_order()
        target_elem = elems.pop(0)
        target_id = target_elem.get_id()
        first_elem = True

        for clipping_elem in elems:
            if not clipping_elem.path:
                continue
            clip_path_id = self.add_clip_path(clipping_elem).get_id()
            parent = layer if delete_original else clipping_elem.getparent()
            if grouping == "group" and not delete_original:
                group = inkex.Group()
                group.set(
                    inkex.addNS("label", "inkscape"), f"{clipping_elem.get_id()}-group"
                )
                clipping_elem.addprevious(group)
                parent.remove(clipping_elem)
                group.add(clipping_elem)

            # If it's the first clipping element, append (move) the target to defs so that
            # it can be referred by other 'use' elements ('original' for the 'clones')
            if first_elem:
                target_elem.getparent().remove(target_elem)
                self.svg.defs.add(target_elem)

            # Create a 'use' (clone) element to apply the clip path to the object
            target_clone = parent.add(inkex.Use())
            target_clone.set("xlink:href", f"#{target_id}")
            target_clone.set("clip-path", f"url(#{clip_path_id})")
            if not delete_original:
                if position == "above":
                    clipping_elem.addprevious(target_clone)
                else:
                    clipping_elem.addnext(target_clone)

            if animate:
                anim_parent = parent if grouping == "group" else target_clone
                self.add_translate_anim(
                    anim_parent, anim_extent_min, anim_extent_max, anim_dur
                )

            to_remove.add(clipping_elem)
            first_elem = False

        if delete_original:
            for clipping_elem in to_remove:
                clipping_elem.getparent().remove(clipping_elem)


MulticlipEffect().run()
