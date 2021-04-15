"""The cnapy elementary flux modes calculator dialog"""
import efmtool_link.efmtool4cobra as efmtool4cobra
import efmtool_link.efmtool_extern as efmtool_extern
import numpy
from cobra.util.array import create_stoichiometric_matrix
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QCheckBox, QDialog, QHBoxLayout, QMessageBox,
                            QPushButton, QVBoxLayout)

from cnapy.cnadata import CnaData
from cnapy.flux_vector_container import FluxVectorMemmap


class EFMtoolDialog(QDialog):
    """A dialog to set up EFM calculation"""

    def __init__(self, appdata: CnaData, centralwidget):
        QDialog.__init__(self)
        self.appdata = appdata
        self.centralwidget = centralwidget

        self.layout = QVBoxLayout()

        l1 = QHBoxLayout()
        self.constraints = QCheckBox("consider 0 in current scenario as off")
        self.constraints.setCheckState(Qt.Checked)
        l1.addWidget(self.constraints)
        self.layout.addItem(l1)

        lx = QHBoxLayout()
        self.button = QPushButton("Compute")
        self.cancel = QPushButton("Close")
        lx.addWidget(self.button)
        lx.addWidget(self.cancel)
        self.layout.addItem(lx)

        self.setLayout(self.layout)

        # Connecting the signal
        self.cancel.clicked.connect(self.reject)
        self.button.clicked.connect(self.compute)

    def compute(self):
        stdf = create_stoichiometric_matrix(
            self.appdata.project.cobra_py_model, array_type='DataFrame')
        reversible, irrev_backwards_idx = efmtool4cobra.get_reversibility(
            self.appdata.project.cobra_py_model)
        if len(irrev_backwards_idx) > 0:
            irrev_back = numpy.zeros(len(reversible), dtype=numpy.bool)
            irrev_back[irrev_backwards_idx] = True
        scenario = {}
        if self.constraints.checkState() == Qt.Checked:
            for r in self.appdata.project.scen_values.keys():
                (vl, vu) = self.appdata.project.scen_values[r]
                if vl == vu and vl == 0:
                    r_idx = stdf.columns.get_loc(r)
                    del reversible[r_idx]
                    # delete the column with this reaction id from the data frame
                    del stdf[r]
                    if len(irrev_backwards_idx) > 0:
                        irrev_back = numpy.delete(irrev_back, r_idx)
                    scenario[r] = (0, 0)
        if len(irrev_backwards_idx) > 0:
            irrev_backwards_idx = numpy.where(irrev_back)[0]
            stdf.values[:, irrev_backwards_idx] *= -1
        work_dir = efmtool_extern.calculate_flux_modes(
            stdf.values, reversible, return_work_dir_only=True)
        reac_id = stdf.columns.tolist()

        self.result2ui(work_dir, reac_id, scenario, irrev_backwards_idx)

    def result2ui(self, work_dir, reac_id, scenario, irrev_backwards_idx):
        if work_dir is None:
            QMessageBox.information(self, 'No modes',
                                    'An error occured and modes have not been calculated.')
        else:
            ems = FluxVectorMemmap('efms.bin', reac_id,
                                   containing_temp_dir=work_dir)
            if len(ems) == 0:
                QMessageBox.information(self, 'No modes',
                                        'No elementary modes exist.')
            else:
                ems.fv_mat[:, irrev_backwards_idx] *= -1
                self.appdata.project.modes = ems
                self.centralwidget.mode_navigator.current = 0
                self.centralwidget.mode_navigator.scenario = scenario
                self.centralwidget.mode_navigator.title.setText(
                    "Mode Navigation")
                self.centralwidget.update_mode()
