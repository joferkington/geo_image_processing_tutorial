import matplotlib.pyplot as plt
import matplotlib as mpl
import ipywidgets
from matplotlib.colorbar import make_axes_gridspec
import matplotlib.widgets


class BaseWidget:

    def callback(self, value):
        raise NotImplementedError

    @property
    def is_native(self):
        """Whether or not we're working with a notebook backend."""
        return mpl.get_backend().lower() not in ['nbagg', 'webagg', 'ipympl']

    def show(self):
        """
        Display the figure. Provided as a method to avoid the need to save a
        reference to this object.
        """
        if self.is_native:
            plt.show()
        else:
            return ipywidgets.interact(self.callback, value=self.widget)

    def _make_room(self, ax, **kwargs):
        """Shrink parent axes and make a new axes for widgets."""
        cax, _ = make_axes_gridspec(ax, **kwargs)
        cax.axis('off')
        cax.set(aspect=1)
        return cax



class Toggler(BaseWidget):
    """
    Toggle between several artists in a matplotlib figure. Uses ipython widgets
    if we're in a notebook, or native matplotlib widgets if we're not.
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
        self.widget = self._native() if self.is_native else self._notebook()
        self._hide()

    def _notebook(self):
        return ipywidgets.RadioButtons(options=self.labels,
                                       description='Overlay:',
                                       value=self.labels[0],
                                       disabled=False)

    def _native(self):
        widget_ax = self._make_room(self.ax)
        widget = mpl.widgets.RadioButtons(widget_ax, self.labels, active=0,
                                          activecolor='black')
        widget.on_clicked(self.callback)
        return widget

    @property
    def labels(self):
        return ['Off'] + [layer.get_label() for layer in self.layers]

    def callback(self, value=None):
        self._hide()
        if self.is_native and not value:
            value = self.widget.value_selected

        layer = self.lookup.get(value)
        if layer:
            layer.set_visible(True)
        self.fig.canvas.draw_idle()

    def _hide(self):
        for artist in self.layers:
            artist.set_visible(False)


class Slider(BaseWidget):
    """
    Simple slider bar that uses a callback. Uses ipython widgets when in a
    notebook or native widgets if using a native backend.
    """
    def __init__(self, ax, vmin, vmax, callback, label='Value', start=None):
        self.ax = ax
        self.fig = self.ax.figure
        self.label = label
        self.vmin = vmin
        self.vmax = vmax
        self._callback = callback
        if start is None:
            start = (vmin + vmax) / 2
        self.start = start
        self.widget = self._native() if self.is_native else self._notebook()

    def _notebook(self):
        return ipywidgets.IntSlider(min=self.vmin, max=self.vmax, step=1,
                                    value=self.start)

    def _native(self):
        widget_ax = self._make_room(self.ax, orientation='horizontal')
        widget = mpl.widgets.Slider(widget_ax, self.label, self.vmin,
                                    self.vmax, self.start)
        widget.on_changed(self.callback)
        return widget

    def callback(self, value):
        self._callback(value)
        self.fig.canvas.draw_idle()
