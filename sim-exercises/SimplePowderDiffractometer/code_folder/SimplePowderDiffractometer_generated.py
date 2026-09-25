#!/usr/bin/env python3
# Automatically generated file. 
# Format:    Python script code
# McStas <http://www.mcstas.org>
# Instrument: SimplePowderDiffractometer.instr (SimplePowderDIffractometer)
# Date:       Tue Sep 22 14:38:27 2026
# File:       SimplePowderDiffractometer_generated.py

import mcstasscript as ms

# Python McStas instrument description
def make(input_path=None):
    instr = ms.McStas_instr("SimplePowderDiffractometer_generated", author = "McCode Py-Generator", origin = "ESS DMSC", input_path=input_path)
    
# Add collected DEPENDENCY strings
    instr.set_dependency(' @NCRYSTALFLAGS@')

    # *****************************************************************************
    # * Start of instrument 'SimplePowderDIffractometer' generated code
    # *****************************************************************************
    # MCSTAS system dir is "/opt/miniforge/envs/DMSC-School/share/mcstas/resources/"


    # *****************************************************************************
    # * instrument 'SimplePowderDIffractometer' and components DECLARE
    # *****************************************************************************

    # Instrument parameters:

    lambda0 = instr.add_parameter('double', 'lambda0', value=1, comment='[AA]  The mean value of  incoming wavelegths (Gaussian distribution)')
    dlambda = instr.add_parameter('double', 'dlambda', value=0.005, comment='[AA] Gaussian sigma of incoming wavelength distribution')
    coll = instr.add_parameter('double', 'coll', value=120, comment='[arcmin] horizontal collimation')
    container = instr.add_parameter('int', 'container', value=0, comment='[1] When >0 a 2mm thick Al pressed powder can is inserted around the sample')
    sample = instr.add_parameter('int', 'sample', value=0, options=[0,1,2,3], comment='[1] 0=Ni, 1=Fe, 2=SiO2, 3=C_diamond, otherwise empty')

    component_definition_metadata = {
    }
    instr.append_declare(r'''
double L1=3;
double LC=1;
double sample_radius=0.005;
double sample_height=0.05;
double al_thickness=0.002;
char samplestring[128];
    ''')


    instr.append_initialize(r'''

if (sample==0) {
  sprintf(samplestring,"Ni.laz");
} else if (sample==1) {
  sprintf(samplestring,"Fe.laz");
} else if (sample==2) {
  sprintf(samplestring,"SiO2_quartza.laz");
} else if (sample==3) {
  sprintf(samplestring,"C_diamond.laz");
} else {
  sprintf(samplestring,"NULL");
}


    ''')


    # *****************************************************************************
    # * instrument 'SimplePowderDIffractometer' TRACE
    # *****************************************************************************
    
    # Comp instance Origin, placement and parameters
    Origin = instr.add_component('Origin','Progress_bar')
    
    Origin.profile = '"NULL"'
    Origin.percent = '10'
    Origin.flag_save = '0'
    Origin.minutes = '0'
    
    # Comp instance source, placement and parameters
    source = instr.add_component('source','Source_simple', AT=['0', '0', '0'], AT_RELATIVE='Origin', ROTATED=['0.0', '0.0', '0.0'], ROTATED_RELATIVE='Origin')
    
    source.radius = '0.1'
    source.yheight = '0'
    source.xwidth = '0'
    source.dist = 'L1'
    source.focus_xw = '2 * sample_radius + 2 * al_thickness'
    source.focus_yh = 'sample_height + 2 * al_thickness'
    source.E0 = '0'
    source.dE = '0'
    source.lambda0 = 'lambda0'
    source.dlambda = 'dlambda'
    source.flux = '5e10'
    source.gauss = '1'
    source.target_index = '1'
    
    # Comp instance collimator, placement and parameters
    collimator = instr.add_component('collimator','Collimator_linear', AT=['0', '0', 'LC'], AT_RELATIVE='source', ROTATED=['0.0', '0.0', '0.0'], ROTATED_RELATIVE='source')
    
    collimator.xmin = '-0.02'
    collimator.xmax = '0.02'
    collimator.ymin = '-0.05'
    collimator.ymax = '0.05'
    collimator.xwidth = '0.2'
    collimator.yheight = '0.2'
    collimator.length = '0.2'
    collimator.divergence = 'coll'
    collimator.transmission = '1'
    collimator.divergenceV = '0'
    
    # Comp instance entry_side, placement and parameters
    entry_side = instr.add_component('entry_side','PowderN', AT=['0', '0', 'L1'], AT_RELATIVE='source', ROTATED=['0.0', '0.0', '0.0'], ROTATED_RELATIVE='source')
    # WHEN ( container > 0 ) at entry_side
    entry_side.set_WHEN('( container > 0 )')
    
    entry_side.reflections = '"Al.laz"'
    entry_side.geometry = '"NULL"'
    entry_side.format = '{ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 }'
    entry_side.radius = 'sample_radius + al_thickness'
    entry_side.yheight = 'sample_height + 2 * al_thickness'
    entry_side.xwidth = '0'
    entry_side.zdepth = '0'
    entry_side.thickness = 'al_thickness'
    entry_side.pack = '1'
    entry_side.Vc = '0'
    entry_side.sigma_abs = '0'
    entry_side.sigma_inc = '0'
    entry_side.delta_d_d = '0'
    entry_side.p_inc = '0.1'
    entry_side.p_transmit = '0.8'
    entry_side.DW = '0'
    entry_side.nb_atoms = '1'
    entry_side.d_omega = '0'
    entry_side.d_phi = '2'
    entry_side.tth_sign = '0'
    entry_side.p_interact = '0.8'
    entry_side.concentric = '1'
    entry_side.density = '0'
    entry_side.weight = '0'
    entry_side.barns = '1'
    entry_side.Strain = '0'
    entry_side.focus_flip = '0'
    entry_side.target_index = '0'
    entry_side.order = '1'
    
    # Comp instance sample, placement and parameters
    sample = instr.add_component('sample','PowderN', AT=['0', '0', 'L1'], AT_RELATIVE='source', ROTATED=['0.0', '0.0', '0.0'], ROTATED_RELATIVE='source')
    
    sample.reflections = 'samplestring'
    sample.geometry = '"NULL"'
    sample.format = '{ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 }'
    sample.radius = 'sample_radius'
    sample.yheight = 'sample_height'
    sample.xwidth = '0'
    sample.zdepth = '0'
    sample.thickness = '0'
    sample.pack = '1'
    sample.Vc = '0'
    sample.sigma_abs = '-1'
    sample.sigma_inc = '-1'
    sample.delta_d_d = '0'
    sample.p_inc = '0'
    sample.p_transmit = '0.1'
    sample.DW = '0'
    sample.nb_atoms = '1'
    sample.d_omega = '0'
    sample.d_phi = '2'
    sample.tth_sign = '0'
    sample.p_interact = '0.8'
    sample.concentric = '0'
    sample.density = '0'
    sample.weight = '0'
    sample.barns = '1'
    sample.Strain = '0'
    sample.focus_flip = '0'
    sample.target_index = '0'
    sample.order = '1'
    
    # Comp instance exit_side, placement and parameters
    exit_side = instr.add_component('exit_side','PowderN', AT=['0', '0', 'L1'], AT_RELATIVE='source', ROTATED=['0.0', '0.0', '0.0'], ROTATED_RELATIVE='source')
    # WHEN ( container > 0 ) at exit_side
    exit_side.set_WHEN('( container > 0 )')
    
    exit_side.reflections = '"Al.laz"'
    exit_side.geometry = '"NULL"'
    exit_side.format = '{ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 }'
    exit_side.radius = 'sample_radius + al_thickness'
    exit_side.yheight = 'sample_height + 2 * al_thickness'
    exit_side.xwidth = '0'
    exit_side.zdepth = '0'
    exit_side.thickness = 'al_thickness'
    exit_side.pack = '1'
    exit_side.Vc = '0'
    exit_side.sigma_abs = '0'
    exit_side.sigma_inc = '0'
    exit_side.delta_d_d = '0'
    exit_side.p_inc = '0.1'
    exit_side.p_transmit = '0.8'
    exit_side.DW = '0'
    exit_side.nb_atoms = '1'
    exit_side.d_omega = '0'
    exit_side.d_phi = '2'
    exit_side.tth_sign = '0'
    exit_side.p_interact = '0.8'
    exit_side.concentric = '0'
    exit_side.density = '0'
    exit_side.weight = '0'
    exit_side.barns = '1'
    exit_side.Strain = '0'
    exit_side.focus_flip = '0'
    exit_side.target_index = '0'
    exit_side.order = '1'
    
    # Comp instance Detector, placement and parameters
    Detector = instr.add_component('Detector','Monitor_nD', AT=['0', '0', '0'], AT_RELATIVE='sample', ROTATED=['0', '0', '180'], ROTATED_RELATIVE='sample')
    
    Detector.user0 = '""'
    Detector.user1 = '""'
    Detector.user2 = '""'
    Detector.user3 = '""'
    Detector.user4 = '""'
    Detector.user5 = '""'
    Detector.user6 = '""'
    Detector.user7 = '""'
    Detector.user8 = '""'
    Detector.user9 = '""'
    Detector.xwidth = 'L1'
    Detector.yheight = '0.20'
    Detector.zdepth = '0'
    Detector.xmin = '0'
    Detector.xmax = '0'
    Detector.ymin = '0'
    Detector.ymax = '0'
    Detector.zmin = '0'
    Detector.zmax = '0'
    Detector.bins = '400'
    Detector.min = '20'
    Detector.max = '100'
    Detector.restore_neutron = '1'
    Detector.radius = '0'
    Detector.options = '"banana, theta"'
    Detector.filename = '"detector.dat"'
    Detector.geometry = '"NULL"'
    Detector.nowritefile = '0'
    Detector.nexus_bins = '0'
    Detector.username0 = '"NULL"'
    Detector.username1 = '"NULL"'
    Detector.username2 = '"NULL"'
    Detector.username3 = '"NULL"'
    Detector.username4 = '"NULL"'
    Detector.username5 = '"NULL"'
    Detector.username6 = '"NULL"'
    Detector.username7 = '"NULL"'
    Detector.username8 = '"NULL"'
    Detector.username9 = '"NULL"'
    
    # Instruct McStasscript not to 'check everythng'
    instr.settings(checks=False)
    return instr


