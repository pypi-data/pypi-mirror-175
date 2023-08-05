from abc import abstractmethod
from os import name
from typing import Dict, List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import Field, validator
from pydantic.class_validators import root_validator
from pydantic.types import conlist, conset

from bofire.domain.desirability_functions import (
    DesirabilityFunction,
    MaxIdentityDesirabilityFunction,
    NoDesirabilityFunction,
)
from bofire.domain.util import KeyModel, is_numeric, name2key


class Feature(KeyModel):
    """The base class for all features."""

    def __lt__(self, other) -> bool:
        """
        Method to compare two models to get them in the desired order.
        Return True if other is larger than self, else False. (see FEATURE_ORDER)

        Args:
            other: The other class to compare to self

        Returns:
            bool: True if the other class is larger than self, else False
        """
        order_self = FEATURE_ORDER[type(self)]
        order_other = FEATURE_ORDER[type(other)]
        if order_self == order_other:
            return self.key < other.key
        else:
            return order_self < order_other

    def to_config(self) -> Dict:
        """Generate serialized version of the feature.

        Returns:
            Dict: Serialized version of the feature as dictionary.
        """
        return {
            "type": self.__class__.__name__,
            **self.dict(),
        }

    @staticmethod
    def from_config(config: Dict) -> "DesirabilityFunction":
        """Generate desirability function out of serialized version.

        Args:
            config (Dict): Serialized version of a desirability function

        Returns:
            DesirabilityFunction: Instaniated desirability function of the type specified in the `config`.
        """
        input_mapper = {
            "ContinuousInputFeature": ContinuousInputFeature,
            "DiscreteInputFeature": DiscreteInputFeature,
            "CategoricalInputFeature": CategoricalInputFeature,
            "CategoricalDescriptorInputFeature": CategoricalDescriptorInputFeature,
            "ContinuousDescriptorInputFeature": ContinuousDescriptorInputFeature,
        }
        output_mapper = {
            "ContinuousOutputFeature_woDesFunc": ContinuousOutputFeature_woDesFunc,
            "ContinuousOutputFeature": ContinuousOutputFeature,
        }
        if config["type"] in input_mapper.keys():
            return input_mapper[config["type"]](**config)
        else:
            d = DesirabilityFunction.from_config(config=config["desirability_function"])
            return output_mapper[config["type"]](
                key=config["key"], desirability_function=d
            )


class InputFeature(Feature):
    """Base class for all input features."""

    @abstractmethod
    def is_fixed() -> bool:
        """Indicates if a variable is set to a fixed value.

        Returns:
            bool: True if fixed, els False.
        """
        pass

    @abstractmethod
    def fixed_value() -> Union[None, str, float]:
        """Method to return the fixed value in case of a fixed feature.

        Returns:
            Union[None,str,float]: None in case the feature is not fixed, else the fixed value.
        """
        pass

    @abstractmethod
    def validate_experimental(
        self, values: pd.Series, strict: bool = False
    ) -> pd.Series:
        """Abstract method to validate the experimental dataFrame

        Args:
            values (pd.Series): A dataFrame with experiments
            strict (bool, optional): Boolean to distinguish if the occurence of fixed features in the dataset should be considered or not. Defaults to False.

        Returns:
            pd.Series: The passed dataFrame with experiments
        """
        pass

    @abstractmethod
    def validate_candidental(self, values: pd.Series) -> pd.Series:
        """Abstract method to validate the suggested candidates

        Args:
            values (pd.Series): A dataFrame with candidates

        Returns:
            pd.Series: The passed dataFrame with candidates
        """
        pass

    @abstractmethod
    def sample(self, n: int) -> pd.Series:
        """Sample a series of allowed values.

        Args:
            n (int): Number of samples

        Returns:
            pd.Series: Sampled values.
        """
        pass


