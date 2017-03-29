
# coding: utf-8

# In[5]:

# Import workflow elements
from nipype import Node, Workflow
from nipype.interfaces import fsl


# In[6]:

# Import necessary interfaces
node_bet = Node(fsl.BET(functional=True), name='fsl_bet')
node_mcflirt =Node(preprocess.MCFLIRT(),name='custom_mcflirt')


# In[7]:

# Initiation of a workflow
wf = Workflow(name="group_workflow")


# In[8]:

# First the "simple", but more restricted method
wf.connect(node_bet, "out_file", node_mcflirt, "in_file")


# In[12]:

wf.inputs.fsl_bet.in_file='/home/jovyan/work/data/ds000114/sub-01/func/sub-01_task-fingerfootlips_bold.nii.gz'
wf.base_dir='/home/jovyan/work/outputs'


# In[13]:

wf.run()


# In[ ]:



