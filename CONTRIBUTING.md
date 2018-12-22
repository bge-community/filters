# Contributing

## Git Workflow

1. Create a fork of this repository under your own GitHub user account.
2. Clone your fork on your workstation:
    ```sh
    git clone https://github.com/<username>/filters.git
    cd filters
    ```
3. Create a branch for you to make new changes:
    ```sh
    git checkout -b <branch_or_feature_name>
    ```
4. Once you made commits on your branch, you can go on the main repository and open a Pull Request:\
   https://github.com/bge-community/filters/pulls.

## Contributing to the Sources

### Library Layout

```yml
# Repository root.
filters:

    # The filter components exposed by the library.
    - __components__:

        # Each filter has its own folder.
        - some_filter:
            - filter_component.py
            - filter_program.fs
        - other_filter:
            - ...
        - ...

        # Index, exposes the components.
        - __init__.py

        # Base filter component.
        - filter.py

    # Miscealeneous repository root files.
    - ...
```

### Adding new filters extending `FilterComponent`

Assuming you are creating a filter called `"my_filter"`, you would edit the following files:

```yml
filters:
    - __components__:

        # Create a new folder for your filter
        - my_filter:

            # Create a Python file to host your FilterComponent
            - my_filter.py

            # Create a Fragment Shader (GLSL) file to host your shader program source.
            - my_filter.fs

        # Add a line to the index to expose your filter.
        - __init__.py

```

Breakdown for each file:

```py
# filters/__components__/my_filter/my_filter.py

from ..filter import FilterComponent, FilterProperty

from mathutils import Vector

class YourFilter(FilterComponent):

    some_property = FilterProperty(
        "Some Property (Label displayed in Blender' UI)",
        'Some Value (Default, string in this case)')

    user_color = FilterProperty('Color', Vector([1.0, 0.0, 0.0, 1.0]))

    def fragment_program(self):
        '''
        This method **must** return your fragment shader program.
        How you do it is not important, you can make it return your hardcoded
        shader in a string if you want, or you can use `self.read(path, relative_to)`
        in order to load the content of a file.
        '''
        return self.read('./my_filter.fs', __file__)

    def setup(self):
        '''
        Called once on startup.
        '''
        print('User defined "Some Property" to be:', self.some_property)

        # You have access to some instance properties:
        self.object # The owner of this component.
        self.scene # The owner's scene.
        self.manager # The scene's filter manager
        self.filter # The KX_2DFilter created by this component.

        # You can set uniforms on the `KX_2DFilter` stored in `self.filter`.
        # See https://pythonapi.upbge.org/bge.types.KX_2DFilter.html
        # and https://pythonapi.upbge.org/bge.types.BL_Shader.html

        # In addition to these properties, every class properties you defined
        # as `FilterProperties` are accessible as instance properties, they return
        # the values that were inputed in Blender's UI.

        self.filter.setUniform4f('color',
            self.user_color.x,
            self.user_color.y,
            self.user_color.z,
            self.user_color.w)

    def update(self):
        '''
        Called on every logic tick.
        You still have access to all instance properties.
        '''
        print('Tick, I am called on each frame.')

```
```glsl
// filters/__components__/my_filter/my_filter.py

uniform vec4 color;

void main()
{
    gl_FragColor = color;
}
```
```py
# filters/__components__/__init__.py

from .screen_color.screen_color import ScreenColorFilter
from .screen_fade.screen_fade import ScreenFadeFilter
# Add your line:
from .my_filter.my_filter import MyFilter
```

## About `FilterComponent` and `FilterProperty`

You may wonder why you do not have to specify an `args` property in your `PythonComponent` class, and why you should use this `FilterProperty` instead.

To make it simple, it is a modification I made in the `FilterComponent` base class that you should extend. When your class gets created in the Python runtime, I am parsing your definitions to find any `FilterProperty` instances, and it will automatically add an `args` field (at runtime) with your properties, and it allows you to then access the values defined in Blender's UI by simply doing `self.the_property`.

One of the benefits of such a system is that I made it possible to inherit from some parent class properties. In fact, everytime you extend the `FilterComponent` class, you inherit a `Pass Index` property, as I assumed every filter would require this field to properly function.
