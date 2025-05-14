import multiprocessing
import os

from UTILITY_quickstart import *


def worker(overrides):
    importedDefaultSettings = loadConfig("setLattice_configs/2024-10-14_twoBunch_baseline.yml")
    importedDefaultSettings = importedDefaultSettings | {"inputBeamFilePathSuffix" : '/beams/2025-05-13_twobunch_unoptimized_shortSpacing/2025-05-13_twobunch_unoptimized_shortSpacing.h5'}
    
    csrTF = False

    tao = initializeTao(
        inputBeamFilePathSuffix = importedDefaultSettings["inputBeamFilePathSuffix"],
        
        csrTF = csrTF,
        numMacroParticles=1e5,
    
        scratchPath = "/tmp",
        randomizeFileNames = True
    )




    activeSettings = importedDefaultSettings | overrides

    setLattice(tao, **activeSettings)
    trackBeam(tao, **activeSettings)
    
    # P = getBeamAtElement(tao, "ENDBC14_2")
    # BC14Length = smallestIntervalImpliedSigma(P.z)
    
    # P = getBeamAtElement(tao, "PENT")
    # PENTLength = smallestIntervalImpliedSigma(P.z)

    # return f"""{overrides["L2PhaseSet"]}, {BC14Length}, {PENTLength}"""

    L1PhaseSet = overrides["L1PhaseSet"]
    L2PhaseSet = overrides["L2PhaseSet"]
    outputFileName = f"{L1PhaseSet}_{L2PhaseSet}.h5"
    
    P = getBeamAtElement(tao, "PENT")
    P.write(outputFileName)

    return f"{L1PhaseSet}, {L2PhaseSet}, {outputFileName}"

    

if __name__ == "__main__":
    num_workers = 4 #8
    tasks = [
        {"L1PhaseSet": L1, "L2PhaseSet": L2}
        # for L2 in np.arange(-40, -28, 2)
        # for L1 in np.arange(-30, 0, 5)
        for L2 in np.arange(-39, -34, 1)
        for L1 in np.arange(-21, -16, 1)
    ]

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(worker, tasks)

    for res in results:
        print(res)