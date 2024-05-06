#!/usr/bin/env python
"""
Inkscape extension to create clip regions from selected image and shapes
Tested with Inkscape version 1.3

Copyright (C) 2024  Shrinivas Kulkarni (khemadeva@gmail.com)

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

import inkex
from lxml import etree
from inkex import Transform
import random


class MulticlipEffect(inkex.Effect):
    def __init__(self):
        """Initialize the Multi-clip extension with command-line arguments."""
        inkex.Effect.__init__(self)
        arg = self.arg_parser.add_argument
        arg(
            "--tab", help="Select Options"
        )  # Option tab in the GUI (not functional, just for layout grouping)
        arg(
            "--delete_original",
            type=inkex.Boolean,
            help="Delete selected paths",
        )
        arg(
            "--add_below",
            type=inkex.Boolean,
            help="Add clipped image below path",
        )
        arg(
            "--group_with_shape",
            type=inkex.Boolean,
            help="Group clipped part with path",
        )
        arg(
            "--animate",
            type=inkex.Boolean,
            help="Add simple animation",
        )

    def get_transform(self, elem, transform=Transform()):
        """
        Recursively accumulate the transformation matrix from the given element up to the root.

        Args:
            elem (lxml.etree.Element): The SVG element from which to start accumulating transformations.
            transform (inkex.Transform): The initial transformation matrix (defaults to identity matrix).

        Returns:
            inkex.Transform: The accumulated transformation matrix.
        """
        transform = Transform(elem.get("transform")) @ transform
        parent = elem.getparent()
        if parent is not None:
            return transform
        return self.get_transform(parent, transform)

    def add_group(self, parent, label):
        """
        Add a new group under the specified parent element and set its label.

        Args:
            parent (lxml.etree.Element): The parent element under which to add the group.
            label (str): The label for the new group, which appears in Inkscape's object properties.

        Returns:
            lxml.etree.Element: The newly created group element.
        """
        group = etree.SubElement(parent, "g")
        group.set(inkex.addNS("label", "inkscape"), label)
        return group

    def add_clip_path(self, defs, clipping_elem):
        """
        Create a clip path in the SVG 'defs' section using the specified clipping element.

        Args:
            defs (lxml.etree.Element): The 'defs' element of the SVG where the clip path is to be added.
            clipping_elem (inkex.PathElement): The element used to define the shape of the clip path.

        Returns:
            lxml.etree.Element: The newly created clipPath element.
        """
        clip_path = etree.SubElement(defs, inkex.addNS("clipPath", "svg"))
        path = etree.SubElement(clip_path, inkex.addNS("path", "svg"))
        # Transform the path of the clipping element according to its cumulative transformation
        tpath = clipping_elem.path.transform(self.get_transform(clipping_elem))
        path.set("d", str(tpath))
        return clip_path

    def add_translate_anim(self, anim_parent, extent_min, extent_max, anim_dur):
        """
        Add a translate animation to the specified parent element, moving the element from a
        random starting point to the origin.

        Args:
            anim_parent (lxml.etree.Element): The SVG element to which the animation is added.
            extent_min (int): The minimum extent of the random start position.
            extent_max (int): The maximum extent of the random start position.
            anim_dur (int): The duration of the animation in seconds.

        Returns:
            lxml.etree.Element: The newly created animateTransform element.
        """
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
        """
        Execute the effect of the Multi-clip extension which clips selected image with shapes and applies additional effects like grouping and animation.
        """

        delete_original = self.options.delete_original
        group_with_shape = self.options.group_with_shape
        animate = self.options.animate
        add_below = self.options.add_below

        # Constants for animation bounds and duration
        anim_extent_min = -150
        anim_extent_max = 150
        anim_dur = 1

        to_remove = set()
        defs = self.svg.getElement("//svg:defs")
        layer = self.document.getroot().get_current_layer()
        img_elems = self.svg.selection.filter(inkex.Image)
        if len(img_elems) == 0:
            inkex.errormsg("Please select at least one image")
            return

        # Consider only the first image element in the selection
        img_elem = img_elems[0]
        img_id = img_elem.get_id()
        first_elem = True

        # Iterate over selected elements to create clip paths and apply effects
        for clipping_elem in self.svg.selection:
            if isinstance(clipping_elem, inkex.Image):
                continue
            clip_path_id = self.add_clip_path(defs, clipping_elem).get_id()

            # Determine the parent for the new 'use' element based on user options
            # (create group if necessary)
            parent = layer if delete_original else clipping_elem.getparent()
            if group_with_shape and not delete_original:
                parent = self.add_group(parent, f"{clipping_elem.get_id()}-group")
                parent.insert(0, clipping_elem)

            # If it's the first clipping element, append (move) the image to defs so that
            # it can be referred by other 'use' elements ('original' for the 'clones')
            if first_elem:
                defs.append(img_elem)

            # Create a 'use' (clone) element to apply the clip path to the image
            image = etree.SubElement(parent, inkex.addNS("use", "svg"))
            image.set("xlink:href", f"#{img_id}")
            image.set("clip-path", f"url(#{clip_path_id})")
            if not delete_original:
                if add_below:
                    clipping_elem.addprevious(image)
                else:
                    clipping_elem.addnext(image)

            if animate:
                anim_parent = parent if group_with_shape else image
                self.add_translate_anim(
                    anim_parent, anim_extent_min, anim_extent_max, anim_dur
                )
            first_elem = False

            to_remove.add(clipping_elem)

        if delete_original:
            for clipping_elem in to_remove:
                clipping_elem.getparent().remove(clipping_elem)


MulticlipEffect().run()
