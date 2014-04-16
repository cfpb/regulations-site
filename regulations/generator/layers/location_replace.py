class LocationReplace(object):
    """ Applies location based layers to XML nodes. We use XML so that we only
    take into account the original text when we're doing a replacement. """
    def __init__(self):
        self.counter = 0
        self.offset_starter = 0
        self.offset_counters = None
        self.offsets = None

    @staticmethod
    def find_all_offsets(pattern, text, offset=0):
        """Don't use regular expressions as they are a tad slow"""
        matches = []
        pattern_len = len(pattern)
        next_match = text.find(pattern)
        while next_match != -1:
            matches.append((next_match + offset,
                            next_match + pattern_len + offset))
            next_match = text.find(pattern, next_match + 1)
        return matches

    @staticmethod
    def replace_at_offset(offset, replacement, text):
        return text[:offset[0]] + replacement + text[offset[1]:]

    def update_offsets(self, original, text):
        """ Offsets change everytime we replace the text, since we add more
        characters. Update the offsets. """
        list_offsets = []
        lt = text.find('<')
        gt = -1
        while lt != -1:
            subtext = text[gt+1: lt]
            list_offsets.extend(LocationReplace.find_all_offsets(
                original, subtext, gt + 1))
            gt = text.find('>', lt)
            lt = text.find('<', gt)
        list_offsets.extend(LocationReplace.find_all_offsets(
            original, text[gt+1:], gt + 1))

        self.offset_counters = range(self.offset_starter,
                                     self.offset_starter + len(list_offsets))
        self.offsets = dict(zip(self.offset_counters, list_offsets))

    def update_offset_starter(self):
        """ As we're navigating the XML node, we need to keep track of how many
        offsets we've already seen. """
        if len(self.offset_counters) > 0:
            self.offset_starter = self.offset_counters[-1] + 1

    def location_replace_text(self, text, original, replacement, locations):
        """Given plain text, do replacements"""
        self.update_offsets(original, text)

        text_segments = []
        relevant_locations = sorted(self.offsets.keys())
        relevant_locations = [l for l in relevant_locations if l in locations]
        text_begin = 0
        for location in relevant_locations:
            start, end = self.offsets[location]
            # unrelated text
            text_segments.append(text[text_begin:start])
            # s/original/replacement
            text_segments.append(replacement)
            text_begin = end
        # tail of unrelated text
        text_segments.append(text[text_begin:])

        # offset_starter is shared between segments of xml nodes (in 
        # location_replace, below)
        if original not in replacement:
            self.offset_starter += len(locations)

        self.update_offset_starter()
        return "".join(text_segments)

    def location_replace(self, xml_node, original, replacement, locations):
        """ For the xml_node, replace the locations instances of orginal with
        replacement.
        @todo: This doesn't appear to be used anymore?"""

        if xml_node.text:
            xml_node.text = self.location_replace_text(
                xml_node.text, original, replacement, locations)

        for c in xml_node.getchildren():
            self.location_replace(c, original, replacement, locations)

        if xml_node.tail:
            xml_node.tail = self.location_replace_text(
                xml_node.tail, original, replacement, locations)
