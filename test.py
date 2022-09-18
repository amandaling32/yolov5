import base64
import numpy as np
random_array = np.random.randn(32,32)
string_repr = base64.binascii.b2a_base64(random_array).decode("ascii")
array = np.frombuffer(base64.binascii.a2b_base64(string_repr.encode("ascii"))) 
array = array.reshape(32,32)

if np.array_equal(random_array, array) and random_array.shape == array.shape and random_array.dtype == array.dtype:
    print("true")