if __name__ == '__main__':
    instr=make()
    # Use instr.settings() to add e.g. seed=1000, ncount=1e7, mpi=8, openacc=True, force_compile=False etc.)
    

# Show diagram
    instr.show_diagram()
    

# Visualise with default parameters (defaults to 'webgl-legacy' visualisation)
    instr.show_instrument()
    

# Generate a dataset with default parameters.
    data = instr.backengine()
    
# Overview plot:
    ms.make_sub_plot(data)
    

# Other useful commands follow...
    
# One plot pr. window
    #ms.make_plot(data)
    
# Load another dataset
    #data2 = ms.load_data('some_other_folder')
    
# Adjusting a specific plot
    #ms.name_plot_options("PSD_4PI", data, log=1, colormap="hot", orders_of_mag=5)
    

# Bring up the 'interface' - only relevant in Jupyter
    #%matplotlib widget
    #import mcstasscript.jb_interface as ms_widget
    #ms_widget.show(data)
    

# Bring up the simulation 'interface' - only relevant in Jupyter
    #%matplotlib widget
    #import mcstasscript.jb_interface as ms_widget
    #sim_widget = ms_widget.SimInterface(instr)
    #sim_widget.show_interface()
    

# Acessing data from the interface
    #data = sim_widget.get_data()


# end of generated Python code SimplePowderDiffractometer_generated.py 
