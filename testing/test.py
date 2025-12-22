import pandas as pd
import test2

# DataFrame.
df = pd.DataFrame(data={
  "x": [10, 20, 25],
  "y": [0, 2, 5]
})

# Print DataFrame
print(df)

# x  y
# 0  10  0
# 1  20  2
# 2  25  5

# Access this functionality
df.row_by_value('x', 10)

# x    10
# y     0
# Name: 0, dtype: int64