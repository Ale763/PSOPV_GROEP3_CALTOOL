
class Observable:
    __obs = []
    __changed = 0

    def add_observer(self, observer):
        if observer not in self.__obs:
            self.__obs.append(observer)

    def delete_observer(self, observer):
        self.__obs.remove(observer)

    def notify_observers(self, arg = None):
        '''If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.'''

        if not self.__changed: return
        # Make a local copy in case of synchronous
        # additions of observers:
        localArray = self.__obs[:]
        self.clear_changed()

        # Updating is not required to be synchronized:
        for observer in localArray:
            observer.update(self, arg)

    def delete_observers(self): self.__obs = []
    def set_changed(self): self.__changed = 1
    def clear_changed(self): self.__changed = 0
    def has_changed(self): return self.__changed
    def count_observers(self): return len(self.obs)