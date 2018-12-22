from collections import OrderedDict, namedtuple
from itertools import chain
from os import path

from mathutils import Color # pylint: disable=E0401
import bge # pylint: disable=E0401
# pylint: disable=E0213,E1139

__all__ = [
    'FilterComponent',
    'FilterProperty',
    'Color',
]

FilterProperty = namedtuple(
    'FilterProperty', 'label value')

class MetaFilterComponent(type):
    '''
    Over complicating things to make them simplier:
    Metaclass parsing class definition to find properties.
    Creates the entries for the `args` field accordingly.
    '''

    def __prepare__(name, bases):
        '''Ensure that the namespace is ordered.'''
        return OrderedDict()

    def __new__(metacls, name, bases, namespace):

        # Get the inherited properties from parent class
        namespace['properties'] = properties = OrderedDict()
        for base in bases:
            if hasattr(base, 'properties'):
                properties.update(OrderedDict(base.properties.items()))

        # Locate and extract FilterProperties
        properties.update(OrderedDict([
            (name, attribute) for name, attribute in namespace.items()
            if isinstance(attribute, FilterProperty)
        ]))

        # Construct the `args` field
        namespace['args'] = OrderedDict({ property.label: property.value
            for property in properties.values()
        })

        # Remove the class properties from the namespace
        for name, _ in properties.items():
            namespace.pop(name, None)

        # Finally, construct the new class
        return super().__new__(metacls, name, bases, namespace)

class FilterComponent(bge.types.KX_PythonComponent, metaclass=MetaFilterComponent):

    pass_index = FilterProperty('Pass Index', 0)

    def __getattr__(self, attribute):
        '''
        Directly refer to FilterProperties by doing `self.prop_name`.
        '''
        property = self.properties[attribute]
        return self._resolved_args[property.label]

    def start(self, args):
        '''
        Base component initialisation.
        Override `setup(self)` to initialize anything extra.
        '''
        self._resolved_args = args
        self.scene = self.object.scene
        self.manager = self.scene.filterManager
        self.filter = self._create_filter()
        self.setup()

    def setup(self):
        '''
        Override this method, called once the 2DFilter is created.
        '''

    def update(self):
        '''
        Override this method to process stuff on each logic tick.
        '''

    def fragment_program(self) -> str:
        '''
        Override this method to return the fragment shader's code.
        '''
        raise NotImplementedError

    def read(self, file_path: str, relative_to: str = None) -> str:
        '''
        Utility function to read a file easily.
        '''

        # In this case, no relative_to is provided:
        # Falling back to using the blendfile as root.
        if relative_to is None:
            relative_to = bge.logic.expandPath('//')

        # In this case, relative_to is provided:
        # Check if it is a file, we always want a folder.
        elif path.isfile(relative_to):
            relative_to = path.dirname(relative_to)

        file_path = path.join(relative_to, file_path)
        with open(file_path, 'r') as file:
            return file.read()

    def _create_filter(self):
        '''
        Default behavior to create the 2DFilter from the component.
        '''
        return self.manager.addFilter(
            self.pass_index,
            bge.logic.RAS_2DFILTER_CUSTOMFILTER,
            self.fragment_program()
        )
