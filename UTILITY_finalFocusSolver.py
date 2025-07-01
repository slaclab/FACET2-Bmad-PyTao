from scipy.optimize import minimize
import numpy as np
from UTILITY_setLattice import setLattice, getBendkG, getQuadkG, getSextkG, setBendkG, setQuadkG, setSextkG, setXOffset, setYOffset

def finalFocusSolverObjective(params, tao, ele, s_offset, targetBetaX, targetAlphaX, targetBetaY, targetAlphaY):
    Q5FFkG, Q4FFkG, Q3FFkG, Q2FFkG, Q1FFkG, Q0FFkG  = params
    
    try:
        #Prevent recalculation until changes are made
        tao.cmd("set global lattice_calc_on = F")
        
        setQuadkG(tao, "Q5FF", Q5FFkG)
        setQuadkG(tao, "Q4FF", Q4FFkG)
        setQuadkG(tao, "Q3FF", Q3FFkG)
        setQuadkG(tao, "Q2FF", Q2FFkG)
        setQuadkG(tao, "Q1FF", Q1FFkG)
        setQuadkG(tao, "Q0FF", Q0FFkG)
        
        #Reenable lattice calculations
        tao.cmd("set global lattice_calc_on = T")
    
    except: #If Bmad doesn't like the proposed solution, don't crash, give a bad number
        return 1e20

    resultTwiss = tao.twiss_at_s(ele = ele, s_offset = s_offset)
    resultBetaX = resultTwiss["beta_a"]
    resultAlphaX = resultTwiss["alpha_a"]
    resultBetaY = resultTwiss["beta_b"]
    resultAlphaY = resultTwiss["alpha_b"]

    #Golden lattice FF settings as of 2025-01-10-11-17-43
    # Q5FFkG :  -71.837
    # Q4FFkG :  -81.251
    # Q3FFkG :  99.225
    # Q2FFkG :  126.35
    # Q1FFkG :  -235.218
    # Q0FFkG :  126.353
    goldenVector = np.array([ -71.837 , -81.251, 99.225, 126.35, -235.218,  126.353 ])

    #Optionally give a very slight preference to solutions that don't move the magnets very much
    moveError = 1e-6 * np.sum( (params - goldenVector) ** 2 ) 
    
    return (resultBetaX - targetBetaX) ** 2 + (resultAlphaX - targetAlphaX) ** 2 + (resultBetaY - targetBetaY) ** 2 + (resultAlphaY - targetAlphaY) ** 2 + moveError


def finalFocusSolver(
    tao,
    ele = "PENT",
    s_offset = 0.0,
    targetBetaX = 0.5,
    targetAlphaX = 0,
    targetBetaY = 0.5,
    targetAlphaY = 0,
    initialGuess = None,
    returnVariablesOrNames = "variables",
    verbose = False
):

    """Find final focus optics to achieve desired Twiss

    Parameters
    ----------
    tao : Tao object
        Active tao object
    ele : str
        Name of element where optimization is performed
    s_offset : float
        Relative longitudinal offset from ele for Twiss calculation. Positive = downstream

    targetBetaX, targetAlphaX, targetBetaY, targetAlphaY : float
        Desired Twiss parameters

    initialGuess : dict
        Optionally specify the initial guess for the optimizer. Otherwise uses golden lattice

    returnVariablesOrNames : "variables" or "name"
        Specifies if the returned solution dictionary is in terms of setLattice() variables (e.g. "Q5FFkG") or element names (e.g. "Q5FF")

    verbose : bool
        Print optimizer info

    Returns
    -------
    dict
        Dictionary of final focus magnet values
    """

    quadNameList = ["Q5FF", "Q4FF", "Q3FF", "Q2FF", "Q1FF", "Q0FF"] 
    quadVariableNameList = ["Q5FFkG", "Q4FFkG", "Q3FFkG", "Q2FFkG", "Q1FFkG", "Q0FFkG"] 

    if not initialGuess:
        initialGuess = { name+"kG" : getQuadkG(tao, name) for name in quadNameList }

    #Dictionary to vector
    initialGuess = [ initialGuess[name] for name in quadVariableNameList ]

    #For now, just hardcoding bounds... could generalize if required
    #From "bounds.yml" as of 2025-01-10-11-11-35
    # Q5FFkGBounds: (-256, 0)  #BCON = -70
    # Q4FFkGBounds: (-446, 0)  #BCON = -71
    # Q3FFkGBounds: (0, 457)   #BCON = 106
    # Q2FFkGBounds: (0, 167)   #BCON = 112
    # Q1FFkGBounds: (-257, 0)  #BCON = -225
    # Q0FFkGBounds: (0, 167)   #BCON = 112

    bounds = [(-256,0), (-446,0), (0,457), (0,167), (-257,0), (0,167)]


    # Perform optimization using Nelder-Mead
    result = minimize(
        finalFocusSolverObjective, 
        initialGuess, 
        method='Nelder-Mead',
        bounds = bounds,
        args = (tao, ele, s_offset, targetBetaX, targetAlphaX, targetBetaY, targetAlphaY)
    )



    if verbose:
        print("Optimization Results:")
        print(f"Optimal Parameters: {result.x}")
        print(f"Objective Function Value at Optimal Parameters: {result.fun}")
        print(f"Number of Iterations: {result.nit}")
        print(f"Converged: {result.success}")

    

    
    if returnVariablesOrNames == "variables":     
        return { quadVariableNameList[i] : result.x[i] for i in range(len(quadVariableNameList)) }
    elif returnVariablesOrNames == "names":     
        return { quadNameList[i] : result.x[i] for i in range(len(quadVariableNameList)) }
    else:
        print("Illegal returnVariablesOrNames") 