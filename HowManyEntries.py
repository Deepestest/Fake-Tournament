import joblib
import pandas as pd
from Main import simulateData
from Polar import analyzeData
import warnings

warnings.filterwarnings("ignore")

teamsCSV = pd.read_csv("Teams.csv")
matchCSV = pd.read_csv("Matches.csv")


def RunOnce(val):
    print("Simulating Tournament", val)
    polarError = analyzeData(simulateData(teamsCSV, matchCSV))
    for j in range(len(polarError)):
        if abs(polarError["Average Error"][j]-polarError["Average Error"].tail(1).item()) < 0.005:
            print ("Finished Simulating Tournament", val)
            return [j*10, polarError["Average Error"][j], polarError["Average Error"][0]]


keys = ["NumEntries", "Error", "JustTBAError"]
output = joblib.Parallel(16)(joblib.delayed(RunOnce)(i) for i in range(32))
outputData = pd.DataFrame(output, columns=keys)
outputData.to_csv("HowManyEntries.csv")