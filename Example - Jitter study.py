# This is a highly simplified jitter study; instead of considering various conditions, it just applies the standard jitter values to an unperturbed reference lattice

import multiprocessing
import os
import json

from UTILITY_quickstart import *



def jitterLinac(
    tao,
    
    L0BMatchStrings = None,
    L1MatchStrings  = None,
    L2MatchStrings  = None,
    L3MatchStrings  = None,
    
    L0BPhaseErrorDeg = 0.1,
    L1PhaseErrorDeg  = 0.7,
    L2PhaseErrorDeg  = 0.4,
    L3PhaseErrorDeg  = 0.4,

    L0BGradientErrorPercent = 0.5, 
    L1GradientErrorPercent  = 0.25,
    L2GradientErrorPercent  = 0.3,
    L3GradientErrorPercent  = 0.3,
):
    """Applies phase and amplitude errors to L0B, L1, L2, and L3
    
    Defaults values from https://docs.google.com/spreadsheets/d/1xeCUImz5uFSq6QA3wV91dG38s-8cyVXQMGw9hjPKa6M/edit?gid=0#gid=0
    """



    #Apply same errors to all elements in the linac region
    clipLimit = np.inf #Optionally limit maximum relative error
    
    #Convert to "turns"
    L0BPhaseError = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L0BPhaseErrorDeg / 360.0 
    L1PhaseError  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L1PhaseErrorDeg  / 360.0 
    L2PhaseError  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L2PhaseErrorDeg  / 360.0 
    L3PhaseError  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L3PhaseErrorDeg  / 360.0

    #Give as multiplier to base gradient
    L0BGradientErrorRelative = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L0BGradientErrorPercent / 100.0
    L1GradientErrorRelative  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L1GradientErrorPercent  / 100.0
    L2GradientErrorRelative  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L2GradientErrorPercent  / 100.0
    L3GradientErrorRelative  = np.clip( np.random.normal(), a_min = -1*clipLimit, a_max = clipLimit) * L3GradientErrorPercent  / 100.0
    
    #Prevent recalculation until changes are made
    tao.cmd("set global lattice_calc_on = F")    
    

    [ tao.cmd(f"change ele {ele} PHI0 {L0BPhaseError}") for ele in L0BMatchStrings ]
    [ tao.cmd(f"change ele {ele} PHI0 {L1PhaseError}")  for ele in L1MatchStrings  ]
    [ tao.cmd(f"change ele {ele} PHI0 {L2PhaseError}")  for ele in L2MatchStrings  ]
    [ tao.cmd(f"change ele {ele} PHI0 {L3PhaseError}")  for ele in L3MatchStrings  ]
    
    for ele in L0BMatchStrings:
        baseGradient = tao.ele_gen_attribs(ele)["GRADIENT"]
        specificGradientError = L0BGradientErrorRelative * baseGradient
        tao.cmd(f"change ele {ele} GRADIENT {specificGradientError}")

    for ele in L1MatchStrings:
        baseGradient = tao.ele_gen_attribs(ele)["GRADIENT"]
        specificGradientError = L1GradientErrorRelative * baseGradient
        tao.cmd(f"change ele {ele} GRADIENT {specificGradientError}")

    for ele in L2MatchStrings:
        baseGradient = tao.ele_gen_attribs(ele)["GRADIENT"]
        specificGradientError = L2GradientErrorRelative * baseGradient
        tao.cmd(f"change ele {ele} GRADIENT {specificGradientError}")

    for ele in L3MatchStrings:
        baseGradient = tao.ele_gen_attribs(ele)["GRADIENT"]
        specificGradientError = L3GradientErrorRelative * baseGradient
        tao.cmd(f"change ele {ele} GRADIENT {specificGradientError}")
    
    #Reenable lattice calculations
    tao.cmd("set global lattice_calc_on = T")

    return {
    "L0BPhaseError" : L0BPhaseError,
    "L1PhaseError"  : L1PhaseError,
    "L2PhaseError"  : L2PhaseError,
    "L3PhaseError"  : L3PhaseError,

    "L0BGradientErrorRelative" : L0BGradientErrorRelative,
    "L1GradientErrorRelative"  : L1GradientErrorRelative,
    "L2GradientErrorRelative"  : L2GradientErrorRelative,
    "L3GradientErrorRelative"  : L3GradientErrorRelative
    }


    
def hashDict(d):
    return str(abs(hash(json.dumps(d, sort_keys=True))))



    
def worker(config):


    csrTF = True
    transverseWakes = False

    importedDefaultSettings = loadConfig("setLattice_configs/2024-10-22_oneBunch_baseline3.yml")


    
    tao = initializeTao(
        inputBeamFilePathSuffix = importedDefaultSettings["inputBeamFilePathSuffix"],
        csrTF = csrTF,
        numMacroParticles=1e4,
        scratchPath = "/tmp",
        randomizeFileNames = True,
        transverseWakes = transverseWakes
    )




    
    # Set up lattice
    setLattice(tao, **importedDefaultSettings)

    L1MatchStrings, L2MatchStrings, L3MatchStrings, selectMarkers = getLinacMatchStrings(tao)
    L0BMatchStrings = ["L0BF"]

    #Since we're jittering, we don't want Bmad to auto-compensate the magnets
    disableAutoMagnetEnergyCompensation(tao)


    
    #Jitter
    jitterDict = jitterLinac(
        tao,
            
        L0BMatchStrings = L0BMatchStrings,
        L1MatchStrings = L1MatchStrings,
        L2MatchStrings = L2MatchStrings,
        L3MatchStrings = L3MatchStrings,
    )

    hashStr = hashDict(jitterDict)





    
    try:
        #Track
        trackBeam(tao, **importedDefaultSettings)
        P = getBeamAtElement(tao, "PENT")

        #Figure of LPS at PENT
        fig = plotMod(P, 'z', 'pz', bins=300, xlim = (-200e-6, 100e-6), ylim = (9.6e9, 10.2e9))


        #Collect useful information like jitterDict into exportDict
        exportDict = config | {"csrTF":csrTF, "transverseWakes":transverseWakes} | jitterDict 
        exportDict = exportDict | getBeamSpecs(P) 
        

        #Specify the output path
        exportPath = "/tmp/jitterStudy/"

        #Make the folder if it doesn't exist
        try:
            os.mkdir(exportPath)
        except:
            pass


        # Export the ParticleGroup beam at PENT, a raw Bmad .lat file, the exportDict as JSON, and a PNG figure of the PENT LPS
        P.write(exportPath+hashStr+"_PENT.h5")
        tao.cmd("write bmad "+exportPath+hashStr+"_lat.bmad")
        
        with open(exportPath+hashStr+"_jitterDict.json", "w") as f:
            json.dump(exportDict, f)

        fig.savefig(exportPath+hashStr+"_PENT.png")


    except Exception as e:
        print("An error occurred:", e)

    return

    

if __name__ == "__main__":
    num_workers = 4 #8

    # For this demo notebook, the workers don't take any arguments
    tasks = [{} for ii in range(10)]

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(worker, tasks)

    for res in results:
        print(res)