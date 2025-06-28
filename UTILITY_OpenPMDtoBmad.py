#This is E. Cropp's implementation, from https://github.com/ericcropp/OpenPMD_to_Bmad
import h5py
import pmd_beamphysics
import numpy as np
from pmd_beamphysics import ParticleGroup

# Look inside Bmad h5 file
def inspect_bmad_h5(filename):
    """
    Looks inside a bmad h5 file.
    Returns a dictionary ("x","y","Px","Py,"Pz","time","timeOffset","totalMomentum").


    Argument:
    filename -- string: full path to file to be inspected

    """
    P={}
    with h5py.File(filename,'r') as f:
        
        pp = pmd_beamphysics.readers.particle_paths(f)
        assert len(pp) == 1, f'Number of particle paths in {filename}: {len(pp)}'
        data = pmd_beamphysics.particles.load_bunch_data(f[pp[0]])

        P['x']=f[pp[0]]['position']['x'][()]
        P['y']=f[pp[0]]['position']['y'][()]
        # P['z']=f['data']['00001']['particles']['position']['z'][()]
        P['Px']=f[pp[0]]['momentum']['x'][()]
        P['Py']=f[pp[0]]['momentum']['y'][()]
        P['Pz']=f[pp[0]]['momentum']['z'][()]
        P['time']=f[pp[0]]['time'][()]
        P['timeOffset']=f[pp[0]]['timeOffset'][()]
        # P['totalMomentum']=f[pp[0]]['totalMomentum'][()]
       
    return P

def all_keys(obj):
    """
    Returns a tuple of all keys in the h5 file.

    
    Argument:
    obj  -- h5 object: contents of an h5 file

    See: https://stackoverflow.com/questions/59897093/get-all-keys-and-its-hierarchy-in-h5-file-using-python-library-h5py
    """
    keys=(obj.name,)
    if isinstance(obj, h5py.Group):
        for key, value in obj.items():
            if isinstance(value, h5py.Group):
                keys=keys+all_keys(value)
            else:
                keys=keys+(value.name,)
    return keys

def all_attr_keys(keys, obj):
    """
    Returns a dictionary (keys, metadata) of metadata attributes.

    
    Argument:
    obj -- h5 object: contents of an h5 file
    keys -- tuple of keys

    """
    attr_keys={}
    for key in keys:
        attr_keys[key]=list(obj[key].attrs.keys())
    return attr_keys

def search_list_partial(l,searchterm):
    """
    See if a search term is present in a list of lists
    
    Returns bool -- True if searchterm is in l.

    
    Argument:
    l -- list of list of terms
    searchterm -- string: term to search for in list of lists

    """
    x=[True for v in l if searchterm in v]
    if True in x:
        y=True
    else: 
        y=False
    return y

def OpenPMD_to_Bmad(filename,tOffset=None,species='electron'):
    """
    Convert from OpenPMD to Bmad h5 format after checking to make sure it is not in Bmad format first
    
    Edits h5 file, but does not return any variables

    
    Argument:
    filename -- string: full path to file to be changed
    tOffset -- 1-D np.array: timeOffset from previous bmad file
    
    """
    with h5py.File(filename,'r+') as f: # Open h5 file for writing
        
        #Make sure this is an OpenPMD file
        keys=all_keys(f)
        attr_keys=all_attr_keys(keys,f)
        list_attrs=[k for i in attr_keys.values() for k in i]
        keys=list(keys)
        
        test_openPMD=search_list_partial(list_attrs,'openPMD')
        # print(test_openPMD)
        
        if test_openPMD==True:
            #Check if it has a timeOffset group
            
            test_offset=search_list_partial(keys,'timeOffset')
            # print(test_offset)
            if test_offset==True:
                raise ValueError('openPMD file already includes timeOffset!')
            else:
                # Get data about particle status and paths (from OpenPMD library)
                pp = pmd_beamphysics.readers.particle_paths(f)
                assert len(pp) == 1, f'Number of particle paths in {filename}: {len(pp)}'
                pp[0] = pp[0] + '/' + species
                data = pmd_beamphysics.particles.load_bunch_data(f[pp[0]])
                
                
                # filter and do calculations
                idx=np.array(data['status'])==1
                
                # Check tOffset
                if tOffset is not None:
                    tOffset=np.array(tOffset)
                    assert len(np.shape(tOffset))==1,"tOffset not valid"
                    assert len(tOffset)==len(np.array(f[pp[0]]['time'])), "tOffset has wrong length"
                
                # If no offset is provided
                if tOffset is None:
                    weights=data['weight']
                    if len(f[pp[0]]['time'])==0:
                        if os.path.isfile('drifted_'+filename):
                            raise ValueError("No time data exists, but drift_to_z() does not resolve the issue")
                        else:
                            P_1 = ParticleGroup(filename)
                            P_1.drift_to_z()
                            P_1.write('drifted_'+filename)
                            
                            OpenPMD_to_Bmad('drifted_'+filename)
                            os.rename(('drifted_'+filename),filename)
                            return
                        
                    tref=np.average(np.array(f[pp[0]]['time'])[idx],weights=weights[idx])

                #Otherwise just use that
                else:
                    tref=tOffset
                    
                t1=np.array(f[pp[0]]['time'])-tref
                
                # Write timeOffset and metadata
                f[pp[0]]['timeOffset']=np.zeros(len(t1))+tref
                for key in f[pp[0]]['time'].attrs.keys():

                    f[pp[0]]['timeOffset'].attrs[key]=f[pp[0]]['time'].attrs[key]
                    
                # Update time 
                f[pp[0]]['time'][...]=t1
                
                
        else:
            raise ValueError('Not an OpenPMD File!')
            
# Get time offset and convert h5 file from bmad to OpenPMD          
def bmad_to_OpenPMD(filename):
    """
    Get time offset and convert h5 file from bmad to OpenPMD      
    
    Edits h5 file, returns a dictionary as specified in inspect_bmad_h5

    
    Argument:
    filename -- string: full path to file to be read and changed
    
    """
    Pdict=inspect_bmad_h5(filename)
    P=ParticleGroup(filename)
    P.drift_to_z()
    P.write(filename)
    return Pdict