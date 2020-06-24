# flake8-import-restrictions
A flake8 plugin used to disallow certain forms of imports.

This plugin talks about the `import` syntax (`import X.Y.Z [as foo]`)
and the `from` syntax (`from X.Y import Z [as foo]`). It talks about
`import` segments (`import X`), `from` segments (`from Y`), and `as`
segments (`as Z`).

## Options
TODO

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

```python
# Bad
import os.path

# Good
import os
from os import path
```


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
