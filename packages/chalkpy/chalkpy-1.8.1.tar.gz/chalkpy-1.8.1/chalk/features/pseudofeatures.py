from datetime import datetime

from chalk.features.feature_field import Feature

__all__ = [
    "CHALK_TS_FEATURE",
    "ID_FEATURE",
    "OBSERVED_AT_FEATURE",
    "REPLACED_OBSERVED_AT_FEATURE",
    "PSEUDOFEATURES",
]

CHALK_TS_FEATURE = Feature(name="CHALK_TS", namespace="__chalk__", typ=datetime)
ID_FEATURE = Feature(name="__id__", namespace="__chalk__", typ=str)
OBSERVED_AT_FEATURE = Feature(name="__observed_at__", namespace="__chalk__", typ=datetime)
REPLACED_OBSERVED_AT_FEATURE = Feature(name="__replaced_observed_at__", namespace="__chalk__", typ=datetime)

PSEUDOFEATURES = [CHALK_TS_FEATURE, ID_FEATURE, OBSERVED_AT_FEATURE, REPLACED_OBSERVED_AT_FEATURE]
