class ColumnNotExists(Exception):
    """Error that raises when columns does not exist"""
    pass
class MixedDtypeError(Exception):
    """Error that raises when have mixed dtypes"""
    pass