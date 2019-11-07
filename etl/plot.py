import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from . import filter, transform


class PlotFactory:
    def __init__(self, analysis):
        self.mapper = {
            'tier_analysis': TierAnalysis,
            'ticket_plots': TicketPlots,
            'donor_weekly': DonorWeekly,
            'mos_plots': ModeOfSalePlots
        }
        self.plotter = self.mapper[analysis]


class TierAnalysis:
    @ staticmethod
    def plot_tier_counts(tier_counts):
        tier_counts_form = tier_counts.pivot(
            index='donor_tier', columns='classification', values='count'
        ).fillna(0)

        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        tier_counts_form.plot(ax=ax, kind='bar', stacked=True)

        # titles
        ax.set_title("Donor Tier Funnel - Number of Donors - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Number of Donors', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()

    @staticmethod
    def plot_tier_revenue(tier_revenue):
        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="donor_tier", y="transaction_amount", data=tier_revenue)

        # titles
        ax.set_title("Revenue Generated per Tier - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Revenue Generated', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()


class TicketPlots:
    @staticmethod
    def returning_singles_plot(data, to_date, series=['Classics', 'Pops', 'Summer'],
                                fys=None):
        data = data.copy()

        data = filter.filter_by_series(data=data, series=series)
        data = filter.filter_non_subs(data=data)
        data = filter.filter_paid_only(data=data, column='paid_amt')
        data = filter.filter_before_date(data=data, col='perf_dt', to_date=to_date)

        if fys:
            data = filter.filter_fys(data=data, fys=fys)

        data = data[['summary_cust_id', 'perf_dt']].reset_index(drop=True)
        data = data.drop_duplicates().reset_index(drop=True)

        concerts_to_dt = transform.add_concert_number(data=data)
        attendances = concerts_to_dt.groupby('summary_cust_id').agg('count').reset_index()

        attendances = attendances.groupby('perf_number').agg({
            'summary_cust_id': 'count'
        }).reset_index()

        # If less than 10, fill out concerts with 0 attendance up to 10
        if len(attendances) < 10:
            for i in range(len(attendances)+1, 11):
                attendances = attendances.append(
                    pd.DataFrame({'perf_number': [i], 'summary_cust_id': [0]})
                )


        # Plot setup
        fig, ax = plt.subplots(figsize=(25,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="perf_number", y="summary_cust_id", data=attendances)

        # titles
        ax.set_title("Non Subscription Retention to Date", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Number of Performances', fontsize=20)
        ax.set_ylabel('Customers', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()


    @staticmethod
    def plot_singles_by_zone(data, series, to_date=None, fys=None):
        data = data.copy()

        data = filter.filter_by_series(data=data, series=series)

        data = filter.filter_non_subs(data=data)
        data = filter.filter_paid_only(data=data, column='paid_amt')

        if to_date:
            to_date = transform.date_convert(to_date)
            data = filter.filter_before_date(data=data, col='perf_dt', to_date=to_date)

        if fys:
            data = filter.filter_fys(data=data, fys=fys)

        data = data.groupby('price_zone').agg({'paid_amt': 'count'}).reset_index()
        data = data.loc[~data.price_zone.isin(['Price B', 'Price P'])]

        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="price_zone", y="paid_amt", data=data)

        # titles
        ax.set_title(f"Single Tickets Sold by Price Zone {series}", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Price Zone', fontsize=20)
        ax.set_ylabel('Total Single Tickets Sold to Date', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()


class DonorWeekly:
    @staticmethod
    def plot_all_campaigns(weekly_report_df):
        today = dt.datetime.today().strftime('%m-%d-%Y')

        for col in weekly_report_df.columns:
            register_matplotlib_converters()

            fig, ax = plt.subplots(figsize=(25,10))
            sns.set(style="ticks")
            sns.lineplot(x=weekly_report_df.index, y=col, data=weekly_report_df)
            ax.set_title(col, fontsize=30)

            # axes
            ax.tick_params(axis='both', labelsize=16)
            ax.set_xlabel('Week', fontsize=20)
            ax.set_ylabel('Revenue', fontsize=20)
            ax.set_xticks(weekly_report_df.index)
            ax.set_xticklabels(weekly_report_df.index.strftime('%m-%d-%Y'))

            plt.xticks(rotation=30)

            # Show plot
            plt.show()

            fig.savefig(f"plots/donor_weekly-{col}-{today}.pdf", bbox_inches='tight')

class ModeOfSalePlots:
    @staticmethod
    def pie_plot(data, category='ordered'):
        '''Plots a pie plot of the data grouped by mode of sale description (mos_desc)
        args:
            category:   either 'ordered' or 'paid' (representing tickets and revenue)
        '''
        data = data.copy()
        data = data.groupby('mos_desc').agg({category: 'sum'}).reset_index()
        data = data.loc[data['mos_desc'] != 'PS Subscription']

        labels = data['mos_desc']
        sizes = data[category]

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
