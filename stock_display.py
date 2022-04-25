"""
Track the stock performance on the stock market and store price development.
Trigger notifications to the user in case of high market volatility.
"""

import argparse
import time
import os
import pandas as pd
# from sqlalchemy import true

from portfolio import Portfolio


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='inputFile', action='store')
    parser.add_argument('-t', dest='time',      action='store')
    args = parser.parse_args()

    timeIntervall = int(args.time)
    dbName = args.inputFile.replace('.csv', '')

    path   = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(path, dbName + '.db')
    inputFilePath = os.path.join(path, args.inputFile)

    if os.path.isfile(inputFilePath):
        df = pd.read_csv(inputFilePath, sep=';')

        portfolio = Portfolio(df, dbName, dbPath)

        while True:
            # portfolio.display_stocks()
            time.sleep(timeIntervall)
            try:
                portfolio.refresh_stocks()
                portfolio.write_database()
            except:
                print("Error... keep going!")
                time.sleep(5)
                portfolio.refresh_stocks()


if __name__ == "__main__":
    main()
