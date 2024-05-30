import pandas as pd
import os

from project_path import PROJECT_ROOT_DIR


def import_data():
    file_path = os.path.join(PROJECT_ROOT_DIR, 'data', 'bbg_data.xlsx')
    pd.read_excel(file_path, sheet_name='')
