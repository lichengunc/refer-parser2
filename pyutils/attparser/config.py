__author__ = 'licheng'

class config():
    def __init__(self):
        self.attribute_names = ['entrylevel', 'color', 'size', 'absolute_location', 'relative_location', 'relative_object', 'generic']

    def buildTable(self, words):
        table = {'wordtoix': {}, 'ixtoword': {}, 'words': []}
        for ix, wd in enumerate(words):
            if wd.find(',') > 0:
                jx = wd.find(',')
                wd1, wd2 = wd[:jx].strip(), wd[jx+1:].strip()
                table['wordtoix'][wd1], table['wordtoix'][wd2] = ix, ix
                table['ixtoword'][ix] = wd1
            else:
                table['wordtoix'][wd] = ix
                table['ixtoword'][ix] = wd
        table['words'] = table['wordtoix'].keys()
        return table


class configCLEF(config):
    def __init__(self):
        config.__init__(self)
        # color
        self.color_words = ['white', 'green, greenish', 'blue, bluish', 'red', 'yellow, yellowish', 'black', 'brown, brownish',
                            'pink', 'dark, darker', 'orange', 'gray, grey', 'purple', 'beige', 'bright']
        self.color_table = self.buildTable(self.color_words)
        # size
        self.size_words = ['big', 'small', 'tall', 'large', 'little', 'short', 'tiny', 'long', 'huge']
        self.size_table = self.buildTable(self.size_words)
        # location
        self.location_words = ['right', 'left', 'top', 'bottom', 'middle, mid', 'second, 2nd', 'first, 1st', 'front',
                               'closest, nearest', 'center, central', 'third, 3rd', 'corner', 'upper', 'back, behind',
                               'far', 'anywhere', 'leftmost', 'lower', 'rightmost', 'farthest, furthest', 'next', 'last',
                               'fourth, 4th', 'up, above', 'below, down', 'side']
        self.location_table = self.buildTable(self.location_words)
        # position
        self.position_words = ['right', 'left', 'top', 'bottom', 'middle, center, centre', 'front', 'back']
        self.position_table = self.buildTable(self.position_words)
        # relative preps
        self.relative_preps_words = ['prep_above', 'prep_about', 'prep_below', 'prep_behind', 'prep_beneath', 'prep_beside',
                                     'prep_between', 'prep_close_to', 'prep_by', 'prep_in_front_of', 'prep_against',
                                     'prep_from', 'prep_next_to', 'prep_through', 'prep_under', 'prep_underneath', 'prep_with',
                                     'prep_near', 'prep_inside']
        self.relative_preps_table = self.buildTable(self.relative_preps_words)
        # ordinal number
        self.ordinal_words = ['first', 'second', 'third', 'fourth', 'fifth', 'most']
        self.ordinal_table = self.buildTable(self.ordinal_words)

class configCOCO(config):
    def __init__(self):
        config.__init__(self)
        # color
        self.color_words = ['white', 'green', 'blue', 'red', 'yellow', 'black', 'brown', 'pink', 'dark, darker', 'orange',
                            'gray', 'purple', 'beige', 'bright']
        self.color_table = self.buildTable(self.color_words)
        # size
        self.size_words = ['big, bigger', 'small, smaller', 'tall, taller', 'large, larger', 'little', 'short, shorter',
                           'tiny', 'long, longer', 'huge']
        self.size_table = self.buildTable(self.size_words)
        # location
        self.location_words = ['right', 'left', 'top', 'bottom', 'middle, mid', 'front', 'closest, nearest', 'center, central',
                               'corner', 'upper', 'back, behind', 'far', 'leftmost', 'lower, low', 'rightmost',
                               'farthest, furthest', 'next', 'last', 'up, above', 'below, down', 'side']
        self.location_table = self.buildTable(self.location_words)
        # position
        self.position_words = ['right', 'left', 'top', 'bottom', 'middle, center, centre', 'front', 'back']
        self.position_table = self.buildTable(self.position_words)
        # relative preps
        self.relative_preps_words = ['prep_above', 'prep_about', 'prep_below', 'prep_behind', 'prep_beneath', 'prep_beside',
                                     'prep_between', 'prep_close_to', 'prep_by', 'prep_in_front_of', 'prep_against',
                                     'prep_from', 'prep_next_to', 'prep_through', 'prep_under', 'prep_underneath', 'prep_with',
                                     'prep_near', 'prep_inside', 'prepc_from']
        self.relative_preps_table = self.buildTable(self.relative_preps_words)
        # ordinal number
        self.ordinal_words = ['first', 'second', 'third', 'fourth', 'fifth']
        self.ordinal_table = self.buildTable(self.ordinal_words)


if __name__ == '__main__':
    c = configCOCO()
    print c.color_table
    print c.size_table
    print c.location_table
    print c.position_table['words']
    print c.relative_preps_table











