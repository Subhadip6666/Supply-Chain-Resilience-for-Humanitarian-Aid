# Constants and configurations

INF = float('inf')
NUM_NODES = 12

NODE_NAMES = {
    0:  "Central Warehouse (HQ)",
    1:  "Depot A",
    2:  "Depot B",
    3:  "Depot C",
    4:  "Village 1",
    5:  "Village 2",
    6:  "Village 3",
    7:  "Village 4",
    8:  "Village 5",
    9:  "Village 6",
    10: "Village 7",
    11: "Village 8",
}

SHORT_NAMES = {
    0: "HQ", 1: "Depot A", 2: "Depot B", 3: "Depot C",
    4: "Village 1", 5: "Village 2", 6: "Village 3", 7: "Village 4",
    8: "Village 5", 9: "Village 6", 10: "Village 7", 11: "Village 8",
}

SUBSIDISED_EDGES = {
    (5, 6): "State government subsidises this coastal road (cost -2)",
    (6, 5): "State government subsidises this coastal road (cost -2)",
    (8, 9): "NGO covers fuel cost on this relief corridor (cost -3)",
    (9, 8): "NGO covers fuel cost on this relief corridor (cost -3)",
}
