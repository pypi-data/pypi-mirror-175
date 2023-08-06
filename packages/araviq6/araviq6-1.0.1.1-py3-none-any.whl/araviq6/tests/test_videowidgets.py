from araviq6 import get_data_path, ClickableSlider
from araviq6.qt_compat import QtCore


VID_PATH = get_data_path("hello.mp4")


def test_ClickableSlider(qtbot):
    slider = ClickableSlider()
    qtbot.addWidget(slider)
    assert slider.value() == 0

    pos = QtCore.QPoint(10, 10)
    qtbot.mouseClick(slider, QtCore.Qt.LeftButton, pos=pos)
    assert slider.value() == slider.pixelPosToRangeValue(pos)
