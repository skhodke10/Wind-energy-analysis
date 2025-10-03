import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from datetime import timedelta


class SmartData:
    """Class for handling and visualization of energy data from smard.de
    TODO: further description and examples
    """

    def __init__(self) -> None:
        self.data = None
        self.__old_data = None

        return

    def import_data(self, filepath):

        self.data = pd.read_csv(
            filepath,
            sep=";",
            parse_dates=[0, 1],
            date_format="%d.%m.%Y %H:%M",
            decimal=",",
            thousands=".",
        )

        self.data.index = self.data["Datum von"]
        self.data.index.name = "Date"

        self.__first_date = self.data["Datum von"].iloc[0]
        self.__last_date = self.data["Datum bis"].iloc[-1]

        self.data.drop(columns=["Datum bis", "Datum von"], inplace=True)

        self.data.columns = [
            "_".join(name.split(" ")[0:-3]) for name in self.data.columns.values
        ]

        return

    def modify(self, condition_limit=0, replace_val=0, column=None):

        if column:
            condition = self.data.loc[:, column] < condition_limit
            self.data.loc[condition, column] = replace_val

        else:
            condition = self.data.loc[:, :] < condition_limit
            self.data[condition] = replace_val

        return True

    # def interpolate(self, freq_in_min=15, interpolation_method="linear"):

    #     if not isinstance(self.__old_data, pd.DataFrame):
    #         self.__old_data = self.data

    #     date_range = pd.date_range(
    #         start=self.__first_date,
    #         end=self.__last_date,
    #         freq=timedelta(minutes=freq_in_min),
    #     )

    #     df_15min = self.__old_data.reindex(date_range[:-1])

    #     timeindex = df_15min.index
    #     df_15min.index = timeindex.astype(int)

    #     df_15min = df_15min.interpolate(method=interpolation_method)

    #     df_15min.index = timeindex

    #     self.data = df_15min

    #     return True

    def interpolate(self, freq_in_min=15, interpolation_method="linear"):

        if not isinstance(self.__old_data, pd.DataFrame):
            self.__old_data = self.data

        # Create a new datetime index with the specified frequency
        date_range = pd.date_range(
            start=self.__first_date,
            end=self.__last_date,
            freq=timedelta(minutes=freq_in_min),
        )

        # Reindex the DataFrame to include the new date range
        df_15min = self.__old_data.reindex(date_range[:-1])

        # Save the original datetime index
        timeindex = df_15min.index

        # Convert datetime index to integer representation (nanoseconds since epoch)
        df_15min.index = timeindex.astype(np.int64)

        # Perform interpolation
        df_15min = df_15min.interpolate(method=interpolation_method)

        # Restore the datetime index
        df_15min.index = timeindex

        # Update the class's data attribute
        self.data = df_15min

        return True


    def plot(self, plottype="line", savename=None, ax=None, **kwargs):
        if not ax:
            ax = plt.gca()

        fig1 = plt.gcf()

        ax1 = self.data.plot(ax=ax, kind=plottype, legend=False, **kwargs)

        fig1.legend(loc="outside right upper")

        if savename:

            fig1.savefig(fname=savename)

        return ax

    def import_by_api(self, timestamp, filter, region="DE"):

        self.df

        return

    def import_smard_data(self, timeframe, list_energy=["PV", "Wind_onshore"]):

        for time in timeframe:

            for energy in list_energy:

                df = self.import_by_api(timestamp=time, filter=energy)

                # concatenate dataframes

    def call_project_step1(self):

        # import data and concatenate

        # visualize data

        return
