# [metaL]anguage

The system uses its own programming language `metaL` targetted especially for
handy graph transformations.

## Object Graph

Every element in a system is a unified object which can hold both scalar value,
attributes, and ordered subelements (subgraphs).

```
class Object:
    def __init__(self,V):
        # type/class tag
        self.type = self.__class__.__name__.lower()
        # scalar value
        self.val  = V
        # attributes = string-keyed array = environment
        self.slot = {}
        # nested elements = ordered vector = stack
        self.nest = []
        # unique object id for persistent storage
        self.sid  = id(self)
```

Every object is universal as it can be used as a single value, string-keyed
associative array, vector, and stack. As it has both environment and stack
storage facilities, any object can be used as a computation context for
expression (graph) evaluations. At a same time, any three objects can be used in
the evaluation & apply operations:

```
class Primitive(Object):
    # evaluate object `self` in the computation context `ctx`
    def eval(self,ctx): return self
    # apply `self' to object `that` as a function in context `ctx`
    def apply(self,that,ctx): return ...
```

So, any object not only a universal data container but also a function.

## Operators

### `\`` quote

Prefix `\`symbol` or `\`(expression)` to prevent from evaluation: leave parsed AST as is.

### `//` push

```
`A // `B -> A.push(B)
```

### `<<` store to type-named slot

```
A << B -> A[B.type] = B
```

### `>>` store to val-named slot

```
A >> B -> A[B.val] = B
```
