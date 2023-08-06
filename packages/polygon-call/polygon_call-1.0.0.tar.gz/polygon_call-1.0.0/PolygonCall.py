from polygon import RESTClient
from sqlalchemy import create_engine
from sqlalchemy import text
import time
import datetime
from math import sqrt
from math import isnan


class PolygonCall:
    def __init__(self, currency_pairs):
        self.currency_pairs = currency_pairs

    # Function slightly modified from polygon sample code to format the date string
    def ts_to_datetime(self, ts) -> str:
        return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

    # Function which clears the raw data tables once we have aggregated the data in a 6 minute interval
    def reset_raw_data_tables(self, engine):
        with engine.begin() as conn:
            for curr in self.currency_pairs:
                conn.execute(text("DROP TABLE " + curr[0] + curr[1] + "_raw;"))
                conn.execute(text(
                    "CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))

    # This creates a table for storing the raw, unaggregated price data for each currency pair in the SQLite database
    def initialize_raw_data_tables(self, engine):
        with engine.begin() as conn:
            for curr in self.currency_pairs:
                conn.execute(text(
                    "CREATE TABLE " + curr[0] + curr[1] + "_raw(ticktime text, fxrate  numeric, inserttime text);"))

    # This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database
    def initialize_aggregated_tables(self, engine):
        with engine.begin() as conn:
            for curr in self.currency_pairs:
                # delete pre-existed tables
                conn.execute(text("DROP TABLE " + curr[0] + curr[1] + "_agg;"))
                conn.execute(text("CREATE TABLE " + curr[0] + curr[
                    1] + "_agg(inserttime text, avgfxrate  numeric, stdfxrate numeric);"))

    # This function is called every 6 minutes to aggregate the data, store it in the aggregate table,
    # and then delete the raw data
    def aggregate_raw_data_tables(self, engine):
        with engine.begin() as conn:
            for curr in self.currency_pairs:
                result = conn.execute(text(
                    "SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM " + curr[0] + curr[1] + "_raw;"))
                for row in result:
                    avg_price = row.avg_price
                    tot_count = row.tot_count
                std_res = conn.execute(text(
                    "SELECT SUM((fxrate - " + str(avg_price) + ")*(fxrate - " + str(avg_price) + "))/(" + str(
                        tot_count) + "-1) as std_price FROM " + curr[0] + curr[1] + "_raw;"))
                for row in std_res:
                    std_price = sqrt(row.std_price)
                date_res = conn.execute(text("SELECT MAX(ticktime) as last_date FROM " + curr[0] + curr[1] + "_raw;"))
                for row in date_res:
                    last_date = row.last_date
                conn.execute(text("INSERT INTO " + curr[0] + curr[
                    1] + "_agg (inserttime, avgfxrate, stdfxrate) VALUES (:inserttime, :avgfxrate, :stdfxrate);"),
                             [{"inserttime": last_date, "avgfxrate": avg_price, "stdfxrate": std_price}])

                # This calculates and stores the return values
                exec("curr[2].append(" + curr[0] + curr[1] + "_return(last_date,avg_price))")
                # exec("print(\"The return for "+curr[0]+curr[1]+" is:"+str(curr[2][-1].hist_return)+" \")")

                if len(curr[2]) > 5:
                    try:
                        avg_pop_value = curr[2][-6].hist_return
                    except:
                        avg_pop_value = 0
                    if isnan(avg_pop_value) == True:
                        avg_pop_value = 0
                else:
                    avg_pop_value = 0
                # Calculate the average return value and print it/store it
                curr_avg = curr[2][-1].get_avg(avg_pop_value)
                # exec("print(\"The average return for "+curr[0]+curr[1]+" is:"+str(curr_avg)+" \")")

                # Now that we have the average return, loop through the last 5 rows in the list to start compiling the
                # data needed to calculate the standard deviation
                for row in curr[2][-5:]:
                    row.add_to_running_squared_sum(curr_avg)

                # Calculate the standard dev using the avg
                curr_std = curr[2][-1].get_std()
                # exec("print(\"The standard deviation of the return for "+curr[0]+curr[1]+" is:"+str(curr_std)+" \")")

                # Calculate the average standard dev
                if len(curr[2]) > 5:
                    try:
                        pop_value = curr[2][-6].std_return
                    except:
                        pop_value = 0
                else:
                    pop_value = 0
                curr_avg_std = curr[2][-1].get_avg_std(pop_value)
                # exec("print(\"The average standard deviation of the return for "+curr[0]+curr[1]+" is:"+str(curr_avg_std)+" \")")

                # -------------------Investment Strategy-----------------------------------------------
                try:
                    return_value = curr[2][-1].hist_return
                except:
                    return_value = 0
                if isnan(return_value) == True:
                    return_value = 0

                try:
                    return_value_1 = curr[2][-2].hist_return
                except:
                    return_value_1 = 0
                if isnan(return_value_1) == True:
                    return_value_1 = 0

                try:
                    return_value_2 = curr[2][-3].hist_return
                except:
                    return_value_2 = 0
                if isnan(return_value_2) == True:
                    return_value_2 = 0

                try:
                    upp_band = curr[2][-1].avg_return + (1.5 * curr[2][-1].std_return)
                    if return_value >= upp_band and curr[
                        3].Prev_Action_was_Buy == True and return_value != 0:  # (return_value > 0) and (return_value_1 > 0) and
                        curr[3].sell_curr(avg_price)
                except:
                    pass

                try:
                    loww_band = curr[2][-1].avg_return - (1.5 * curr[2][-1].std_return)
                    if return_value <= loww_band and curr[
                        3].Prev_Action_was_Buy == False and return_value != 0:  # and  (return_value < 0) and (return_value_1 < 0)
                        curr[3].buy_curr(avg_price)
                except:
                    pass

    # This main function repeatedly calls the polygon api every 1 seconds for 24 hours
    # and stores the results.
    def call(self):
        print("?")
        # The api key given by the professor
        key = "JINOK3dmG_iko6hkXlgKXIAqoLtDVofg"

        # Number of list iterations - each one should last about 1 second
        count = 0
        agg_count = 0

        # Create an engine to connect to the database; setting echo to false should stop it from logging in std.out
        engine = create_engine("sqlite+pysqlite:///sqlite/final.db", echo=False, future=True)

        # Create the needed tables in the database
        # call reset data table to delete pre-existed table
        self.reset_raw_data_tables(engine, self.currency_pairs)
        self.initialize_aggregated_tables(engine, self.currency_pairs)

        # Open a RESTClient for making the api calls
        with RESTClient(key) as client:
            # Loop that runs until the total duration of the program hits 24 hours.
            while count < 86400: # 86400 seconds = 24 hours
                # Make a check to see if 6 minutes has been reached or not
                if agg_count == 360:
                    # Aggregate the data and clear the raw data tables
                    self.aggregate_raw_data_tables(engine, self.currency_pairs)
                    self.reset_raw_data_tables(engine, self.currency_pairs)
                    agg_count = 0

                # Only call the api every 1 second, so wait here for 0.75 seconds, because the
                # code takes about .15 seconds to run
                time.sleep(0.75)
