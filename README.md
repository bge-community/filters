# BGE `filters` Library

This repository is a library of 2D Filters that you can use as components for the Blender Game Engine.

[Contributing](CONTRIBUTING.md).

## How to use in your game

Clone this repository next to your main game file:

```sh
git clone https://github.com/bge-community/filters.git
```

Then register a new component with one of the available FilterComponents.

## Current list of `FilterComponents`:

```yml
- filters.ScreenColorFilter # Outputs a full color to the screen.
- filters.ScreenFadeFilter # Fade the screen to some color, based on time.
```