class OutputFeature(Feature):
    """Base class for all output features.

    Attributes:
        desirability_function (Desirability_function, optional): Desirability function of
            the feature indicating in which direction it should be optimzed. Defaults to `MaxIdentityDesirabilityFunction`.
    """

    desirability_function: Optional[DesirabilityFunction] = Field(
        default_factory=lambda: MaxIdentityDesirabilityFunction(w=1.0)
    )

    def to_config(self) -> Dict:
        """Generate serialized version of the feature.

        Returns:
            Dict: Serialized version of the feature as dictionary.
        """
        return {
            "type": self.__class__.__name__,
            "key": self.key,
            "desirability_function": self.desirability_function.to_config(),
        }

    def plot(
        self,
        lower: float,
        upper: float,
        df_data: Optional[pd.DataFrame] = None,
        plot_details: bool = True,
        line_options: Optional[Dict] = None,
        scatter_options: Optional[Dict] = None,
        label_options: Optional[Dict] = None,
        title_options: Optional[Dict] = None,
    ):
        """Plot the assigned reward function.

        Args:
            lower (float): lower bound for the plot
            upper (float): upper bound for the plot
            df_data (Optional[pd.DataFrame], optional): If provided, scatter also the historical data in the plot. Defaults to None.
        """
        line_options = line_options or {}
        scatter_options = scatter_options or {}
        label_options = label_options or {}
        title_options = title_options or {}

        line_options["color"] = line_options.get("color", "black")
        scatter_options["color"] = scatter_options.get("color", "red")

        x = np.linspace(lower, upper, 5000)
        reward = self.desirability_function.__call__(x)
        fig, ax = plt.subplots()
        ax.plot(x, reward, **line_options)
        # TODO: validate dataframe
        if df_data is not None:
            x_data = df_data.loc[df_data[self.key].notna(), self.key].values
            ax.scatter(
                x_data,
                self.desirability_function.__call__(x_data),
                **scatter_options,
            )
        ax.set_title("Desirability %s" % self.key, **title_options)
        ax.set_ylabel("Desirability", **label_options)
        ax.set_xlabel(self.key, **label_options)
        if plot_details:
            ax = self.desirability_function.plot_details(ax=ax)
        return fig, ax

    def __str__(self) -> str:
        return self.desirability_function.__class__.__name__


class NumericalInputFeature(InputFeature):
    """Abstracht base class for all numerical (ordinal) input features."""

    def is_fixed(self):
        """Method to check if the feature is fixed

        Returns:
            Boolean: True when the feature is fixed, false otherwise.
        """
        return self.lower_bound == self.upper_bound

    def fixed_value(self):
        """Method to get the value to which the feature is fixed

        Returns:
            Float: Return the feature value or None if the feature is not fixed.
        """
        if self.is_fixed():
            return self.lower_bound
        else:
            return None

    def validate_experimental(self, values: pd.Series, strict=False) -> pd.Series:
        """Method to validate the experimental dataFrame

        Args:
            values (pd.Series): A dataFrame with experiments
            strict (bool, optional): Boolean to distinguish if the occurence of fixed features in the dataset should be considered or not. Defaults to False.

        Raises:
            ValueError: when a value is not numerical
            ValueError: when there is no variation in a feature provided by the experimental data

        Returns:
            pd.Series: A dataFrame with experiments
        """
        if not is_numeric(values):
            raise ValueError(
                f"not all values of input feature `{self.key}` are numerical"
            )
        if strict:
            lower, upper = self.get_real_feature_bounds(values)
            if lower == upper:
                raise ValueError(
                    f"No variation present or planned for feature {self.key}. Remove it."
                )
        return values

    def validate_candidental(self, values: pd.Series) -> pd.Series:
        """Validate the suggested candidates for the feature.

        Args:
            values (pd.Series): suggested candidates for the feature

        Raises:
            ValueError: Error is raised when one of the values is not numerical.

        Returns:
            pd.Series: the original provided candidates
        """
        if not is_numeric(values):
            raise ValueError(
                f"not all values of input feature `{self.key}` are numerical"
            )
        return values

    def get_real_feature_bounds(self, values: pd.Series):
        """Method to extract the feature boundaries from the provided experimental data

        Args:
            values (pd.Series): Experimental data

        Returns:
            (float, float): Returns lower and upper bound based on the passed data
        """
        lower = min(self.lower_bound, values.min())
        upper = max(self.upper_bound, values.max())
        return lower, upper


