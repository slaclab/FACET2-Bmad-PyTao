#Adapted from https://github.com/ericcropp/Impact-T_Examples/blob/main/FACET-II_Impact_Bmad/Impact_Bmad.ipynb
from UTILITY_quickstart import *


from distgen import Generator
from impact import Impact, run_impact_with_distgen, evaluate_impact_with_distgen
from impact.autophase import autophase_and_scale
import copy
import yaml

import impact
import os

def runImpact(
    filePath = None,
    impactGridCount = 8,
    impactNumProcs = 1, 
    numMacroParticles = 1e4,
    GFILESuffix = 'distgen.yaml',
    L0APhaseOffset = 0,
    solenoidTValue = -0.4185,
    impactChargepC = 1600, 
    returnImpactObject = False,
    **kwargs
):
    print("Running Impact")
    
    if not filePath:
        filePath = os.getcwd()
        print(f"Assuming default file path: {filePath}")



    impactFolderPath = filePath+"/impact/"
    GFILE = impactFolderPath+GFILESuffix # Distgen input file
    YFILE = impactFolderPath+'ImpactT.yaml' # To be created based on template and updated for final run
    YFILE_TEMPLATE = impactFolderPath+'ImpactT-template.yaml' #Initial settings

    L0AF_E_Gain=62924849.46502216 # Calculated L0AF energy gain from January 2024 nominal power readbacks
    sim_sol_conv=1.6 #Convert from PV value to T/m (simulation input)
    L0AF_Phase=0 #L0AF phase; 0 is max E phase

    #Impact settings
    SETTINGS0 = {
        #'numprocs':(len(os.sched_getaffinity(0)))-1, #Number of available cores, minus one (jupyter is running in one core)
        'numprocs':impactNumProcs,
        'header:Nx':impactGridCount,
        'header:Ny':impactGridCount,  
        'header:Nz':impactGridCount, 
        'stop_1:s':4.2,
        'distgen:n_particle':numMacroParticles,
        'distgen:total_charge': {'value': impactChargepC, 'units': 'pC'},

        
        #'GUNF:theta0_deg':26.8-90.5,#30 degrees-adjustment for phase def.
        #'GUNF:rf_field_scale': 123/2.44885*1e6,
        #New from Eric 2024-10-07
        'GUNF:theta0_deg':29.3-90,#31.83 degrees-adjustment for phase def.
        'GUNF:rf_field_scale': 119/2.44885*1e6,
        
        'SOL10111:solenoid_field_scale':-0.41/sim_sol_conv,
        #'PR10241:sample_frequency':1,
        #'workdir':os.path.expandvars('~/'),
        #'command': '/opt/homebrew/anaconda3/envs/bmadclone/bin/ImpactTexe',    
        #'command_mpi': '/sdf/home/c/cropp/conda/envs/xopt/bin/ImpactTexe-mpi',
        # 'mpi_run':'salloc --partition milano --account ad:ard-online -N 1 -n {nproc} /usr/lib64/openmpi/bin/mpirun -n {nproc} {command_mpi}'
        #'mpi_run':'/usr/lib64/openmpi/bin/mpirun --oversubscribe -n {nproc} {command_mpi}'
    }


    I = Impact.from_yaml(YFILE_TEMPLATE)
    G = Generator(GFILE)

    I=update_impact(I,SETTINGS0)

    I2=copy.deepcopy(I)

    P0 = pmd_beamphysics.single_particle(pz=1e-15, z=1e-15)
    
    
    I2.numprocs=1
    t=I2.track(P0,s=0.9)
    
    E=t['mean_energy']
    #print(E)


    I['L0AF_scale']['rf_field_scale']=30e6
    I['L0AF_phase']['theta0_deg']=29
    I.numprocs=1
    
    target_L0AF=E+L0AF_E_Gain
    
    #print(target_L0AF)

    print("\t Impact: Autophasing")
    res_L0AF = impact.autophase.autophase_and_scale(I, phase_ele_name='L0AF_phase', scale_ele_name='L0AF_scale', target=target_L0AF, scale_range=(10e6, 100e6), initial_particles=P0, verbose=False)

    I['L0AF_phase']['theta0_deg']=I['L0AF_phase']['theta0_deg'] - L0AF_Phase  + L0APhaseOffset

    with open(YFILE_TEMPLATE, 'r') as file:
        impact_input = yaml.safe_load(file)

    impact_input['group']['L0AF_phase']['value']=float(I['L0AF_phase']['theta0_deg'])
    impact_input['group']['L0AF_scale']['value']=float(I['L0AF_scale']['rf_field_scale'])

    with open(YFILE, 'w') as file:
        yaml.dump(impact_input, file)


    #NMM overwrite; replace solenoid scan
    t = solenoidTValue#-0.4185

    print("\t Impact: Distgen")
    G=update_distgen(G,SETTINGS0,verbose=False)
    G.input

    print("\t Impact: Tracking")
    
    G.run()
    P = G.particles
    I.initial_particles = P

    I.numprocs=SETTINGS0['numprocs']

    I['SOL10111:solenoid_field_scale']=t/sim_sol_conv
    #print(I)

    I.workdir = impactFolderPath
    I.verbose=True
    I.run()

    P1 = I.particles['L0AFEND'].copy()
    # P1 = P1.resample(100_000)
    P1.drift_to_z()
    P1.z[:] = 0
    P1.t[:] -= P1['mean_t']
    P1['mean_energy']
    
    P1.write(filePath+"/beams/"+"ImpactBeam.h5")

    if returnImpactObject:
        return I

    

    

def update_impact(I,settings=None,
               impact_config=None,
               verbose=False):
    
    I.verbose=verbose
    if settings:
        for key in settings:
            val = settings[key]
            if not key.startswith('distgen:'):
               # Assume impact
                if verbose:
                    print(f'Setting impact {key} = {val}')          
                I[key] = val                
   
    return I

def update_distgen(G,settings=None,verbose=False):
    G.verbose=verbose
    if settings:
        for key in settings:
            val = settings[key]
            if key.startswith('distgen:'):
                key = key[len('distgen:'):]
                if verbose:
                    print(f'Setting distgen {key} = {val}')
                G[key] = val
            
    
    # Get particles
    
    return G