# Tensorutils
Small utils for Tensorflow in Python.

# Select CPU if not GPU

A function to force Tensorflow to use CPU instead of GPU if this is not present.
This function is very easy to use. For example:

```python
from tensorutils import select_cpu_if_not_gpu

# With static memory size
select_cpu_if_not_gpu()

# With dynamic memory size
select_cpu_if_not_gpu(True)
```

