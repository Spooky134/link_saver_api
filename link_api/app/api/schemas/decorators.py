from pydantic import field_validator
from typing import Any, List, Optional

def validate_ids_field(field_name: str):
    """Декоратор для конвертации строковых ID в int в указанном поле"""
    
    def decorator(cls):
        @field_validator(field_name, mode='before')
        @classmethod
        def convert_ids(cls, v: Any) -> Optional[List[int]]:
            if v is None:
                return None
            if isinstance(v, list):
                return [
                    int(item) if isinstance(item, str) and item.isdigit()
                    else item
                    for item in v
                ]
            return v
        
        # Динамически добавляем валидатор к классу
        setattr(cls, f"_validate_{field_name}", convert_ids)
        return cls
    
    return decorator