import abc


# Abstract base — any observer must implement update() or Python raises TypeError at startup
class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, event_data):
        raise NotImplementedError(f'{self.__class__.__name__} must implement update(event_data).')


# Holds a list of observers and broadcasts events to all of them
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):  # subscribe
        self._observers.append(observer)

    def detach(self, observer):  # unsubscribe
        self._observers.remove(observer)

    def notify(self, event_data):
        for observer in self._observers:
            observer.update(event_data)
