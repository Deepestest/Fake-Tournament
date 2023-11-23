import pandas as pd
from Main import simulateData
from Polar import analyzeData


keys = ["NumEntries", "Error", "JustTBAError"]
convergeData = pd.DataFrame(columns=keys)
for i in range(1000):
    simulateData()
    analyzeData()
    polarError = pd.read_csv("PolarError.csv")
    for j in range(len(polarError)):
        if abs(polarError["Average Error"][j]-polarError["Average Error"].tail(1).item()) < 0.005:
            convergeData.loc[len(convergeData)] = [j*10, polarError["Average Error"][j], polarError["Average Error"][0]]
            break
    print("simulation", i+1, "complete")
    print(convergeData[keys].tail(1))
convergeData.to_csv("ConvergeData.csv")