class ContinuousInputFeature(NumericalInputFeature):
    """Base class for all continuous input features.

    Attributes:
        lower_bound (float): Lower bound of the feature in the optimization.
        upper_bound (float): Upper bound of the feature in the optimization.
    """

    lower_bound: float
    upper_bound: float

    @root_validator(pre=False)
    def validate_lower_upper(cls, values):
        """Validates that the lower bound is lower than the upper bound

        Args:
            values (Dict): Dictionary with attributes key, lower and upper bound

        Raises:
            ValueError: when the lower bound is higher than the upper bound

        Returns:
            Dict: The attributes as dictionary
        """
        if values["lower_bound"] > values["upper_bound"]:
            raise ValueError(
                f'lower bound must be <= upper bound, got {values["lower_bound"]} > {values["upper_bound"]}'
            )
        return values

    def validate_candidental(self, values: pd.Series) -> pd.Series:
        """Method to validate the suggested candidates

        Args:
            values (pd.Series): A dataFrame with candidates

        Raises:
            ValueError: when non numerical values are passed
            ValueError: when values are larger than the upper bound of the feature
            ValueError: when values are lower than the lower bound of the feature

        Returns:
            pd.Series: The passed dataFrame with candidates
        """
        noise = 10e-8
        super().validate_candidental(values)
        if (values < self.lower_bound - noise).any():
            raise ValueError(
                f"not all values of input feature `{self.key}`are larger than lower bound `{self.lower_bound}` "
            )
        if (values > self.upper_bound + noise).any():
            raise ValueError(
                f"not all values of input feature `{self.key}`are smaller than upper bound `{self.upper_bound}` "
            )
        return values

    def sample(self, n: int) -> pd.Series:
        """Draw random samples from the feature.

        Args:
            n (int): number of samples.

        Returns:
            pd.Series: drawn samples.
        """
        return pd.Series(
            name=self.key,
            data=np.random.uniform(self.lower_bound, self.upper_bound, n),
        )

    def __str__(self) -> str:
        """Method to return a string of lower and upper bound

        Returns:
            str: String of a list with lower and upper bound
        """
        return f"[{self.lower_bound},{self.upper_bound}]"


class DiscreteInputFeature(NumericalInputFeature):
    """Feature with discretized ordinal values allowed in the optimization.

    Attributes:
        key(str): key of the feature.
        values(List[float]): the discretized allowed values during the optimization.
    """

    values: conlist(item_type=float, min_items=1)

    @validator("values")
    def validate_values_unique(cls, values):
        """Validates that provided values are unique.

        Args:
            values (List[float]): List of values

        Raises:
            ValueError: when values are non-unique.

        Returns:
            List[values]: Sorted list of values
        """
        if len(values) != len(set(values)):
            raise ValueError("Discrete values must be unique")
        return sorted(values)

    @property
    def lower_bound(self) -> float:
        """Lower bound of the set of allowed values"""
        return min(self.values)

    @property
    def upper_bound(self) -> float:
        """Upper bound of the set of allowed values"""
        return max(self.values)

    def validate_candidental(self, values: pd.Series) -> pd.Series:
        """Method to validate the provided candidates.

        Args:
            values (pd.Series): suggested candidates for the feature

        Raises:
            ValueError: Raises error when one of the provided values is not contained in the list of allowed values.

        Returns:
            pd.Series: _uggested candidates for the feature
        """
        super().validate_candidental(values)
        if not np.isin(values.values, np.array(self.values)).all():
            raise ValueError(
                f"Not allowed values in candidates for feature {self.key}."
            )
        return values

    def sample(self, n: int) -> pd.Series:
        """Draw random samples from the feature.

        Args:
            n (int): number of samples.

        Returns:
            pd.Series: drawn samples.
        """
        return pd.Series(name=self.key, data=np.random.choice(self.values, n))


