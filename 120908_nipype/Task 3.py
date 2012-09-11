# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Convert two DTI images and run DTIFit

# <codecell>

from glob import glob
from nipype.interfaces.dcm2nii import Dcm2nii
from nipype.interfaces.fsl import DTIFit, BET

import nipype.pipeline.engine as pe

# <markdowncell>


# ### Version 2: Mapnodes

# <codecell>

convert = pe.MapNode(Dcm2nii(), name='convert_dicom', iterfield=['source_names'])
skull_stripper = pe.MapNode(BET(mask=True), name = 'skull_stripper', iterfield=['in_file'])
dtifit = pe.MapNode(DTIFit(), name = 'dtifit', iterfield=['dwi','bvals', 'bvecs','mask'])

convert_flow = pe.Workflow(name = 'convert_and_fit_mapnode')
convert_flow.connect([(convert, dtifit, [('converted_files', 'dwi'),
                                         ('bvals', 'bvals'),
                                         ('bvecs', 'bvecs')]),
                      (convert, skull_stripper, [('converted_files', 'in_file')]),
                      (skull_stripper, dtifit, [('mask_file', 'mask')])
                      ])

# <codecell>

fl = glob('/opt/data/NIPYPE_DATA/2475376/session*/DTI_mx_137/*-0001.dcm')
convert_flow.inputs.convert_dicom.source_names = fl
convert_flow.base_dir = '/mnt/mydir/'

# <codecell>

from nipype.interfaces.io import DataGrabber, DataSink

# <codecell>

dg = pe.Node(DataGrabber(infields=['subject_id', 'session'], outfields=['diffusion']),
             name = 'datasource')
dg.inputs.base_directory = '/opt/data/NIPYPE_DATA/'
dg.inputs.template = '%s/session%d/DTI*/*-0001.dcm'
dg.inputs.subject_id = '2475376'
dg.inputs.session = [1, 2]

# <codecell>

convert_flow.connect(dg, 'diffusion', convert, 'source_names')

# <codecell>

ds = pe.Node(DataSink(), name='sinker')
ds.inputs.base_directory = '/mnt/mydir/outputs'
convert_flow.connect(skull_stripper, 'mask_file', ds, 'mask')
convert_flow.connect(dtifit, 'FA', ds, 'dti.@FA')
convert_flow.connect(dtifit, 'MD', ds, 'dti.@MD')

# <codecell>

dg.iterables = ('subject_id', ['2475376', '3313349',  '9630905'])

# <codecell>

eg = convert_flow.run(plugin='MultiProc', plugin_args={'n_procs': 2})

# <codecell>


