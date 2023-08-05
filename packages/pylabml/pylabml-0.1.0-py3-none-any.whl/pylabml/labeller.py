from typing import List

import pandas as pd

_labellers = {}

def register(labeller) -> None:
    name = labeller.__name__
    if name in _labellers:
        raise ValueError(f"Labeller with name '{name}' already registered.")
    _labellers[labeller.__name__] = labeller

def labeller_names() -> List[str]:
    return list(_labellers.keys())

def label(data: pd.DataFrame, labellers=None):
    if labellers is None:
        labellers = _labellers.values()
    res = []
    for tuple in data.itertuples(index=False):
        for labeller in labellers:
            label = labeller(tuple)
            if label is not None:
                res.append(label)
                break
        else:
            res.append(None)
    return pd.Series(res)

def label_with(data: pd.DataFrame, labeller_name: str):
    res = []
    labeller = _labellers[labeller_name]
    for tuple in data.itertuples(index=False):
        label = labeller(tuple)
        res.append(label)
    return pd.Series(res)