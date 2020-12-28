#Version 12/27/20
import pandas as pd
import numpy as np
import colinfo

def ConvertFlagColToBoolean(df, col):
    """
    Convert a flag column from 1/blank format to Boolean

    Inputs: df [DataFrame] DataFrame containing flag (1/blank) column
            col [string] Flag column to convert to Boolean
    Return: df with modified, Boolean flag column

    JDL 12/22/20
    """

    df[col] = df[col].map(lambda x: False if pd.isnull(x) else True)
    return df

def ImportCSV(file, tblCI):
    """
    Import a CSV file and set column data types
    """
    df = pd.read_csv(file)
    df = colinfo.SetDataTypesFromColInfo(df, tblCI)
    return df
