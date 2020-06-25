# flake8-import-restrictions
[![Build Status](https://github.com/atollk/flake8-import-restrictions/workflows/tox/badge.svg)](https://github.com/atollk/flake8-import-restrictions/actions)
[![Build Status](https://github.com/atollk/flake8-import-restrictions/workflows/pylint/badge.svg)](https://github.com/atollk/flake8-import-restrictions/actions)
[![Build Status](https://github.com/atollk/flake8-import-restrictions/workflows/black/badge.svg)](https://github.com/atollk/flake8-import-restrictions/actions)
[![Build Status](https://github.com/atollk/flake8-import-restrictions/workflows/flake8/badge.svg)](https://github.com/atollk/flake8-import-restrictions/actions)

A flake8 plugin used to disallow certain forms of imports.

This plugin talks about the `import` syntax (`import X.Y.Z [as foo]`)
and the `from` syntax (`from X.Y import Z [as foo]`). It talks about
`import` segments (`import X`), `from` segments (`from Y`), and `as`
segments (`as Z`).

## Options
For every error `I20xx` listed below, there are options `--i20xx_include` and `--i20xx_exclude` 
which are passed a comma separated list of UNIX wildcard patterns each. The error
will then only be reported on imports of modules that match a include pattern but no exclude 
pattern.

By default, I2000, I2001, I2021, I2041, and I2043 include all (`*`) modules. Only I2041 excludes the
`typing` module from checks, the other errors have no excludes by default.

## General Import Errors

### I2000
Imports should only happen on module level, not locally.

```python
# Bad
def f():
    import os.path
    return os.path.join("a", "b")

# Good
import os.path
def f():
    return os.path.join("a", "b")
```

### I2001
Alias identifiers defined from `as` segments should be at
least two characters long.

```python
# Bad
import os.path as p

# Good
import os.path as path
```


## `import` Syntax Errors

### I2020
When using the `import` syntax, if the imported module is a submodule,
i.e. not a top level module, an `as` segment should be present.

```python
# Bad
import os.path

# Good
import sys
import os.path as path
```

### I2021
When using the `import` syntax, each import statement should
only import one module.

```python
# Bad
import sys, os

# Good
import sys
import os
```

### I2022
The `import` syntax should not be used.


## `from` Syntax Errors

### I2040
When using the `from` syntax, the `import` segment only contains one
import.

```python
# Bad
from os import path, environ

# Good
from os import path
from os import environ
```

### I2041
When using the `from` syntax, only submodules are imported, not
module elements.

```python
# Bad
from os.path import join

# Good
from os import path
```

### I2042
When using the `from` syntax, only module elements are imported,
not submodules.

```python
# Bad
from os import path

# Good
from os.path import join
```

### I2043
When using the `from` syntax, `import *` should not be used.

```python
# Bad
from os.path import *

# Good
from os.path import join
```

### I2044
Relative imports should not be used.

```python
# Bad
from . import foo

# Good
from flake8_import_restrictions import foo
```

### I2045
The `from` syntax should not be used.
