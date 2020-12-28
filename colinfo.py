#Version 12/27/20
import pandas as pd
import numpy as np
import pdutil

class tblcolinfo():
    def __init__(self):
        self.name = 'name'
        self.desc = 'description'
        self.units = 'units'
        self.dtype = 'type'
        self.dict_types = {}
        self.dict_isflagcol = {}
        self.file = 'colinfo.csv'
        self.dfcolinfo = pd.DataFrame

def BuildTypeAndFlagDicts(tblCI):
    """
    Build dictionaries of data types and flag status for columns

    Inputs: df [DataFrame] DataFrame for which type dictionary is needed
            tblCI [colinfo Class Instance] colinfo for the project

    Return: tblCI Class instance with type and isflagcol dictionaries populated

    JDL 12/22/20
    """

    #Re-initialize dictionaries
    tblCI.dict_types, tblCI.dict_isflagcol = {}, {}

    #Loop through colinfo rows (index is column names in project)
    for col, dtype in zip(tblCI.dfcolinfo.index, tblCI.dfcolinfo[tblCI.dtype]):
        if not pd.isnull(dtype):

            #Add the column's dtype and flag status to dictionaries
            tblCI.dict_types = DictAddColInfoType(col, dtype, tblCI)
            tblCI.dict_isflagcol[col] = False
            if dtype == 'bool_flag': tblCI.dict_isflagcol[col] = True
    return tblCI

def SetDataTypesFromColInfo(df, tblCI):
    """
    Use colinfo dictionaries to set newly-imported (CSV) DataFrame column types and Boolean Flag columns
    """
    for col in df.columns:

        #If col is a flag column (1/blank), convert to Boolean for memory and feather file size efficiency
        if (col in tblCI.dict_isflagcol):
            if (tblCI.dict_isflagcol[col]): df = pdutil.ConvertFlagColToBoolean(df, col)

        #If the column is in the data type dictionary, set its type using either .to_datetime() or .astype()
        if col in tblCI.dict_types:
            if tblCI.dict_types[col] == 'dt':
                df[col] = pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype(tblCI.dict_types[col])
    return df

def DictAddColInfoType(col, dtype, tblCI):
    """
    Convert colinfo type (string) to dictionary item

    Inputs: col [string] column name to add to dictionary of column dict_types
            dtype [string] string format data type for col (read from colinfo.csv)
            dict_types [dictionary] dictionary of column types

    Return: dict_types with new entry for column

    JDL 12/22/20
    """

    if dtype == 'dt':
        tblCI.dict_types[col] = 'dt'
    elif dtype  == 'bool_flag':
            tblCI.dict_types[col] = 'bool'
    else:
        tblCI.dict_types[col] = dtype
    return tblCI.dict_types
