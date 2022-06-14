# Indent-Detent parser for Python

An easy-use tool to parse Python code into Indent-Detent format.

Useful for some code related pretrained models (e.g. [PLBART](https://github.com/wasiahmad/PLBART)).

Original code:

```python
import torch
def example(X,Y):
    X = X.narrow(1,0,Y.shape[1])
    ret = torch.cat((X,Y),0)
    return ret
```

Indent-Detent format:

```python
import torchNEW_LINEdef example(X,Y):NEW_LINEINDENT X = X.narrow(1,0,Y.shape[1])NEW_LINEret = torch.cat((X,Y),0)NEW_LINEreturn retNEW_LINE
```

# Usage

```python
from parse import pre_process_code, post_process_code
code = '''import torch
def example(X,Y):
    X = X.narrow(1,0,Y.shape[1])
    ret = torch.cat((X,Y),0)
    return ret'''

parsed_code = pre_process_code(code)  # origin code -> indent-dedent format
origin_code = post_process_code(parsed_code)  # indent-dedent format -> origin code
```