# TODO: write a Descriptor base class from which both Categorical and Continuous Descriptor are inheriting
class ContinuousDescriptorInputFeature(ContinuousInputFeature):
    """Class for continuous input features with descriptors

    Attributes:
        lower_bound (float): Lower bound of the feature in the optimization.
        upper_bound (float): Upper bound of the feature in the optimization.
        descriptors (List[str]): Names of the descriptors.
        values (List[float]): Values of the descriptors.
    """

    descriptors: conlist(item_type=str, min_items=1)
    values: conlist(item_type=float, min_items=1)

    @validator("descriptors")
    def descriptors_to_keys(cls, descriptors):
        """validates the descriptor names and transforms it to valid keys

        Args:
            descriptors (List[str]): List of descriptor names

        Returns:
            List[str]: List of valid keys
        """
        return [name2key(name) for name in descriptors]

    @root_validator(pre=False)
    def validate_list_lengths(cls, values):
        """compares the length of the defined descriptors list with the provided values

        Args:
            values (Dict): Dictionary with all attribues

        Raises:
            ValueError: when the number of descriptors does not math the number of provided values

        Returns:
            Dict: Dict with the attributes
        """
        if len(values["descriptors"]) != len(values["values"]):
            raise ValueError(
                'must provide same number of descriptors and values, got {len(values["descriptors"])} != {len(values["values"])}'
            )
        return values

    def to_df(self) -> pd.DataFrame:
        """tabular overview of the feature as DataFrame

        Returns:
            pd.DataFrame: tabular overview of the feature as DataFrame
        """
        return pd.DataFrame(
            data=[self.values], index=[self.key], columns=self.descriptors
        )


