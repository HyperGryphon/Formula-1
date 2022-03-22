---
title: An R Markdown document converted from "F1/gear ratios.ipynb"
output: html_document
---

```{python}
import fastf1
from fastf1 import plotting
from fastf1 import utils
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
```

```{python}
# Enable the cache
fastf1.Cache.enable_cache('F1/cache')

# Load the session data
session = fastf1.get_testing_session(2022, 2, 2)

# Collect all race laps
laps = session.load_laps(with_telemetry=True)
```

```{python}
# Get laps of the drivers
driver1 = 'RUS'
laps_1 = laps.pick_driver(driver1)
laps_1.telemetry.head()
```

```{python}
#estimating gear relationship
#diameter of a tyre = .72m
tyre_rpm = laps_1.telemetry.loc[(laps_1.telemetry.nGear==4) & (laps_1.telemetry.Speed>30)].Speed*(1000/60)/(2*3.141592653589793*(0.72/2))
eng_rpm = laps_1.telemetry.loc[(laps_1.telemetry.nGear==4) & (laps_1.telemetry.Speed>30)].RPM

plotting.setup_mpl()
#plt.style.use('fivethirtyeight')
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(tyre_rpm, eng_rpm, 'bo', markersize=3)

#linear regression model
model = LinearRegression()
x = np.array([tyre_rpm]).reshape(-1, 1)
y = np.array([eng_rpm]).reshape(-1, 1)
model.fit(x, y)
model = LinearRegression().fit(x, y)
x_new = np.linspace(min(x), max(x), 100)
y_new = model.predict(x_new[:])
ax.plot(x_new, y_new, color="red", linewidth=3)
ax.set_xlabel('Tyre RPM')
ax.set_ylabel('Engine RPM')
plt.show()
print('slope:', np.round(model.coef_, 2))
print('coefficient of determination:', np.round(model.score(x, y), 2))
```

