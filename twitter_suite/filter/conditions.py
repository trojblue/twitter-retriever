import os
import pandas as pd
from abc import ABC, abstractmethod
from typing import Callable, Dict


class Condition(ABC):
    """
    Abstract base class for conditions used in file moving operations.
    Each subclass must implement the `check` method.
    """

    @abstractmethod
    def check(self, df: pd.DataFrame) -> pd.Series:
        """
        Check condition for each row of the DataFrame.

        Parameters:
        df (pd.DataFrame): DataFrame containing the data for the check.

        Returns:
        pd.Series: A Boolean Series indicating the rows where the condition holds.
        """
        pass


class BaseCondition(Condition):
    """
    Base class for conditions. It implements the `infer_dtype` method used for data type inference.
    """

    def __init__(self, condition: Callable[[pd.Series], pd.Series], dtype: str = None):
        """
        Initialize BaseCondition with a condition function and optionally a dtype.

        Parameters:
        condition (Callable[[pd.Series], pd.Series]): Function to apply to a pandas Series to get a Boolean Series.
        dtype (str, optional): Desired data type to convert the Series into before applying the condition. Default to None.
        """
        self.condition = condition
        self.dtype = dtype

    def infer_dtype(self, df: pd.DataFrame, column: str):
        """
        Infer data type for a given DataFrame column.

        Parameters:
        df (pd.DataFrame): DataFrame containing the column for which to infer data type.
        column (str): Name of the column for which to infer data type.

        Returns:
        pd.Series: Column of the DataFrame with the inferred data type.
        """
        if self.dtype is not None:
            df[column] = df[column].astype(self.dtype)
        else:
            df = df.infer_objects()
        return df[column]

    @abstractmethod
    def check(self, df: pd.DataFrame) -> pd.Series:
        pass


class CsvCondition(BaseCondition):
    """
    Condition for checking a column of a CSV file.
    """

    def __init__(self, column: str, condition: Callable[[pd.Series], pd.Series], dtype: str = None):
        """
        Initialize CsvCondition with a column name, a condition function and optionally a dtype.

        Parameters:
        column (str): Name of the column to which to apply the condition.
        """
        super().__init__(condition, dtype)
        self.column = column

    def check(self, df: pd.DataFrame) -> pd.Series:
        """
        Check condition for the specified column of the DataFrame.
        """
        column = self.infer_dtype(df, self.column)
        return self.condition(column)


class MTimeCondition(BaseCondition):
    """
    Condition for checking the last modification time of files.
    """
    def __init__(self, root_dir: str, condition: Callable[[pd.Series], pd.Series], dtype: str = None):
        """
        Initialize MTimeCondition with a root directory, a condition function and optionally a dtype.

        Parameters:
        root_dir (str): Root directory containing the files for the check.
        """
        super().__init__(condition, dtype)
        self.root_dir = root_dir

    def check(self, df: pd.DataFrame) -> pd.Series:
        """
        Check condition for the specified column of the DataFrame.
        """
        if "mtime" not in df.columns:
            df["mtime"] = df["filename"].apply(lambda x: os.path.getmtime(os.path.join(self.root_dir, x)))
        mtime_series = self.infer_dtype(df, "mtime")
        return self.condition(mtime_series)
