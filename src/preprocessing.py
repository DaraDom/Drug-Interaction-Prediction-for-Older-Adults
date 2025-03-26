import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    def __init__(self, filepaths: list, join_on_column_names=[]) -> None:
        if len(filepaths) > 1:
            for filepath in filepaths:
                data = pd.read_excel(filepath)
            self.data = ""
        else:
            self.data = pd.read_excel(filepaths[0])

        self.label_encoder = LabelEncoder()

    def drop_columns(self, column_names: list) -> None:
        self.data.drop(columns=column_names)

    def explode_column(self, column_name: str, delimiter: str) -> None:
        self.data[column_name] = self.data[column_name].str.split(delimiter)
        self.data = self.data.explode(column_name)
    
    def encode_column(self, column_name: str) -> None:
        self.data[column_name] = self.label_encoder.fit_transform(self.data[column_name])
    
    def ensure_numeric_column(self, column_name: str, decimal=False) -> None:
        self.data[column_name] = self.data[column_name].str.replace(r'\D+', '', regex=True)
        if decimal:
            self.data[column_name] = self.data[column_name].astype(float)
        else:
            self.data[column_name] = self.data[column_name].astype(int)
        self.data[column_name] = pd.to_numeric(self.data[column_name], errors='coerce')
    
    def get_dummies(self, column_names: list) -> None:
        self.data = pd.get_dummies(self.data, columns=column_names, prefix='', prefix_sep='')

    def convert_nulls(self, column_name: str, nulls=["Not Specified"], output="NaN") -> None:
        for null in nulls:
            self.data[column_name] = self.data[column_name].replace(null, output)

    def drop_all_nulls(self) -> None:
        self.data.dropna(inplace=True)

    def get_standardised_train_test_split(self, x_columns: list, y: str, test_size: float, random_state: int) -> tuple:
        x_train, x_test, y_train, y_test = train_test_split(self.data[x_columns], self.data[y], test_size=test_size, random_state=random_state)
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        return (x_train, x_test, y_train, y_test)

    def get_value_counts(self, column_name: str) -> pd.DataFrame:
        return self.data[column_name].value_counts()

    def get_dataframe(self) -> pd.DataFrame:
        return self.data