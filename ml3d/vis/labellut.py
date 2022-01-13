from colorsys import rgb_to_yiq


class LabelLUT:
    """The class to manage look-up table for assigning colors to labels."""

    class Label:

        def __init__(self, name, value, color):
            self.name = name
            self.value = value
            self.color = color
    # semantic kitti color
    # Colors = [[0., 0., 0.], [0.96078431, 0.58823529, 0.39215686],
    #           [0.96078431, 0.90196078, 0.39215686],
    #           [0.58823529, 0.23529412, 0.11764706],
    #           [0.70588235, 0.11764706, 0.31372549], [1., 0., 0.],
    #           [0.11764706, 0.11764706, 1.], [0.78431373, 0.15686275, 1.],
    #           [0.35294118, 0.11764706, 0.58823529], [1., 0., 1.],
    #           [1., 0.58823529, 1.], [0.29411765, 0., 0.29411765],
    #           [0.29411765, 0., 0.68627451], [0., 0.78431373, 1.],
    #           [0.19607843, 0.47058824, 1.], [0., 0.68627451, 0.],
    #           [0., 0.23529412,
    #            0.52941176], [0.31372549, 0.94117647, 0.58823529],
    #           [0.58823529, 0.94117647, 1.], [0., 0., 1.], [1.0, 1.0, 0.25],
    #           [0.5, 1.0, 0.25], [0.25, 1.0, 0.25], [0.25, 1.0, 0.5],
    #           [0.25, 1.0, 1.25], [0.25, 0.5, 1.25], [0.25, 0.25, 1.0],
    #           [0.125, 0.125, 0.125], [0.25, 0.25, 0.25], [0.375, 0.375, 0.375],
    #           [0.5, 0.5, 0.5], [0.625, 0.625, 0.625], [0.75, 0.75, 0.75],
    #           [0.875, 0.875, 0.875]]

    # rellis color
    # Colors = [[0., 0., 0.], [0., 0.4, 0.], [0., 1., 0.], [0., 0.6, 0.6],
    #        [0., 0.50196078, 1.], [1., 1., 0.], [0.4, 0., 0.], [0.8, 0.6, 1.],
    #        [0.4, 0., 0.8], [1., 0.6, 0.8], [0.66666667, 0.66666667, 0.66666667],
    #        [0.16078431, 0.4745098, 1.], [0.5254902, 1., 0.9372549],
    #        [0.38823529, 0.25882353, 0.13333333], [0.43137255, 0.08627451, 0.54117647]]
    Colors = [[0., 0., 0.],
           [0., 0.4, 0.],
           [0., 1., 0.],
           [0.6, 0.6, 0.],
           [1., 0.50196078, 0.],
           [0., 1., 1.],
           [0., 0., 0.4],
           [1., 0.6, 0.8],
           [0.8, 0., 0.4],
           [0.8, 0.6, 1.],
           [0.66666667, 0.66666667, 0.66666667],
           [1., 0.4745098, 0.16078431],
           [0.9372549, 1., 0.5254902],
           [0.13333333, 0.25882353, 0.38823529],
           [0.54117647, 0.08627451, 0.43137255]]
             

    def __init__(self, label_to_names=None):
        """
        Args:
            label_to_names: Initialize the colormap with this mapping from
                labels (int) to class names (str).
        """
        self._next_color = 0
        self.labels = {}
        if label_to_names is not None:
            for val in sorted(label_to_names.keys()):
                self.add_label(label_to_names[val], val)

    def add_label(self, name, value, color=None):
        """Adds a label to the table.

        Example:
            The following sample creates a LUT with 3 labels::

                lut = ml3d.vis.LabelLUT()
                lut.add_label('one', 1)
                lut.add_label('two', 2)
                lut.add_label('three', 3, [0,0,1]) # use blue for label 'three'

        Args:
            name: The label name as string.
            value: The value associated with the label.
            color: Optional RGB color. E.g., [0.2, 0.4, 1.0].
        """
        if color is None:
            if self._next_color >= len(self.Colors):
                color = [0.85, 1.0, 1.0]
            else:
                color = self.Colors[self._next_color]
                self._next_color += 1
        self.labels[value] = self.Label(name, value, color)

    @classmethod
    def get_colors(self, name='default', mode=None):
        """Return full list of colors in the lookup table.

        Args:
            name (str): Name of lookup table colormap. Only 'default' is
                supported.
            mode (str): Colormap mode. May be None (return as is), 'lightbg" to
                move the dark colors earlier in the list or 'darkbg' to move
                them later in the list. This will provide better visual
                discrimination for the earlier classes.

        Returns:
            List of colors (R, G, B) in the LUT.
        """
        if mode is None:
            return self.Colors
        dark_colors = list(
            filter(lambda col: rgb_to_yiq(*col)[0] < 0.5, self.Colors))
        light_colors = list(
            filter(lambda col: rgb_to_yiq(*col)[0] >= 0.5, self.Colors))
        if mode == 'lightbg':
            return dark_colors + light_colors
        if mode == 'darkbg':
            return light_colors + dark_colors
