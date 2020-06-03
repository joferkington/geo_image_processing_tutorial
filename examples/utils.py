import matplotlib.pyplot as plt
from matplotlib.colorbar import make_axes_gridspec
from matplotlib.widgets import RadioButtons


class Toggler:
    """
    Toggle between several artists in a matplotlib figure.
    """
    def __init__(self, *layers):
        """
        Parameters
        ----------
        *layers : Matplotlib artist to enable toggling on/off.
        """
        self.layers = layers
        self.lookup = {x.get_label(): x for x in self.layers}
        self.ax = self.layers[0].axes
        self.fig = self.ax.figure
        self.widget_ax = self._make_room()
        self.widget = self._create_buttons()
        self._hide()

    def _callback(self, event):
        self._hide()
        layer = self.lookup.get(self.widget.value_selected)
        if layer:
            layer.set_visible(True)
        self.fig.canvas.draw()

    def _create_buttons(self):
        labels = ['Off'] + [layer.get_label() for layer in self.layers]
        widget = RadioButtons(self.widget_ax, labels, active=0,
                              activecolor='lightblue')
        widget.on_clicked(self._callback)
        return widget

    def _make_room(self):
        ax, _ = make_axes_gridspec(self.ax)
        ax.axis('off')
        ax.set(aspect=1)
        return ax

    def _hide(self):
        for artist in self.layers:
            artist.set_visible(False)

    def show(self):
        """
        Display the figure. Provided as a method to avoid the need to save a
        reference to this object.
        """
        plt.show()
