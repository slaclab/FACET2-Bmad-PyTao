from UTILITY_quickstart import *

#Initialize the tao object
tao = initializeTao()

#Example usage 
print(
    setLatticeAndGetMatrix(
        tao,
        "PENT",                            #Starting element
        "DTOTR",                           #Final element
        startOffset = 0.25,                #Optional: Calculation offset from starting element in meters. Positive = downstream
        endOffset = 0,                     #Optional: Calculation offset from ending element in meters. Positive = downstream
        overrideSettings = {"Q0DkG" : -50} #Override a single magnet, but otherwise use golden lattice
    )
)

#Import all the IP quad settings from the golden lattice. Mostly to show the naming scheme
quadSettingList = ["Q5FFkG", "Q4FFkG", "Q3FFkG", "Q2FFkG", "Q1FFkG", "Q0FFkG", "Q0DkG", "Q1DkG", "Q2DkG"]
goldenLatticeConfig = loadConfig("setLattice_configs/defaults.yml")
goldenLatticeMagnetSettings = {ele : goldenLatticeConfig[ele] for ele in quadSettingList}
print(goldenLatticeMagnetSettings)


#Example usage. Assert every magnet value
print(
    setLatticeAndGetMatrix(
        tao,
        "PENT",
        "DTOTR",
        startOffset = 0.25,
        endOffset = 0,
        overrideSettings = goldenLatticeMagnetSettings
    )
)