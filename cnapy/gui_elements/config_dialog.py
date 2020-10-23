"""The cnapy configuration dialog"""
from PySide2.QtWidgets import (QFileDialog, QColorDialog, QLabel, QButtonGroup, QComboBox, QDialog, QHBoxLayout,
                               QLineEdit, QPushButton, QRadioButton,
                               QVBoxLayout)

from PySide2.QtGui import QColor, QDrag, QMouseEvent, QPainter, QPalette

from PySide2.QtCore import Qt
from cnapy.cnadata import CnaData


class ConfigDialog(QDialog):
    """A dialog to set values in cnapy-config.txt"""

    def __init__(self, appdata: CnaData):
        QDialog.__init__(self)
        self.appdata = appdata
        self.layout = QVBoxLayout()
        h1 = QHBoxLayout()
        label = QLabel("CNA path")
        h1.addWidget(label)
        self.cna_path = QLineEdit()
        self.cna_path.setReadOnly(True)
        self.cna_path.setMinimumWidth(800)
        self.cna_path.setText(self.appdata.cna_path)
        h1.addWidget(self.cna_path)
        self.choose_cna_path_btn = QPushButton("Choose Directory")
        h1.addWidget(self.choose_cna_path_btn)
        self.layout.addItem(h1)

        h2 = QHBoxLayout()
        label = QLabel("Default color for values in a scenario:")
        h2.addWidget(label)
        self.scen_color_btn = QPushButton()
        palette = self.scen_color_btn.palette()
        palette.setColor(QPalette.Button, self.appdata.Scencolor)
        self.scen_color_btn.setPalette(palette)
        h2.addWidget(self.scen_color_btn)
        self.layout.addItem(h2)

        h3 = QHBoxLayout()
        label = QLabel(
            "Default color for computed values not part of the scenario:")
        h3.addWidget(label)
        self.comp_color_btn = QPushButton()
        palette = self.comp_color_btn.palette()
        palette.setColor(QPalette.Button, self.appdata.Compcolor)
        self.comp_color_btn.setPalette(palette)
        h3.addWidget(self.comp_color_btn)
        self.layout.addItem(h3)

        h4 = QHBoxLayout()
        label = QLabel(
            "Special Color used for non equal flux bounds:")
        h4.addWidget(label)
        self.spec1_color_btn = QPushButton()
        palette = self.spec1_color_btn.palette()
        palette.setColor(QPalette.Button, self.appdata.SpecialColor1)
        self.spec1_color_btn.setPalette(palette)
        h4.addWidget(self.spec1_color_btn)
        self.layout.addItem(h4)

        h5 = QHBoxLayout()
        label = QLabel(
            "Special Color 2 used for non equal flux bounds that exclude 0:")
        h5.addWidget(label)
        self.spec2_color_btn = QPushButton()
        palette = self.spec2_color_btn.palette()
        palette.setColor(QPalette.Button, self.appdata.SpecialColor2)
        self.spec2_color_btn.setPalette(palette)
        h5.addWidget(self.spec2_color_btn)
        self.layout.addItem(h5)

        # self.Defaultcolor = Qt.gray
        # self.rel_tol = 1e-9
        # self.abs_tol = 0.0001
        # self.rounding = 3

        l2 = QHBoxLayout()
        self.button = QPushButton("Apply Changes")
        self.cancel = QPushButton("Cancel")
        l2.addWidget(self.button)
        l2.addWidget(self.cancel)
        self.layout.addItem(l2)
        self.setLayout(self.layout)

        # Connecting the signal
        self.choose_cna_path_btn.clicked.connect(self.choose_cna_path)
        self.scen_color_btn.clicked.connect(self.choose_scen_color)
        self.comp_color_btn.clicked.connect(self.choose_comp_color)
        self.spec1_color_btn.clicked.connect(self.choose_spec1_color)
        self.spec2_color_btn.clicked.connect(self.choose_spec2_color)
        self.cancel.clicked.connect(self.reject)
        self.button.clicked.connect(self.apply)

    def choose_cna_path(self):
        dialog = QFileDialog(self)
        # dialog.setFileMode(QFileDialog.Directory)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        directory: str = dialog.getExistingDirectory()
        self.cna_path.setText(directory)
        pass

    def choose_scen_color(self):
        dialog = QColorDialog(self)
        color: str = dialog.getColor()

        palette = self.scen_color_btn.palette()
        palette.setColor(QPalette.Button, color)
        self.scen_color_btn.setPalette(palette)
        pass

    def choose_comp_color(self):
        dialog = QColorDialog(self)
        color: str = dialog.getColor()

        palette = self.comp_color_btn.palette()
        palette.setColor(QPalette.Button, color)
        self.comp_color_btn.setPalette(palette)
        pass

    def choose_spec1_color(self):
        dialog = QColorDialog(self)
        color: str = dialog.getColor()

        palette = self.spec1_color_btn.palette()
        palette.setColor(QPalette.Button, color)
        self.spec1_color_btn.setPalette(palette)
        pass

    def choose_spec2_color(self):
        dialog = QColorDialog(self)
        color: str = dialog.getColor()

        palette = self.spec2_color_btn.palette()
        palette.setColor(QPalette.Button, color)
        self.spec2_color_btn.setPalette(palette)
        pass

    def apply(self):

        self.appdata.cna_path = self.cna_path.text()
        palette = self.scen_color_btn.palette()
        self.appdata.Scencolor = palette.color(QPalette.Button)

        palette = self.comp_color_btn.palette()
        self.appdata.Compcolor = palette.color(QPalette.Button)

        palette = self.spec1_color_btn.palette()
        self.appdata.SpecialColor1 = palette.color(QPalette.Button)

        palette = self.spec2_color_btn.palette()
        self.appdata.SpecialColor2 = palette.color(QPalette.Button)

        import configparser
        configFilePath = r'cnapy-config.txt'
        parser = configparser.ConfigParser()
        parser.add_section('cnapy-config')
        parser.set('cnapy-config', 'cna_path', self.appdata.cna_path)
        parser.set('cnapy-config', 'scen_color',
                   str(self.appdata.Scencolor.rgb()))
        parser.set('cnapy-config', 'comp_color',
                   str(self.appdata.Compcolor.rgb()))
        parser.set('cnapy-config', 'spec1_color',
                   str(self.appdata.SpecialColor1.rgb()))
        parser.set('cnapy-config', 'spec2_color',
                   str(self.appdata.SpecialColor2.rgb()))

        fp = open(configFilePath, 'w')
        parser.write(fp)
        fp.close()

        self.accept()