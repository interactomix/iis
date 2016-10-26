from typing import Dict, Any, List, Tuple, Union


def get_choices(so_far: Dict[str, Union[List[Any], str]]
                ) -> List[Tuple[str, str]]:
    return [("one", "One"), ("two", "Two")]
