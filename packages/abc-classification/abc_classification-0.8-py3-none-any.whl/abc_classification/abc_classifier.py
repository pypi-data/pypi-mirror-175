"""Module for ABC classification in business analysis."""
import pandas as pd
import numpy as np


class ABCClassifier:
    """ABC classification class"""

    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Provided object is not pd.DataFrame')

        self.data = data

    def classify(self, abc_column: str, criterion: str) -> pd.DataFrame:
        """Make ABC classification for values from abc_column.
        Dataframe must be grouped by abc_column.

        Args:
            abc_column (str): column with values to classify.
            criterion (str): column with criterion for classification.

        Returns:
            abc_df (pd.DataFrame): classified dataframe.

        Raises:
            ValueError: if args are not str."""
        if not isinstance(abc_column, str):
            raise ValueError(f'Column name must be string not {type(abc_column)}')
        if not isinstance(criterion, str):
            raise ValueError(f'Column name must be string not {type(criterion)}')

        abc_df = self.data[[abc_column, criterion]].copy()
        abc_df.sort_values(by=criterion, inplace=True, ascending=False)
        total = self.data[criterion].sum()
        abc_df['percentage'] = abc_df[criterion] / total
        abc_df[f'cumulative_{criterion}'] = abc_df['percentage'].cumsum()
        conditions = [(abc_df[f'cumulative_{criterion}'] <= 0.7),
                      (abc_df[f'cumulative_{criterion}'] <= 0.9),
                      (abc_df[f'cumulative_{criterion}'] > 0.9)]
        values = ['A', 'B', 'C']
        abc_df['class'] = np.select(conditions, values)
        abc_df.drop(['percentage', f'cumulative_{criterion}'], axis=1, inplace=True)

        return abc_df

    def brief_abc(self, abc_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregates dataframe by class with summarized information.

        Args:
            abc_df (pd.DataFrame): DataFrame for brief information calculation.

        Returns:
            brief_abc_df (pd.DataFrame): Dataframe with summarized info.

        Raises:
            ValueError: if abc_df is not pd.DataFrame."""
        if not isinstance(abc_df, pd.DataFrame):
            raise ValueError('Passed object is not pd.DataFrame.')
        brief_abc_df = abc_df.groupby('class').sum().reset_index()
        return brief_abc_df
