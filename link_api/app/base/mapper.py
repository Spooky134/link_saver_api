from typing import TypeVar, Generic, Type, Any

T = TypeVar('T')
E = TypeVar('E')

#TODO может читать неподгруженные данные
class BaseMapper(Generic[T, E]):
    @staticmethod
    def model_to_dict(model: Any) -> dict:
        if model is None:
            return {}
        return {c.key: getattr(model, c.key) for c in model.__table__.columns}

# class BaseMapper(Generic[T, E]):
#     @staticmethod
#     def model_to_dict(model: Any) -> dict:
#         if model is None:
#             return {}
#         state = inspect(model)
#         return {
#             c.key: state.dict.get(c.key) for c in model.__table__.columns
#             if c.key in state.__dict__
#         }