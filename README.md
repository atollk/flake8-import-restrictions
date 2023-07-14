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
For every error `IMR2xx` listed below, there are options `--imr2xx_include` and `--imr2xx_exclude` 
which are passed a comma separated list of UNIX wildcard patterns each. The error
will then only be reported on imports of modules that match a include pattern but no exclude 
pattern.

By default, IMR200, IMR201, IMR202, IMR221, IMR223, IMR241, and IMR243 include all (`*`) modules. Only IMR241 excludes the
`typing` module from checks, the other errors have no excludes by default.

## General Import Errors

### IMR200
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

### IMR201
Alias identifiers defined from `as` segments should be at
least two characters long.

```python
# Bad
import os.path as p

# Good
import os.path as path
```

### IMR202
Alias identifiers should not have the same name as the imported object.

```python
# Bad
import sys as sys

# Good
import sys
```

## `import` Syntax Errors

### IMR220
When using the `import` syntax, if the imported module is a submodule,
i.e. not a top level module, an `as` segment should be present.

```python
# Bad
import os.path

# Good
import sys
import os.path as path
```

### IMR221
When using the `import` syntax, each import statement should
only import one module.

```python
# Bad
import sys, os

# Good
import sys
import os
```

### IMR222
The `import` syntax should not be used.


### IMR223
When using the `import` syntax, do not duplicate module names in the `as`
segment.

```python
# Bad
import os.path as path

# Good
from os import path
import os.path as ospath
```


## `from` Syntax Errors

### IMR240
When using the `from` syntax, the `import` segment only contains one
import.

```python
# Bad
from os import path, environ

# Good
from os import path
from os import environ
```

### IMR241
When using the `from` syntax, only submodules are imported, not
module elements.

```python
# Bad
from os.path import join

# Good
from os import path
```

### IMR242
When using the `from` syntax, only module elements are imported,
not submodules.

```python
# Bad
from os import path

# Good
from os.path import join
```

### IMR243
When using the `from` syntax, `import *` should not be used.

```python
# Bad
from os.path import *

# Good
from os.path import join
```

### IMR244
Relative imports should not be used.

```python
# Bad
from . import foo

# Good
from flake8_import_restrictions import foo
```

### IMR245
The `from` syntax should not be used.
