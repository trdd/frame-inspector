import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=12, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = []
        self.axes.append(fig.add_subplot(311))
        self.axes.append(fig.add_subplot(312, sharex=self.axes[0],
                sharey=self.axes[0]))
        self.axes.append(fig.add_subplot(313, sharex=self.axes[0],
                sharey=self.axes[0]))
        self.axes[0].set_title('frame_1')
        self.axes[1].set_title('frame_2')
        self.axes[2].set_title('frame_1 - frame_2')
        for a in self.axes:
            a.axis([-0.5, 1474.5, 194.5, -0.5])
            a.set_aspect('equal')
        fig.set_tight_layout(True)
        super(MplCanvas, self).__init__(fig)

