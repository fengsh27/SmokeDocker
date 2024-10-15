
class SpaGFTSmokeAdapter:
    def __init__(self) -> None:
        self.data_output = None

    def generate_dependency_prompt(self):
        return "Data preparation Python scripts need package: gdown"

    def generate_data_preparation_script(self):
        """
        This step is to prepare smoke data to directory smoke_data/.
        If there is no smoke data, we can leave it empty.
        """
        data_preparation = """
import os
import gdown
if not os.path.exists("/data"):
    os.makedirs("/data")
res = gdown.download_folder(
    id="1XNQh4FH52bgsRzHRjcwdqkhVT-9mKDgB",
    output="/data",
)"""
        return data_preparation
        # with open("./data_preparation.py", "w") as fobj:
        #     fobj.write(data_preparation)
        #     return "./data_preparation.py"

    def generate_running_script(self):
        """
        This step is to generate smoke test script to smoke_test/smoke_test.sh
        """
        import_script =  """
import os
import SpaGFT as spg
import numpy as np
import pandas as pd
import scanpy as sc

sc.settings.verbosity = 1
sc.logging.print_header()
sc.settings.set_figure_params(dpi=80, facecolor='white')"""

        prepare_output_script = """
results_folder = './results/mouse_brain_coronal_analysis/'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)"""
        read_script = (
            'adata = sc.read_visium("/data/SpaGFT/mouse-he-coronal")'
            "adata.var_names_make_unique()"
            "# Add raw to anndata object"
            "adata.raw = adata"
        )
        qc_script = """
# QC
sc.pp.filter_genes(adata, min_cells=10)
# Normalization
sc.pp.normalize_total(adata, inplace=True)
sc.pp.log1p(adata)"""
        spg_script = """
# determine the number of low-frequency FMs and high-frequency FMs
(ratio_low, ratio_high) = spg.gft.determine_frequency_ratio(adata,
                                                            ratio_neighbors=1)"""

        scripts = "\n".join([
            import_script,
            prepare_output_script,
            read_script,
            qc_script,
            spg_script,
        ])
        return scripts