class CategoricalInputFeature(InputFeature):
    """Base class for all categorical input features.

    Attributes:
        categories (List[str]): Names of the categories.
        allowed (List[bool]): List of bools indicating if a category is allowed within the optimization.
    """

    categories: conlist(item_type=str, min_items=2)
    allowed: Optional[conlist(item_type=bool, min_items=2)]

    @validator("categories")
    def validate_categories_unique(cls, categories):
        """validates that categories have unique names

        Args:
            categories (List[str]): List of category names

        Raises:
            ValueError: when categories have non-unique names

        Returns:
            List[str]: List of the categories
        """
        categories = [name2key(name) for name in categories]
        if len(categories) != len(set(categories)):
            raise ValueError("categories must be unique")
        return categories

    @root_validator(pre=False)
    def init_allowed(cls, values):
        """validates the list of allowed/not allowed categories

        Args:
            values (Dict): Dictionary with attributes

        Raises:
            ValueError: when the number of allowences does not fit to the number of categories
            ValueError: when no category is allowed

        Returns:
            Dict: Dictionary with attributes
        """
        if "categories" not in values or values["categories"] is None:
            return values
        if "allowed" not in values or values["allowed"] is None:
            values["allowed"] = [True for _ in range(len(values["categories"]))]
        if len(values["allowed"]) != len(values["categories"]):
            raise ValueError("allowed must have same length as categories")
        if sum(values["allowed"]) == 0:
            raise ValueError("no category is allowed")
        return values

    def is_fixed(self):
        """Returns True if there is only one allowed category.

        Returns:
            [bool]: True if there is only one allowed category
        """
        return sum(self.allowed) == 1

    def fixed_value(self):
        """Returns the categories to which the feature is fixed, None if the feature is not fixed

        Returns:
            List[str]: List of categories or None
        """
        if self.is_fixed():
            return self.get_allowed_categories()[0]
        else:
            return None

    def get_allowed_categories(self):
        """Returns the allowed categories.

        Returns:
            list of str: The allowed categories
        """
        return [c for c, a in zip(self.categories, self.allowed) if a]

    def validate_experimental(
        self, values: pd.Series, strict: bool = False
    ) -> pd.Series:
        """Method to validate the experimental dataFrame

        Args:
            values (pd.Series): A dataFrame with experiments
            strict (bool, optional): Boolean to distinguish if the occurence of fixed features in the dataset should be considered or not. Defaults to False.

        Raises:
            ValueError: when an entry is not in the list of allowed categories
            ValueError: when there is no variation in a feature provided by the experimental data

        Returns:
            pd.Series: A dataFrame with experiments
        """
        if sum(values.isin(self.categories)) != len(values):
            raise ValueError(
                f"invalid values for `{self.key}`, allowed are: `{self.categories}`"
            )
        if strict:
            possible_categories = self.get_possible_categories(values)
            if len(possible_categories) != len(self.categories):
                raise ValueError(
                    f"Categories {list(set(self.categories)-set(possible_categories))} of feature {self.key} not used. Remove them."
                )
        return values

    def validate_candidental(self, values: pd.Series) -> pd.Series:
        """Method to validate the suggested candidates

        Args:
            values (pd.Series): A dataFrame with candidates

        Raises:
            ValueError: when not all values for a feature are one of the allowed categories

        Returns:
            pd.Series: The passed dataFrame with candidates
        """
        if sum(values.isin(self.get_allowed_categories())) != len(values):
            raise ValueError(
                f"not all values of input feature `{self.key}` are a valid allowed category from {self.get_allowed_categories()}"
            )
        return values

    def get_forbidden_categories(self):
        """Returns the non-allowed categories

        Returns:
            List[str]: List of the non-allowed categories
        """
        return list(set(self.categories) - set(self.get_allowed_categories()))

    def get_possible_categories(self, values: pd.Series) -> list:
        """Return the superset of categories that have been used in the experimental dataset and
        that can be used in the optimization

        Args:
            values (pd.Series): Series with the values for this feature

        Returns:
            list: list of possible categories
        """
        return sorted(
            list(set(list(set(values.tolist())) + self.get_allowed_categories()))
        )

    def sample(self, n: int) -> pd.Series:
        """Draw random samples from the feature.

        Args:
            n (int): number of samples.

        Returns:
            pd.Series: drawn samples.
        """
        return pd.Series(
            name=self.key, data=np.random.choice(self.get_allowed_categories(), n)
        )

    def __str__(self) -> str:
        """Returns the number of categories as str

        Returns:
            str: Number of categories
        """
        return f"{len(self.categories)} categories"


