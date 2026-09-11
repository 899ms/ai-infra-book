"""Provenance for declared scenario inputs (archived file path or "book")."""
from fractions import Fraction


def input_sources(inputs: dict, sources) -> dict:
    """Validate an input-name -> source mapping; every key must name a declared input."""
    if sources is None:
        return {}
    if not isinstance(sources, dict):
        raise ValueError('input_sources must map input names to archived file paths or "book"')
    unknown = set(sources) - set(inputs)
    if unknown:
        raise ValueError(f'input_sources names unknown inputs: {sorted(unknown)}')
    for name, value in sources.items():
        if not isinstance(value, str) or not value:
            raise ValueError(f'input_sources[{name}] must be a nonempty string')
    return dict(sources)


def exact(value, name, *, allow_zero=False):
    """Exact rational from int or decimal/fraction string; floats are rejected."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError(f'{name} must be an integer or exact decimal/fraction string')
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f'Invalid {name}') from error
    if result < 0 or (result == 0 and not allow_zero):
        raise ValueError(f'{name} must be positive')
    return result
