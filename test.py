import numpy as np

vec1 = np.array([0,1,2,3])
vec2 = np.array([0,1,2,3])



result = np.sqrt(sum(pow(vec1-vec2,2)))

print(result)