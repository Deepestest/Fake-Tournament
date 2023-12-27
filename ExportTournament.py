
import json
import pandas as pd
from Main import simulateData
from Performance import NpEncoder

teamsCSV = pd.read_csv("Teams.csv")
matchCSV = pd.read_csv("Matches.csv")
data = simulateData(teamsCSV, matchCSV)
output = data[0]
tbaOutput = data[1]
scoutingOutput = data[2]
outputFile = open("Output.json", "w")
json.dump(output, outputFile, cls=NpEncoder)
tbaOutputFile = open("TBAOutput.json", "w")
json.dump(tbaOutput, tbaOutputFile, cls=NpEncoder)
scoutingOutputFile = open("ScoutingOutput.json", "w")
json.dump(scoutingOutput, scoutingOutputFile, cls=NpEncoder)