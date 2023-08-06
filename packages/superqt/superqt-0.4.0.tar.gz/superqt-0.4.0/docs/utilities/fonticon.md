# Font icons

The `superqt.fonticon` module provides a set of utilities for working with font
icons such as [Font Awesome](https://fontawesome.com/) or [Material Design
Icons](https://materialdesignicons.com/).

## Basic Example

```python
from fonticon_fa5 import FA5S

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QApplication, QPushButton

from superqt.fonticon import icon, pulse

app = QApplication([])

btn2 = QPushButton()
btn2.setIcon(icon(FA5S.smile, color="blue"))
btn2.setIconSize(QSize(225, 225))
btn2.show()

app.exec()
```

{{ show_widget(225) }}

## Font Icon plugins

Ready-made fonticon packs are available as plugins:

### [Font Awesome 5](https://fontawesome.com/v5/search)

```bash
pip install fonticon-fontawesome5
```

### [Font Awesome 6](https://fontawesome.com/v6/search)

```bash
pip install fonticon-fontawesome6
```

### [Material Design Icons](https://materialdesignicons.com/)

```bash
pip install fonticon-materialdesignicons6
```

### See also

- <https://github.com/tlambert03/fonticon-bootstrapicons>
- <https://github.com/tlambert03/fonticon-linearicons>
- <https://github.com/tlambert03/fonticon-feather>

`superqt.fonticon` is a pluggable system, and font icon packs may use the `"superqt.fonticon"`
entry point to register themselves with superqt.  See [`fonticon-cookiecutter`](https://github.com/tlambert03/fonticon-cookiecutter) for a template, or look through the following repos for examples:

- <https://github.com/tlambert03/fonticon-fontawesome6>
- <https://github.com/tlambert03/fonticon-fontawesome5>
- <https://github.com/tlambert03/fonticon-materialdesignicons6>

## API

::: superqt.fonticon.icon
    options:
        heading_level: 3

::: superqt.fonticon.setTextIcon
    options:
        heading_level: 3

::: superqt.fonticon.font
    options:
        heading_level: 3

::: superqt.fonticon.IconOpts
    options:
        heading_level: 3

::: superqt.fonticon.addFont
    options:
        heading_level: 3

## Animations

the `animation` parameter to `icon()` accepts a subclass of
`Animation` that will be

::: superqt.fonticon.Animation
    options:
        heading_level: 3

::: superqt.fonticon.pulse
    options:
        heading_level: 3

::: superqt.fonticon.spin
    options:
        heading_level: 3