class CategoricalDescriptorInputFeature(CategoricalInputFeature):
    """Class for categorical input features with descriptors

    Attributes:
        categories (List[str]): Names of the categories.
        allowed (List[bool]): List of bools indicating if a category is allowed within the optimization.
        descriptors (List[str]): List of strings representing the names of the descriptors.
        calues (List[List[float]]): List of lists representing the descriptor values.
    """

    descriptors: conlist(item_type=str, min_items=1)
    values: conlist(item_type=conlist(item_type=float, min_items=1), min_items=1)

    @validator("descriptors")
    def validate_descriptors(cls, descriptors):
        """validates that descriptors have unique names

        Args:
            categories (List[str]): List of descriptor names

        Raises:
            ValueError: when descriptors have non-unique names

        Returns:
            List[str]: List of the descriptors
        """
        descriptors = [name2key(name) for name in descriptors]
        if len(descriptors) != len(set(descriptors)):
            raise ValueError("descriptors must be unique")
        return descriptors

    @validator("values")
    def validate_values(cls, v, values):
        """validates the compatability of passed values for the descriptors and the defined categories

        Args:
            v (List[List[float]]): Nested list with descriptor values
            values (Dict): Dictionary with attributes

        Raises:
            ValueError: when values have different length than categories
            ValueError: when rows in values have different length than descriptors
            ValueError: when a descriptor shows no variance in the data

        Returns:
            List[List[float]]: Nested list with descriptor values
        """
        if len(v) != len(values["categories"]):
            raise ValueError("values must have same length as categories")
        for row in v:
            if len(row) != len(values["descriptors"]):
                raise ValueError("rows in values must have same length as descriptors")
        a = np.array(v)
        for i, d in enumerate(values["descriptors"]):
            if len(set(a[:, i])) == 1:
                raise ValueError("No variation for descriptor {d}.")
        return v

    def to_df(self):
        """tabular overview of the feature as DataFrame

        Returns:
            pd.DataFrame: tabular overview of the feature as DataFrame
        """
        data = {cat: values for cat, values in zip(self.categories, self.values)}
        return pd.DataFrame.from_dict(data, orient="index", columns=self.descriptors)

    def get_real_descriptor_bounds(self, values) -> pd.Series:
        """Method to generate a dataFrame as tabular overview of lower and upper bounds of the descriptors (excluding non-allowed descriptors)

        Args:
            values (pd.Series): The categories present in the passed data for the considered feature

        Returns:
            pd.Series: Tabular overview of lower and upper bounds of the descriptors
        """
        df = self.to_df().loc[self.get_possible_categories(values)]
        data = {
            "lower": [min(df[desc].tolist()) for desc in self.descriptors],
            "upper": [max(df[desc].tolist()) for desc in self.descriptors],
        }
        return pd.DataFrame.from_dict(data, orient="index", columns=self.descriptors)

    def validate_experimental(
        self, values: pd.Series, strict: bool = False
    ) -> pd.Series:
        """Method to validate the experimental dataFrame

        Args:
            values (pd.Series): A dataFrame with experiments
            strict (bool, optional): Boolean to distinguish if the occurence of fixed features in the dataset should be considered or not. Defaults to False.

        Raises:
            ValueError: when an entry is not in the list of allowed categories
            ValueError: when there is no variation in a feature provided by the experimental data
            ValueError: when no variation is present or planed for a given descriptor

        Returns:
            pd.Series: A dataFrame with experiments
        """
        values = super().validate_experimental(values, strict)
        if strict:
            bounds = self.get_real_descriptor_bounds(values)
            for desc in self.descriptors:
                if bounds.loc["lower", desc] == bounds.loc["upper", desc]:
                    raise ValueError(
                        f"No variation present or planned for descriptor {desc} for feature {self.key}. Remove the descriptor."
                    )
        return values

    @classmethod
    def from_df(cls, key: str, df: pd.DataFrame):
        """Creates a feature from a dataframe

        Args:
            key (str): The name of the feature
            df (pd.DataFrame): Categories as rows and descriptors as columns

        Returns:
            _type_: _description_
        """
        return cls(
            key=key,
            categories=list(df.index),
            allowed=[True for _ in range(len(df))],
            descriptors=list(df.columns),
            values=df.values.tolist(),
        )


class ContinuousOutputFeature(OutputFeature):
    """The base class for a continuous output feature

    Attributes:
        desirability_function (Desirability_function, optional): Desirability function of
            the feature indicating in which direction it should be optimzed. Defaults to `MaxIdentityDesirabilityFunction`.
    """

    pass


class ContinuousOutputFeature_woDesFunc(ContinuousOutputFeature):
    """A class for continuous output features which should not be optimized. Deprecated."""

    desirability_function = NoDesirabilityFunction


# A helper constant for the default value of the weight parameter
FEATURE_ORDER = {
    ContinuousInputFeature: 1,
    ContinuousDescriptorInputFeature: 2,
    DiscreteInputFeature: 3,
    CategoricalInputFeature: 4,
    CategoricalDescriptorInputFeature: 5,
    ContinuousOutputFeature: 6,
    ContinuousOutputFeature_woDesFunc: 7,
}

## TODO: REMOVE THIS --> it is not needed!
def is_continuous(var: Feature) -> bool:
    """Checks if Feature is continous

    Args:
        var (Feature): Feature to be checked

    Returns:
        bool: True if continuous, else False
    """
    # TODO: generalize query via attribute continuousFeature (not existing yet!)
    if isinstance(var, ContinuousInputFeature) or isinstance(
        var, ContinuousOutputFeature
    ):
        return True
    else:
        False
