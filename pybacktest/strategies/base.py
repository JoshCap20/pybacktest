from ..data.data_series import DataSeries

class BaseObserver(object):
    """
    Base class for all observers.
    """

    def apply(self, row: DataSeries) -> bool:
        raise NotImplementedError
    
    def exeecute(self, row: DataSeries) -> None:
        raise NotImplementedError
    
    def __str__(self) -> str:   
        """
        Returns the name of the strategy.
        """
        return self.__class__.__name__
    

