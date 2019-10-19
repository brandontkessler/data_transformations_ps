import pandas as pd

from .helpers import donor_dtype

class _DonorBase:
    DEFAULT_PATH = '../../data/donor/'
    DEFAULT_FILE_YR = '08'
    DTYPE = donor_dtype

    def __init__(self, path=None, file_yr=None):
        self._path = path or self.DEFAULT_PATH
        self._file_yr = file_yr or self.DEFAULT_FILE_YR
        self.data = self._import_data()

    # ---------------------- Build Dataset --------------
    def _import_data(self):
        file = self._build_file()
        data = pd.read_csv(self._path + file, encoding='ISO-8859-1', dtype=self.DTYPE)
        data = self._parse_campaign_fy(data)
        data['cont_dt'] = self._date_convert(data['cont_dt'])
        return data

    def _build_file(self):
        file = f"donors_fy{self._file_yr}-present.csv"
        return file

    def _date_convert(self, obj):
        if isinstance(obj, pd.Series):
            return pd.to_datetime(obj).reset_index(drop=True)
        return pd.to_datetime(obj)

    @staticmethod
    def _parse_campaign_fy(data):
        '''parses the campaign year into a new column called "fy"'''
        fy = data['campaign'].str[6:8]
        data['fy'] = fy

        # Build mapper to map for fiscal year
        fy_mapper = {fy: False for fy in data['fy'].drop_duplicates()}
        for fy, _ in fy_mapper.items():
            try:
                int(fy[0])
                fy_mapper[fy] = True
            except:
                continue

        mask = data['fy'].map(fy_mapper) # map the fys
        data = data.loc[mask].reset_index(drop=True)
        data = data.astype({'fy': 'int64'}) # convert to int

        return data


    # ------------ magic -------------------
    def __repr__(self):
        return f"Donors(path='{self._path}', file_yr='{self._file_yr}')"

    def __str__(self):
        return f"{self.data.columns}"

    def __len__(self):
        return len(self.data)
