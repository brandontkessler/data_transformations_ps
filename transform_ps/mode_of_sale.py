import pandas as pd
import matplotlib.pyplot as plt

class ModeOfSale:
    '''Class for working with mode of sale data from the mode of sale report
    in tessitura

    args:
        qtr: options are 1, 2, 3, or 4

    '''

    def __init__(self, qtr, fy, path='../../data/mode_of_sale/'):
        self._qtr = self._check_qtr(qtr)
        self._fy = self._check_fy(fy)
        self._path = path
        self._data = self._build_dataset()

    # --------------------- constructor methods ------------------
    def _check_qtr(self, qtr):
        if qtr not in (1, 2, 3, 4):
            raise TypeError(f'Argument qtr={qtr} must be an integer of 1, 2, 3, or 4')
        return qtr

    def _check_fy(self, fy):
        if not isinstance(fy, int) or len(str(fy)) != 2:
            raise TypeError(f'Argument fy={fy} must be an integer of length 2, ie. 19')
        return fy

    def _build_dataset(self):
        data = pd.read_csv(f'{self._path}q{self._qtr}_{self._fy}.csv')
        data['season'] = [season.split(' ')[2] for season in data['season']]
        data['ordered'] = data['ps_num_ord'] + data['cs_num_ord']
        data['paid'] = data['ps_tot_paid_amt'] + data['cs_tot_paid_amt']
        data = self._fix_mos_desc(data)
        return data

    def _fix_mos_desc(self, data):
        mapper = {
            'OC Box Office': 'OC Box Office',
            'OC Donor Relations': 'OC Box Office',
            'OC House': 'OC Box Office',
            'OC Mobile': 'OC Box Office'
        }

        data['mos_desc'] = data['mos_desc'].replace(mapper)
        data['mos_desc'] = data['mos_desc'].replace({'OC': 'SCFTA'}, regex=True)
        return data

    # ---------------------- filters ------------------------------
    def filter_seasons(self, seasons=['Classics', 'Pops', 'Family', 'Summer', 'Specials']):
        '''Filters dataset to only keep provided seasons'''
        self._data = self._data.loc[self._data['season'].isin(seasons)]
        return


    # ---------------------- transformations -----------------------
    def pie_plot(self, category='ordered'):
        '''Plots a pie plot of the data grouped by mode of sale description (mos_desc)

        args:
            category:   either 'ordered' or 'paid' (representing tickets and revenue)
        '''
        data = self._data.copy()
        data = data.groupby('mos_desc').agg({'ordered': 'sum'}).reset_index()
        data = data.loc[data['mos_desc'] != 'PS Subscription']

        labels = data.mos_desc
        sizes = data.ordered

        fig, ax = plt.subplots(figsize=(11.74,10))

        ax.pie(sizes, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 20})

        # titles
        ax.set_title("Channels by Tix Sold", fontsize=30)

        # axes
        ax.legend(labels, fontsize=16, loc='lower left')
        ax.axis('equal')

        # Show plot
        plt.show()

    # --------------------- magic methods ------------------
    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"ModeOfSale(quarter='{self._qtr}Q{self._fy}')"
