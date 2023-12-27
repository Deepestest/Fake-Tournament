
import json
from GeneticPolar import analyzeData

print(analyzeData([json.load(open("Output.json")), json.load(open("TBAOutput.json")), json.load(open("ScoutingOutput.json"))]))
