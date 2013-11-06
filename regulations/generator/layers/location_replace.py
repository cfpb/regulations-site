class LocationReplace(object):
    """ Applies location based layers to XML nodes. We use XML so that we only
    take into account the original text when we're doing a replacement. """
    def __init__(self):
        self.counter = 0
        self.offset_starter = 0
        self.offset_counters = None
        self.offsets = None

    @staticmethod
    def find_all_offsets(pattern, text):
        """Don't use regular expressions as they are a tad slow"""
        matches = []
        pattern_len = len(pattern)
        next_match = text.find(pattern)
        while next_match != -1:
            matches.append((next_match, next_match + pattern_len))
            next_match = text.find(pattern, next_match + 1)
        return matches

    @staticmethod
    def replace_at_offset(offset, replacement, text):
        return text[:offset[0]] + replacement + text[offset[1]:]

    def update_offsets(self, original, text):
        """ Offsets change everytime we replace the text, since we add more
        characters. Update the offsets. """

        list_offsets = LocationReplace.find_all_offsets(original, text)

        angles_at = []
        lt = text.find('<')
        while lt != -1:
            gt = text.find('>', lt)
            angles_at.append((lt, gt))
            lt = text.find('<', gt)

        # Ignore everything in angle brackets
        list_offsets = [offsets for offsets in list_offsets
                        if not any(e[0] <= offsets[0] <= e[1]
                                   or e[1] <= offsets[1] <= e[1]
                                   for e in angles_at)]

        self.offset_counters = range(self.offset_starter,
                                     self.offset_starter + len(list_offsets))
        self.offsets = dict(zip(self.offset_counters, list_offsets))

    def update_offset_starter(self):
        """ As we're navigating the XML node, we need to keep track of how many
        offsets we've already seen. """
        if len(self.offset_counters) > 0:
            self.offset_starter = self.offset_counters[-1] + 1

    def apply_layer_to_text(self, original, replacement, text, locations):
        self.update_offsets(original, text)
        offset = self.offsets[locations[self.counter]]

        self.counter += 1
        return LocationReplace.replace_at_offset(offset, replacement, text)

    def location_replace_text(self, text, original, replacement, locations):
        """Given plain text, do replacements"""
        self.update_offsets(original, text)

        while (self.counter < len(locations)
               and locations[self.counter] in self.offsets):
            text = self.apply_layer_to_text(original, replacement, text,
                                            locations)

        self.update_offset_starter()
        return text

    def location_replace(self, xml_node, original, replacement, locations):
        """ For the xml_node, replace the locations instances of orginal with
        replacement."""

        if xml_node.text:
            xml_node.text = self.location_replace_text(
                xml_node.text, original, replacement, locations)

        for c in xml_node.getchildren():
            self.location_replace(c, original, replacement, locations)

        if xml_node.tail:
            xml_node.tail = self.location_replace_text(
                xml_node.tail, original, replacement, locations)
