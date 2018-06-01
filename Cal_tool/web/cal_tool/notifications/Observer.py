# Util/Observer.py
# Class support for "observer" pattern.

class Observer:
    def update(self, observable, arg):
        '''Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change.'''
        pass
