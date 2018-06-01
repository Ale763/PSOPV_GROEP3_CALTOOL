from enum import Enum


class AttributeStatus(Enum):
    ADDED = 0
    CHANGED = 1
    REMOVED = 2


class changed_event:
    def __init__(self, p_old_event, p_new_event):
        self.__old_event = p_old_event                  # Event object, representing old version of Event
        self.__new_event = p_new_event                  # Event object, representing new version of Event
        self.__attributes = {}                          # Dictionary containing all changed attributes of changed event
        self.parse_changes()

    # --------------------------------------------------------------------------------------------------------------------
    # Getters

    def get_old(self):
        return self.__old_event

    def get_new(self):
        return self.__new_event

    def get_attributes(self):
        return self.__attributes


    @staticmethod
    def __get_attribute_dict(p_event):
        dict = {}
        for attribute, value in p_event.items():
            dict[attribute] = value
        return dict

    # --------------------------------------------------------------------------------------------------------------------

    def parse_changes(self):
        """
        Parses both events to search for attributes that are not STRICTLY the same
        Parses dictionary with all changed attributes as key
        and status of those attributes (ADDED, REMOVED or CHANGED) as value
        """
        changed_attributes = {}
        # old_event = self.__get_attribute_dict(self.__old_event)
        new_event = self.__get_attribute_dict(self.__new_event)

        # Search for changes in event
        for attribute, value in self.__old_event.items():
            # If attribute was not found in new version, the attribute was REMOVED
            if new_event.get(attribute) is None:
                changed_attributes[attribute] = AttributeStatus.REMOVED
                # del old_event[attribute]
                # del new_event[attribute]
            # If attribute was found, but is not the same, the attribute was CHANGED
            elif self.__old_event.decoded(attribute) != self.__new_event.decoded(attribute):
                changed_attributes[attribute] = AttributeStatus.CHANGED
                # del old_event[attribute]
                del new_event[attribute]
            else:
                del new_event[attribute]

        # The remaining attributes in the new version, are the attributes that are ADDED
        for attribute, value in new_event.items():
            changed_attributes[attribute] = AttributeStatus.ADDED

        self.__attributes = changed_attributes

