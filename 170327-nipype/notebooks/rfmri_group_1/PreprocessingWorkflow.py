
# coding: utf-8

# In[1]:

# Import workflow elements
from nipype import Node, Workflow


# In[2]:

# Import necessary interfaces
from nipype.interfaces import fsl, afni


# In[19]:

#Define workflow and create nodes
wf = Workflow(name="group1_pre_process")
wf.base_dir = 'group1_results'

#Skullstrip
node_skull_strip = Node(fsl.BET(functional=True), name='bet')

#FLIRT
node_volreg = Node(fsl.MCFLIRT(), name='volreg')

#Volreg AFNI
node_afni_volreg = Node(afni.Volreg(), name='volreg_afni')



# In[20]:

#Connet nodes
wf.connect(node_skull_strip, 'out_file', node_volreg,'in_file')
wf.connect(node_skull_strip, 'out_file', node_afni_volreg,'in_file')


# In[21]:

node_afni_volreg.help()


# In[22]:

wf.inputs.bet.in_file = "/home/jovyan/work/data/ds000114/sub-01/func/sub-01_task-linebisection_bold.nii.gz"
wf.run()


# In[23]:

from IPython.display import Image
Image(wf.write_graph())


# In[ ]:




# In[ ]:



