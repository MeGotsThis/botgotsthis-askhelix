from typing import Mapping, Optional


def features() -> Mapping[str, Optional[str]]:
    if not hasattr(features, 'features'):
        setattr(features, 'features', {
            'helixfossil': 'Ask Helix Fossil',
            })
    return getattr(features, 'features')
