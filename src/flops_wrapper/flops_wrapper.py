"""
OpenMDAO Wrapper for Flops


This wrapper is based on the ModelCenter Java wrapper, version 2.00 Beta 
and version 0.13 OpenMDAO wrapper
"""



from __future__ import print_function

#from namelist_util import Namelist/
from openmdao.util.namelist_util import Namelist, ToBool

from openmdao.api import Component
from openmdao.api import ExternalCode
from numpy import int64 as numpy_int64
from numpy import float64 as numpy_float64
from numpy import str as numpy_str
from numpy import zeros, array,ndarray,size
from openmdao.core.problem import Problem
from openmdao.core.group import Group
from openmdao.util.file_wrap import FileParser
import sys
from six import iteritems, itervalues, iterkeys
import os
import numpy as np
dirname = os.path.dirname(os.path.abspath(__file__))


    
class FlopsWrapper(ExternalCode):
    """Wrapper for FlopsWrapper"""
    def __init__(self):
        '''Constructor for the FlopsWrapper component'''
        super(FlopsWrapper,self).__init__()
        
        self.add_output('output:ERROR',val='none',pass_by_obj=True)
        self.add_output('output:HINT',val='none',pass_by_obj=True)

        self.add_param('input:missin:Basic:npcon',val=0, iotype='in', desc='Number of PCONIN namelists to be created',pass_by_obj=True)

        self.nseg = 0
        self.npcons = []



        self.add_param('input:title',val='none',typeVar='Str',pass_by_obj=True)#adding title for namecards
        self.loadInputVars()
        #top = Problem()
        #top.root =  Group()
        #top.root.add('my_flops',self)
        #top.setup(check=False)
        self.setInputOutput()


        # This stuff is global in the Java wrap.
        # These are used when adding and removing certain segments.
        self.nseg0 = 0
        self.npcon0 = 0
        self.nrern0 = 0
        self.npcons0 = []
        self.npcons0.append(0)
        self.nmseg = 0


    def solve_nonlinear(self,params,unknowns,resids):
      
        self.generate_input() 
        super(FlopsWrapper,self).solve_nonlinear(params,unknowns,resids)
        self.parse_output()



    def setInputOutput(self,input_filepath='flops.inp',output_filepath='flops.out',flops_exec='flops'):
        # External Code public variables

        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.flops_exec=flops_exec
        #self.stderr = 'flops.err'

        #self.options['external_input_files'] = [self.input_filepath]
        #self.options['external_output_files'] = [self.output_filepath]
        #self.options['command'] = ['flops',self.input_filepath,self.output_filepath]
        self.options['command']=['python',dirname+'/local_flops.py',self.flops_exec,self.input_filepath,self.output_filepath]

    '''functions to manipulate inputs before setup()'''
    def assignValue(self,variable,value,index=None):
            #support the modification of input variables before calling setup
            #comp -> component
            # variable is  a string
            if hasattr(self.params, 'keys'):
                if index==None:
                    self.params[variable]=value
                else:
                    self.params[variable][index]=value
            else:
                if index==None:
                    self._init_params_dict[variable]['val']=value
                else:
                    self._init_params_dict[variable]['val'][index]=value

    def getValue(self,variable,output=False):
            #support the modification of input variables before calling setup
            #comp -> component

            if hasattr(self.params, 'keys'):
                val = self.params[variable]
            else:
                val = self._init_params_dict[variable]['val']
            return val

    '''functions to manipulate outputs before setup()'''
    def assignValueOutput(self,variable,value,index=None):
            #support the modification of input variables before calling setup
            # variable is  a string
            if hasattr(self.params, 'keys'):
                if index==None:
                    self.unknowns[variable]=value
                else:
                    self.unknowns[variable][index]=value
            else:
                if index==None:
                    self._unknowns_dict[variable]['val']=value
                else:
                    self._unknowns_dict[variable]['val'][index]=value


    def getValueOutput(self,variable,output=False):
            #support the modification of input variables before calling setup

            if hasattr(self.unknowns, 'keys'):
                val = self.unknowns[variable]
            else:
                val = self._unknowns_dict[variable]['val']
            return val

    def remove_container(self,name):
            #support the modification of input variables before calling setup
            #This should only be used before setup().
            boolPrint = True
            for key in self._params_dict.keys():
                if name in key:
                    del self._params_dict[key]
                    boolPrint = False
            if boolPrint==True:
                print("Warning in flops_wrapper.py->remove_container.\nNo container to remove")

    '''define output variables'''
    def loadOutputVars(self):
                
        self.FlopsWrapper_output_Weight_Wing()
        self.FlopsWrapper_output_Weight_Inertia()
        self.FlopsWrapper_output_Weight()
        self.FlopsWrapper_output_Plot_Files()
        self.FlopsWrapper_output_Performance_Segments()
        self.FlopsWrapper_output_Performance_Constraints()
        self.FlopsWrapper_output_Performance()
        self.FlopsWrapper_output_Payload()
        self.FlopsWrapper_output_Noise()
        self.FlopsWrapper_output_Geometry_BWB()
        self.FlopsWrapper_output_Geometry()
        self.FlopsWrapper_output_Engine()
        self.FlopsWrapper_output_Econ()



    def FlopsWrapper_output_Weight_Wing(self):
        """Container for output.Weight.Wing"""
        strChain = "output:Weight:Wing:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'w',val=0.0, desc='Bending material factor. For detailed wing definition, this factor is calculated by numerical integration along the specified load path to determine the amount of bending material required to support an elliptical load distribution.  The wing is treated as an idealized beam with dimensions proportional to the wing local chord and thickness. The bending factor is modified for aeroelastic penalties (flutter, divergence, and aeroelastic loads) depending on wing sweep (including forward), aspect ratio, degree of aeroelastic tailoring, and strut bracing, if any.  These modifications are based on a curve fit of the results of a study performed using the Aeroelastic Tailoring and Structural Optimization (ATSO) code to structurally optimize a large matrix of wings.\n\nIf the detailed wing definition is not used, an equivalent bending factor is computed assuming a trapezoidal wing with constant t/c.',typeVar='Float')
        self.add_output(strChain+'ew',val=0.0, desc='Engine inertia relief factor.',typeVar='Float')
        self.add_output(strChain+'w1',val=0.0, desc='The first term in the wing weight is the bending factor. It is adjusted for inertia relief for the wing itself and for any engines on the wing.',typeVar='Float')
        self.add_output(strChain+'w2',val=0.0, desc='The second term represents control surfaces and shear material.  According to structural and statistical studies conducted during weight module development, the weight of spars and ribs depends almost entirely on control surfaces.  The amount of shear material required to carry structural loads is not critical.',typeVar='Float')
        self.add_output(strChain+'w3',val=0.0, desc='The third term depends entirely on wing area and covers multitude of miscellaneous items.',typeVar='Float')


    def FlopsWrapper_output_Weight_Inertia(self):
        """Container for output.Weight.Inertia"""
        strChain = "output:Weight:Inertia:"

        inrtia = self.getValue("input:wtin:Inertia:inrtia")

        if inrtia>0:
            nfcon = self.getValue("input:wtin:Inertia:tf").shape[0]
            # OpenMDAO Public Variables
            self.add_output(strChain+'cgx',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'cgy',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'cgz',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxroll',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxptch',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxyaw',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixz',val=zeros(1+nfcon),typeVar='Array,Float',pass_by_obj=True)
        else:
            # OpenMDAO Public Variables
            self.add_output(strChain+'cgx',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'cgy',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'cgz',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxroll',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxptch',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixxyaw',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)
            self.add_output(strChain+'ixz',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)


    def FlopsWrapper_output_Weight(self):
        """Container for output.Weight"""
        strChain = "output:Weight:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'dowe',val=0.0,typeVar='Float')
        self.add_output(strChain+'paylod',val=0.0,typeVar='Float')
        self.add_output(strChain+'fuel',val=0.0,typeVar='Float')
        self.add_output(strChain+'rampwt',val=0.0,typeVar='Float')
        self.add_output(strChain+'wsr',val=0.0,typeVar='Float')
        self.add_output(strChain+'thrso',val=0.0,typeVar='Float')
        self.add_output(strChain+'esf',val=0.0,typeVar='Float')
        self.add_output(strChain+'twr',val=0.0,typeVar='Float')
        self.add_output(strChain+'wldg',val=0.0,typeVar='Float')
        self.add_output(strChain+'fultot',val=0.0,typeVar='Float')
        self.add_output(strChain+'exsful',val=0.0,typeVar='Float')
        self.add_output(strChain+'frwi',val=0.0,typeVar='Float')
        self.add_output(strChain+'frht',val=0.0,typeVar='Float')
        self.add_output(strChain+'frvt',val=0.0,typeVar='Float')
        self.add_output(strChain+'frfin',val=0.0,typeVar='Float')
        self.add_output(strChain+'frcan',val=0.0,typeVar='Float')
        self.add_output(strChain+'frfu',val=0.0,typeVar='Float')
        self.add_output(strChain+'wlg',val=0.0,typeVar='Float')
        self.add_output(strChain+'frna',val=0.0,typeVar='Float')
        self.add_output(strChain+'wengt',val=0.0,typeVar='Float')
        self.add_output(strChain+'wthr',val=0.0,typeVar='Float')
        self.add_output(strChain+'wpmisc',val=0.0,typeVar='Float')
        self.add_output(strChain+'wfsys',val=0.0,typeVar='Float')
        self.add_output(strChain+'frsc',val=0.0,typeVar='Float')
        self.add_output(strChain+'wapu',val=0.0,typeVar='Float')
        self.add_output(strChain+'win',val=0.0,typeVar='Float')
        self.add_output(strChain+'whyd',val=0.0,typeVar='Float')
        self.add_output(strChain+'welec',val=0.0,typeVar='Float')
        self.add_output(strChain+'wavonc',val=0.0,typeVar='Float')
        self.add_output(strChain+'wfurn',val=0.0,typeVar='Float')
        self.add_output(strChain+'wac',val=0.0,typeVar='Float')
        self.add_output(strChain+'wai',val=0.0,typeVar='Float')
        self.add_output(strChain+'wempty',val=0.0,typeVar='Float')
        self.add_output(strChain+'wflcrbw',val=0.0,typeVar='Float')
        self.add_output(strChain+'wwstuab',val=0.0,typeVar='Float')
        self.add_output(strChain+'wuf',val=0.0,typeVar='Float')
        self.add_output(strChain+'woil',val=0.0,typeVar='Float')
        self.add_output(strChain+'wsrv',val=0.0,typeVar='Float')
        self.add_output(strChain+'zfw',val=0.0,typeVar='Float')
        self.add_output(strChain+'wbomb',val=0.0,typeVar='Float')

        '''Not declared in old FLOPS wrapper'''
        #self.add_output(strChain+'thrsop',val=zeros(0),typeVar='Array,Float',pass_by_obj=True)


    def FlopsWrapper_output_Plot_Files(self): 
        """Container for output.Plot_Files"""

        '''From old FLOPS wrapper'''
        # OpenMDAO Public Variables
        # TODO - Do we really need to read these in every time? Let's not for now.
        #cnfile = File(iotype='out', desc='Contour or thumbprint plot data file')
        #msfile = File(iotype='out', desc='Mission summary data file')
        #crfile = File(iotype='out', desc='Cruise schedule summary data file')
        #tofile = File(iotype='out', desc='Takeoff and landing aerodynamic and thrust data file')
        #nofile = File(iotype='out', desc='Takeoff and climb profile data file')
        #apfile = File(iotype='out', desc='Drag polar plot data file')
        #thfile = File(iotype='out', desc='Engine plot data file name')
        #hsfile = File(iotype='out', desc='Design history plot file')
        #psfile = File(iotype='out', desc='Excess power and load factor plot data file')


    def FlopsWrapper_output_Performance_Segments(self):
        """Container for output.Performance.Segments"""
        strChain = "output:Performance:Segments:"
        mission = self.getValue("input:mission_definition:mission")
        mission = ' '.join(mission)#list is now a string. Each list element is separated by a space

        ianal  = self.getValue("input:option:Program_Control:ianal")
        msumpt = self.getValue("input:missin:Basic:msumpt")

        if ianal==3 and msumpt>0:
            local_nmseg = mission.count('CLIMB') + mission.count('CRUISE') + \
                         mission.count('REFUEL') + mission.count('RELEASE') + \
                         mission.count('ACCEL') + mission.count('TURN') + \
                         mission.count('COMBAT') + mission.count('HOLD') + \
                         mission.count('DESCENT')
            # OpenMDAO Public Variables
            self.add_output(strChain+'segment',val=array(['']*(local_nmseg),dtype='<S20'),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weights',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alts',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'machs',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'thrusts',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'totmaxs',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'lods',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'ex_pow',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'sfcs',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'engparms',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weighte',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alte',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'mache',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'thruste',val=zeros(local_nmseg),typeVar='Array,float',pass_by_obj=True)
            self.add_output(strChain+'totmaxe',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'lode',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'sfce',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'engparme',val=zeros(local_nmseg),typeVar='Array',pass_by_obj=True)

        else:
            # OpenMDAO Public Variables
            self.add_output(strChain+'segment',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weights',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alts',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'machs',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'thrusts',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'totmaxs',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'ex_pow',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'lods',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'sfcs',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'engparms',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weighte',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alte',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'mache',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'thruste',val=array([]),typeVar='Array,float',pass_by_obj=True)
            self.add_output(strChain+'totmaxe',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'lode',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'sfce',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'engparme',val=array([]),typeVar='Array',pass_by_obj=True)



    def FlopsWrapper_output_Performance_Constraints(self):
        """Container for output.Performance.Constraints"""
        strChain = "output:Performance:Constraints:"
        ianal  = self.getValue("input:option:Program_Control:ianal")
        # OpenMDAO Public Variables
        if self.npcon0 > 0 and ianal == 3:
            self.add_output(strChain+'constraint',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'value',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'units',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'limit',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weight',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'mach',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alt',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'g',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'location',val=zeros(self.npcon0),typeVar='Array',pass_by_obj=True)
        else:
            self.add_output(strChain+'constraint',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'value',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'units',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'limit',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'weight',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'mach',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'alt',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'g',val=zeros(0),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'location',val=zeros(0),typeVar='Array',pass_by_obj=True)
  




    def FlopsWrapper_output_Performance(self):
        """Container for output.Performance"""
        strChain = "output:Performance:"
    # OpenMDAO Public Variables
        self.add_output(strChain+'fuel',val=0.0,typeVar='Float')
        self.add_output(strChain+'range',val=0.0,typeVar='Float')
        self.add_output(strChain+'vapp',val=0.0,typeVar='Float')
        self.add_output(strChain+'taxofl',val=0.0,typeVar='Float')
        self.add_output(strChain+'faroff',val=0.0,typeVar='Float')
        self.add_output(strChain+'farldg',val=0.0,typeVar='Float')
        self.add_output(strChain+'amfor',val=0.0,typeVar='Float')
        self.add_output(strChain+'ssfor',val=0.0,typeVar='Float')
        self.add_output(strChain+'esf',val=0.0,typeVar='Float')
        self.add_output(strChain+'thrso',val=0.0,typeVar='Float')
        self.add_output(strChain+'vmmo',val=0.0,typeVar='Float')



    def FlopsWrapper_output_Payload(self):
        """Container for output.Payload"""
        strChain = "output:Payload:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'npf',val=0,typeVar='Int')
        self.add_output(strChain+'npb',val=0,typeVar='Int')
        self.add_output(strChain+'npt',val=0,typeVar='Int')
        self.add_output(strChain+'nstu',val=0,typeVar='Int')
        self.add_output(strChain+'ngalc',val=0,typeVar='Int')
        self.add_output(strChain+'nflcr',val=0,typeVar='Int')
        self.add_output(strChain+'nstuag',val=0,typeVar='Int')
        self.add_output(strChain+'wppass',val=0.0,typeVar='Float')
        self.add_output(strChain+'bpp',val=0.0,typeVar='Float')
        self.add_output(strChain+'cargow',val=0.0,typeVar='Float')
        self.add_output(strChain+'cargof',val=0.0,typeVar='Float')
        self.add_output(strChain+'wcon',val=0.0,typeVar='Float')


    def FlopsWrapper_output_Noise(self):
        """Container for output.Noise"""
        strChain = "output:Noise:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'nsplot',val='', msg='Noise output filename',typeVar='Str')


    def FlopsWrapper_output_Geometry_BWB(self):
        """Container for output:Geometry:BWB"""
        strChain = "output:Geometry:BWB:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'xlp',val=0.0, units='ft', desc='Length of centerline',typeVar='Float')
        self.add_output(strChain+'xlw',val=0.0, units='ft', desc='Length of side wall',typeVar='Float')
        self.add_output(strChain+'wf',val=0.0, units='ft', desc='Width of cabin',typeVar='Float')
        self.add_output(strChain+'acabin',val=0.0, units='ft*ft', desc='Cabin area',typeVar='Float')
        self.add_output(strChain+'nbaw',val=0, desc='Number of bays',typeVar='Int')
        self.add_output(strChain+'bayw',val=0.0, units='ft', desc='Width of bay',typeVar='Float')
        self.add_output(strChain+'nlava',val=0, desc='NUMBER OF LAVATORIES',typeVar='Int')
        self.add_output(strChain+'ngally',val=0, desc='Number of galleys',typeVar='Int')
        self.add_output(strChain+'nclset',val=0, desc='Number of closets',typeVar='Int')
        self.add_output(strChain+'xl',val=0.0, units='ft', desc='Total fuselage length',typeVar='Float')
        self.add_output(strChain+'df',val=0.0, units='ft', desc='Fuselage maximum depth',typeVar='Float')


    def FlopsWrapper_output_Geometry(self):
        """Container for output.Geometry"""
        strChain="output:Geometry:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'xl',val=0.0,typeVar='Float')
        self.add_output(strChain+'wf',val=0.0,typeVar='Float')
        self.add_output(strChain+'df',val=0.0,typeVar='Float')
        self.add_output(strChain+'xlp',val=0.0,typeVar='Float')
        self.add_output(strChain+'ar',val=0.0,typeVar='Float')
        self.add_output(strChain+'sw',val=0.0,typeVar='Float')
        self.add_output(strChain+'tr',val=0.0,typeVar='Float')
        self.add_output(strChain+'sweep',val=0.0,typeVar='Float')
        self.add_output(strChain+'tca',val=0.0,typeVar='Float')
        self.add_output(strChain+'span',val=0.0,typeVar='Float')
        self.add_output(strChain+'glov',val=0.0,typeVar='Float')
        self.add_output(strChain+'sht',val=0.0,typeVar='Float')
        self.add_output(strChain+'svt',val=0.0,typeVar='Float')
        self.add_output(strChain+'xnac',val=0.0,typeVar='Float')
        self.add_output(strChain+'dnac',val=0.0,typeVar='Float')
        self.add_output(strChain+'xmlg',val=0.0,typeVar='Float')
        self.add_output(strChain+'xnlg',val=0.0,typeVar='Float')

 


    def FlopsWrapper_output_Engine(self):
        """Container for output.Engine"""
        strChain="output:Engine:"
        # OpenMDAO Public Variables
        self.add_output(strChain+'ofile',val='',typeVar='Str')
        self.add_output(strChain+'eofile',val='',typeVar='Str')
        self.add_output(strChain+'anopp',val='',typeVar='Str')
        self.add_output(strChain+'footpr',val='',typeVar='Str')
        self.add_output(strChain+'pltfil',val='',typeVar='Str')



    def FlopsWrapper_output_Econ(self):
        """Container for output.Econ"""
        strChain="output:Econ:"
        ianal  = self.getValue("input:option:Program_Control:ianal")
        noffdr = size(self.getValue("input:missin:Basic:offdr"))
        if ianal == 3:
            ndim = 1 + noffdr + self.nrern0
            # OpenMDAO Public Variables
            self.add_output(strChain+'sl',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockt',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockf',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockNx',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'wpayl',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'wgross',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'range',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'vapp',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'faroff',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'farldg',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'amfor',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'ssfor',val=zeros(ndim),typeVar='Array',pass_by_obj=True)
        else:
            # OpenMDAO Public Variables
            self.add_output(strChain+'sl',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockt',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockf',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'blockNx',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'wpayl',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'wgross',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'range',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'vapp',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'faroff',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'farldg',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'amfor',val=array([]),typeVar='Array',pass_by_obj=True)
            self.add_output(strChain+'ssfor',val=array([]),typeVar='Array',pass_by_obj=True)





    def loadInputVars(self):
        # adding input variables to the model
        #aerin 

        self.FlopsWrapper_input_aerin_Takeoff_Landing()
        self.FlopsWrapper_input_aerin_Internal_Aero()
        self.FlopsWrapper_input_aerin_Basic()

        #aero_data
        self.FlopsWrapper_input_aero_data()

        #asclin
        self.FlopsWrapper_input_asclin()

        #confin
        self.FlopsWrapper_input_confin_Basic()
        self.FlopsWrapper_input_confin_Objective()
        self.FlopsWrapper_input_confin_Design_Variables()

        #costin
        self.FlopsWrapper_input_costin_Mission_Performance()
        self.FlopsWrapper_input_costin_Cost_Technology()
        self.FlopsWrapper_input_costin_Basic()

        #engdin
        self.FlopsWrapper_input_engdin_Special_Options()
        self.FlopsWrapper_input_engdin_Basic()
        self.FlopsWrapper_input_engdin()

        #engine
        self.FlopsWrapper_input_engine_Other()
        self.FlopsWrapper_input_engine_Noise_Data()
        self.FlopsWrapper_input_engine_IC_Engine()
        self.FlopsWrapper_input_engine_Engine_Weight()
        self.FlopsWrapper_input_engine_Design_Point()
        self.FlopsWrapper_input_engine_Basic()
        self.FlopsWrapper_input_engine()

        #enginedeck
        self.FlopsWrapper_input_engine_deck()

        #fusein
        self.FlopsWrapper_input_fusein_Basic()
        self.FlopsWrapper_input_fusein_BWB()


        #missin
        self.FlopsWrapper_input_missin_User_Weights()
        self.FlopsWrapper_input_missin_Turn_Segments()
        self.FlopsWrapper_input_missin_Store_Drag()
        self.FlopsWrapper_input_missin_Reserve()
        self.FlopsWrapper_input_missin_Ground_Operations()
        self.FlopsWrapper_input_missin_Descent()
        self.FlopsWrapper_input_missin_Cruise()
        self.FlopsWrapper_input_missin_Climb()
        self.FlopsWrapper_input_missin_Basic()
    
        #mission_definition
        self.FlopsWrapper_input_mission_definition()

        #nacell
        self.FlopsWrapper_input_nacell()

        #noisin
        self.FlopsWrapper_input_noisin_Turbine()
        self.FlopsWrapper_input_noisin_Shielding()
        self.FlopsWrapper_input_noisin_Propeller()
        self.FlopsWrapper_input_noisin_Propagation()
        self.FlopsWrapper_input_noisin_Observers()
        self.FlopsWrapper_input_noisin_MSJet()
        self.FlopsWrapper_input_noisin_Jet()
        self.FlopsWrapper_input_noisin_Ground_Effects()
        self.FlopsWrapper_input_noisin_Flap_Noise()
        self.FlopsWrapper_input_noisin_Fan()
        self.FlopsWrapper_input_noisin_Engine_Parameters()
        self.FlopsWrapper_input_noisin_Core()
        self.FlopsWrapper_input_noisin_Basic()
        self.FlopsWrapper_input_noisin_Airframe()

        #option
        self.FlopsWrapper_input_option_Program_Control()
        self.FlopsWrapper_input_option_Plot_Files()
        self.FlopsWrapper_input_option_Excess_Power_Plot()
        
        #proin
        self.FlopsWrapper_input_proin()

        #rfhin
        self.FlopsWrapper_input_rfhin()

        #syntin
        self.FlopsWrapper_input_syntin_Variables()
        self.FlopsWrapper_input_syntin_Optimization_Control()

        #tolin
        self.FlopsWrapper_input_tolin_Thrust_Reverser()
        self.FlopsWrapper_input_tolin_Takeoff()
        self.FlopsWrapper_input_tolin_Landing()
        self.FlopsWrapper_input_tolin_Integration_Intervals()
        self.FlopsWrapper_input_tolin_Basic()

        #wtin
        self.FlopsWrapper_input_wtin_Wing_Data()
        self.FlopsWrapper_input_wtin_Tails_Fins()
        self.FlopsWrapper_input_wtin_Propulsion()
        self.FlopsWrapper_input_wtin_Override()
        self.FlopsWrapper_input_wtin_OEW_Calculations()
        self.FlopsWrapper_input_wtin_Landing_Gear()
        self.FlopsWrapper_input_wtin_Inertia()
        self.FlopsWrapper_input_wtin_Fuselage()
        self.FlopsWrapper_input_wtin_Fuel_System()
        self.FlopsWrapper_input_wtin_Detailed_Wing()
        self.FlopsWrapper_input_wtin_Crew_Payload()
        self.FlopsWrapper_input_wtin_Center_of_Gravity()
        self.FlopsWrapper_input_wtin_Basic()


    def FlopsWrapper_input_option_Plot_Files(self):
        """Container for input:option:Plot_Files"""
        strChain = 'input:option:Plot_Files:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ixfl',val=0,optionsVal=(0,1), desc='Generate mission summary plot files', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj = True)
        self.add_param(strChain+'npfile',val=0,optionsVal=(0,1,2), desc='Output takeoff and climb profiles for use with ANOPP preprocessor (andin)', aliases=('No', 'Yes', 'XFlops'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'lpfile',val=0,optionsVal=(0,1), desc='Approach and Landing Profile File for Noise Calculations (LPROF) 1, Detailed approach and landing profiles will be output on file LOFILE for use with ANOPP preprocessor. = 0, Otherwise',typeVar='Enum',pass_by_obj=True)

        self.add_param(strChain+'ipolp',val=0,optionsVal=(0,1,2), desc='Drag polar plot data', aliases=('None', 'Drag polars at existing Mach numbers', 'User specified Mach numbers'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'polalt',val=0.0, units='ft', desc='Altitude for drag polar plots',typeVar='Float')
        self.add_param(strChain+'nmach',val=0, desc=' Number of input Mach numbers for IPOLP = 2',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'pmach',val=array([]), desc='Mach numbers for drag polar plot data',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ipltth',val=0,optionsVal=(0,1,2), desc='Generate engine plot data', aliases=('None', 'Initial engine', 'Final scaled engine'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iplths',val=0,optionsVal=(0,1), desc='Design history plot data', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'cnfile',val='', desc='Contour or thumbprint plot data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'msfile',val='', desc='Mission summary data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'crfile',val='', desc='Cruise schedule summary data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'tofile',val='', desc='Takeoff and landing aerodynamic and thrust data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'nofile',val='', desc='Takeoff and climb profile data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'apfile',val='', desc='Drag polar plot data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'thfile',val='', desc='Engine plot data filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'hsfile',val='', desc='Design history plot filename',typeVar='Str',pass_by_obj=True)
        self.add_param(strChain+'psfile',val='', desc='Excess power and load factor plot data filename',typeVar='Str',pass_by_obj=True)





    def add_segin(self):
        """Adds a new SEGIN namelist."""

        name = "input:segin" + str(self.nseg0)+":"
        self.nseg0 += 1


        self.add_param(name+'key', val='CHAN', desc="Key word specifying reason for end of segment",typeVar="Str",pass_by_obj=True)
        self.add_param(name+'nflap', val=-1, desc="Number of drag polar to use\nIf NFLAP = -1, default value or previous value is used",typeVar='Str',pass_by_obj=True)
        self.add_param(name+'ifix', val=-1, desc="Constraints for climb segments after OBSTACLE\nIf IFIX = 0, default value or previous value is used" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'engscl', val=-1., desc="Engine setting as a fraction of thrust at IPCMAX\nIf ENGSCL = -1., default value or previous value is used" ,typeVar='Float')
        self.add_param(name+'afix', val=-10., units='deg', desc="Fixed angle of attack for IFIX = 3 or 6\nIf AFIX = -10., final value from previous segment is used" ,typeVar='Float')
        self.add_param(name+'gfix', val=-10., units='deg', desc="Fixed flight path angle for IFIX = 2 or 4, or fixed cabin floor angle for IFIX = 5\nIf GFIX = -10., final value from previous segment is used" ,typeVar='Float')
        self.add_param(name+'vfix', val=-1., units='nmi/h', desc="Fixed velocity for IFIX = 1, 4 or 6\nIf VFIX = -1., final value from previous segment is used" ,typeVar='Float')
        self.add_param(name+'hstop', val=-1., units='ft', desc="Segment termination altitude\nIf HSTOP = -1., default value is used" ,typeVar='Float')
        self.add_param(name+'dstop', val=-1., units='ft', desc="Segment termination distance\nIf DSTOP = -1., value from following segment is used" ,typeVar='Float')
        self.add_param(name+'tstop', val=-1., units='s', desc="Segment termination time\nIf TSTOP = -1., value from following segment is used" ,typeVar='Float')
        self.add_param(name+'vstop', val=-1., units='nmi/h', desc="Segment termination velocity\nIf VSTOP = -1., default value is used" ,typeVar='Float')
        self.add_param(name+'hmin', val=-1., units='ft', desc="Minimum altitude for segment termination; overrides STOP variables above\nIf HMIN = -1., value is not used" ,typeVar='Float')
        self.add_param(name+'sprate', val=-1., desc="Thrust reduction rate during segments where the power setting is reduced\nIf SPRATE = -1., default value or previous value is used" ,typeVar='Float')
        self.add_param(name+'iplr', val=-1, desc="Programmed lapse rate switch for this segment\nIf IPLR = -1, default value is used" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'noycal', val=-1, desc="Noise calculation switch - available only for simplified noise calculations in DOSS version\nIf NOYCAL = -1, default value is used" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'delt', val=-1., units='s', desc="Time step for post OBSTACLE segments\nIf DELT = -1., default value is used" ,typeVar='Float')
        self.add_param(name+'grdaeo', val=-1., units='deg', desc="Flight path angle for CUTBACK with all engines operating\nIf GRDAEO = -1., default value is used" ,typeVar='Float')
        self.add_param(name+'grdoeo', val=-1., units='deg', desc="Flight path angle for CUTBACK with one engine out\nIf GRDOEO = -1., default value is used",typeVar='Float')

    def remove_segin(self):
        """Removes a SEGIN namelist. Actually, it removes the most recently added SEGIN, as per the MC wrapper."""

        if self.nseg0 == 0:
            raise RuntimeError('No &SEGIN namelists to remove!')

        self.nseg0 += -1
        name = "input:segin" + str(self.nseg0)+":"

        self.remove_container(name)


    def add_pconin(self):
        """Method to add a pconin* group to the list of input variables.  This method
        can be invoked multiple times to add as many pconin* groups as desired.
        The first group added is input.pconin0, the second is input.pconin1, etc.
        Local var self.npcon0 keeps track of the number of groups added."""

        if self.npcon0 == 30:
            raise RuntimeError('Maximum of 30 performance constraints')

        name = "input:pconin" + str(self.npcon0)+":"
        self.npcon0 += 1


        self.add_param(name+'conalt', val=-1., units='ft', desc="Altitude at which constraint is to be evaluated (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'conmch', val=-1., units='nmi/h', desc="Velocity at which constraint is to be evaluated, kts.  If less than or equal to 5., assumed to be Mach number (Default = value from preceding constraint)" ,typeVar='Float')

        if self.npcon0 == 1:
            self.add_param(name+'connz', val=1., desc="Load factor (Nz) at which constraint is to be evaluated, G's (Default = value from preceding constraint or 1.)" ,typeVar='Float')
            self.add_param(name+'conpc', val=1., desc="Engine power setting parameter\n< 1., Fraction of maximum available thrust\n= 1., Maximum thrust at this Mach number and altitude\n> 1., Power setting for engine deck (3. would indicate the third highest thrust)\n(Default = value from preceding constraint or 1.)" ,typeVar='Float')
            self.add_param(name+'icstdg', val=0, desc="Number of store drag schedule (see Namelist $MISSIN) to be applied to this constraint (Default = value from preceding constraint or 0)" ,typeVar='Int',pass_by_obj=True)
        else:
            self.add_param(name+'connz', val=-1., desc="Load factor (Nz) at which constraint is to be evaluated, G's (Default = value from preceding constraint or 1.)" ,typeVar='Float')
            self.add_param(name+'conpc', val=-10., desc="Engine power setting parameter\n< 1., Fraction of maximum available thrust\n= 1., Maximum thrust at this Mach number and altitude\n> 1., Power setting for engine deck (3. would indicate the third highest thrust)\n(Default = value from preceding constraint or 1.)" ,typeVar='Float')
            self.add_param(name+'icstdg', val=-1, desc="Number of store drag schedule (see Namelist $MISSIN) to be applied to this constraint (Default = value from preceding constraint or 0)" ,typeVar='Int',pass_by_obj=True)

        self.add_param(name+'conlim', val=-999., desc="Constraint minimum or maximum value" ,typeVar='Float')
        self.add_param(name+'conaux', val=-1., desc="Additional constraint parameter" ,typeVar='Float')
        self.add_param(name+'neo', val=-1, desc="Number of engines operating (Default = value from preceding constraint or all)"  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'conwt', val=-1., units='lb', desc="Fixed weight (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'iconsg', val=-1, desc="Weight at start of mission segment ICONSG is used (Default = value from preceding constraint)" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'confm', val=-1., desc="Fuel multiplier or fraction of fuel burned (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'conwta', val=-999., units='lb', desc="Delta weight (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'icontp', val=-1,valueOptions= (-1,5,6,7,8,9,10,11,12,13,16,17,20,30), desc="Type of constraint (Default = value from preceding constraint)", \
                                      aliases=("Previous","Min. climb rate","Max. time-to-climb","Max. time-to-distance","Min. sustained load factor","Min. instant. load factor","Min. turn rate","Max. turn radius","Min. excess energy","Min. climb ceiling","Max. accel./decel. time","Min. max. speed","Min. energy bleed rate","Min. thrust margin"),typeVar='Enum',pass_by_obj=True)

    def remove_pconin(self):
        """Removes a PCONIN namelist. Actually, it removes the most recently added PCONIN, as per the MC wrapper."""

        if self.npcon0 == 0:
            raise RuntimeError('No &PCONIN namelists to remove!')

        self.npcon0 += -1
        name = "input:pconin" + str(self.npcon0)+":"

        self.remove_container(name)

    def add_rerunpconin(self, i):
        """Method to add a pconin* group to the list of input variables, within an
        existing rerun* group .  This method can be invoked multiple times to add
        as many pconin* groups as desired.  Local array self.npcons keeps track of the
        number of groups added to each rerun*."""

        if self.npcons0[i] == 30:
            raise RuntimeError('Maximum of 30 performance constraints')

        rerun_name = "rerun" + str(i)

        if not hasattr(self.input,rerun_name):
            raise RuntimeError('Attempted to add a PCONIN group to a nonexistant RERUN group')

        name = "input:"+rerun_name+":pconin" + str(self.npcons0[i])+":"
        self.npcons0[i] += 1


        self.add_param(name+'conalt', val=-1., units='ft', desc="Altitude at which constraint is to be evaluated (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'conmch', val=-1., units='nmi/h', desc="Velocity at which constraint is to be evaluated, kts.  If less than or equal to 5., assumed to be Mach number (Default = value from preceding constraint)"  ,typeVar='Float')
        self.add_param(name+'connz', val=-1., desc="Load factor (Nz) at which constraint is to be evaluated, G's (Default = value from preceding constraint or 1.)"  ,typeVar='Float')
        self.add_param(name+'conpc', val=-10., desc="Engine power setting parameter\n< 1., Fraction of maximum available thrust\n= 1., Maximum thrust at this Mach number and altitude\n> 1., Power setting for engine deck (3. would indicate the third highest thrust)\n(Default = value from preceding constraint or 1.)"  ,typeVar='Float')
        self.add_param(name+'icstdg', val=-1, desc="Number of store drag schedule (see Namelist $MISSIN) to be applied to this constraint (Default = value from preceding constraint or 0)" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'conlim', val=-999., desc="Constraint minimum or maximum value"  ,typeVar='Float')
        self.add_param(name+'conaux', val=-1., desc="Additional constraint parameter"  ,typeVar='Float')
        self.add_param(name+'neo', val=-1, desc="Number of engines operating (Default = value from preceding constraint or all)" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'conwt', val=-1., units='lb', desc="Fixed weight (Default = value from preceding constraint)"  ,typeVar='Float')
        self.add_param(name+'iconsg', val=-1, desc="Weight at start of mission segment ICONSG is used (Default = value from preceding constraint)" ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'confm', val=-1., desc="Fuel multiplier or fraction of fuel burned (Default = value from preceding constraint)"  ,typeVar='Float')
        self.add_param(name+'conwta', val=-999., units='lb', desc="Delta weight (Default = value from preceding constraint)" ,typeVar='Float')
        self.add_param(name+'icontp', val=-1, valueOption=(-1,5,6,7,8,9,10,11,12,13,16,17,20,30), desc="Type of constraint (Default = value from preceding constraint)", \
                                      aliases=("Previous","Min. climb rate","Max. time-to-climb","Max. time-to-distance","Min. sustained load factor","Min. instant. load factor","Min. turn rate","Max. turn radius","Min. excess energy","Min. climb ceiling","Max. accel./decel. time","Min. max. speed","Min. energy bleed rate","Min. thrust margin"),typeVar='Enum',pass_by_obj=True)

    def remove_rerunpconin(self, i):
        """Removes a PCONIN from an existing RERUN group. Actually, it removes
        the most recently added PCONIN, as per the MC wrapper."""

        if self.npcons0[i] == 0:
            raise RuntimeError('No &PCONIN namelists to remove!')

        self.npcons0[i] += -1
        rerun_name = "rerun" + str(i)

        name = "input:"+rerun_name+":pconin" + str(self.npcons0[i])+":"
        self.remove_container(name)



    def add_rerun(self):
        """ Method to add a rerun* group to the list of input variables.  This method
        can be invoked multiple times to add as many rerun* groups as desired.
        The first group added is input.rerun0, the second is input.rerun1, etc.
        An additional missin group and mission definition file are also created
        within the new group.  Local var self.nrern0 keeps track of the number of
        groups added."""

        name = "input:rerun" + str(self.nrern0)+":"
        self.nrern0 += 1
        self.npcons0.append(0)


        self.add_param(name+'desrng', val=-1., units="nmi/s" ,typeVar='Float')
        self.add_param(name+'mywts',  val=-1 ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'rampwt',  val=-1., units="lb" ,typeVar='Float')
        self.add_param(name+'dowe',  val=-1., units="lb" ,typeVar='Float')
        self.add_param(name+'paylod',  val=-1., units="lb" ,typeVar='Float')
        self.add_param(name+'fuemax',  val=-1., units="lb" ,typeVar='Float')
        self.add_param(name+'itakof',  val=-1  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'iland',  val=-1  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'nopro',  val=-1  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'noise',  val=-1  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'icost',  val=-1  ,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'wsr',  val=-1. ,typeVar='Float')
        self.add_param(name+'twr',  val=-1. ,typeVar='Float')


        self.add_param(name+'missin:Basic:indr', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:fact', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:fleak', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:fcdo', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:fcdi', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:fcdsub', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:fcdsup', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:iskal', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:owfact', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:iflag', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:msumpt', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:dtc', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:irw', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:rtol', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:nhold', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:iata', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:tlwind', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:dwt', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Basic:offdr', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Basic:idoq', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:nsout', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:nsadj', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Basic:mirror', val=-999,typeVar='Int',pass_by_obj=True)


        self.add_param(name+'missin:Store_Drag:stma', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Store_Drag:cdst', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Store_Drag:istcl', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Store_Drag:istcr', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Store_Drag:istde', val=-999,typeVar='Int',pass_by_obj=True)


        self.add_param(name+'missin:User_Weights:mywts', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:User_Weights:rampwt', val=-999.,typeVar='Float')
        self.add_param(name+'missin:User_Weights:dowe', val=-999.,typeVar='Float')
        self.add_param(name+'missin:User_Weights:paylod', val=-999.,typeVar='Float')
        self.add_param(name+'missin:User_Weights:fuemax', val=-999.,typeVar='Float')


        self.add_param(name+'missin:Ground_Operations:takotm', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:taxotm', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:apprtm', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:appfff', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:taxitm', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:ittff', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Ground_Operations:takoff', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:txfufl', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:ftkofl', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:ftxofl', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:ftxifl', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Ground_Operations:faprfl', val=-999.,typeVar='Float')


        self.add_param(name+'missin:Turn_Segments:xnz', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Turn_Segments:xcl', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Turn_Segments:xmach', val=array([]),typeVar='Array,float',pass_by_obj=True)


        self.add_param(name+'missin:Climb:nclimb', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:clmmin', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:clmmax', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:clamin', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:clamax', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:nincl', val=-999,typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:fwf', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:ncrcl', val=array([]),typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:cldcd', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:ippcl', val=array([]),typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:maxcl', val=array([]),typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:no', val=array([]),typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:keasvc', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:actab', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:vctab', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:ifaacl', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:ifaade', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:nodive', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:divlim', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Climb:qlim', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Climb:spdlim', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Climb:nql', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Climb:qlalt', val=array([]),typeVar='Array,float',pass_by_obj=True)
        self.add_param(name+'missin:Climb:vqlm', val=array([]),typeVar='Array,float',pass_by_obj=True)


        self.add_param(name+'missin:Cruise:ncruse', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Cruise:ioc', val=array([]),typeVar='Array,int',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:crmach', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:cralt', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:crdcd', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:flrcr', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:crmmin', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:crclmx', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:hpmin', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:ffuel', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:fnox', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:ifeath', val=array([]),typeVar='Array,int',pass_by_obj=True)
        self.add_param(name+'missin:Cruise:feathf', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:cdfeth', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:dcwt', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Cruise:rcin', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Cruise:wtbm', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Cruise:altbm', val=array([]),typeVar='Array,float',pass_by_obj=False)


        self.add_param(name+'missin:Descent:ivs', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Descent:decl', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:demmin', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:demmax', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:deamin', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:deamax', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:ninde', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Descent:dedcd', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:rdlim', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Descent:ns', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Descent:keasvd', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Descent:adtab', val=array([]),typeVar='Array,float',pass_by_obj=False)
        self.add_param(name+'missin:Descent:vdtab', val=array([]),typeVar='Array,float',pass_by_obj=False)


        self.add_param(name+'missin:Reserve:irs', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:resrfu', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:restrp', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:timmap', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:altran', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:nclres', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:ncrres', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:sremch', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:eremch', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:srealt', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:erealt', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:holdtm', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:ncrhol', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:ihopos', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:icron', val=-999,typeVar='Int',pass_by_obj=True)
        self.add_param(name+'missin:Reserve:thold', val=-999.,typeVar='Float')
        self.add_param(name+'missin:Reserve:ncrth', val=-999,typeVar='Int',pass_by_obj=True)

    def remove_rerun(self):
        """Removes a Rerun namelist. Actually, it removes the most recently added Rerun, as per the MC wrapper."""

        if self.nrern0 == 0:
            raise RuntimeError('No &PCONIN namelists to remove!')

        self.nrern0 += -1
        name = "input:rerun" + str(self.nrern0)+":"

        self.remove_container(name)
        self.npcons0 = self.npcons0[:-1]

    def reinitialize(self):
        """Method to add pconin*, segin* and rerun* groups to the list of input
        variables.  This method can be invoked by the user to add the appropriate
        number of groups based on input variables npcon, nseg, nrerun and
        npcons[]."""

        # Add or remove an appropriate number of pconin* groups to the input variable
        # list.

        n0 = self.npcon0
        n = self.getValue("input:missin:Basic:npcon")
        if n > n0:
            for i in range(0,n-n0):
                self.add_pconin()
        elif n < n0:
            for i in range(0,n0-n):
                self.remove_pconin()

        # Add or remove an appropriate number of segin* groups to the input variable
        # list.

        n0 = self.nseg0
        n = self.nseg
        if n > n0:
            for i in range(0,n-n0):
                self.add_segin()
        elif n < n0:
            for i in range(0,n0-n):
                self.remove_segin()

        # Add or remove an appropriate number of rerun* groups to the input variable
        # list.

        n0 = self.nrern0
        n = self.nrerun
        if n > n0:
            for i in range(0,n-n0):
                self.add_rerun()
        elif n < n0:
            for i in range(0,n0-n):
                self.remove_rerun()

        # Add or remove an appropriate number of rerun*.pconin* groups to the input
        # variable list.

        for i in range(0,self.nrern0):
            n0 = self.npcons0[i]
            n = self.npcons[i]
            if n > n0:
                for j in range(0,n-n0):
                    self.add_rerunpconin(i)
            elif n < n0:
                for j in range(0,n0-n):
                    self.remove_rerunpconin(i)





    def FlopsWrapper_input_wtin_Wing_Data(self):
        """Container for input:wtin:Wing_Data"""
        strChain = 'input:wtin:Wing_Data:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'span',val=0.0, units='ft', desc='Wing span (optional, see &CONFIN - SW and AR)',typeVar='Float')
        self.add_param(strChain+'dih',val=0.0, units='deg', desc='Wing dihedral (positive) or anhedral (negative) angle',typeVar='Float')
        self.add_param(strChain+'flapr',val=0.3330, desc='Flap ratio -- ratio of total movable wing surface area (flaps, elevators, spoilers, etc.) to wing area',typeVar='Float')
        self.add_param(strChain+'glov',val=0.0, units='ft*ft', desc='Total glove and bat area beyond theoretical wing',typeVar='Float')
        self.add_param(strChain+'varswp',val=0.0, desc='Fraction of wing variable sweep weight penalty = 0., Fixed-geometry wing = 1., Full variable-sweep wing',typeVar='Float')
        self.add_param(strChain+'fcomp',val=0.0, desc='Decimal fraction of amount of composites used in wing structure = 0., No composites = 1., Maximum use of composites, approximately equivalent to FRWI1=.6, FRWI2=.83, FRWI3=.7 (Not necessarily all composite) This only applies to the wing.  Use override parameters for other components such as FRHT=.75, FRVT=.75, FRFU=.82, FRLGN=.85, FRLGM=.85, FRNA=.8',typeVar='Float')
        self.add_param(strChain+'faert',val=0.0, desc='Decimal fraction of amount of aeroelastic tailoring used in design of wing = 0., No aeroelastic tailoring = 1., Maximum aeroelastic tailoring',typeVar='Float')
        self.add_param(strChain+'fstrt',val=0.0, desc='Wing strut-bracing factor = 0., No wing strut = 1., Full benefit from strut bracing',typeVar='Float')


    def FlopsWrapper_input_wtin_Tails_Fins(self):
        """Container for input:wtin:Tails_Fins"""
        strChain = 'input:wtin:Tails_Fins:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'sht',val=0.0, units='ft*ft', desc='Horizontal tail theoretical area',typeVar='Float')
        self.add_param(strChain+'swpht',val=-100.0, units='deg', desc='Horizontal tail 25% chord sweep angle (Default = SWEEP, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'arht',val=-100.0, desc='Horizontal tail theoretical aspect ratio (Default = AR/2, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'trht',val=-100.0, desc='Horizontal tail theoretical taper ratio (Default = TR, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'tcht',val=0.0, desc='Thickness-chord ratio for the horizontal tail (Default = TCA, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'hht',val=-100.0, desc='Decimal fraction of vertical tail span where horizontal tail is mounted = 0. for body mounted (Default for transports with all engines on the wing and for fighters) = 1. for T tail (Default for transports with multiple engines on the fuselage)',typeVar='Float')
        self.add_param(strChain+'nvert',val=1, desc='Number of vertical tails',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'svt',val=0.0, units='ft*ft', desc='Vertical tail theoretical area (per tail)',typeVar='Float')
        self.add_param(strChain+'swpvt',val=-100.0, units='deg', desc='Vertical tail sweep angle at 25% chord (Default = SWPHT)',typeVar='Float')
        self.add_param(strChain+'arvt',val=-100.0, desc='Vertical tail theoretical aspect ratio (Default = ARHT/2)',typeVar='Float')
        self.add_param(strChain+'trvt',val=-100.0, desc='Vertical tail theoretical taper ratio (Default = TRHT)',typeVar='Float')
        self.add_param(strChain+'tcvt',val=0.0, desc='Thickness-chord ratio for the vertical tail (Default = TCHT)',typeVar='Float')
        self.add_param(strChain+'nfin',val=0, desc='Number of fins',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'sfin',val=0.0, units='ft*ft', desc='Vertical fin theoretical area',typeVar='Float')
        self.add_param(strChain+'arfin',val=-100.0, desc='Vertical fin theoretical aspect ratio',typeVar='Float')
        self.add_param(strChain+'trfin',val=-100.0, desc='Vertical fin theoretical taper ratio',typeVar='Float')
        self.add_param(strChain+'swpfin',val=-100.0, units='deg', desc='Vertical fin sweep angle at 25% chord',typeVar='Float')
        self.add_param(strChain+'tcfin',val=0.0, desc='Vertical fin thickness - chord ratio',typeVar='Float')
        self.add_param(strChain+'scan',val=0.0, units='ft*ft', desc='Canard theoretical area',typeVar='Float')
        self.add_param(strChain+'swpcan',val=-100.0, units='deg', desc='Canard sweep angle at 25% chord',typeVar='Float')
        self.add_param(strChain+'arcan',val=-100.0, desc='Canard theoretical aspect ratio',typeVar='Float')
        self.add_param(strChain+'trcan',val=-100.0, desc='Canard theoretical taper ratio',typeVar='Float')
        self.add_param(strChain+'tccan',val=0.0, desc='Canard thickness-chord ratio (Default = TCHT)',typeVar='Float')


    def FlopsWrapper_input_wtin_Propulsion(self):
        """Container for input:wtin:Propulsion"""
        strChain = 'input:wtin:Propulsion:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'new',val=0, desc='Number of wing mounted engines',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'nef',val=0, desc='Number of fuselage mounted engines',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'thrso',val=0.0, units='lb', desc='Rated thrust of baseline engine as described in Engine Deck (Default = THRUST, see &CONFIN)',typeVar='Float')
        self.add_param(strChain+'weng',val=0.0, units='lb', desc='Weight of each baseline engine or bare engine if WINL and WNOZ (below) are supplied (Default = THRSO/5.5 for transports and THRSO/8 for fighters)',typeVar='Float')
        self.add_param(strChain+'eexp',val=1.15, desc='Engine weight scaling parameter\nW(Engine) = WENG*(THRUST/THRSO)**EEXP\nIf EEXP is less than 0.3,\nW(Engine) = WENG + (THRUST-THRSO)*EEXP',typeVar='Float')
        self.add_param(strChain+'winl',val=0.0, units='lb', desc='Inlet weight for baseline engine if not included in WENG above',typeVar='Float')
        self.add_param(strChain+'einl',val=1.0, desc='Inlet weight scaling exponent\nW(Inlet) = WINL*(THRUST/THRSO)**EINL',typeVar='Float')
        self.add_param(strChain+'wnoz',val=0.0, units='lb', desc='Nozzle weight for baseline engine if not included in WENG above',typeVar='Float')
        self.add_param(strChain+'enoz',val=1.0, desc='Nozzle weight scaling exponent\nW(Nozzle) = WNOZ*(THRUST/THRSO)**ENOZ',typeVar='Float')
        self.add_param(strChain+'xnac',val=0.0, units='ft', desc='Average length of baseline engine nacelles.  Scaled by SQRT(THRUST/THRSO)',typeVar='Float')
        self.add_param(strChain+'dnac',val=0.0, units='ft', desc='Average diameter of baseline engine nacelles.  Scaled by SQRT(THRUST/THRSO)',typeVar='Float')
        self.add_param(strChain+'wpmisc',val=0.0, desc='Additional miscellaneous propulsion system weight or fraction of engine weight if < 1.  This is added to the engine control and starter weight and may be overridden if WPMSC is input.',typeVar='Float')


    def FlopsWrapper_input_wtin_Override(self):
        """Container for input:wtin:Override"""
        strChain = 'input:wtin:Override:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'frwi',val=1.0, desc='Total wing weight - fixed weight overrides FRWI1, FRWI2, FRWI3, FRWI4 below, scale factor is cumulative \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n \n',typeVar='Float')
        self.add_param(strChain+'frwi1',val=1.0, desc='First term in wing weight equation - loosely corresponds to bending material weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n',typeVar='Float')
        self.add_param(strChain+'frwi2',val=1.0, desc='Second term in wing weight equation - loosely corresponds to control surfaces, spars and ribs \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n',typeVar='Float')
        self.add_param(strChain+'frwi3',val=1.0, desc='Third term in wing weight equation - miscellaneous, just because it',typeVar='Float')
        self.add_param(strChain+'frwi4',val=1.0, desc='Fourth term in wing weight equation - miscellaneous, just because it',typeVar='Float')
        self.add_param(strChain+'frht',val=1.0, desc='Horizontal tail weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frvt',val=1.0, desc='Vertical tail weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frfin',val=1.0, desc='Wing vertical fin weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frcan',val=1.0, desc='Canard weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frfu',val=1.0, desc='Fuselage weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frlgn',val=1.0, desc='Landing gear weight, nose \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frlgm',val=1.0, desc='Landing gear weight, main \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frna',val=1.0, desc='Total weight of nacelles and/or air induction system \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wthr',val=0.0, desc='Total weight of thrust reversers\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wpmsc',val=1.0, desc='Weight of miscellaneous propulsion systems such as engine controls, starter and wiring \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wfsys',val=1.0, desc='Weight of fuel system \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'frsc',val=1.0, desc='Surface controls weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wapu',val=1.0, desc='Auxiliary power unit weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'win',val=1.0, desc='Instrument Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'whyd',val=1.0, desc='Hydraulics Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'welec',val=1.0, desc='Electrical Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wavonc',val=1.0, desc='Avionics Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'warm',val=0.0, desc='Armament Group weight - includes thermal protection system or armor and fixed weapons\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wfurn',val=1.0, desc='Furnishings Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wac',val=1.0, desc='Air Conditioning Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wai',val=1.0, desc='Transports: Anti-icing Group weight\n            Fighters:   Auxiliary gear \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wuf',val=1.0, desc='Weight of unusable fuel \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'woil',val=1.0, desc='Engine oil weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wsrv',val=1.0, desc='Transports: Passenger service weight\n             Fighters: Ammunition and nonfixed weapons weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wcon',val=1.0, desc='Transports: Cargo and baggage container weight Fighters:   Miscellaneous operating items weight If < 0.5, as a fraction of Gross Weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wauxt',val=1.0, desc='Auxiliary fuel tank weight (Fighters only) \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wflcrb',val=1.0, desc='Total weight of flight crew and baggage\n           (Defaults:  Transports    - 225.*NFLCR\n           Fighters      - 215.*NFLCR\n           Carrier-based - 180.*NFLCR)\n           \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'wstuab',val=1.0, desc='Total weight of cabin crew and baggage (Default = 155.*NSTU + 200.*NGALC) \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')
        self.add_param(strChain+'ewmarg',val=0.0, desc='Empty weight margin (Special Option) - delta weight added to Weight Empty.  If abs(EWMARG) < 5., it is interpreted as a fraction of calculated Weight Empty.  May be positive or negative\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typeVar='Float')


    def FlopsWrapper_input_wtin_OEW_Calculations(self):
        """Container for input:wtin:OEW_Calculations:"""
        strChain = 'input:wtin:OEW_Calculations:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ispowe',val=0,optionsVal=(0,1), desc='= 0, Normal FLOPS weight equations will be used\n= 1, Special equation for Operating Weight Empty will be used:\n            \n            OWE = SPWTH*THRUST + SPWSW*SW + SPWGW*GW + SPWCON\n            \n            Structures group weights will be scaled to meet the calculated OWE.\n            \n            = 2, Use response surface for weights - available only in DOSS version', aliases=('Normal FLOPS', 'Special eqn for OEW'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'spwth',val=2.2344, units='lb/lb', desc='Multiplier for thrust/engine in special equation for Operating Weight Empty\nSPWTH = \n                                  AIRFLOWref\n(PODsclr + dOEWsclr) * ------------\n                               SLSTHRUSTref\n            ',typeVar='Float')
        self.add_param(strChain+'spwsw',val=9.5, units='psf', desc='Multiplier for wing area in special equation for Operating Weight Empty',typeVar='Float')
        self.add_param(strChain+'spwgw',val=0.104087, units='lb/lb', desc='Multiplier for gross weight in special equation for Operating Weight Empty\nSPWGW = \n            MTOWsclr+OEWgrwth*MTOWgrwth\n        -----------------------------------\n            1. + MTOWgrowth\n\n',typeVar='Float')
        self.add_param(strChain+'spwcon',val=38584.0, units='lb', desc='Constant weight term in special equation for Operating Weight Empty\n            \nSPWCON = OEWuncycled\n            - MTOWscalar*MTOWuncycled\n            - WINGscalar*SWref\n            - (PODscalar + dOEWscalar)\n            *AIRFLOWref\n',typeVar='Float')


    def FlopsWrapper_input_wtin_Landing_Gear(self):
        """Container for input:wtin:Landing_Gear"""
        strChain = 'input:wtin:Landing_Gear:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xmlg',val=0.0, units='inch', desc='Length of extended main landing gear oleo (Default is computed internally)',typeVar='Float')
        self.add_param(strChain+'xnlg',val=0.0, units='inch', desc='Length of extended nose landing gear oleo (Default is computed internally)',typeVar='Float')
        self.add_param(strChain+'wldg',val=0.0, units='lb', desc='Design landing weight (if WRATIO is input in Namelist &AERIN, WLDG = GW*WRATIO) See Namelist &AERIN for WRATIO defaults.',typeVar='Float')
        self.add_param(strChain+'mldwt',val=0,optionsVal=(1,0), desc='= 1, The design landing weight is set to the end of descent weight for the main mission plus DLDWT.  Use only if IRW = 1 in Namelist &MISSIN.  = 0, The design landing weight is determined by WLDG above or WRATIO in Namelist &AERIN',typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'dldwt',val=0.0, units='lb', desc='Delta landing weight for MLDWT = 1',typeVar='Float')
        self.add_param(strChain+'carbas',val=0.0, desc='Carrier based aircraft switch, affects weight of flight crew, avionics and nose gear = 1., Carrier based = 0., Land based',typeVar='Float')


    def FlopsWrapper_input_wtin_Inertia(self):
        """Container for input:wtin:Inertia"""
        strChain = 'input:wtin:Inertia:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inrtia',val=0,optionsVal=(1,0), desc='= 1, Aircraft inertias will be calculated = 0, Otherwise', aliases=('Calculate', 'Do not calculate'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'zht',val=0.0, units='inch', desc='Vertical C.G. of the horizontal tail (optional)',typeVar='Float')
        self.add_param(strChain+'zvt',val=0.0, units='inch', desc='Vertical C.G. of the vertical tail (optional)',typeVar='Float')
        self.add_param(strChain+'zfin',val=0.0, units='inch', desc='Vertical C.G. of the vertical fin (optional)',typeVar='Float')
        self.add_param(strChain+'yfin',val=0.0, units='inch', desc='Lateral C.G. of the vertical fin (optional)',typeVar='Float')
        self.add_param(strChain+'zef',val=0.0, units='inch', desc='Vertical C.G. of two forward mounted engines (optional)',typeVar='Float')
        self.add_param(strChain+'yef',val=0.0, units='inch', desc='Lateral C.G. of two forward mounted engines (optional, may be input as a fraction of the semispan)',typeVar='Float')
        self.add_param(strChain+'zea',val=0.0, units='inch', desc='Vertical C.G. of one or two aft mounted engines (optional)',typeVar='Float')
        self.add_param(strChain+'yea',val=0.0, units='inch', desc='Lateral C.G. of one or two aft mounted engines (optional, may be input as a fraction of the semispan)',typeVar='Float')
        self.add_param(strChain+'zbw',val=0.0, units='inch', desc='Lowermost point of wing root airfoil section',typeVar='Float')
        self.add_param(strChain+'zap',val=0.0, units='inch', desc='Vertical C.G. of Auxiliary Power Unit (optional)',typeVar='Float')
        self.add_param(strChain+'zrvt',val=0.0, units='inch', desc='Vertical datum line (Water Line) of vertical tail theoretical root chord (optional, if blank assumes at maximum height of fuselage)',typeVar='Float')
        self.add_param(strChain+'ymlg',val=0.0, units='inch', desc='Lateral C.G. of extended main landing gear',typeVar='Float')
        self.add_param(strChain+'yfuse',val=0.0, units='inch', desc='Lateral C.G. of outboard fuselage if there is more than one fuselage',typeVar='Float')
        self.add_param(strChain+'yvert',val=0.0, units='inch', desc='Lateral C.G. of outboard vertical tail if there is more than one vertical tail',typeVar='Float')
        self.add_param(strChain+'swtff',val=0.0, desc='Gross fuselage wetted area (Default = internally computed)',typeVar='Float')
        self.add_param(strChain+'tcr',val=0.0, desc='Wing root thickness-chord ratio (Default = TOC(0) or TCA in &CONFIN)',typeVar='Float')
        self.add_param(strChain+'tct',val=0.0, desc='Wing tip thickness-chord ratio (Default = TOC(NETAW) or TCA in &CONFIN)',typeVar='Float')
        self.add_param(strChain+'incpay',val=0,optionsVal=(1,0), desc='For inertia calculations, all mission fuel is placed in "tanks." \n \n = 1, Include passengers, passenger baggage, and cargo in the fuselage and contents for inertia calculations. \n \n = 0, For inertia calculations, all payload (passengers, passenger baggage, and cargo) are placed in "tanks" like the fuel', aliases=('Passengers-etc in fuse', 'All payload in tanks'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'tx',val=array([]), units='inch', desc='x coordinates of the centroid of the Ith tank',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ty',val=array([]), units='inch', desc='y coordinates of the centroid of the Ith tank',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tz',val=array([]), units='inch', desc='z coordinates of the centroid of the Ith tank',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tl',val=array([]), desc='Length of the Ith tank (optional, used only in calculating I0',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tw',val=array([]), desc='Width of the Ith tank (optional, used only in calculating I0',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'td',val=array([]), desc='Depth of the Ith tank (optional, used only in calculating I0',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tf',val=array([]), units='lb', desc='Weight of fuel (or payload) in Ith tank for the Jth fuel condition NOTE: Dimensions are [J,I]',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_wtin_Fuselage(self):
        """Container for input:wtin:Fuselage"""
        strChain = 'input:wtin:Fuselage:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'nfuse',val=1, desc='Number of fuselages',typeVar='Int')
        self.add_param(strChain+'xl',val=0.0, units='ft', desc='Fuselage total length (See Fuselage Design Data)',typeVar='Float')
        self.add_param(strChain+'wf',val=0.0, units='ft', desc='Maximum fuselage width',typeVar='Float')
        self.add_param(strChain+'df',val=0.0, units='ft', desc='Maximum fuselage depth',typeVar='Float')
        self.add_param(strChain+'xlp',val=0.0, units='ft', desc='Length of passenger compartment (Default is internally computed)',typeVar='Float')


    def FlopsWrapper_input_wtin_Fuel_System(self):
        """Container for input:wtin:Fuel_System"""
        strChain = 'input:wtin:Fuel_System:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ntank',val=7, desc='Number of fuel tanks',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'fulwmx',val=-1.0, units='lb', desc='Total fuel capacity of wing.  The default is internally calculated from:\n \n                             TCA * SW**2         TR\n FULWMX = FWMAX * ---------- * ( 1 - -------- )\n                                SPAN         (1+TR)**2\n \n Where the default value of FWMAX is 23.  If FULWMX is input < 50, it is interpreted as FWMAX and the above equation is used.  This equation is also used for scaling when the wing area, t/c, aspect ratio, or taper ratio is varied or optimized.\n \n Alternatively,  FULWMX = FUELRF + FUSCLA*(SW**1.5 - FSWREF**1.5)\n + FUSCLB*(SW - FSWREF)\n',typeVar='Float')
        self.add_param(strChain+'fulden',val=1.0, desc='Fuel density ratio for alternate fuels compared to jet fuel (typical density of 6.7 lb/gal), used in the calculation of FULWMX (if FULWMX is not input) and in the calculation of fuel system weight.',typeVar='Float')
        self.add_param(strChain+'fuelrf',val=0.0, units='lb', desc='Fuel capacity at FSWREF for alternate method',typeVar='Float')
        self.add_param(strChain+'fswref',val=-1.0, units='ft*ft', desc='Reference wing area for alternate method (Default = SW in Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'fuscla',val=0.0, desc='Alternate fuel capacity scaling method - Factor A',typeVar='Float')
        self.add_param(strChain+'fusclb',val=0.0, desc='Alternate fuel capacity scaling method - Factor B',typeVar='Float')
        self.add_param(strChain+'fulfmx',val=0.0, desc='Total fuel capacity of fuselage (wing ',typeVar='Float')
        self.add_param(strChain+'ifufu',val=0, desc='= 1, Fuselage fuel capacity is adjusted to meet the required fuel capacity for the primary mission.  Use only if IRW = 1 in Namelist &MISSIN, and use with care - some passengers can',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'fulaux',val=0.0, units='lb', desc='Auxiliary (external) fuel tank capacity (Fighters only)',typeVar='Float')
        self.add_param(strChain+'fmxtot',val=-999., units='lb', desc='Total fuel capacity of the aircraft including wing,fuselage and auxiliary tanks, lb.  Used in generating payload-range diagram  (Default = FULWMX + FULFMX + FULAUX)',typeVar='Float')

           


    def FlopsWrapper_input_wtin_Detailed_Wing(self):
        """Container for input:wtin:Detailed_Wing"""
        strChain = 'input:wtin:Detailed_Wing:'

        self.add_param(strChain+'etae',val=array([0.3, 0.6, 0.0, 0.0]), dtype=array([]), desc='Engine locations - fraction of semispan or distance from fuselage centerline.  Actual distances are not scaled with changes in span.  NEW/2 values are input',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pctl',val=1.0, desc='Fraction of load carried by defined wing',typeVar='Float')
        self.add_param(strChain+'arref',val=0.0, desc='Reference aspect ratio (Default = AR in &CONFIN)',typeVar='Float')
        self.add_param(strChain+'tcref',val=0.0, desc='Reference thickness-chord ratio (Default = TCA in &CONFIN)',typeVar='Float')
        self.add_param(strChain+'nstd',val=50, desc='Number of integration stations',typeVar='Int')
        self.add_param(strChain+'pdist',val=2.0, desc='Pressure distribution indicator\n= 0., Input distribution - see below\n= 1., Triangular distribution\n= 2., Elliptical distribution\n= 3., Rectangular distribution PDIST is a continuous variable, i.e., a value of 1.5 would be half way between triangular and elliptical.\nCAUTION - the constants in the wing weight calculations were correlated with existing aircraft assuming an elliptical distribution.  Use the default value unless you have a good reason not to.',typeVar='Float')
        self.add_param(strChain+'etap',val=array([]), desc='Fraction of wing semispan',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pval',val=array([]), desc='Relative spanwise pressure at ETAP(J)',typeVar='Array',pass_by_obj=True)
        # OpenMDAO Public Variables
        self.add_param(strChain+'etaw',val=array([]), desc='Wing station location - fraction of semispan or distance from fuselage centerline.  Typically, goes from 0. to 1.  Input fixed distances (>1.1) are not scaled with changes in span.',typeVar='Array',pass_by_obj = True)


        self.add_param(strChain+'chd',val=array([]), desc='Chord length - fraction of semispan or actual chord.   Actual chord lengths (>5.) are not scaled.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'toc',val=array([]), desc='Thickness - chord ratio',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'swl',val=array([]), units='deg', desc='Sweep of load path.  Typically parallel to rear spar tending toward max t/c of airfoil.  The Ith value is used between wing stations I and I+1.',typeVar='Array',pass_by_obj=True)






    def FlopsWrapper_input_wtin_Crew_Payload(self):
        """Container for input:wtin:Crew_Payload"""
        strChain = 'input:wtin:Crew_Payload:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'npf',val=0, desc='Number of first class passengers',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'npb',val=0, desc='Number of business class passengers',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'npt',val=0, desc='Number of tourist passengers',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'nstu',val=-1, desc='Number of flight attendants (optional)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'ngalc',val=-1, desc='Number of galley crew (optional)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'nflcr',val=-1, desc='Number of flight crew (optional)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'wppass',val=165.0, units='lb', desc='Weight per passenger',typeVar='Float')
        self.add_param(strChain+'bpp',val=-1.0, units='lb', desc='Weight of baggage per passenger (Default = 35., or 40. if DESRNG in Namelist &CONFIN > 900., or 44. if DESRNG > 2900.)',typeVar='Float')
        self.add_param(strChain+'cargf',val=0.0, desc='Military cargo aircraft floor factor = 0., Passenger transport\n= 1., Military cargo transport floor',typeVar='Float')
        self.add_param(strChain+'cargow',val=0.0, units='lb', desc='Cargo carried in wing (Weight of wing-mounted external stores for fighters)',typeVar='Float')
        self.add_param(strChain+'cargof',val=0.0, units='lb', desc='Cargo (other than passenger baggage) carried in fuselage (Fuselage external stores for fighters)',typeVar='Float')
        self.add_param('input:wtin:Crew_optional:paylmx',val=-999., units='lb', desc='Maximum payload for the aircraft, including passengers and cargo, lb.  Used in generating payload-range diagram',typeVar='Float')




    def FlopsWrapper_input_wtin_Center_of_Gravity(self):
        """Container for input:wtin:Center_of_Gravity"""
        strChain = 'input:wtin:Center_of_Gravity:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cgw',val=0.0, units='inch', desc='Longitudinal C.G. of wing',typeVar='Float')
        self.add_param(strChain+'cght',val=0.0, units='inch', desc='Longitudinal C.G. of horizontal tail',typeVar='Float')
        self.add_param(strChain+'cgvt',val=0.0, units='inch', desc='Longitudinal C.G. of vertical tail',typeVar='Float')
        self.add_param(strChain+'cgfin',val=0.0, units='inch', desc='Longitudinal C.G. of wing vertical fins',typeVar='Float')
        self.add_param(strChain+'cgcan',val=0.0, units='inch', desc='Longitudinal C.G. of canard',typeVar='Float')
        self.add_param(strChain+'cgf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage',typeVar='Float')
        self.add_param(strChain+'cglgn',val=0.0, units='inch', desc='Longitudinal C.G. of nose landing gear',typeVar='Float')
        self.add_param(strChain+'cglgm',val=0.0, units='inch', desc='Longitudinal C.G. of main landing gear',typeVar='Float')
        self.add_param(strChain+'cgef',val=0.0, units='inch', desc='Longitudinal C.G. of two forward mounted engines',typeVar='Float')
        self.add_param(strChain+'cgea',val=0.0, units='inch', desc='Longitudinal C.G. of one or two aft mounted engines',typeVar='Float')
        self.add_param(strChain+'cgap',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary power unit',typeVar='Float')
        self.add_param(strChain+'cgav',val=0.0, units='inch', desc='Longitudinal C.G. of avionics group (optional)',typeVar='Float')
        self.add_param(strChain+'cgarm',val=0.0, units='inch', desc='Longitudinal C.G. of armament group - includes thermal protection system or armor and fixed weapons (Default = CGF)',typeVar='Float')
        self.add_param(strChain+'cgcr',val=0.0, units='inch', desc='Longitudinal C.G. of flight crew',typeVar='Float')
        self.add_param(strChain+'cgp',val=0.0, units='inch', desc='Longitudinal C.G. of passengers',typeVar='Float')
        self.add_param(strChain+'cgcw',val=0.0, units='inch', desc='Longitudinal C.G. of wing cargo or external stores',typeVar='Float')
        self.add_param(strChain+'cgcf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage cargo or external stores',typeVar='Float')
        self.add_param(strChain+'cgzwf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage fuel',typeVar='Float')
        self.add_param(strChain+'cgfwf',val=0.0, units='inch', desc='Longitudinal C.G. of wing fuel in full condition',typeVar='Float')
        self.add_param(strChain+'cgais',val=0.0, units='inch', desc='Longitudinal C.G. of air induction system',typeVar='Float')
        self.add_param(strChain+'cgacon',val=0.0, units='inch', desc='Longitudinal C.G. of air conditioning system',typeVar='Float')
        self.add_param(strChain+'cgaxg',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary gear',typeVar='Float')
        self.add_param(strChain+'cgaxt',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary tanks',typeVar='Float')
        self.add_param(strChain+'cgammo',val=0.0, units='inch', desc='Longitudinal C.G. of ammunition and nonfixed weapons',typeVar='Float')
        self.add_param(strChain+'cgmis',val=0.0, units='inch', desc='Longitudinal C.G. of miscellaneous operating items',typeVar='Float')


    def FlopsWrapper_input_wtin_Basic(self):
        """Container for input:wtin:Basic"""
        strChain = 'input:wtin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ulf',val=3.75, desc='Structural ultimate load factor',typeVar='Float')
        self.add_param(strChain+'dgw',val=1.0, units='lb', desc='Design gross weight - fraction of GW (see &CONFIN) or weight',typeVar='Float')
        self.add_param(strChain+'vmmo',val=0.0, desc='Maximum operating Mach number (Default = VCMN, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'nwref',val=39,optionsVal=(39,37,33,26), desc='The number of the reference weight for percentage weight output.', aliases=('Ramp weight', 'Zero fuel weight', 'Operating weight empty', 'Weight empty'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'cgrefl',val=0.0, units='inch', desc='Reference length for percentage C.G. location output (Default = XL*12., fuselage length)',typeVar='Float')
        self.add_param(strChain+'cgrefx',val=0.0, units='inch', desc='X - location of start of reference length',typeVar='Float')
        self.add_param(strChain+'mywts',val=0,optionsVal=(0,1), desc='= 0, Weights will be computed\n = 1, Otherwise (See User-Specified Weights, Namelist &MISSIN)', aliases=('Compute weight', 'User-specified'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'hydpr',val=3000.0, units='psi', desc='Hydraulic system pressure',typeVar='Float')
        self.add_param(strChain+'wpaint',val=0.0, units='psf', desc='Weight of paint for all wetted areas',typeVar='Float')
        self.add_param(strChain+'ialtwt',val=0,optionsVal=(0,1), desc='= 1, Alternate weight equations for some components will be used (Special option)\n= 0, Normal FLOPS weight equations will be used', aliases=('Normal', 'Alternate'),typeVar='Enum',pass_by_obj=True)




    def FlopsWrapper_input_tolin_Thrust_Reverser(self):
        """Container for input:tolin:Thrust_Reverser"""
        strChain = 'input:tolin:Thrust_Reverser:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inthrv',val=-1, desc='= -1, Use takeoff thrust\n=  0, Input thrust values will be used\n=  1, Input values will be scaled\n>  1, Scaled engine deck for the (INTHRV-1)th power setting will be used',typeVar='Int')
        self.add_param(strChain+'rvfact',val=0.0, desc='Fraction of thrust reversed - net  (Real values should be negative)',typeVar='Float')
        self.add_param(strChain+'velrv',val=array([]), units='ft/s', desc='Velocities for reverse thrust',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'thrrv',val=array([]), units='lb', desc='Thrust values',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tirvrs',val=5.0, units='s', desc='Time after touchdown to reverse thrust',typeVar='Float')
        self.add_param(strChain+'revcut',val=-1000.0, units='nmi', desc='Cutoff velocity for thrust reverser',typeVar='Float')
        self.add_param(strChain+'clrev',val=0.0, desc='Change in lift coefficient due to thrust reverser',typeVar='Float')
        self.add_param(strChain+'cdrev',val=0.0, desc='Change in drag coefficient due to thrust reverser',typeVar='Float')


    def FlopsWrapper_input_tolin_Takeoff(self):
        """Container for input:tolin:Takeoff"""
        strChain = 'input:tolin:Takeoff:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cltom',val=-1.0, desc='Maximum CL for takeoff (Default, see &AERIN)',typeVar='Float')
        self.add_param(strChain+'cdmto',val=0.0, desc='Minimum CD for takeoff, typically, this is the drag coefficient at zero lift',typeVar='Float')
        self.add_param(strChain+'fcdmto',val=0.3, desc='Fraction of CDMTO due to wing',typeVar='Float')
        self.add_param(strChain+'almxto',val=25.0, units='deg', desc='Maximum angle of attack during takeoff',typeVar='Float')
        self.add_param(strChain+'obsto',val=-1.0, units='ft', desc='Takeoff obstacle height (Defaults, Transport = 35., Fighter = 50.)',typeVar='Float')
        self.add_param(strChain+'alpto',val=array([-100.0]), dtype=array([]), units='deg', desc='Angles of attack for takeoff polar',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clto',val=array([-100.0]), dtype=array([]), desc='Lift coefficients for takeoff polar.  These are not generated internally',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdto',val=array([-100.0]), dtype=array([]), desc='Drag coefficients for takeoff polar.  These are not generated internally',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'inthto',val=0, desc='= 0, Input thrust values will be used\n= 1, The input values will be scaled\n> 1, Scaled engine data deck for the (INTHTO-1)th power setting will be used',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'velto',val=array([]), units='ft/s', desc='Velocities for takeoff thrust',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'thrto',val=array([]), units='lb', desc='Thrust values',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'alprot',val=-100.0, desc='Maximum angle of attack during rotation phase of takeoff (Default = ALMXTO)',typeVar='Float')
        self.add_param(strChain+'vrotat',val=1.05, desc='Minimum rotation start speed, knots or fraction of Vstall',typeVar='Float')
        self.add_param(strChain+'vangl',val=2.0, units='deg/s', desc='Rotation rate',typeVar='Float')
        self.add_param(strChain+'thfact',val=1.0, desc='Thrust multiplier for input or extracted thrust data',typeVar='Float')
        self.add_param(strChain+'ftocl',val=1.0, desc='Factor for takeoff lift.  Also applied to drag polars input in &PROIN',typeVar='Float')
        self.add_param(strChain+'ftocd',val=1.0, desc='Factor for takeoff drag.  Also applied to drag polars input in &PROIN',typeVar='Float')
        self.add_param(strChain+'igobs',val=0,optionsVal=(0,1), desc='Gear retraction switch', aliases=('Liftoff + TDELG', 'Obstacle + TDELG'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'tdelg',val=0.0, units='s', desc='Time delay after liftoff/obstacle before start of landing gear retraction',typeVar='Float')
        self.add_param(strChain+'tigear',val=2.0, units='s', desc='Time required to retract landing gear.  Landing gear drag is reduced using a cosine function.',typeVar='Float')
        self.add_param(strChain+'ibal',val=1,optionsVal=(1,2,0), desc='Option to compute balanced field length', aliases=('pre-1998 FAA rules', 'post-1998 FAA rules', 'Do not compute'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'itxout',val=0,optionsVal=(1,0), desc='Weight to use for takeoff field length calculations', aliases=('Ramp weight - taxi out fuel', 'Ramp weight'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'pilott',val=1.0, units='s', desc='Actual pilot reaction time from engine failure to brake application.  Spoilers, brakes, and thrust reversal are assumed to become effective and engine cutback occurs at PILOTT + 2 seconds after engine failure.',typeVar='Float')
        self.add_param(strChain+'tispa',val=0.0, units='s', desc='Not currently used',typeVar='Float')
        self.add_param(strChain+'tibra',val=0.0, units='s', desc='Not currently used',typeVar='Float')
        self.add_param(strChain+'tirva',val=0.0, units='s', desc='Not currently used',typeVar='Float')
        self.add_param(strChain+'ispol',val=1,optionsVal=(0,1), desc='Option for spoiler use during aborted takeoff', aliases=('Not used', 'Used'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'irev',val=1,optionsVal=(0,1,2), desc='Option for thrust reversal during aborted takeoff', aliases=('Not used', 'Only if all engines operational', 'Always used'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_tolin_Landing(self):
        """Container for input:tolin:Landing"""
        strChain = 'input:tolin:Landing:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'clldm',val=-1.0, desc='Maximum CL for landing (Default, see &AERIN)',typeVar='Float')
        self.add_param(strChain+'cdmld',val=0.0, desc='Minimum CD for landing',typeVar='Float')
        self.add_param(strChain+'fcdmld',val=-1.0, desc='Fraction of CDMLD due to wing (Default = FCDMTO)',typeVar='Float')
        self.add_param(strChain+'almxld',val=25.0, units='deg', desc='Maximum angle of attack during landing',typeVar='Float')
        self.add_param(strChain+'obsld',val=50.0, units='ft', desc='Landing obstacle height',typeVar='Float')
        self.add_param(strChain+'alpld',val=array([]), units='deg', desc='Angles of attack for landing polar',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clld',val=array([]), desc='Lift coefficients for landing polar.  These are not generated internally',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdld',val=array([]), desc='Drag coefficients for landing polar.  These are not generated internally',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'inthld',val=0, desc='= 0, Input thrust values will be used\n= 1, The input values will be scaled\n> 1, Scaled engine data deck will be used',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'velld',val=array([]), units='ft/s', desc='Velocities for landing',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'thrld',val=array([]), units='lb', desc='Thrust values',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'thdry',val=-1.0, units='lb', desc='Maximum dry thrust at missed appproach for fighters (Default = takeoff thrust)',typeVar='Float')
        self.add_param(strChain+'aprhgt',val=100.0, units='ft', desc='Height above ground for start of approach',typeVar='Float')
        self.add_param(strChain+'aprang',val=-3.0, units='deg', desc='Approach flight path angle',typeVar='Float')
        self.add_param(strChain+'fldcl',val=1.0, desc='Factor for landing lift',typeVar='Float')
        self.add_param(strChain+'fldcd',val=1.0, desc='Factor for landing drag',typeVar='Float')
        self.add_param(strChain+'tdsink',val=0.0, units='ft/s', desc='Sink rate at touchdown (Must be positive if input)',typeVar='Float')
        self.add_param(strChain+'vangld',val=0.0, units='deg/s', desc='Flare rate (Default = VANGL)',typeVar='Float')
        self.add_param(strChain+'noflar',val=0,optionsVal=(1,0), desc='Option for flare during landing.  If no flare, sink rate at touchdown is the approach sink rate with ground effects.', aliases=('No flare', 'Flare'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'tispol',val=2.0, units='s', desc='Time after touchdown to spoiler actuation',typeVar='Float')
        self.add_param(strChain+'ticut',val=3.0, units='s', desc='Time after touchdown to cut back of engines to zero thrust',typeVar='Float')
        self.add_param(strChain+'tibrak',val=4.0, units='s', desc='Time after touchdown to brake application',typeVar='Float')
        self.add_param(strChain+'acclim',val=16.0, units='ft/(s*s)', desc='Deceleration limit',typeVar='Float')
        self.add_param(strChain+'magrup',val=-1,optionsVal=(1,0,-1), desc='Missed approach landing gear switch', aliases=('Gear up during missed approach', 'Gear down during missed approach', 'Use default'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_tolin_Integration_Intervals(self):
        """Container for input:tolin:Integration_Intervals"""
        strChain = 'input:tolin:Integration_Intervals:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'delvto',val=4.0, units='ft/s', desc='Velocity step during ground run',typeVar='Float')
        self.add_param(strChain+'deltro',val=0.2, units='s', desc='Time step during rotation',typeVar='Float')
        self.add_param(strChain+'deltcl',val=0.2, units='s', desc='Time step during climbout',typeVar='Float')
        self.add_param(strChain+'delhap',val=10.0, units='ft', desc='Altitude step during approach',typeVar='Float')
        self.add_param(strChain+'deldfl',val=10.0, units='ft', desc='Distance step during flare',typeVar='Float')
        self.add_param(strChain+'deltrn',val=0.25, units='s', desc='Time step during runout',typeVar='Float')


    def FlopsWrapper_input_tolin_Basic(self):
        """Container for input:tolin:Basic"""
        strChain = 'input:tolin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'apa',val=0.0, units='ft', desc='Airport altitude',typeVar='Float')
        self.add_param(strChain+'dtct',val=0.0, units='degC', desc='Delta temperature from standard day.  (This parameter is independent from the DTC in Namelist &MISSIN and DTCE in Namelist &ENGINE.)',typeVar='Float')
        self.add_param(strChain+'swref',val=-1.0, units='ft*ft', desc='Wing area on which takeoff and landing drag polars are based (Default = SW, Namelist &CONFIN). If different from SW, polars will be scaled.',typeVar='Float')
        self.add_param(strChain+'arret',val=-1.0, desc='Wing aspect ratio on which takeoff and landing drag polars are based (Default = AR, Namelist &CONFIN). If different from AR, polars will be modified.',typeVar='Float')
        self.add_param(strChain+'whgt',val=8.0, units='ft', desc='Wing height above ground',typeVar='Float')
        self.add_param(strChain+'alprun',val=0.0, units='deg', desc='Angle of attack on ground',typeVar='Float')
        self.add_param(strChain+'tinc',val=0.0, units='deg', desc='Thrust incidence on ground',typeVar='Float')
        self.add_param(strChain+'rollmu',val=0.025, desc='Coefficient of rolling friction',typeVar='Float')
        self.add_param(strChain+'brakmu',val=0.3, desc='Coefficient of friction, brakes on',typeVar='Float')
        self.add_param(strChain+'cdgear',val=0.0, desc='Landing gear drag coefficient',typeVar='Float')
        self.add_param(strChain+'cdeout',val=0.0, desc='Delta drag coefficient due to engine out condition.  Includes effect of stopped or windmilling engine and the trim drag associated with compensating for asymmetric thrust.',typeVar='Float')
        self.add_param(strChain+'clspol',val=0.0, desc='Spoiler delta lift coefficient (Should be negative)',typeVar='Float')
        self.add_param(strChain+'cdspol',val=0.0, desc='Spoiler delta drag coefficient',typeVar='Float')
        self.add_param(strChain+'incgef',val=1,optionsVal=(1,0), desc='Ground effects switch', aliases=('Ground effects', 'No ground effects'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'argef',val=1.0, desc='Aspect ratio factor for ground effects',typeVar='Float')
        self.add_param(strChain+'itime',val=0,optionsVal=(1,0), desc='Detailed takeoff and landing profiles print option', aliases=('Print', 'No print'),typeVar='Enum',pass_by_obj=True)




    def FlopsWrapper_input_syntin_Variables(self):
        """Container for input:syntin:Variables"""
        strChain = 'input:syntin:Variables:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'desrng',val=-1.0, desc='Design range, n.mi. (or endurance, min.). See INDR in Namelist &MISSIN (Overrides input in Namelist &CONFIN).',typeVar='Float')
        self.add_param(strChain+'vappr',val=-1.0, units='nmi', desc='Maximum allowable landing approach velocity (Overrides input in Namelist &AERIN)',typeVar='Float')
        self.add_param(strChain+'flto',val=-1.0, units='ft', desc='Maximum allowable takeoff field length (Overrides input in Namelist &AERIN)',typeVar='Float')
        self.add_param(strChain+'flldg',val=-1.0, units='ft', desc='Maximum allowable landing field length (Overrides input in Namelist &AERIN)',typeVar='Float')
        self.add_param(strChain+'exfcap',val=0.0, units='lb', desc='Minimum allowable excess fuel capacity',typeVar='Float')
        self.add_param(strChain+'cdtmax',val=-1.0, units='degR', desc='Maximum allowable compressor discharge temperature (Overrides input in Namelist &ENGINE',typeVar='Float')
        self.add_param(strChain+'cdpmax',val=-1.0, units='psi', desc='Maximum allowable compressor discharge pressure (Overrides input in Namelist &ENGINE',typeVar='Float')
        self.add_param(strChain+'vjmax',val=-1.0, units='ft/s', desc='Maximum allowable jet velocity (Overrides input in Namelist &ENGINE',typeVar='Float')
        self.add_param(strChain+'stmin',val=-1.0, units='lb/lb/s', desc='Minimum allowable specific thrust (Overrides input in Namelist &ENGINE',typeVar='Float')
        self.add_param(strChain+'armax',val=-1.0, desc='Maximum allowable ratio of the bypass area to the core area of a mixed flow turbofan (Overrides input in Namelist &ENGINE',typeVar='Float')
        self.add_param(strChain+'gnox',val=0.0, units='lb', desc='Maximum allowable NOx emissions',typeVar='Float')
        self.add_param(strChain+'roclim',val=100.0, units='ft/min', desc='Minimum allowable potential rate of climb during climb segments',typeVar='Float')
        self.add_param(strChain+'dhdtlm',val=100.0, units='ft/min', desc='Minimum allowable actual rate of climb during climb segments',typeVar='Float')
        self.add_param(strChain+'tmglim',val=0.1, desc='Minimum allowable thrust margin, (Thrust-Drag)/Drag, during climb segments',typeVar='Float')
        self.add_param(strChain+'ig',val=array([]), desc='= 1, Ith behavioral constraint is used in optimization\n= 0, Otherwise',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ibfgs',val=1,optionsVal=(0,1,2,3,4,5), desc='Search algorithm for optimization', aliases=('Davidon-Fletcher-Powell', 'Broyden-Fletcher-Goldfarb-Shano', 'Conjugate Gradient (Polak-Ribiere)', 'Steepest Descent', 'Univariate Search', 'Kreisselmeier-Steinhauser with DFP'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'itfine',val=0,optionsVal=(1,0), desc='Option to set IRW = 1 for final analysis', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_syntin_Optimization_Control(self):
        """Container for input:syntin:Optimization_Control"""
        strChain = 'input:syntin:Optimization_Control:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ndd',val=0, desc='Number of drawdowns (Defaults to analysis only - no optimization is performed.  Suggested value = 3 or 4)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'rk',val=0.0, desc='Initial value of RK (Default internally computed)',typeVar='Float')
        self.add_param(strChain+'fdd',val=0.2, desc='RK multiplier for successive drawdowns',typeVar='Float')
        self.add_param(strChain+'nlin',val=-1, desc='Maximum number of gradients per drawdown (Default = number of active design variables times 2)',typeVar='Int')
        self.add_param(strChain+'nstep',val=20, desc='Maximum number of steps per one-dimensional minimization (Default = 20)',typeVar='Int')
        self.add_param(strChain+'ef',val=3.0, desc='Limits one-dimensional minimization step size to EF times previous step',typeVar='Float')
        self.add_param(strChain+'eps',val=0.001, desc='Fraction of initial design variable value used as a finite difference delta',typeVar='Float')
        self.add_param(strChain+'amult',val=10.0, desc='The initial step in a one-dimensional search is controlled by the design variable value times EPS times AMULT',typeVar='Float')
        self.add_param(strChain+'dep',val=0.001, desc='One-dimensional search convergence criterion on step size as a fraction of move distance',typeVar='Float')
        self.add_param(strChain+'accux',val=3.0e-4, desc='One-dimensional search convergence criterion on step size as a fraction of initial design variable value',typeVar='Float')
        self.add_param(strChain+'glm',val=0.0, desc='Value of G at which constraint switches to quadratic extended form, a value of .002 is recommended',typeVar='Float')
        self.add_param(strChain+'gfact',val=array([]), desc='Scaling factor for each behavioral constraint',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'autscl',val=1.0, desc='Design variable scale factor exponent.  Scale factors for design variables default to VALUE ** AUTSCL',typeVar='Float')
        self.add_param(strChain+'icent',val=0,optionsVal=(0,1), desc='Type of differencing to be used in gradient calculations', aliases=('Forward', 'Central'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'rhomin',val=0.0, desc='Starting value for RHO, a scalar multiplying factor used in the KS function.  (Default is computed internally)',typeVar='Float')
        self.add_param(strChain+'rhomax',val=300.0, desc='Maximum value for RHO',typeVar='Float')
        self.add_param(strChain+'rhodel',val=0.0, desc='RHO increment (Default is computed internally)',typeVar='Float')
        self.add_param(strChain+'itmax',val=30, desc='Maximum number of iterations',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'jprnt',val=2, desc='KS module print control\n= 0, No output from the KS module\n= 999, Maximum output',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'rdfun',val=0.01, desc='If the relative change in the KS function is less than RDFUN for three consecutive iterations, optimization is terminated.',typeVar='Float')
        self.add_param(strChain+'adfun',val=0.001, desc='If the absolute change in the KS function is less than ADFUN for three consecutive iterations, optimization is terminated.',typeVar='Float')




    def FlopsWrapper_input_rfhin(self):
        """Container for input:rfhin"""
        strChain = 'input:rfhin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'tmach',val=array([]), desc='Mach numbers in increasing order',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdmin',val=array([]), desc='Minimum drag for each Mach number.\nThe lift dependent drag coefficient for the Ith Mach number is computed from:\n\nCD = CDMIN(I) + CK(I) * [CL - CLB(I)] ** 2\n+ C1SW(I) * (SW/REFAS - REFBS) ** EXPS\n+ C1TH(I) * (THRUST/REFAT - REFBT) ** EXPT\n\nwhere SW and THRUST are the current values for the wing area and for the thrust per engine, and CL is the lift coefficient.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ck',val=array([]), desc='Drag-due-to-lift factors for each Mach number',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clb',val=array([]), desc='Lift coefficients corresponding to each CDMIN',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'c1sw',val=array([]), desc='Coefficient for wing area term for each Mach number.  May be a drag coefficient or D/Q depending on the values of REFAS, REFBS and EXPS.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'c1th',val=array([]), desc='Coefficient for thrust term for each Mach number.  May be a drag coefficient or D/Q depending on the values of REFAT, REFBT and EXPT.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'refas',val=1.0, desc='Wing area reference value',typeVar='Float')
        self.add_param(strChain+'refbs',val=0.0, desc='Wing area base value',typeVar='Float')
        self.add_param(strChain+'exps',val=1.0, desc='Wing area term exponent',typeVar='Float')
        self.add_param(strChain+'refat',val=1.0, desc='Thrust reference value',typeVar='Float')
        self.add_param(strChain+'refbt',val=0.0, desc='Thrust base value',typeVar='Float')
        self.add_param(strChain+'expt',val=1.0, desc='Thrust term exponent',typeVar='Float')


    def FlopsWrapper_input_proin(self):
        """Container for input:proin"""
        strChain = 'input:proin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'npol',val=0, desc='Number of drag polars to be printed out (Default = size of dflap)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'alpro',val=array([]), units='deg', desc='Angles of attack for each drag polar',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clpro',val=array([]), desc='Lift coefficients for each drag polar',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdpro',val=array([]), desc='Drag coefficients for each drag polar',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'dflap',val=array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), dtype=array([]), units='deg', desc='Flap deflection corresponding to each drag polar.  Used only for output',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'ntime',val=0,optionsVal=(1,0), desc='Option for printing detailed takeoff and climb profiles for noise', aliases=('Print', 'No print'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ipcmax',val=1, desc='Maximum engine power code (This variable could be used, for example, to limit takeoff and climb to dry power settings on an afterburning engine.)',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'keas',val=0,optionsVal=(1,0), desc='Type of velocity given by VFIX in namelist &SEGIN', aliases=('Knots equivalent airspeed (keas)', 'True airspeed'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'txf',val=-1.0, units='lb', desc='Fuel used in taxiing out to runway (Default is computed in mission analysis)',typeVar='Float')
        self.add_param(strChain+'alpmin',val=0.0, units='deg', desc='Minimum angle of attack during climb segment',typeVar='Float')
        self.add_param(strChain+'gamlim',val=0.0, units='deg', desc='Minimum flight path angle during fixed angle of attack segments',typeVar='Float')
        self.add_param(strChain+'inm',val=0,optionsVal=(1,0), desc='Option to generate data files necessary for transporting FLOPS takeoff and climb profile data to the FAA Integrated Noise Model (INM) program', aliases=('Generate', 'Do not generate'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iatr',val=0,optionsVal=(1,0), desc='Automatic thrust restoration indicator option (INM=1, has no effect of takeoff and climb profile)', aliases=('ATR', 'No ATR'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'fzf',val=1.25, desc='Maneuver speed factor (INM=1)',typeVar='Float')
        self.add_param(strChain+'thclmb',val=-1.0, desc='Climb throttle setting (INM=1)',typeVar='Float')
        self.add_param(strChain+'flapid',val=[], desc='Six character label for each of the NPOL input drag polars, for example, "gearup"',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_option_Program_Control(self):
        """Container for input:option:Program_Control"""
        strChain = 'input:option:Program_Control:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'mprint',val=1,optionsVal=(0,1), desc='Print control \n = 0, Print only 3-5 line summary for each analysis. Usually used only for contour plots (IOPT = 4) \n = 1, Normal output for all analyses', aliases=('Short Summary', 'Normal'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iopt',val=1,optionsVal=(1,2,3,4), desc='Execution Type', aliases=('Analysis', 'Parametric Variation', 'Optimization', 'Contour or Thumbprint plot'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ianal',val=3,optionsVal=(1,2,3,4), desc='Analysis Type', aliases=('Weights', 'Weights and Aerodynamics', 'Full Analysis', 'Propulsion'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ineng',val=0,optionsVal=(0,1), desc='Force engine Data Read', aliases=('If necessary', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'itakof',val=0,optionsVal=(0,1), desc='Detailed takeoff', aliases=('No', 'Yes (Namelist &TOLIN required)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iland',val=0,optionsVal=(0,1), desc='Detailed landing', aliases=('No', 'Yes (Namelist &TOLIN required)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nopro',val=0,optionsVal=(0,1), desc='Generate takeoff and climb profiles (Namelists &TOLIN &PROIN and &SEGIN required)', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'noise',val=0,optionsVal=(0,1,2), desc='Calculate noise', aliases=('No', 'Yes (Namelist &COSTIN required)', 'Yes for final analysis only'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icost',val=0,optionsVal=(0,1), desc='Calculate costs', aliases=('No', 'Yes (Namelist &COSTIN required)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifite',val=0,optionsVal=(0,1,2,3), desc='Weight equations', aliases=('Transports', 'Fighter/attack', 'General aviation', 'Blended wing body'),typeVar='Enum',pass_by_obj=True)




    def FlopsWrapper_input_option_Excess_Power_Plot(self):
        """Container for input:option:Excess_Power_Plot"""
        strChain = 'input:option:Excess_Power_Plot:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xmax',val=0.9, desc='Maximum Mach number for plots',typeVar='Float')
        self.add_param(strChain+'xmin',val=0.3, desc='Minimum Mach number for plots',typeVar='Float')
        self.add_param(strChain+'xinc',val=0.2, desc='Mach number increment for plots',typeVar='Float')
        self.add_param(strChain+'ymax',val=40000.0, units='ft', desc='Maximum altitude for plots',typeVar='Float')
        self.add_param(strChain+'ymin',val=0.0, units='ft', desc='Minimum altitude for plots',typeVar='Float')
        self.add_param(strChain+'yinc',val=10000.0, units='ft', desc='Altitude increment for plots',typeVar='Float')
        self.add_param(strChain+'pltnz',val=array([]), desc='Nz at which Ps contours are plotted (or Nz)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pltpc',val=array([]), desc='Engine power (fraction if =< 1; else setting)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ipstdg',val=array([]), desc='Store drag schedule (see Namelist &MISSIN)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pltwt',val=array([]), units='lb', desc='Fixed weight',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ipltsg',val=array([]), desc='Weight at start of mission segment IPLTSG is used',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pltfm',val=array([]), desc='Fraction of fuel burned',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'pltwta',val=array([]), units='lb', desc='Delta weight',typeVar='Array',pass_by_obj=True)




    def FlopsWrapper_input_noisin_Turbine(self):
        """Container for input:noisin:Turbine"""
        strChain = 'input:noisin:Turbine:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'tsupp',val=array([]), desc='Turbine suppression spectrum',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'tbndia',val=-1.0, units='ft', desc='Diameter of last-stage turbine',typeVar='Float')
        self.add_param(strChain+'gear',val=1.0, desc='Gear ratio:  turbine RPM/fan RPM',typeVar='Float')
        self.add_param(strChain+'cs',val=0.0, desc='Stator chord to rotor spacing ratio',typeVar='Float')
        self.add_param(strChain+'nblr',val=-1, desc='Number of last stage rotor blades',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'ityptb',val=0,optionsVal=(1,0), desc='Type of exit plane', aliases=('Turbofans', 'Turbojets or coplanar exits'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'etdop',val=4.0, desc='Exponent on source motion (Doppler) amplification on turbine noise',typeVar='Float')


    def FlopsWrapper_input_noisin_Shielding(self):
        """Container for input:noisin:Shielding"""
        strChain = 'input:noisin:Shielding:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'iuotw',val=0,optionsVal=(1,0), desc='Engine location relative to wing', aliases=('Over the wing', 'Under the wing'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'sfuse',val=10.0, desc='Maximum fuselage shielding',typeVar='Float')
        self.add_param(strChain+'swide',val=60.0, units='deg', desc='Degrees of arc where fuselage shielding is greater than SFUSE/e',typeVar='Float')
        self.add_param(strChain+'swing',val=10.0, desc='Maximum wing shielding for over-the-wing engine',typeVar='Float')
        self.add_param(strChain+'smx',val=90.0, units='deg', desc='Angle in flyover plane of maximum over-the-wing shielding',typeVar='Float')
        self.add_param(strChain+'cfuse',val=10.0, units='ft', desc='Characteristic fuselage dimension (such as diameter)',typeVar='Float')
        self.add_param(strChain+'cwing',val=10.0, units='ft', desc='Characteristic wing dimension (such as chord)',typeVar='Float')


    def FlopsWrapper_input_noisin_Propeller(self):
        """Container for input:noisin:Propeller"""
        strChain = 'input:noisin:Propeller:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'nb',val=0, desc='Number of blades per propeller',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'bldia',val=0.0, units='ft', desc='Diameter of propeller',typeVar='Float')
        self.add_param(strChain+'blarea',val=0.0, units='ft*ft', desc='Total blade area for one side of propeller',typeVar='Float')
        self.add_param(strChain+'gearp',val=1.0, desc='Ratio of propeller rpm / engine rpm',typeVar='Float')
        self.add_param(strChain+'epdop',val=1.0, desc='Exponent on source motion (Doppler) amplification on propeller noise',typeVar='Float')
        self.add_param(strChain+'blth',val=0.0, units='ft', desc='Blade thickness at 70% span',typeVar='Float')
        self.add_param(strChain+'blch',val=0.0, units='ft', desc='Blade chord at 70% span',typeVar='Float')
        self.add_param(strChain+'blattk',val=0.0, units='deg', desc='Blade angle of attack at 70% span',typeVar='Float')
        self.add_param(strChain+'dharm',val=0.5, desc='Rate of decrease in harmonic level beyond tenth, dB/harmonic',typeVar='Float')
        self.add_param(strChain+'nph',val=10, desc='Number of harmonics of BDF desired',typeVar='Int',pass_by_obj=True)
        self.add_param(strChain+'ivor',val=1,optionsVal=(1,0), desc='Calculate vortex noise component', aliases=('Vortex noise', 'No vortex noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'irot',val=1,optionsVal=(1,0), desc='Calculate rotational noise component', aliases=('Rotational noise', 'No rotational noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ipdir',val=0,optionsVal=(1,0), desc='Apply Boeing directivity correction', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'psupp',val=array([]), desc='Propeller noise suppression spectrum',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_noisin_Propagation(self):
        """Container for input:noisin:Propagation"""
        strChain = 'input:noisin:Propagation:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'isupp',val=0,optionsVal=(1,0), desc='Apply suppression spectra to each source for which they are supplied', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'idop',val=0,optionsVal=(1,0), desc='Apply Doppler frequency and intensity correction to total noise', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ignd',val=0,optionsVal=(0,1,2), desc='Ground reflection option', aliases=('None', 'Perfect reflection', 'Putnam method'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iatm',val=0,optionsVal=(0,1,2), desc='Atmospheric absorption correction', aliases=('None', 'SAE ARP 866', 'Bass & Shields'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iega',val=0,optionsVal=(1,0), desc='Extra ground attenuation', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ishld',val=0,optionsVal=(1,0), desc='Shielding of fan, jet, core, turbine and propeller sources', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'deldb',val=20.0, desc='Number of dB down from the peak noise level to cut off printing of noise time histories',typeVar='Float')
        self.add_param(strChain+'heng',val=0.0, units='ft', desc='Height of engine above ground during taxi',typeVar='Float')
        self.add_param(strChain+'filbw',val=1.0, desc='Fraction of filter bandwidth with a gain of 1',typeVar='Float')
        self.add_param(strChain+'tdi',val=1.0, units='s', desc='Reception time increment',typeVar='Float')
        self.add_param(strChain+'rh',val=70.0, desc='Ambient relative humidity',typeVar='Float')


    def FlopsWrapper_input_noisin_Observers(self):
        """Container for input:noisin:Observers"""
        strChain = 'input:noisin:Observers:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xo',val=array([]), units='ft', desc='X-coordinates of observers',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'yo',val=array([]), units='ft', desc='Y-coordinates of observers',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'zo',val=0.0, units='ft', desc='Height of all observers above the ground',typeVar='Float')
        self.add_param(strChain+'ndprt',val=1,optionsVal=(1,0), desc='Print observer noise histories',typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifoot',val=0,optionsVal=(1,0), desc='Print noise levels of input observers in countour format to file NSPLOT for subsequent plotting of the noise footprint', aliases=('Print', 'No print'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'igeom',val=0,optionsVal=(1,0), desc='Print geometric relations of aircraft/observer at each time point', aliases=('Print', 'No print'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'thrn',val=-1.0, units='lb', desc='Thrust of baseline engine.  Geometry data and engine parameter arrays will be scaled accordingly (Default=THRSO, Namelist &WTIN)',typeVar='Float')
        self.add_param(strChain+'icorr',val=0,optionsVal=(1,0), desc='Apply corrections to engine parameters to correct for ambient conditions', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'tcorxp',val=1.0, desc='Exponent for core temperature correction in engine parameter arrays',typeVar='Float')


    def FlopsWrapper_input_noisin_MSJet(self):
        """Container for input:noisin:MSJet"""
        strChain = 'input:noisin:MSJet:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'iy9',val=1,optionsVal=(1,2,3,4,5,6), desc='Type of nozzle', aliases=('Convergent conical', 'Single multitube', 'Single multichute', 'Dual convergent conical', 'Dual, multitube on outer', 'Dual, multichute/spoke on outer'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'n',val=1, desc='Number of tubes (IY9=2,5) or elements (IY9=3,6)',typeVar='Int')
        self.add_param(strChain+'rp',val=0.0, units='ft', desc='Centerbody plug radius (IY9=2,3,5,6)',typeVar='Float')
        self.add_param(strChain+'b9',val=0.0, units='deg', desc='Tube centerline cant angle (IY9-2,5)\nChute/spoke exit cant angle (IY9=3,6)',typeVar='Float')
        self.add_param(strChain+'dt',val=0.0, units='inch', desc='Tube diameter (IY9=2,5)',typeVar='Float')
        self.add_param(strChain+'z5',val=0.0, desc='Number of rows of tubes, counting center tube (if present) as zero (IY9=2,5)',typeVar='Float')
        self.add_param(strChain+'s1j',val=0.0, desc='Tube centerline spacing to tube diameter ratio (IY9=2,5)',typeVar='Float')
        self.add_param(strChain+'a6',val=0.0, desc='Ratio of ejector inlet area to nozzle (total or annulus) area (input zero for no ejector) (IY9=2,3,5,6)',typeVar='Float')
        self.add_param(strChain+'zl9',val=0.0, desc='Ratio of ejector length to suppressor nozzle equivalent diameter (IY9=2,3,5,6)',typeVar='Float')
        self.add_param(strChain+'a',val=array([]), desc='A(0): Ejector treatment faceplate thickness, in\nA(1): Ejector treatment hole diameter, in\nA(2): Ejector treatment cavity depth, in\nA(3): Ejector treatment open area ratio\n(IY9=2,3,5,6)',typeVar='Array',pass_by_obj=True)

    # TODO - rr and rx are units of 'Rayl' (rayleigh)
        self.add_param(strChain+'rr',val=array([]), desc='Ejector treatment specific resistance (59 values required) (IY9=2,3,5,6)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'rx',val=array([]), desc='Ejector treatment specific reactance (59 values required) (IY9=2,3,5,6)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'r4',val=0.0, units='inch', desc='Outer circumferential flow dimension (IY9=3,6)',typeVar='Float')
        self.add_param(strChain+'r6',val=0.0, units='inch', desc='Inner circumferential flow dimension (IY9=3,6)',typeVar='Float')
        self.add_param(strChain+'ss',val=0.0, units='inch', desc='Outer circumferential element dimension (IY9=3,6)',typeVar='Float')
        self.add_param(strChain+'dn',val=0.0, units='ft', desc='Nozzle outer diameter',typeVar='Float')
        self.add_param(strChain+'aa',val=0.0, desc='Unknown variable',typeVar='Float')
        self.add_param(strChain+'nflt',val=1, desc='Unknown variable',typeVar='Int')
        self.add_param(strChain+'htr',val=0.0, desc='Unknown variable',typeVar='Float')
        self.add_param(strChain+'nst',val=1, desc='Unknown variable',typeVar='Int')


    def FlopsWrapper_input_noisin_Jet(self):
        """Container for input:noisin:Jet"""
        strChain = 'input:noisin:Jet:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inoz',val=0,optionsVal=(1,0), desc='Type of nozzle', aliases=('Coaxial', 'Circular'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iplug',val=0,optionsVal=(1,0), desc='Plug nozzle on primary', aliases=('Plug', 'No plug'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'islot',val=0,optionsVal=(1,0), desc='Slot nozzle on primary', aliases=('Slot nozzle', 'No slot'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iaz',val=0,optionsVal=(1,0), desc='Azimuthal correction for nozzle geometry', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'dbaz',val=0.0, desc='Noise reduction due to nozzle geometry at phi = 75 degrees, used only if IAZ = 1',typeVar='Float')
        self.add_param(strChain+'ejdop',val=1.0, desc='Exponent on source motion (Doppler) amplification on shock noise only.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'zmdc',val=1.0, desc='Core (primary) jet design Mach number.  Used for application of non-ideally expanded shock noise.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'gammac',val=-1.0, desc='Core (primary) jet exhaust gamma Used for IJET=1,2,6 (Default = 1.4)',typeVar='Float')
        self.add_param(strChain+'gasrc',val=-1.0, units='(ft*lb)/(lb*degR)', desc='Core exhaust gas constant, Used for IJET=1,2 (Default = 53.35)',typeVar='Float')
        self.add_param(strChain+'annht',val=0.0, units='ft', desc='Core nozzle annulus height.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'zmdf',val=1.0, desc='Fan (secondary) jet design Mach number.  Used for application of non-ideally expanded shock noise.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'gammap',val=-1.0, desc='Fan (secondary) jet exhaust gamma Used for IJET=1,2 (Default = GAMMAF)',typeVar='Float')
        self.add_param(strChain+'gasrf',val=53.35, units='(ft*lb)/(lb*degR)', desc='Fan exhaust gas constant.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'annhtf',val=0.0, units='ft', desc='Fan nozzle annulus height.  Used for IJET=1,2',typeVar='Float')
        self.add_param(strChain+'dhc',val=-1.0, units='ft', desc='Core nozzle hydraulic diameter.  Used for IJET=3,4',typeVar='Float')
        self.add_param(strChain+'dhf',val=0.0, units='ft', desc='Fan nozzle hydraulic diameter.  Used for IJET=3,4',typeVar='Float')
        self.add_param(strChain+'zl2',val=0.0, units='ft', desc='Axial distance from the outer exit plane to the exit plane of the inner nozzle.  Used for IJET=3,4',typeVar='Float')
        self.add_param(strChain+'ifwd',val=0,optionsVal=(1,0), desc='Forward velocity effects on source.  Used for IJET=1,2,3,4,5', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ishock',val=1,optionsVal=(1,0), desc='Calculate shock noise.  Used for IJET=1,2,3,4,5', aliases=('Shock noise', 'No shock'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'zjsupp',val=array([]), desc='Jet suppression spectrum.  Used for IJET=1,2,3,4,5',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_noisin_Ground_Effects(self):
        """Container for input:noisin:Ground_Effects"""
        strChain = 'input:noisin:Ground_Effects:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'itone',val=0,optionsVal=(1,0), desc='1/3-octave bands exceeding adjacent bands by 3 dB or more are approximated as tones', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        #self.add_param(strChain+'nht',val=0, desc='Number of heights to be used to approximate a distributed source by multiple sources',typeVar='Int')
        self.add_param(strChain+'dk',val=array([]), units='ft', desc='Heights of multiple sources from source center',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_noisin_Flap_Noise(self):
        """Container for input:noisin:Flap_Noise"""
        strChain = 'input:noisin:Flap_Noise:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ilnoz',val=0,optionsVal=(2,1,0), desc='Nozzle type', aliases=('Coaxial, mixed flow', 'Coaxial, separate flow', 'Circular'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'insens',val=0,optionsVal=(1,0), desc='Configuration with noise levels insensitive to flap angle', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ac1',val=0.0, units='ft*ft', desc='Core (primary) nozzle area',typeVar='Float')
        self.add_param(strChain+'af1',val=0.0, units='ft*ft', desc='Fan (secondary) nozzle area',typeVar='Float')
        self.add_param(strChain+'bpr',val=0.0, desc='Bypass ratio, for mixed flow coaxial nozzle',typeVar='Float')
        self.add_param(strChain+'wingd',val=0.0, desc='Ratio of wing chord to total nozzle diameter, used for large BPR designs when WINGD < 3',typeVar='Float')
        self.add_param(strChain+'flsupp',val=array([]), desc='Flap noise suppression spectrum',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'eldop',val=0.0, desc='Exponent on source motion (Doppler) amplification on flap noise',typeVar='Float')


    def FlopsWrapper_input_noisin_Fan(self):
        """Container for input:noisin:Fan"""
        strChain = 'input:noisin:Fan:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'igv',val=0,optionsVal=(1,0), desc='Inlet guide vane option', aliases=('Inlet guide vane', 'No IGV'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifd',val=0,optionsVal=(1,0), desc='Inlet flow distortion option during ground run', aliases=('Inlet flow distortion', 'No distortion'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iexh',val=2,optionsVal=(0,1,2), desc='Fan inlet, exhaust noise options', aliases=('Inlet only', 'Exhaust only', 'Both inlet & exhaust'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nfh',val=10, desc='Number of harmonics to be considered in blade-passing tone',typeVar='Int')
        self.add_param(strChain+'nstg',val=-1, desc='Number of fan stages',typeVar='Int')
        self.add_param(strChain+'suppin',val=array([]), desc='Fan inlet suppression spectrum',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'suppex',val=array([]), desc='Fan exhaust suppression spectrum',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'methtip',val=1,optionsVal=(1,2,3), desc='Method for calculation of relative tip Mach number', aliases=('ANOPP method', 'Clark', 'Use ATIPM'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icomb',val=1,optionsVal=(1,0), desc='Option to include combination tones if relative tip Mach number is supersonic', aliases=('Combination tones', 'No combination tones'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'decmpt',val=0.0, desc='Decrement to apply to combination tones',typeVar='Float')
        self.add_param(strChain+'gammaf',val=1.4, desc='Gamma of fan air',typeVar='Float')
        self.add_param(strChain+'nbl',val=-1, desc='Number of fan blades',typeVar='Int')
        self.add_param(strChain+'nvan',val=-1, desc='Number of stator vanes',typeVar='Int')
        self.add_param(strChain+'fandia',val=-1.0, units='ft', desc='Fan diameter',typeVar='Float')
        self.add_param(strChain+'fanhub',val=-1.0, units='ft', desc='Fan hub diameter',typeVar='Float')
        self.add_param(strChain+'tipmd',val=-1.0, desc='Design relative tip Mach number',typeVar='Float')
        self.add_param(strChain+'rss',val=100.0, desc='Rotor-stator spacing in percent',typeVar='Float')
        self.add_param(strChain+'efdop',val=4.0, desc='Exponent on source motion (Doppler) amplification on fan noise',typeVar='Float')
        self.add_param(strChain+'faneff',val=0.88, desc='Constant first stage fan efficiency, < 1.0.  Overridden by AFANEF',typeVar='Float')
        self.add_param(strChain+'nbl2',val=-1, desc='Number of fan blades for second stage (Default = NBL)',typeVar='Int')
        self.add_param(strChain+'nvan2',val=-1, desc='Number of stator vanes for second stage (Default = NVAN)',typeVar='Int')
        self.add_param(strChain+'fand2',val=-1.0, units='ft', desc='Fan diameter for second stage (Default = FANDIA)',typeVar='Float')
        self.add_param(strChain+'tipmd2',val=-1.0, desc='Design relative tip Mach number for second stage (Default = TIPMD)',typeVar='Float')
        self.add_param(strChain+'rss2',val=-1.0, desc='Rotor-stator spacing in percent for second stage (Default = RSS)',typeVar='Float')
        self.add_param(strChain+'efdop2',val=-1.0, desc='Exponent on source motion (Doppler) amplification on second stage fan noise (Default = EFDOP)',typeVar='Float')
        self.add_param(strChain+'fanef2',val=0.88, desc='Constant second stage fan efficiency, < 1.0.  Overridden by AFANF2',typeVar='Float')
        self.add_param(strChain+'trat',val=-1.0, desc='Ratio of second stage temperature rise (DELT2) to that of first stage.  Either TRAT or PRAT is used to calculate DELT2.',typeVar='Float')
        self.add_param(strChain+'prat',val=1.0, desc='Ratio of second stage fan pressure ratio to that of first stage',typeVar='Float')


    def FlopsWrapper_input_noisin_Engine_Parameters(self):
        """Container for input:noisin:Engine_Parameters"""
        strChain = 'input:noisin:Engine_Parameters:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'aepp',val=array([]), desc='Throttle settings as a fraction of net thrust',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'avc',val=array([]), units='ft/s', desc='Core/primary exhaust jet velocity (ideally expanded velocity; exclude friction and expansion alterations).  Used for IJET=1,2,3,4,6',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'avf',val=array([]), units='ft/s', desc='Fan/secondary exhaust jet velocity (ideally expanded velocity; exclude friction and expansion alterations).  Used for IJET=1,2,3,4',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'atc',val=array([]), units='degR', desc='Core/primary jet exhaust total temperature.  Used for IJET=1,2,3,4,6',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'atf',val=array([]), units='degR', desc='Fan/secondary jet exhaust total temperature.  Used for IJET=1,2,3,4',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'aac',val=array([]), units='ft*ft', desc='Core jet nozzle exhaust area.  For IJET=1,2,6, AAC represents exit area; for IJET=3,4, AAC represents throat area.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'aaf',val=array([]), units='ft*ft', desc='Fan jet nozzle exhaust area.  For IJET=1 or IJET=2, AAF represents exit area; for IJET=3,4, AAF represents throat area.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'adj',val=array([]), units='ft', desc='Core outer diameter; at the equivalent throat if the nozzle is C-D.   Used only for IJET=3,4',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'adj2',val=array([]), units='ft', desc='Fan outer diameter; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'ahj',val=array([]), units='ft', desc='Core annulus height; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'ahj2',val=array([]), units='ft', desc='Fan annulus height; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'afuel',val=array([]), units='lb/s', desc='Fuel flow.  Used if ICORE, ITURB=1; and IJET=1,2 and only if calculating GAMMAC and GASRC.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'atipm',val=array([]), desc='Fan first-stage relative tip Mach number.  These are approximated if not input.  Used if IFAN=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'atipm2',val=array([]), desc='Fan second-stage relative tip Mach number.  These are approximated if not input.  Used if IFAN=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'awafan',val=array([]), units='lb/s', desc='Total engine airflow.  Used if IFAN=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'adelt',val=array([]), units='degR', desc='Fan temperature rise.  Used if IFAN=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'afpr',val=array([]), desc='Fan pressure ratio.  This is not needed if ADELT is input.  Otherwise, values for ADELT will be calculated using AFANEF and AFANF2 values.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'afanef',val=array([]), desc='Fan first-stage efficiency.  These are required if AFPR is supplied rather than ADELT.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'afanf2',val=array([]), desc='Fan second-stage efficiency.  These are required if AFPR is supplied rather than ADELT.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'arpm',val=array([]), units='rpm', desc='Fan or turbine speed.  Used if IFAN, ITURB=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'awcore',val=array([]), units='lb/s', desc='Burner and turbine airflow.  Used if ICORE or ITURB=1 and IJET=1,2 and only if calculating GAMMAC and GASRC.',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'ap3',val=array([]), units='psf', desc='Burner inlet pressure.  Used if ICORE=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'at3',val=array([]), units='degR', desc='Burner inlet temperature.  Used if ICORE=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'at4',val=array([]), units='degR', desc='Burner exit static temperature.  These are approximated from the fuel/air ratio if not input.  Used if ICORE=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'aturts',val=array([]), units='ft/s', desc='Turbine last stage rotor relative tip speed.  These are approximated if not input.  Used if ITURB=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'atctur',val=array([]), units='degR', desc='Turbine exit temperature.  These are assumed the same as ATC if not supplied.  Used if ITURB=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'aepwr',val=array([]), units='hp', desc='Horsepower supplied to propeller.  Used if IPROP=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'athrst',val=array([]), units='lb', desc='Propeller thrust.  Used if IPROP=1',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsp9',val=array([]), desc='Nozzle pressure ratio: entance total to ambient static.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amstt3',val=array([]), units='degR', desc='Nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsa9',val=array([]), units='ft*ft', desc='Nozzle exit area.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsa7',val=array([]), desc='Nozzle ejector chute area ratio.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsaa8',val=array([]), units='ft*ft', desc='Inner nozzle flow area.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amstt4',val=array([]), units='degR', desc='Inner nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsp4',val=array([]), desc='Inner nozzle pressure ratio: entrance total to ambient static.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amstt5',val=array([]), units='degR', desc='Outer nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'amsp5',val=array([]), desc='Outer nozzle pressure ratio: entrance total to ambient static.  Used for M*S code jet predictions, IJET=5',typeVar='Array,float',pass_by_obj=True)


    def FlopsWrapper_input_noisin_Core(self):
        """Container for input:noisin:Core"""
        strChain = 'input:noisin:Core:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'csupp',val=array([]), desc='Core suppression spectrum',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'gamma',val=1.4, desc='Specific heat ratio;  required if using AP3 rather than AT3',typeVar='Float')
        self.add_param(strChain+'imod',val=0,optionsVal=(1,0), desc='Use modified core level prediction', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'dtemd',val=-1.0, units='degR', desc='Design turbine temperature drop',typeVar='Float')
        self.add_param(strChain+'ecdop',val=2.0, desc='Exponent on source motion (Doppler) amplification on core noise',typeVar='Float')


    def FlopsWrapper_input_noisin_Basic(self):
        """Container for input:noisin:Basic"""
        strChain = 'input:noisin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'iepn',val=0,optionsVal=(0,1,2), desc='= 0, Stage III\n= 1, Stage III - Delta dB (see DEPNT, DEPNS and DEPNL)\n=2, Find the X-coordinate where the maximum EPNL occurs.  NOB, XO and YO must be input.  YO should be constant.  IEPN=2 is usually used to get a sideline (YO) noise for GA aircraft.', aliases=('Stage III', 'Stage III - Delta', 'Find max. EPNL'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'depnt',val=0.0, desc='Increment below Stage III for takeoff (see IEPN)',typeVar='Float')
        self.add_param(strChain+'depns',val=0.0, desc='Increment below Stage III for sideline (see IEPN).\nIf IEPN=2, DEPNS is the upper limit for sideline noise.',typeVar='Float')
        self.add_param(strChain+'depnl',val=0.0, desc='Increment below Stage III for landing (see IEPN)',typeVar='Float')
        self.add_param(strChain+'itrade',val=0,optionsVal=(1,0), desc='Option to trade 2 dB between sideline and flyover noise', aliases=('Trade', 'No trade'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ijet',val=0,optionsVal=(0,1,2,3,4,5,6), desc='Jet noise option', aliases=('None', 'Stone/Clark', 'Kresja', 'Stone ALLJET', 'Stone JET181', 'GE M*S', 'SAE A-21 (ANOPP)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifan',val=0,optionsVal=(0,1,2), desc='Fan noise option', aliases=('None', 'Heidmann', 'Gliebe'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icore',val=0,optionsVal=(0,1), desc='Core noise option', aliases=('None', 'Core noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iturb',val=0,optionsVal=(0,1), desc='Turbine noise option', aliases=('None', 'Turbine noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iprop',val=0,optionsVal=(0,1,2), desc='Propeller noise option', aliases=('None', 'SAE', 'Gutin'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iflap',val=0,optionsVal=(0,1), desc='Flap noise/Jet-flap impingement noise option', aliases=('None', 'Flap & jet/flap noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iairf',val=0,optionsVal=(0,1), desc='Airframe noise option', aliases=('None', 'Airframe noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'igear',val=0,optionsVal=(0,1), desc='Gear box noise option', aliases=('None', 'Approx. gear box noise'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_noisin_Airframe(self):
        """Container for input:noisin:Airframe"""
        strChain = 'input:noisin:Airframe:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ifl',val=0,optionsVal=(1,0), desc='Include slotted flap noise', aliases=('Slotted flap noise', 'No slotted flap noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nf',val=2, desc='Number of trailing edge flap slots for IFL = 1',typeVar='Int')
        self.add_param(strChain+'pfchd',val=0.25, desc='Average chord for slotted flap, ft or fraction of wing chord.  Used only if IFL = 1',typeVar='Float')
        self.add_param(strChain+'itypw',val=1,optionsVal=(1,2), desc='Type of wing', aliases=('Conventional', 'Delta'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iclean',val=0,optionsVal=(1,0), desc='Aerodynamically clean aircraft', aliases=('Aerodynamically clean', 'Conventional'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iwing',val=0,optionsVal=(1,0), desc='Wing, horizontal and vertical tail noise', aliases=('Wing, horiz., vert. tail noise', 'No wing, tail noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'islat',val=0,optionsVal=(1,0), desc='Slatted leading edge noise', aliases=('Slatted l.e. noise', 'No slatted l.e. noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ilg',val=0,optionsVal=(1,0), desc='Nose and main landing gear noise', aliases=('Landing gear noise', 'No landing gear noise'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ng',val=array([]), desc='NG(0):  Number of nose gear trucks\nNG(1):  Number of main gear trucks',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'nw',val=array([]), desc='NW(0):  Number of wheels per nose gear truck\nNW(1):  Number of wheels per main gear truck',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'dw',val=array([]), units='ft', desc='DW(0):  Diameter of nose gear tires\nDW(1):  Diameter of main gear tires',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cg',val=array([]), desc='CG(0):  Ratio of nose strut length to DW(0)\nCG(1):  Ratio of main strut length to DW(1)',typeVar='Array',pass_by_obj=True)





    def FlopsWrapper_input_nacell(self):
        """Container for input:nacell"""
        strChain = 'input:nacell:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'x1r',val=2.06, desc='X1 / R.  If IVAR = -1, X1R is the cowl length divided by the inlet capture radius.',typeVar='Float')
        self.add_param(strChain+'x2r',val=1.58, desc='X2 / R',typeVar='Float')
        self.add_param(strChain+'r1r',val=0.354, desc='R1 / R',typeVar='Float')
        self.add_param(strChain+'r2r',val=0.585, desc='R2 / R',typeVar='Float')
        self.add_param(strChain+'angle',val=7.0, units='deg', desc='Average angle of the subsonic diffuser portion of the inlet between the throat and the engine face',typeVar='Float')
        self.add_param(strChain+'clang',val=0.0, units='deg', desc='Cowl lip angle',typeVar='Float')
        self.add_param(strChain+'mixed',val=-1,optionsVal=(-1,0,1), desc='Inlet compression type indicator\n= -1, Inlet geometry is based solely on the geometry variables described above.\n=  0, Inlet geometry is based in the internal geometry data base for external compression inlets and the given inlet design Mach number.\n=  1, Inlet geometry is based in the internal geometry data base for mixed compression inlets and the given inlet design Mach number', aliases=('Use geometry variables', 'External compression inlet', 'Mixed compression inlet'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'radd',val=3.0, units='inch', desc='Distance from the engine compressor tip to the exterior of the nacelle.  If RADD < 1. the added radial distance is RADD times the compressor tip radius.',typeVar='Float')
        self.add_param(strChain+'xnlod',val=-10.0, desc='Nozzle length / diameter (Default is computed',typeVar='Float')
        self.add_param(strChain+'xnld2',val=-10.0, desc='Fan nozzle length / diameter (Default is computed',typeVar='Float')
        self.add_param(strChain+'inac',val=0,optionsVal=(-5,-4,-3,-2,-1,0,1,2,3,4,5), desc='Nacelle type indicator', aliases=('2-D Bifurcated inlet + axisymmetric nozzle + podded together', '2-D Bifurcated inlet + 2-D nozzle + podded together', '2-D inlet + axisymmetric nozzle + podded together', '2-D + podded together', 'Axisymmetric + podded together', 'None', 'Axisymmetric', '2-D', '2-D inlet + Axisymmetric nozzle', '2-D Bifurcated inlet + 2-D nozzle', '2-D Bifurcated inlet + axisymmetric nozzle'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ivar',val=1,optionsVal=(-1,0,1,2,3), desc='Inlet variable geometry switch used to estimate weight factor WTCB1', aliases=('Fixed no centerbody', 'Fixed centerbody', 'Translating centerbody', 'Collapsing centerbody', 'Translating & collapsing centerbody'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nvar',val=0,optionsVal=(0,1,2,3,4), desc='Nozzle variable geometry switch used to estimate weight factor WTNOZ', aliases=('Fixed geometry', 'Variable area throat', 'Variable area exit', 'Variable throat & exit', 'Fixed plug core & fixed fan nozzle'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'wtcb1',val=-10.0, desc='Weighting factor for the inlet centerbody up to the throat.   Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typeVar='Float')
        self.add_param(strChain+'wtcb2',val=-10.0, desc='Weighting factor for the inlet centerbody from the throat to the engine face.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typeVar='Float')
        self.add_param(strChain+'wtint',val=-10.0, desc='Weighting factor for the internal cowl up to the engine face.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typeVar='Float')
        self.add_param(strChain+'wtext',val=-10.0, desc='Weighting factor for the external nacelle.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typeVar='Float')
        self.add_param(strChain+'wtnoz',val=-10.0, desc='Weighting factor for the nozzle.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typeVar='Float')
        self.add_param(strChain+'h2w',val=1.0, desc='Inlet height to width ratio for 2-D inlets',typeVar='Float')


    def FlopsWrapper_input_mission_definition(self):
        """Container for input:mission_definition"""
        strChain = 'input:mission_definition:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'mission',val='in' ,typeVar='List',other='itype')


    def FlopsWrapper_input_missin_User_Weights(self):
        """Container for input:missin:User_Weights"""
        strChain = 'input:missin:User_Weights:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'mywts',val=0,optionsVal=(0,1), desc='Weight input switch, overrides value input in Namelist &WTIN.', aliases=('Compute weight', 'User-specified'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'rampwt',val=0.0, units='lb', desc='Gross weight before taxi out (Default = DOWE + PAYLOD + FUEMAX)',typeVar='Float')
        self.add_param(strChain+'dowe',val=0.0, units='lb', desc='Fixed operating weight empty',typeVar='Float')
        self.add_param(strChain+'paylod',val=0.0, units='lb', desc='Fixed payload weight',typeVar='Float')
        self.add_param(strChain+'fuemax',val=0.0, units='lb', desc='Total usable fuel weight\nFUEMAX = RAMPWT - DOWE - PAYLOD.\nRequired only if RAMPWT is not input',typeVar='Float')


    def FlopsWrapper_input_missin_Turn_Segments(self):
        """Container for input:missin:Turn_Segments"""
        strChain = 'input:missin:Turn_Segments:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'xnz',val=array([]), units='g', desc='Maximum turn load factor at each Mach number',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'xcl',val=array([]), desc='Maximum turn lift coefficient at each Mach number',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'xmach',val=array([]), desc='Mach number array corresponding to both XNZ and XCL',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_missin_Store_Drag(self):
        """Container for input:missin:Store_Drag"""
        strChain = 'input:missin:Store_Drag:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'stma',val=array([]), desc='Mach number schedule for store drags.  Store drags can also be assessed in ACCEL and TURN segments of the mission as covered in the Segment Definition Cards section, in PS and NZ plots (see Namelist &OPTION), and in performance constraints (see Namelist &PCONIN)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdst',val=array([]), desc='Corresponding drag coefficients or D/q',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'istcl',val=array([]), desc='Store drag condition applied to climb schedule K\n= 0, No store drag for climb schedule K',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'istcr',val=array([]), desc='Store drag condition applied to cruise schedule K\n= 0, No store drag for cruise schedule K',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'istde',val=0, desc='Store drag condition applied to descent schedule\n= 0, No store drag for descent schedule',typeVar='Int')


    def FlopsWrapper_input_missin_Reserve(self):
        """Container for input:missin:Reserve"""
        strChain = 'input:missin:Reserve:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'irs',val=2,optionsVal=(1,2,3), desc='Reserve fuel calculation switch', aliases=('Calculated for trip to alternate airport plus RESRFU and/or RESTRP', 'Constant values (RESRFU and/or RESTRP) only', 'Reserve fuel is what is left over after primary mission'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'resrfu',val=0.0, desc='> 1., Fixed reserve fuel, lb\n< 1., Reserve fuel as a fraction of total usable fuel weight',typeVar='Float')
        self.add_param(strChain+'restrp',val=0.0, desc='Reserve fuel as a fraction of total trip fuel weight',typeVar='Float')
        self.add_param(strChain+'timmap',val=0.0, units='min', desc='Missed approach time',typeVar='Float')
        self.add_param(strChain+'altran',val=0.0, units='nmi', desc='Range to alternate airport',typeVar='Float')
        self.add_param(strChain+'nclres',val=1, desc='Climb schedule number used in reserve mission',typeVar='Int')
        self.add_param(strChain+'ncrres',val=1, desc='Cruise schedule number used in reserve mission',typeVar='Int')
        self.add_param(strChain+'sremch',val=-1.0, desc='Start reserve Mach number (Default = CLMMIN[NCLRES])',typeVar='Float')
        self.add_param(strChain+'eremch',val=-1.0, desc='End reserve Mach number (Default = DEMMIN)',typeVar='Float')
        self.add_param(strChain+'srealt',val=-1.0, units='ft', desc='Start reserve altitude (Default = CLAMIN[NCLRES])',typeVar='Float')
        self.add_param(strChain+'erealt',val=-1.0, units='ft', desc='End reserve altitude (Default = DEAMIN)',typeVar='Float')
        self.add_param(strChain+'holdtm',val=0.0, units='min', desc='Reserve holding time',typeVar='Float')
        self.add_param(strChain+'ncrhol',val=0, desc='Cruise schedule number for hold (Default = NCRRES)',typeVar='Int')
        self.add_param(strChain+'ihopos',val=1,optionsVal=(0,1,2), desc='Hold position switch', aliases=('Between main descent and missed approach', 'End of reserve cruise', 'End of reserve descent'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icron',val=0,optionsVal=(0,1,2), desc='Type of flight to alternate airport', aliases=('Climb-cruise-descend', 'Climb-cruise-beam down to airport', 'Cruise only'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'thold',val=0.0, desc='Used to define a hold segment between main mission descent and missed approach.\n> 1., Reserve holding time, min\n< 1., Fraction of flight time to be used as reserve holding time.  (Effective only if IRW = 1)\n= 0., This option is ignored',typeVar='Float')
        self.add_param(strChain+'ncrth',val=1, desc='Cruise schedule number for THOLD',typeVar='Int')


    def FlopsWrapper_input_missin_Ground_Operations(self):
        """Container for input:missin:Ground_Operations"""
        strChain = 'input:missin:Ground_Operations:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'takotm',val=0.0, units='min', desc='Takeoff time',typeVar='Float')
        self.add_param(strChain+'taxotm',val=0.0, units='min', desc='Taxi out time',typeVar='Float')
        self.add_param(strChain+'apprtm',val=0.0, units='min', desc='Approach time',typeVar='Float')
        self.add_param(strChain+'appfff',val=2.0, desc='Approach fuel flow factor applied to sea level static idle fuel flow',typeVar='Float')
        self.add_param(strChain+'taxitm',val=0.0, units='min', desc='Taxi in time',typeVar='Float')
        self.add_param(strChain+'ittff',val=0, desc='> 0, Engine deck power setting for takeoff (Usually = 1 if specified).  Taxi fuel flow is sea level static idle.\n= 0, Use TAKOFF and TXFUFL.',typeVar='Int')
        self.add_param(strChain+'takoff',val=0.0, units='lb/h', desc='Takeoff fuel flow',typeVar='Float')
        self.add_param(strChain+'txfufl',val=0.0, units='lb/h', desc='Taxi fuel flow',typeVar='Float')
        self.add_param(strChain+'ftkofl',val=0.0, units='lb', desc='Fixed takeoff fuel.  This ovverides the calculated value and is not scaled with engine thrust',typeVar='Float')
        self.add_param(strChain+'ftxofl',val=0.0, units='lb', desc='Fixed taxi out fuel.  This ovverides the calculated value and is not scaled with engine thrust',typeVar='Float')
        self.add_param(strChain+'ftxifl',val=0.0, units='lb', desc='Fixed taxi in fuel.  This ovverides the calculated value and is not scaled with engine thrust',typeVar='Float')
        self.add_param(strChain+'faprfl',val=0.0, units='lb', desc='Fixed approach fuel.  This ovverides the calculated value and is not scaled with engine thrust',typeVar='Float')


    def FlopsWrapper_input_missin_Descent(self):
        """Container for input:missin:Descent"""
        strChain = 'input:missin:Descent:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ivs',val=1,optionsVal=(0,1,2), desc='Descent option switch', aliases=('No descent time or distance or fuel', 'Descend at optimum L/D', 'Descend at constance lift coefficient'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'decl',val=0.8, desc='Descent lift coefficient for IVS = 2',typeVar='Float')
        self.add_param(strChain+'demmin',val=0.3, desc='Minimum Mach number',typeVar='Float')
        self.add_param(strChain+'demmax',val=0.0, desc='Max Mach number (Default = VCMN, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'deamin',val=0.0, units='ft', desc='Minimum altitude',typeVar='Float')
        self.add_param(strChain+'deamax',val=0.0, units='ft', desc='Max altitude (Default = CH, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'ninde',val=31, desc='Number of descent steps',typeVar='Int')
        self.add_param(strChain+'dedcd',val=0.0, desc='Drag coefficient increment applied to descent',typeVar='Float')
        self.add_param(strChain+'rdlim',val=-99999.0, units='ft/min', desc='Limiting or constant rate of descent.  Must be negative',typeVar='Float')
        self.add_param(strChain+'ns',val=0, desc='Number of altitudes for q limit schedule (Default = 0 - QLIM is used, Maximum = 20 )',typeVar='Int')
        self.add_param(strChain+'keasvd',val=0,optionsVal=(0,1), desc='= 1, VDTAB is in knots equivalent airspeed (keas)\n\n= 0, VDTAB is true airspeed or Mach number (Default)', aliases=('VDTAB is Mach number', 'VDTAB in knots'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'adtab',val=array([]), units='ft', desc='Descent altitude schedule.  If only part of the descent profile is specified, the portion of the profile outside the energy range defined by values of ADTAB and VDTAB will be optimized for the descent schedule.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'vdtab',val=array([]), desc='Descent speed schedule, kts or Mach number',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_missin_Cruise(self):
        """Container for input:missin:Cruise"""
        strChain = 'input:missin:Cruise:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ncruse',val=1, desc='Number of cruise schedules to be defined (Default = 1, Maximum = 6, Include reserve cruise)',typeVar='Int')
        self.add_param(strChain+'ioc',val=1, optionsVal='(0,1,2,3,4,5,6,7,8,9,10)', aliases=('Opt. alt. and Mach for specific range', 'Fixed Mach + opt. alt. for specific range', 'Fixed Mach at input max. alt. or cruise ceiling', 'Fixed alt. + opt. Mach for specific range', 'Fixed alt. + opt. Mach for endurance (min. fuel flow)', 'Fixed alt. + constant lift coefficient (CRCLMX)', 'Fixed Mach + opt. alt. for endurance', 'Opt. Mach and alt. for endurance', 'Max. Mach at input fixed alt.', 'Max. Mach at opt. alt.', 'Fixed Mach + constant lift coefficient (CRCLMX'), desc='Cruise option switch',typeVar='Array,int',pass_by_obj=True)
        self.add_param(strChain+'crmach',val=array([0.0]), dtype=array([]), desc='Maximum or fixed Mach number (or velocity, kts) (Default = VCMN, Namelist &CONFIN)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cralt',val=array([-1.0]), dtype=array([]), units='ft', desc='Maximum or fixed altitude (Default = CH, Namelist &CONFIN)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'crdcd',val=array([0.0]), dtype=array([]), desc='Drag coefficient increment',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'flrcr',val=array([1.0]), dtype=array([]), desc='Specific range factor for long range cruise Mach number - used if IOC = 3',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'crmmin',val=array([0.0]), dtype=array([]), desc='Minimum Mach number',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'crclmx',val=array([0.0]), dtype=array([]), desc='Maximum or fixed lift coefficient',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'hpmin',val=array([1000.0]), dtype=array([]), units='ft', desc='Minimum cruise altitude.\nFor fixed Mach number cruise schedules, HPMIN can be used to enforce a dynamic pressure (Q) limit.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ffuel',val=array([1.0]), dtype=array([]), desc='Fuel factor in cruise profile optimization',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'fnox',val=array([0.0]), dtype=array([]), desc='NOx emissions factor in cruise profile optimization.\nSince for supersonic engines the NOx emissions are on the order of 1 - 3 percent of fuel, FNOX should be relatively large (30. - 100.) to get comparable weighting.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ifeath',val=0, optionsVal='(1,0,-1)', desc='Cruise feathering option', aliases=('Engines may be feathered', 'No feathering', 'Engines must be feathered'),typeVar='List')
        self.add_param(strChain+'feathf',val=array([0.5]), dtype=array([]), desc='Fraction of engines remaining after feathering',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cdfeth',val=array([0.0]), dtype=array([]), desc='Drag coefficient increase due to feathered engines',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'dcwt',val=1.0, units='lb', desc='Weight increment used to compute cruise tables (Default = the greater of 1. or DWT/20)',typeVar='Float')
        self.add_param(strChain+'rcin',val=100.0, units='ft/min', desc='Instantaneous rate of climb for ceiling calculation',typeVar='Float')
        self.add_param(strChain+'wtbm',val=array([]), desc='Array of weights for specification of max. allowable altitude for low sonic boom configurations (must be in ascending order) Since linear interpolation/extrapolation is used, data should cover the entire expected weight range.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'altbm',val=array([]), units='ft', desc='Corresponding array of maximum altitudes',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_missin_Climb(self):
        """Container for input:missin:Climb"""
        strChain = 'input:missin:Climb:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nclimb',val=1, desc='Number of climb schedules to be defined (Default = 1, Maximum = 4, Include reserve climb)',typeVar='Int')
        self.add_param(strChain+'clmmin',val=array([0.3]), dtype=array([]), desc='Minimum Mach number for each climb schedule.\nNote: Separate climb schedules are not required if the only changes are in the minimum or maximum Mach number or altitude.  Just make sure all climbs are bracketed.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clmmax',val=array([0.0]), dtype=array([]), desc='Maximum Mach number (Default = VCMN, Namelist &CONFIN).\nNote: Separate climb schedules are not required if the only changes are in the minimum or maximum Mach number or altitude.  Just make sure all climbs are bracketed.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clamin',val=array([0.0]), dtype=array([]), units='ft', desc='Minimum altitude',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'clamax',val=array([0.0]), dtype=array([]), units='ft', desc='Maximum altitude (Default = CH, Namelist &CONFIN)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'nincl',val=array([31]), dtype=array([]), desc='Number of climb steps',typeVar='Array,int',pass_by_obj=True)
        self.add_param(strChain+'fwf',val=array([-0.0010]), dtype=array([]), desc='Climb profile optimization function control parameter.  Recommended aircraft in parentheses.\n=  1., minimum fuel-to-distance profile (Subsonic transports, do NOT use for supersonic transports)\n=  0., minimum time-to-distance profile (Interceptors only)\n1. > FWF > 0., combination of the above\n= -.001, minimum time-to-climb profile (Fighters)\n= -1., minimum fuel-to-climb profile (Supersonic transports, Subsonic transports)\n-1. < FWF < -.001, combination of the above',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ncrcl',val=array([1]), dtype=array([]), desc='Number of the cruise schedule to be used in fuel- or time-to-distance profile climb optimization comparisons',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'cldcd',val=array([0.0]), dtype=array([]), desc='Drag coefficient increment applied to each climb schedule.  If coefficient varies with Mach number, see ISTCL above.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ippcl',val=array([1]), dtype=array([]), desc='Number of power settings to be considered for climb.  Program will select the most efficient.  Should be used only with afterburning engines for minimum fuel climb profiles.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'maxcl',val=array([1]), dtype=array([]), desc='Maximum power setting used for climb',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'actab',val=zeros(shape=(0,0)), dtype=array([]), units='ft', desc='Altitude schedule.  If not input, climb profile will be optimized',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'vctab',val=zeros(shape=(0,0)), dtype=array([]), units='nmi', desc='Climb speed schedule.  If not input, climb profile will be optimized',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'keasvc',val=0,optionsVal=(1,0), desc='Type of velocity input in VCTAB', aliases=('Knots equivalent airspeed (keas)', 'True airspeed or Mach no.'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifaacl',val=1,optionsVal=(0,1,2), desc='Climb speed limit option', aliases=('Optimum speed', 'Max. 250 knots CAS below 10,000 ft', 'Climb to 250 kcas at 1500 ft then SPDLIM at 10,000 ft'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ifaade',val=-1,optionsVal=(-1,0,1), desc='Descent speed limit option', aliases=('Use default', 'Optimum speed', 'Max. 250 knots CAS below 10,000 ft'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nodive',val=0,optionsVal=(0,1), desc='Rate of climb limit option', aliases=('Optimum altitude at each energy level', 'Min. rate of climb limit enfored'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'divlim',val=0.0, units='ft/min', desc='Minimum allowable rate of climb or descent.\nEnforced only if NODIVE = 1, may be negative to allow a shallow dive during climb.',typeVar='Float')
        self.add_param(strChain+'qlim',val=0.0, units='psf', desc='Constant dynamic pressure limit.  Applied at all climb and descent points not covered by the variable dynamic pressure limit below.',typeVar='Float')
        self.add_param(strChain+'spdlim',val=0.0, desc='Maximum speed at 10,000 ft, used only for IFAACL = 2, kts or Mach number  (Default is computed from\n  a) the variable dynamic pressure limit below, if applicable,\n  b) QLIM above, if QLIM > 0., or\n  c) a dynamic pressure of 450 psf, in that order)',typeVar='Float')
        self.add_param(strChain+'nql',val=0, desc='Number of altitudes for q limit schedule (Default = 0 - QLIM is used, Maximum = 20 )',typeVar='Int')
        self.add_param(strChain+'qlalt',val=array([]), units='ft', desc='Altitudes, in increasing order, for variable dynamic pressure limit schedule',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'vqlm',val=array([]), units='psf', desc='Corresponding dynamic pressure limits',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_missin_Basic(self):
        """Container for input:missin:Basic"""
        strChain = 'input:missin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'indr',val=0,optionsVal=(0,1), desc='= 0, DESRNG is design range in n.mi.\n= 1, DESRNG is endurance in minutes', aliases=('Range', 'Endurance'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'fact',val=1.0, desc='Factor to increase or decrease fuel flows.  Cumulative with FFFSUB and FFFSUP in Namelist &ENGDIN.',typeVar='Float')
        self.add_param(strChain+'fleak',val=0.0, units='lb/h', desc='Constant delta fuel flow',typeVar='Float')
        self.add_param(strChain+'fcdo',val=1.0, desc='Factor to increase or decrease lift-independent drag coefficients',typeVar='Float')
        self.add_param(strChain+'fcdi',val=1.0, desc='Factor to increase or decrease lift-dependent drag coefficients',typeVar='Float')
        self.add_param(strChain+'fcdsub',val=1.0, desc='Factor to increase or decrease all subsonic drag coefficients.  Cumulative with FCDO and FCDI.',typeVar='Float')
        self.add_param(strChain+'fcdsup',val=1.0, desc='Factor to increase or decrease all supersonic drag coefficients.  Cumulative with FCDO and FCDI.',typeVar='Float')
        self.add_param(strChain+'iskal',val=1,optionsVal=(1,0), desc='Special option used to turn off engine scaling using THRUST/THRSO', aliases=('Scale engine', 'No scaling'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'owfact',val=1.0, desc='Factor for increasing or decreasing OWE',typeVar='Float')
        self.add_param(strChain+'iflag',val=0,optionsVal=(0,1,2,3), desc='Mission print option', aliases=('Mission summary only', 'Plus cruise', 'Plus climb & descent', 'Plus scaled engine'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'msumpt',val=0,optionsVal=(1,0), desc='Option to calculate and print detailed mission summary', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'dtc',val=0.0, units='degC', desc='Deviation from standard day temperature (See also DTCT in Namelist &TOLIN and DTCE in Namelist &ENGINE.  These temperature deviations are independent.)',typeVar='Float')
        self.add_param(strChain+'irw',val=2,optionsVal=(1,2), desc='Range/weight calculation option', aliases=('Range fixed-calculate ramp weight', 'Ramp weight fixed-calculate range'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'rtol',val=0.001, units='nmi', desc='Tolerance in range calculation for IRW = 1',typeVar='Float')
        self.add_param(strChain+'nhold',val=0, desc='Special option - Time for segment NHOLD (which must be a Hold Segment) is adjusted until the specified range is met for the input ramp weight.  Note - IRW must be 1',typeVar='Int')
        self.add_param(strChain+'iata',val=1,optionsVal=(1,0), desc='Option to adjust range for ATA Traffic Allowance', aliases=('Yes', 'No'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'tlwind',val=0.0, units='nmi', desc='Velocity of tail wind (Input negative value for head wind)',typeVar='Float')
        self.add_param(strChain+'dwt',val=1.0, units='lb', desc='Gross weight increment for performance tables (Default is internally computed)',typeVar='Float')
        self.add_param(strChain+'offdr',val=([]), units='nmi', desc='Off design range.  Note: This simply performs the defined mission with the sized airplane with a different design range.  If more changes are desired or if additional analyses are required (e.g., cost analysis), use Namelist &RERUN.  If OFFDR is used with a cost analysis, costs will be computed for the last design range.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'idoq',val=0,optionsVal=(1,0), desc='Form for drag increments', aliases=('D/q', 'Drag coefficients'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nsout',val=0, desc='Last segment number in outbound leg (Combat Radius Mission - Iterates until outbound leg and inbound leg are equal.  IRW must be equal to 2, and there must be at least two cruise segments).  If NSOUT = 0, radius is not calculated',typeVar='Int')
        self.add_param(strChain+'nsadj',val=0, desc='Cruise segment in outbound leg to be adjusted for radius calculation (Default = NSOUT).  Note: Make sure that the NSADJ Cruise segment is terminated on total rather than segment distance in the Mission Definition Data.',typeVar='Int')
        self.add_param(strChain+'mirror',val=0, desc='Cruise segment in inbound leg to be set equal to segment NSADJ  (if MIRROR = 0, only total leg lengths are forced to be equal).  This option would be used for a high-low-low-high mission where the dash in and dash out are unknown but must be equal to each other.  NSADJ would be the dash in segment number, and MIRROR would be the dash out segment number.',typeVar='Int')


    def FlopsWrapper_input_fusein_Basic(self):
        """Container for input:fusein:Basic"""
        strChain = 'input:fusein:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'fpitch',val=0.0, units='inch', desc='Seat pitch for the first class passengers',typeVar='Float')
        self.add_param(strChain+'nfabr',val=0, desc='Number of first class passengers abreast',typeVar='Int')
        self.add_param(strChain+'bpitch',val=0.0, units='inch', desc='Seat pitch for business class passengers',typeVar='Float')
        self.add_param(strChain+'nbabr',val=0, desc='Number of business class passengers abreast',typeVar='Int')
        self.add_param(strChain+'tpitch',val=0.0, units='inch', desc='Seat pitch for tourist class passengers',typeVar='Float')
        self.add_param(strChain+'ntabr',val=0, desc='Number of tourist class passengers abreast',typeVar='Int')


    def FlopsWrapper_input_fusein_BWB(self):
        """Container for input:fusein:BWB"""
        strChain = 'input:fusein:BWB:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'osspan',val=0.0, units='ft', desc='Outboard semispan (Default = ETAW(NETAW), required if ETAW(NETAW) is less than or equal to 1.0 and IFITE = 3 and NETAW > 1)\nThis variable is used if a detailed wing outboard panel (See Detailed Wing Data in Namelist $WTIN) is being added to a BWB fuselage.',typeVar='Float')
        self.add_param(strChain+'tipchd',val=0.0, units='ft', desc='Wing tip chord (Default = 0.06*Wing span)\nThis variable is used if the wing outer panel is defined as a trapezoid attached to the BWB cabin.',typeVar='Float')
        self.add_param(strChain+'nesob',val=0, desc='Wing eta station number for outboard side of body.  If this variable is greater than 1, the detailed wing definition is assumed to include the cabin.  Weight calculations for the outboard wing start at this eta station. (If = 0, the detailed outboard wing is added to the cabin as indicated above.)',typeVar='Int')
        self.add_param(strChain+'acabin',val=0.0, units='ft*ft', desc='Fixed area of passenger cabin for blended wing body transports (Default is internally computed based on passenger data)',typeVar='Float')
        self.add_param(strChain+'xlw',val=0.0, units='ft', desc='Fixed length of side wall.\nThis is the outboard wall of the passenger cabin and is used to define the outboard wing root chord.',typeVar='Float')
        self.add_param(strChain+'xlwmin',val=0.0, units='ft', desc='Minimum side wall length.  The typical value of 38.5 ft is based on a required maximum depth at the side wall of 8.25 ft divided by a fuselage thickness/chord ratio of 0.15 and 70 percent of the resulting wing root chord of 55 ft.',typeVar='Float')
        self.add_param(strChain+'nbay',val=0, desc='Fixed number of bays',typeVar='Int')
        self.add_param(strChain+'nbaymx',val=0, desc='Maximum number of bays',typeVar='Int')
        self.add_param(strChain+'bayw',val=0.0, units='ft', desc='Fixed bay width',typeVar='Float')
        self.add_param(strChain+'baywmx',val=0.0, units='ft', desc='Maximum bay width',typeVar='Float')
        self.add_param(strChain+'swple',val=45.0, units='deg', desc='Sweep angle of the leading edge of the passenger cabin',typeVar='Float')
        self.add_param(strChain+'cratio',val=0.0, desc='Fixed ratio of the centerline length to the cabin width (XLP/WF)',typeVar='Float')
        self.add_param(strChain+'tcf',val=0.0, desc='Fuselage thickness/chord ratio (Default = TCA, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'tcsob',val=0.0, desc='Fuselage thickness/chord ratio at side of body (Default = TCF)',typeVar='Float')
        self.add_param(strChain+'rspchd',val=0.0, desc='Rear spar percent chord for BWB fuselage and wing (Default = 70 percent)',typeVar='Float')
        self.add_param(strChain+'rspsob',val=0.0, desc='Rear spar percent chord for BWB fuselage at side of body (Default = 70 percent)',typeVar='Float')



    def FlopsWrapper_input_engine_deck(self):
        """Container for input:engine_deck"""
        strChain = 'input:engine_deck:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'engdek',val='',typeVar='Str')


    def FlopsWrapper_input_engine_Other(self):
        """Container for input:engine:Other"""
        strChain = 'input:engine:Other:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'hpcpr',val=5.0, desc='Pressure ratio of the high pressure (third) compressor (Only used if there are three compressor components)',typeVar='Float')
        self.add_param(strChain+'aburn' ,val=False, desc='True if there is an afterburner',typeVar='Bool')
        self.add_param(strChain+'dburn',val=False, desc='True if there is a duct burner (Separate flow turbofans only).  ABURN and DBURN cannot both be true.',typeVar='Bool')
        self.add_param(strChain+'effab',val=0.85, desc='Afterburner/duct burner efficiency',typeVar='Float')
        self.add_param(strChain+'tabmax',val=3500.0, units='degR', desc='Maximum afterburner/duct burner temperature',typeVar='Float')
        self.add_param(strChain+'ven',val=False, desc='True if the exhaust nozzle has a variable flow area.  The nozzle flow area is automatically allowed to vary for cases when the afterburner or duct burner is on.',typoVar='Bool')
        self.add_param(strChain+'costbl',val=1.0, units='lb/s', desc='Customer high pressure compressor bleed',typeVar='Float')
        self.add_param(strChain+'fanbl',val=0.0, desc='Fan bleed fraction, only used for bypass engines',typeVar='Float')
        self.add_param(strChain+'hpext',val=200.0, units='hp', desc='Customer power extraction',typeVar='Float')
        self.add_param(strChain+'wcool',val=-1.0e-4, desc='Turbine cooling flow as a fraction of high pressure compressor mass flow. The cooling flow defaults to the value in the engine cycle definition file. If WCOOL is input greater than or equal to zero the default will be overridden.\nIf WCOOL > 1., the turbine cooling flow fraction required to bring the turbine inlet temperature down to WCOOL will be computed.',typeVar='Float')
        self.add_param(strChain+'fhv',val=18500.0, units='Btu/lb', desc='Fuel heating value',typeVar='Float')
        self.add_param(strChain+'dtce',val=0.0, units='degC', desc='Deviation from standard day temperature.  The deviation, as used in the cycle analysis module, is DTCE at sea level and varies to zero at ALC (see below). The design point is at standard temperature.',typeVar='Float')
        self.add_param(strChain+'alc',val=10000.0, units='ft', desc='The altitude at which DTCE (see above) becomes zero.',typeVar='Float')
        self.add_param(strChain+'year',val=1985.0, desc='Technology availability date used to estimate compressor polytropic efficiency',typeVar='Float')
        self.add_param(strChain+'boat',val=False, desc='True to include boattail drag',typeVar='Bool')
        self.add_param(strChain+'ajmax',val=0.0, units='ft*ft', desc='Nozzle reference area for boattail drag.  Used only if BOAT = true.  Default is the largest of\n1) 1.1 times the inlet capture area\n2) Nozzle exit area at the inlet design point\n3) Estimated engine frontal area\n4) Estimated nozzle entrance area\nor\nIf nacelle weight and geometry calculations are\nperformed (see NGINWT below) AJMAX is set to the\nnacelle cross-sectional area at the customer connect. \nor\nIf AJMAX is less than zero, the cruise design point\nnozzle exit area multiplied by the absolute value\nof AJMAX is used as the reference.',typeVar='Float')
        self.add_param(strChain+'spill',val=False, desc='True to include spillage and lip drag in engine performance data',typeVar='Bool')
        self.add_param(strChain+'lip',val =False, desc='Compute inlet cowl lip drag.  Used only if SPILL = true',typeVar='Bool')
        self.add_param(strChain+'blmax',val=-1.0, desc='Inlet bleed flow fraction of total flow at the inlet design point (Default = .016 * AMINDS**1.5).  Used only if SPILL = true',typeVar='Float')
        self.add_param(strChain+'spldes',val=0.01, desc='Inlet design spillage fraction.  Used only if SPILL = true',typeVar='Float')
        self.add_param(strChain+'aminds',val=0.0, desc='Inlet design Mach number (Default = XMMAX).  Used only if SPILL = true',typeVar='Float')
        self.add_param(strChain+'alinds',val=0.0, units='ft', desc='Inlet design altitude (Default = AMAX).  Used only if SPILL = true',typeVar='Float')
        self.add_param(strChain+'etaprp',val=0.84, desc='Maximum propeller efficiency (Turboprops only). The actual propeller efficiency is based on an internal schedule of efficiency versus Mach number with the maximum efficiency (ETAPRP) occurring at a Mach number of 0.80.  To use the Hamilton Standard Method set ETAPRP=1 and input the propeller characteristics as defined under ',typeVar='Float')
        self.add_param(strChain+'shpowa',val=60.0, units='hp/(lb/s)', desc='Design point shaft horsepower divided by the design point core airflow',typeVar='Float')
        self.add_param(strChain+'cdtmax',val=99999.0, units='degR', desc='Maximum allowable compressor discharge temperature',typeVar='Float')
        self.add_param(strChain+'cdpmax',val=99999.0, units='psi', desc='Maximum allowable compressor discharge pressure',typeVar='Float')
        self.add_param(strChain+'vjmax',val=99999.0, units='ft/s', desc='(IENG < 100) Maximum allowable jet velocity\n(IENG > 100) Propeller tip speed',typeVar='Float')
        self.add_param(strChain+'stmin',val=1.0, units='lb/lb/s', desc='Minimum allowable specific thrust',typeVar='Float')
        self.add_param(strChain+'armax',val=99999.0, desc='Maximum allowable ratio of the bypass area to the core area of a mixed flow turbofan',typeVar='Float')
        self.add_param(strChain+'limcd',val=1,optionsVal=(0,1,2), desc='Switch to use the compressor discharge temperature and pressure limits only for optimization.', aliases=('Limit at cruise design Mach and altitude only for optimization', 'Limit at all points in envelope', 'Limit max. compressor discharge temp. everywhere'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_engine_Noise_Data(self):
        """Container for input:engine:Noise_Data"""
        strChain = 'input:engine:Noise_Data:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nprint',val=0,optionsVal=(-1,0,1,2), desc='Noise data print control', aliases=('Print compressor operating line', 'No print', 'Print to ANOPP', 'Print to FOOTPR'),typeVar='Enum',pass_by_obj=True)
        #self.add_param(strChain+'ivat',val=0,optionsVal=(0,1), desc='Flag for variable exit area low pressure turbine.  Used only for estimating LPT exit area when NPRINT=1', aliases=('Fixed', 'Variable'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'jet',val=-1,optionsVal=(-1,0,1,2,3,4,5,6), desc='FOOTPR input data generation control', aliases=('No noise data', 'No jet noise', 'Stone/Clark', 'Kresja', 'Stone ALLJET', 'Stone JET181', 'GE M*S', 'SAE A-21'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ftmach',val=0.0, desc='Mach number to calculate FOOTPR input data',typeVar='Float')
        self.add_param(strChain+'ftalt',val=0.0, desc='Altitude to calculate FOOTPR input data',typeVar='Float')


    def FlopsWrapper_input_engine_IC_Engine(self):
        """Container for input:engine:IC_Engine"""
        strChain = 'input:engine:IC_Engine:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ncyl',val=4, desc='Number of cylinders',typeVar='Int')
        self.add_param(strChain+'deshp',val=180.0, units='hp', desc='Baseline engine power',typeVar='Float')
        self.add_param(strChain+'alcrit',val=0.0, units='ft', desc='Critical turbocharger altitude.  The altitude to which turbocharged IC engines are able to maintain DESHP',typeVar='Float')
        self.add_param(strChain+'sfcmax',val=0.52, units='lb/h/hp', desc='Brake specific fuel consumption at maximum power',typeVar='Float')
        self.add_param(strChain+'sfcmin',val=0.4164, units='lb/h/hp', desc='Minimum brake specific fuel consumption or SFC',typeVar='Float')
        self.add_param(strChain+'pwrmin',val=0.65, desc='Fraction of maximum power where SFCMIN occurs. If NRPM > 0 and PWRMIN > 1 then PWRMIN is the rotational speed where SFCMIN occurs (recommend PWRMIN > 1 if SFCMIN is less than about 0.4',typeVar='Float')
        self.add_param(strChain+'engspd',val=2700.0, units='1/min', desc='Maximum engine crankshaft speed',typeVar='Float')
        self.add_param(strChain+'prpspd',val=2700.0, units='1/min', desc='Maximum propeller shaft speed',typeVar='Float')
        self.add_param(strChain+'iwc',val=0,optionsVal=(0,1), desc='Cooling system', aliases=('Air cooled', 'Water cooled'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ecid',val=361.0, units='inch*inch*inch', desc='Engine displacement',typeVar='Float')
        self.add_param(strChain+'ecr',val=8.5, desc='Engine compression ratio',typeVar='Float')
        self.add_param(strChain+'eht',val=19.96, units='inch', desc='Engine envelope height',typeVar='Float')
        self.add_param(strChain+'ewid',val=33.37, units='inch', desc='Engine envelope width',typeVar='Float')
        self.add_param(strChain+'elen',val=31.83, units='inch', desc='Engine envelope length',typeVar='Float')
        self.add_param(strChain+'ntyp',val=2,optionsVal=(1,2,3,4,5,6), desc='Propeller type indicator', aliases=('Fixed pitch', 'Variable pitch', 'Variable pitch + full feathering', 'Variable pitch + full feathering + deicing', 'Variable pitch + full feathering + deicing w/reverse', 'Ducted fan'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'af',val=87.6, desc='Activity factor',typeVar='Float')
        self.add_param(strChain+'cli',val=0.569, desc='Integrated design lift coefficient',typeVar='Float')
        self.add_param(strChain+'blang',val=20.0, units='deg', desc='Blade angle for fixed pitch propeller',typeVar='Float')
        self.add_param(strChain+'dprop',val=6.375, units='ft', desc='Propeller diameter',typeVar='Float')
        self.add_param(strChain+'nblade',val=0, desc='Number of blades',typeVar='Int')
        self.add_param(strChain+'gbloss',val=0.02, desc='Gearbox losses, fraction. If PRPSPD = ENGSPD, there are no losses.',typeVar='Float')
        self.add_param(strChain+'arrpm',val=array([]), units='rpm', desc='Rotational speed (descending order)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'arpwr',val=array([]), units='hp', desc='Engine shaft power at ARRPM(I)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'arful',val=array([]), desc='Engine fuel requirements at ARRPM(I) (Required only if LFUUN is not equal to zero)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'lfuun',val=0,optionsVal=(0,1,2,3), desc='Fuel input type indicator', aliases=('Fuel flows are computed from SFCMAX SFCMIN and PWRMIN', 'Brake specific fuel consumption values are input in ARFUL', 'Actual fuel flows are input in ARFUL (lb/hr)', 'Actual fuel flows are input in ARFUL (gal/hr)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'feng',val=1.0, desc='Scale factor on engine weight',typeVar='Float')
        self.add_param(strChain+'fprop',val=1.0, desc='Scale factor on propeller weight',typeVar='Float')
        self.add_param(strChain+'fgbox',val=1.0, desc='Scale factor on gear box weight',typeVar='Float')


    def FlopsWrapper_input_engine_Engine_Weight(self):
        """Container for input:engine:Engine_Weight"""
        strChain = 'input:engine:Engine_Weight:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nginwt',val=0,optionsVal=(-4,-3,-2,-1,0,1,2,3,4,5), desc='Switch for engine weight calculations.   Use the negative value to calculate the weight for the initial design and then scale engine weights and dimensions with airflow.  Zero or a negative value should always be used during optimization with engine cycle design variables.  (IENG > 100 options in parentheses)', aliases=('-Engine + inlet + nacelle + nozzle', '-Engine + inlet + nacelle', '-Engine and inlet', '-Engine only', 'None', 'Engine only (Total prop. system)', 'Engine and inlet (Propeller)', 'Engine + inlet + nacelle (Propeller + cowl + mounts)', 'Engine + inlet + nacelle + nozzle ( Propeller + cowl + mounts + exhaust)', '(Propeller + cowl + mounts + exhaust + alternator)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iwtprt',val=1,optionsVal=(0,1,2,3,4), desc='Printout control for engine weight calculations.  Printout is on file OFILE.', aliases=('No output', 'Print component weights and dimensions', 'Print component design details', 'Plus initial and final optimization data', 'Print component details at each iteration'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iwtplt',val=0,optionsVal=(-4,-3,-2,-1,0,1,2,3,4), desc='PostScript plot control for engine (and nacelle) schematics on file PLTFIL.  If the negative value is input, only the final design will be plotted.',typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'gratio',val=1.0, desc='Ratio of the RPM of the low pressure compressor to the RPM of the connected fan',typeVar='Float')
        self.add_param(strChain+'utip1',val=0.0, units='ft/s', desc='Tip speed of the first compressor (or fan) in the flow.  Default is based on YEAR, engine type, and other design considerations.',typeVar='Float')
        self.add_param(strChain+'rh2t1',val=0.0, desc='Hub to tip radius ratio of the first compressor (or fan) in the flow.  Default is based on YEAR, engine type, and other design considerations.',typeVar='Float')
        self.add_param(strChain+'igvw',val=0,optionsVal=(-2,-1,0,1,2), desc='Flag for compressor inlet guide vanes', aliases=('Variable-no fan IGV', 'Fixed-no fan IGV', 'None', 'Fixed', 'Variable'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'trbrpm',val=0.0, units='rpm', desc='The rotational speed of any free turbine.  TRBAN2 is used to set the free turbine rotational speed if TRBRPM is not input. TRBRPM overrides TRBAN2.',typeVar='Float')
        self.add_param(strChain+'trban2',val=0.0, units='(inch*inch)/(min*min)', desc='Maximum allowable AN**2 for turbine components.  The input value is the actual maximum divided by 10**10.  AN**2 is the flow area multiplied by the rotational speed squared.  The default is based on year.',typeVar='Float')
        self.add_param(strChain+'trbstr',val=15000.0, units='psi', desc='Turbine usable stress lower limit.  Normally when component weights are predicted, the usable stress is a function of operating conditions.  For turbine components, this can be unusually low because cooling effects are not accounted for.',typeVar='Float')
        self.add_param(strChain+'cmpan2',val=0.0, units='(inch*inch)/(min*min)', desc='Maximum allowable AN**2 for compressor components.  The input value is the actual maximum divided by 10**10.  AN**2 is the flow area multiplied by the rotational speed squared.  The default is based on year.',typeVar='Float')
        self.add_param(strChain+'cmpstr',val=25000.0, units='psi', desc='Requested compressor usable stress.  This forces a change in compressor material when the current (lower temperature) material starts to run out of strength as temperature increases.',typeVar='Float')
        self.add_param(strChain+'vjpnlt',val=0.0, units='lb', desc='Weight penalty factor for a suppressor to reduce the core jet velocity to 1500 ft/sec',typeVar='Float')
        self.add_param(strChain+'wtebu',val=0.2, desc='Fraction for weight of engine build up unit (pylon, mounting hardware, etc)',typeVar='Float')
        self.add_param(strChain+'wtcon',val=0.05, desc='Fraction for weight of engine controls',typeVar='Float')


    def FlopsWrapper_input_engine_Design_Point(self):
        """Container for input:engine:Design_Point"""
        strChain = 'input:engine:Design_Point:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'desfn',val=0.0, units='lb', desc='Engine design point net dry thrust (Default = THRUST, Namelist &CONFIN).  Do not use the default for afterburning engines since THRUST is the maximum wet thrust rating.  The maximum wet (afterburning) thrust for the generated engine is transferred back to THRSO for scaling with THRUST.',typeVar='Float')
        self.add_param(strChain+'xmdes',val=-9999.0, desc='Engine optimization point Mach number (Default = VCMN, Namelist &CONFIN).  XMDES and XADES are used for propulsion only analyses (IANAL = 4).',typeVar='Float')
        self.add_param(strChain+'xades',val=-9999.0, units='ft', desc='Engine optimization point altitude (Default = CH, Namelist &CONFIN).  If XADES < 0., it is interpreted as the negative of the design point dynamic pressure (psf), and the altitude is back-calculated with a minimum of 0.',typeVar='Float')
        self.add_param(strChain+'oprdes',val=25.0, desc='Overall pressure ratio',typeVar='Float')
        self.add_param(strChain+'fprdes',val=1.5, desc='Fan pressure ratio (turbofans only)',typeVar='Float')
        self.add_param(strChain+'bprdes',val=0.0, desc='Bypass ratio (Turbofans only, Default is computed based on OPRDES, FPRDES, TTRDES, XMDES and ALDES).  If BPRDES < -1, then the bypass ratio is computed such that the ratio of the fan to core jet velocities equals the absolute value of BPRDES.  For turbine bypass engines, BPRDES must be input and is defined as the fraction of compressor exit airflow that is bypassed around the main burner and the turbine.  If both EBPR and BPRDES are zero, the optimum bypass ratio is computed at the design Mach number and altitude (XMDES, XADES).',typeVar='Float')
        self.add_param(strChain+'tetdes',val=2500.0, units='degR', desc='Engine design point turbine entry temperature',typeVar='Float')
        self.add_param(strChain+'ttrdes',val=1.0, desc='Engine throttle ratio defined as the ratio of the maximum allowable turbine inlet temperature divided by the design point turbine inlet temperature.  If TTRDES is greater than TETDES, it is assumed to be the maximum allowable turbine inlet temperature.',typeVar='Float')


    def FlopsWrapper_input_engine_Basic(self):
        """Container for input:engine:Basic"""
        strChain = 'input:engine:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ieng',val=1,optionsVal=(0,1,2,3,4,5,6,7,8,9,101), desc='Engine cycle definition input file indicator', aliases=('User-defined', 'Turbojet', 'Separate flow turbofan w/ 2 compressors', 'Mixed flow turbofan w/ 2 compressors', 'Turboprop', 'Turbine bypass', 'Separate flow turofan w/ 3 compressors', 'Mixed flow turbofan w/ 3 compressors', '3-spool separate flow turbofan w/ 3 compressors', '2-spool turbojet', 'IC engine'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iprint',val=1, desc='Engine cycle analysis printout control.  Printout is on file OFILE',typeVar='Int')
        self.add_param(strChain+'gendek' ,val=False, desc='Engine data will be saved on the file designated by EOFILE as an Engine Deck for future use',typeVar='Bool')
        self.add_param(strChain+'ithrot',val=1,optionsVal=(0,1,2), desc='Controls frequency of part power data generation', aliases=('All Mach-altitude combos', 'Max. altitude for each Mach', 'Max. altitude for max. Mach'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'npab',val=0, desc='Maximum number of afterburning throttle settings for each Mach-altitude combination',typeVar='Int')
        self.add_param(strChain+'npdry',val=15, desc='Maximum number of dry (non-afterburning) throttle settings',typeVar='Int')
        self.add_param(strChain+'xidle',val=0.05, desc='Fraction of maximum dry thrust used as a cutoff for part power throttle settings',typeVar='Float')
        self.add_param(strChain+'nitmax',val=50, desc='Maximum iterations per point',typeVar='Int')
        self.add_param(strChain+'xmmax',val=-1.0, desc='Max Mach number (Default = VCMN, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'amax',val=-1.0, units='ft', desc='Max altitude (Default = CH, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'xminc',val=0.2, desc='Mach number increment (Default = .2)',typeVar='Float')
        self.add_param(strChain+'ainc',val=5000.0, units='ft', desc='Altitude increment (Default = 5000.)',typeVar='Float')
        self.add_param(strChain+'qmin',val=150.0, units='psf', desc='Minimum dynamic pressure',typeVar='Float')
        self.add_param(strChain+'qmax',val=1200.0, units='psf', desc='Maximum dynamic pressure',typeVar='Float')


    def FlopsWrapper_input_engine(self):
        """Container for input:engine"""
        strChain = 'input:engine:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ifile' ,val='',desc='Name of cycle definition input file.  Used only if IENG = 0.',typeVar='Str')
        self.add_param(strChain+'tfile',val='ENGTAB', desc='Name of the file containing component map tables.',typeVar='Str')


    def FlopsWrapper_input_engdin_Special_Options(self):
        """Container for input:engdin:Special_Options"""
        strChain = 'input:engdin:Special_Options:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'dffac',val=0.0, desc='Fuel flow scaling constant term.\nThe engine fuel flow scale factor for ENGSKAL = THRUST/THRSO is\nENGSKAL*[1. + DFFAC + FFFAC*(1. - ENGSKAL)]',typeVar='Float')
        self.add_param(strChain+'fffac',val=0.0, desc='Fuel flow scaling linear term.\nThe engine fuel flow scale factor for ENGSKAL = THRUST/THRSO is\nENGSKAL*[1. + DFFAC + FFFAC*(1. - ENGSKAL)]',typeVar='Float')
        self.add_param(strChain+'emach',val=array([]), desc='Array of Mach numbers in descending order at which engine data are to be generated (Default computed internally, Do not zero fill)',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'alt',val=zeros(shape=(0,0)), dtype=array([]), units='ft', desc='Arrays of altitudes in descending order, one set for each Mach number, at which engine data are to be generated (Default computed internally, do not zero fill).  Altitudes and numbers of altitudes do not have to be consistent between Mach numbers.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'insdrg',val=0,optionsVal=(0,1,2,3), desc='Nozzle installation drag scaling switch', aliases=('No drag scaling', 'Scale with A10', 'Calculate using A10', 'Calculate for Cd=0 at A9=A9ref'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nab',val=6969, desc='Table number in CDFILE to be used for afterbody drag',typeVar='Int')
        self.add_param(strChain+'nabref',val=6969, desc='Table number in CDFILE to be used for reference afterbody drag',typeVar='Int')
        self.add_param(strChain+'a10',val=0.0, units='inch*inch', desc='Maximum nozzle area (Required if INSDRG > 0)',typeVar='Float')
        self.add_param(strChain+'a10ref',val=0.0, units='inch*inch', desc='Reference maximum nozzle area (Required if INSDRG > 0)',typeVar='Float')
        self.add_param(strChain+'a9ref',val=0.0, units='inch*inch', desc='Reference nozzle exit area (Required if INSDRG = 3)',typeVar='Float')
        self.add_param(strChain+'xnoz',val=0.0, units='inch', desc='Nozzle length (Required if INSDRG > 0)',typeVar='Float')
        self.add_param(strChain+'xnref',val=0.0, units='inch', desc='Reference nozzle length (Required if INSDRG > 0)',typeVar='Float')
        self.add_param(strChain+'rcrv',val=-1.0, desc='Nozzle radius of curvature parameter (Triggers special nozzle drag option)',typeVar='Float')


    def FlopsWrapper_input_engdin_Basic(self):
        """Container for input:engdin:Basic"""
        strChain = 'input:engdin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ngprt',val=1,optionsVal=(0,1,2), desc='Print engine data tables', aliases=('No printout', 'Print tables', 'Print sorted tables'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'igenen',val=0,optionsVal=(-3,-2,-1,0,1), desc='Switch indicating source of Engine Deck', aliases=('Response surfaces', 'External file (horsepower/rpm/fuel flow', 'External file (thrust/fuel flow)', 'Follows namelist &ENGDIN', 'Engine deck to be generated'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'extfac',val=1.0, desc='Slope factor for extrapolating engine fuel flows for thrust levels above the maximum for that Mach number and altitude',typeVar='Float')
        self.add_param(strChain+'fffsub',val=1.0, desc='Fuel flow factor for all subsonic engine points',typeVar='Float')
        self.add_param(strChain+'fffsup',val=1.0, desc='Fuel flow factor for all supersonic engine points',typeVar='Float')
        self.add_param(strChain+'idle',val=0, desc='> 0, Flight idle data will be internally generated with zero thrust and an extrapolated fuel flow.  The fuel flow must be at least FIDMIN times the fuel flow at power setting number IDLE and no more than FIDMAX times the fuel flow at power setting number IDLE.  If NONEG (below) = 0 and negative thrusts exist, an idle power setting is not generated.\n= 0, The lowest input power setting is assumed to be flight idle (Not recommended.  Results will be more consistent with IDLE > 0)',typeVar='Int')
        self.add_param(strChain+'noneg',val=0,optionsVal=(1,0), desc='Option for using points in the Engine Deck with negative thrust', aliases=('Ignore', 'Use all points'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'fidmin',val=0.08, desc='Minimum fraction of the fuel flow at power setting number IDLE for generated flight idle fuel flows',typeVar='Float')
        self.add_param(strChain+'fidmax',val=1.0, desc='Maximum fraction of the fuel flow at power setting number IDLE for generated flight idle fuel flows',typeVar='Float')
        self.add_param(strChain+'ixtrap',val=1, desc='Option for extrapolation of engine data beyond altitudes provided in input data, which may result in radically improved SFC',typeVar='Int')
        self.add_param(strChain+'ifill',val=2, desc='Option for filling in part power data\n=0, No part power data will be generated\n> 0, Part power cruise data will be filled in for Mach-altitude points for which IFILL (or fewer) thrust levels have been input\nFor NPCODE > 1, data will be filled in for each specified power code that is not input for each Mach-altitude point.',typeVar='Int')
        self.add_param(strChain+'maxcr',val=2, desc='Maximum power setting used for cruise',typeVar='Int')
        self.add_param(strChain+'nox',val=0,optionsVal=(0,1,2,3), desc='Option for NOx emissions data.  If IGENEN=-2, NOx emissions data are replaced with engine shaft speed, rpm', aliases=('Do not use', 'Indices in engine deck or generated', 'Emissions lb/hr in engine deck', 'Another parameter in engine deck'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'pcode',val=array([]), desc='Power codes to be used in sorting the Engine Deck.  Values correspond to thrust levels in descending order, i.e., climb, maximum continuous, part power cruise settings, and flight idle.  Actual values are arbitrary (they are just used as labels), but only points in the Engine Deck with corresponding values for PC will be used.',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'boost',val=0.0, desc='> 0., Scale factor for boost engine to be added to baseline engine for takeoff and climb.  Climb thrust of the boost engine in the Engine Deck must be artificially increased by 100,000.\n= 0., No boost engine',typeVar='Float')
        self.add_param(strChain+'igeo',val=0,optionsVal=(0,1), desc='Engine deck altitude type', aliases=('Geometric', 'Geopotential-will be converted'),typeVar='Enum',pass_by_obj=True)


    def FlopsWrapper_input_engdin(self):
        """Container for input:engdin"""
        strChain = 'input:engdin:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'cdfile' ,val='',typeVar='Str')

        # Special addition for analysis runs where we aren't connected to NPSS.
        self.add_param(strChain+'eifile' ,val='', desc="Engine deck filename",typeVar='Str')



    def FlopsWrapper_input_costin_Mission_Performance(self):
        """Container for input:costin:Mission_Performance"""
        strChain = 'input:costin:Mission_Performance:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'desmch',val=0.0, desc='Design Mach number (Default = VCMN, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'dprsmx',val=0.0, units='psf', desc='Maximum dynamic pressure (Default = 460. * DESMCH)',typeVar='Float')
        self.add_param(strChain+'veloc',val=0.0, units='mi/h', desc='Cruise velocity (Default = 660. * DESMCH)',typeVar='Float')
        self.add_param(strChain+'blockf',val=0.9, units='lb', desc='Block fuel, or fraction of aircraft fuel capacity  (Default = 0.90 * (FULWMX+FULFMX), Namelist &WTIN)',typeVar='Float')
        self.add_param(strChain+'blockt',val=0.0, units='h', desc='Block time (Default = DESRNG/VELOC + 0.65)',typeVar='Float')


    def FlopsWrapper_input_costin_Cost_Technology(self):
        """Container for input:costin:Cost_Technology"""
        strChain = 'input:costin:Cost_Technology:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'fafrd',val=1.0, desc='Technology factor on Airframe R&D',typeVar='Float')
        self.add_param(strChain+'fenrd',val=1.0, desc='Technology factor on Engine R&D',typeVar='Float')
        self.add_param(strChain+'fmac',val=1.0, desc='Technology factor on Air conditioning',typeVar='Float')
        self.add_param(strChain+'fmai',val=1.0, desc='Technology factor on Anti-icing',typeVar='Float')
        self.add_param(strChain+'fmapu',val=1.0, desc='Technology factor on Auxiliary power unit',typeVar='Float')
        self.add_param(strChain+'fmav',val=1.0, desc='Technology factor on Avionics',typeVar='Float')
        self.add_param(strChain+'fmbody',val=1.0, desc='Technology factor on Fuselage',typeVar='Float')
        self.add_param(strChain+'fmcomp',val=1.0, desc='Technology factor on Composite materials (applied to the wing, tails, fuselage, and nacelles)',typeVar='Float')
        self.add_param(strChain+'fmel',val=1.0, desc='Technology factor on Electrical systems',typeVar='Float')
        self.add_param(strChain+'fmeng',val=1.0, desc='Technology factor on Engine',typeVar='Float')
        self.add_param(strChain+'fmensy',val=1.0, desc='Technology factor on Engine systems',typeVar='Float')
        self.add_param(strChain+'fmfcs',val=1.0, desc='Technology factor on Surface controls',typeVar='Float')
        self.add_param(strChain+'fmfeq',val=1.0, desc='Technology factor on Furnishings and equipment',typeVar='Float')
        self.add_param(strChain+'fmfusy',val=1.0, desc='Technology factor on Fuel systems',typeVar='Float')
        self.add_param(strChain+'fmgear',val=1.0, desc='Technology factor on Landing gear',typeVar='Float')
        self.add_param(strChain+'fmhyd',val=1.0, desc='Technology factor on Hydraulic systems',typeVar='Float')
        self.add_param(strChain+'fmins',val=1.0, desc='Technology factor on Instruments',typeVar='Float')
        self.add_param(strChain+'fmnac',val=1.0, desc='Technology factor on Nacelles',typeVar='Float')
        self.add_param(strChain+'fmpnm',val=1.0, desc='Technology factor on Pneumatics',typeVar='Float')
        self.add_param(strChain+'fmtail',val=1.0, desc='Technology factor on Tail',typeVar='Float')
        self.add_param(strChain+'fmtrv',val=1.0, desc='Technology factor on Thrust reversers',typeVar='Float')
        self.add_param(strChain+'fmwing',val=1.0, desc='Technology factor on Wing',typeVar='Float')
        self.add_param(strChain+'foac',val=1.0, desc='Technology factor on Air conditioning',typeVar='Float')
        self.add_param(strChain+'foai',val=1.0, desc='Technology factor on Anti-icing',typeVar='Float')
        self.add_param(strChain+'foapu',val=1.0, desc='Technology factor on Auxiliary power unit',typeVar='Float')
        self.add_param(strChain+'foav',val=1.0, desc='Technology factor on Avionics',typeVar='Float')
        self.add_param(strChain+'fobody',val=1.0, desc='Technology factor on Fuselage',typeVar='Float')
        self.add_param(strChain+'focomp',val=1.0, desc='Technology factor on Composite materials',typeVar='Float')
        self.add_param(strChain+'foel',val=1.0, desc='Technology factor on Electrical systems',typeVar='Float')
        self.add_param(strChain+'fofcs',val=1.0, desc='Technology factor on Flight control system',typeVar='Float')
        self.add_param(strChain+'fofeq',val=1.0, desc='Technology factor on Furnishings and equipment',typeVar='Float')
        self.add_param(strChain+'fofusy',val=1.0, desc='Technology factor on Fuel systems',typeVar='Float')
        self.add_param(strChain+'fogear',val=1.0, desc='Technology factor on Landing gear',typeVar='Float')
        self.add_param(strChain+'fohyd',val=1.0, desc='Technology factor on Hydraulic systems',typeVar='Float')
        self.add_param(strChain+'foins',val=1.0, desc='Technology factor on Instruments',typeVar='Float')
        self.add_param(strChain+'fonac',val=1.0, desc='Technology factor on Nacelles',typeVar='Float')
        self.add_param(strChain+'fopnm',val=1.0, desc='Technology factor on Pneumatics',typeVar='Float')
        self.add_param(strChain+'foprop',val=1.0, desc='Technology factor on Propulsion system',typeVar='Float')
        self.add_param(strChain+'fowing',val=1.0, desc='Technology factor on Wing',typeVar='Float')
        self.add_param(strChain+'feacsr',val=1.0, desc='Technology factor on Aircraft servicing',typeVar='Float')
        self.add_param(strChain+'fecfee',val=1.0, desc='Technology factor on Aircraft control fee',typeVar='Float')
        self.add_param(strChain+'fecrw',val=1.0, desc='Technology factor on Flight crew',typeVar='Float')
        self.add_param(strChain+'fedep',val=1.0, desc='Technology factor on Depreciation',typeVar='Float')
        self.add_param(strChain+'feflta',val=1.0, desc='Technology factor on Flight attendants',typeVar='Float')
        self.add_param(strChain+'feins',val=1.0, desc='Technology factor on Insurance',typeVar='Float')
        self.add_param(strChain+'felabr',val=1.0, desc='Technology factor on R&D labor rate',typeVar='Float')
        self.add_param(strChain+'feldfe',val=1.0, desc='Technology factor on Landing fee',typeVar='Float')
        self.add_param(strChain+'femain',val=1.0, desc='Technology factor on Maintenance hours',typeVar='Float')


    def FlopsWrapper_input_costin_Basic(self):
        """Container for input:costin:Basic"""
        strChain = 'input:costin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ac',val=350.0, units='lb/min', desc='Airconditioning total pack air flow',typeVar='Float')
        self.add_param(strChain+'apuflw',val=400.0, units='lb/min', desc='Auxiliary power unit flow rate',typeVar='Float')
        self.add_param(strChain+'apushp',val=170.0, units='hp', desc='Auxiliary power unit shaft horsepower',typeVar='Float')
        self.add_param(strChain+'depper',val=14.0, units='year', desc='Depreciation period',typeVar='Float')
        self.add_param(strChain+'devst',val=1980.0, units='year', desc='Development start time',typeVar='Float')
        self.add_param(strChain+'dlbur',val=2.0, desc='Direct labor burden factor',typeVar='Float')
        self.add_param(strChain+'dyear',val=1986, desc='Desired year for dollar calculations',typeVar='Int')
        self.add_param(strChain+'epr',val=20.0, desc='Engine pressure ratio at sea level static',typeVar='Float')
        self.add_param(strChain+'fafmsp',val=0.1, desc='Spares factor for production airframes',typeVar='Float')
        self.add_param(strChain+'fare',val=0.0, units='USD/pax/mi', desc='Fare (Triggers calculation of return on investment)',typeVar='Float')
        self.add_param(strChain+'fengsp',val=0.3, desc='Spares factor for production engines',typeVar='Float')
        self.add_param(strChain+'fppft',val=0.5, desc='Spares factor for prototype and flight test engines',typeVar='Float')
        self.add_param(strChain+'fuelpr',val=0.5, units='USD/galUS', desc='Fuel price',typeVar='Float')
        self.add_param(strChain+'hydgpm',val=150.0, desc='Gallon per minute flow of hydraulic pumps',typeVar='Float')
        self.add_param(strChain+'iacous',val=0,optionsVal=(0,1), desc='Acoustic treatment in nacelle', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ibody',val=0,optionsVal=(0,1), desc='Body type indicator', aliases=('Narrow', 'Wide'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icirc',val=1,optionsVal=(1,2), desc='Circuit indicator - fire detection', aliases=('Single', 'Dual'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icorev',val=1,optionsVal=(0,1), desc='Thrust reverser', aliases=('No core reverser', 'Core reverser'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'icostp',val=1,optionsVal=(1,2,3,4,5), desc='Type of cost calculation desired', aliases=('Life cycle cost (LCC)', 'Acquisition cost', 'Direct operating cost (DOC)', 'Indirect operating cost (IOC)', 'Operating cost only (DOC + IOC - Depreciation)'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'idom',val=1,optionsVal=(1,2), desc='Operation type indicator', aliases=('Domestic', 'International'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'imux',val=0,optionsVal=(0,1), desc='Multiplex indicator', aliases=('No multiplex', 'Multiplex'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'inozz',val=1,optionsVal=(1,2,3,4,5), desc='Nozzle type indicator', aliases=('Translating sleeve', 'Simple target w/ separate flow nozzle', 'Simple target w/ mixed flow nozzle', 'Separate flow exhaust w/o thrust reverser', 'Short duct w/o thrust reverser'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ipflag',val=1,optionsVal=(0,1), desc='Print controller for Cost Module', aliases=('Print major elements', 'Print details'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'irad',val=1,optionsVal=(0,1), desc='Indicator to include research and development', aliases=('Ignore R&D costs', 'Include R&D costs'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'irange',val=1,optionsVal=(0,1,2), desc='Range indicator', aliases=('Short', 'Medium', 'Long'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ispool',val=0,optionsVal=(0,1), desc='Auxiliary power unit complexity indicator', aliases=('Single spool fixed vane', 'Double spool variable vane APU'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'itran',val=0,optionsVal=(0,1), desc='Cargo/baggage transfer operation indicator', aliases=('No transfer', 'Transfer'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iwind',val=0,optionsVal=(0,1), desc='Windshield type indicator', aliases=('Flat', 'Curved'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'kva',val=200.0, desc='KVA rating of full-time generators',typeVar='Float')
        self.add_param(strChain+'lf',val=55.0, desc='Passenger load factor',typeVar='Float')
        self.add_param(strChain+'life',val=14.0, desc='Number of years for Life Cycle Cost calculation',typeVar='Float')
        self.add_param(strChain+'napu',val=1, desc='Number of auxiliary power units',typeVar='Int')
        self.add_param(strChain+'nchan',val=1,optionsVal=(1,2,3), desc='Number of autopilot channels',typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nfltst',val=2, desc='Number of flight test aircraft',typeVar='Int')
        self.add_param(strChain+'ngen',val=3,optionsVal=(3,4), desc='Number of inflight operated generators',typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'nins',val=0, desc='Number of inertial navigation systems',typeVar='Int')
        self.add_param(strChain+'npod',val=4, desc='Number of podded engines',typeVar='Int')
        self.add_param(strChain+'nprotp',val=2, desc='Number of prototype aircraft',typeVar='Int')
        self.add_param(strChain+'pctfc',val=10.0, desc='Percent of seats for first class',typeVar='Float')
        self.add_param(strChain+'plmqt',val=1984.0, units='year', desc='Planned MQT (150-hour Model Qualification Test or FAA certification)',typeVar='Float')
        self.add_param(strChain+'prorat',val=15.0, desc='Manufacturers',typeVar='Float')
        self.add_param(strChain+'prproc',val=0.0, desc='Prior number of engines procured',typeVar='Float')
        self.add_param(strChain+'q',val=100.0, desc='Airframe production quantities',typeVar='Float')
        self.add_param(strChain+'resid',val=2.0, desc='Residual value at end of lifetime',typeVar='Float')
        self.add_param(strChain+'roi',val=10.0, desc='Return on investment (Triggers calculation of required fare)',typeVar='Float')
        self.add_param(strChain+'sfc',val=0.6, units='lb/h/lb', desc='Engine specific fuel consumption',typeVar='Float')
        self.add_param(strChain+'taxrat',val=0.33, desc='Corporate tax rate for ROI calculations',typeVar='Float')
        self.add_param(strChain+'temp',val=1800.0, units='degF', desc='Maximum turbine inlet temperature',typeVar='Float')




    def FlopsWrapper_input_confin_Objective(self):
        """Container for input:confin:Objective"""
        strChain = 'input:confin:Objective:'

       # OpenMDAO Public Variables
        self.add_param(strChain+'ofg',val=0.0, desc='Objective function weighting factor for gross weight \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'off',val=1.0, desc='Objective function weighting factor for mission fuel \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofm',val=0.0, desc='Objective function weighting factor for Mach*(L/D), should be negative to maximize \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofr',val=0.0, desc='Objective function weighting factor for Range, should be negative to maximize. \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofc',val=0.0, desc='Objective function weighting factor for Cost \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'osfc',val=0.0, desc='Objective function weighting factor for Specific Fuel Consumption at the engine design point.  Generally used only for engine design cases (IANAL = 4). \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofnox',val=0.0, desc='Objective function weighting factor for NOx emissions \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofnf',val=0.0, desc='Objective function weighting factor for flyover noise (used primarily for contour plots) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofns',val=0.0, desc='Objective function weighting factor for sideline noise (used primarily for contour plots) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofnfom',val=0.0, desc='Objective function weighting factor for noise figure of merit \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'oarea',val=0.0, desc='Objective function weighting factor for area of noise footprint (not implemented) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')
        self.add_param(strChain+'ofh',val=0.0, desc='Objective function weighting factor for hold time for segment NHOLD (See Namelist &MISSIN) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typeVar='Float')


    def FlopsWrapper_input_confin_Design_Variables(self):
        """Container for input:confin:Design_Variables"""
        strChain = 'input:confin:Design_Variables:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'gw',val=array([]), units='lb', desc='GW(0)=Ramp weight (Required.  If IRW = 1, a good initial guess must be input.)\nGW(1)=Activity status, active if > 0\nGW(2)=Lower bound\nGW(3)=Upper bound\nGW(4)=Optimization scale factor',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'ar',val=array([]), desc='AR(0)=Wing aspect ratio\nAR(1)=Activity status, active if > 0\nAR(2)=Lower bound\nAR(3)=Upper bound\nAR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'thrust',val=array([]), units='lb', desc='THRUST(0)=Maximum rated thrust per engine, or thrust-weight ratio if TWR = -1.\nTHRUST(1)=Activity status, active if > 0\nTHRUST(2)=Lower bound\nTHRUST(3)=Upper bound\nTHRUST(4)=Optimization scale factor',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'sw',val=array([]), units='ft*ft', desc='SW(0)=Reference wing area, or wing loading if WSR = -1.\nSW(1)=Activity status, active if > 0\nSW(2)=Lower bound\nSW(3)=Upper bound\nSW(4)=Optimization scale factor',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'tr',val=array([]), desc='TR(0)=Taper ratio of the wing (Required)\nTR(1)=Activity status, active if > 0\nTR(2)=Lower bound\nTR(3)=Upper bound\nTR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'sweep',val=array([]), units='deg', desc='SWEEP(0)=Quarter-chord sweep angle of the wing (Required)\nSWEEP(1)=Activity status, active if > 0\nSWEEP(2)=Lower bound\nSWEEP(3)=Upper bound\nSWEEP(4)=Optimization scale factor',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'tca',val=array([]), desc='TCA(0)=Wing thickness-chord ratio (weighted average) (Required)\nTCA(1)=Activity status, active if > 0\nTCA(2)=Lower bound\nTCA(3)=Upper bound\nTCA(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'vcmn',val=array([]), desc='VCMN(0)=Cruise Mach number (Required)\nVCMN(1)=Activity status, active if > 0\nVCMN(2)=Lower bound\nVCMN(3)=Upper bound\nVCMN(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ch',val=array([]), units='ft', desc='CH(0)=Maximum cruise altitude (Required)\nCH(1)=Activity status, active if > 0\nCH(2)=Lower bound\nCH(3)=Upper bound\nCH(4)=Optimization scale factor',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'varth',val=array([]), desc='VARTH(0)=Thrust derating factor for takeoff noise Fraction of full thrust used in takeoff\nVARTH(1)=Activity status, active if > 0\nVARTH(2)=Lower bound\nVARTH(3)=Upper bound\nVARTH(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'rotvel',val=array([]), desc='ROTVEL(0)=Rotation velocity for takeoff noise abatement (default is minimum required to meet takeoff performance constraints)\nROTVEL(1)=Activity status, active if > 0\nROTVEL(2)=Lower bound\nROTVEL(3)=Upper bound\nROTVEL(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'plr',val=array([]), desc='PLR(0)=Thrust fraction after programmed lapse rate (default thrust is specified in each segment)\nPLR(1)=Activity status, active if > 0\nPLR(2)=Lower bound\nPLR(3)=Upper bound\nPLR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'etit',val=array([]), units='degR', desc='ETIT(0)=Engine design point turbine entry temperature\nETIT(1)=Activity status, active if > 0\nETIT(2)=Lower bound\nETIT(3)=Upper bound\nETIT(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'eopr',val=array([]), desc='EOPR(0)=Overall pressure ratio\nEOPR(1)=Activity status, active if > 0\nEOPR(2)=Lower bound\nEOPR(3)=Upper bound\nEOPR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'efpr',val=array([]), desc='EFPR(0)=Fan pressure ratio (turbofans only)\nEFPR(1)=Activity status, active if > 0\nEFPR(2)=Lower bound\nEFPR(3)=Upper bound\nEFPR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ebpr',val=array([]), desc='EBPR(0)=Bypass ratio (turbofans only)\nEBPR(1)=Activity status, active if > 0\nEBPR(2)=Lower bound\nEBPR(3)=Upper bound\nEBPR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ettr',val=array([]), desc='ETTR(0)=Engine throttle ratio defined as the ratio of the maximum allowable turbine inlet temperature divided by the design point turbine inlet temperature.\nIf ETTR is greater than ETIT, it is assumed to be the maximum allowable turbine inlet temperature.\nETTR(1)=Activity status, active if > 0\nETTR(2)=Lower bound\nETTR(3)=Upper bound\nETTR(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'ebla',val=array([]), units='deg', desc='EBLA(0)=Blade angle for fixed pitch propeller\nEBLA(1)=Activity status, active if > 0\nEBLA(2)=Lower bound\nEBLA(3)=Upper bound\nEBLA(4)=Optimization scale factor',typeVar='Array',pass_by_obj=True)


    def FlopsWrapper_input_confin_Basic(self):
        """Container for input:confin:Basic"""
        strChain = 'input:confin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'desrng',val=0.0, desc='Design range (or endurance).  See INDR in Namelist &MISSIN)\nRequired - if IRW = 2 in Namelist &MISSIN, the range is computed, but a reasonable guess must still be input',typeVar='Float')
        self.add_param(strChain+'wsr',val=0.0, desc='Required wing loading if > 0.\nDo not set WSR > 0 during optimization or if wing area is being varied.\nInterpret SW as wing loading for parametric variation if = -1.\nDo not use for optimization.',typeVar='Float')
        self.add_param(strChain+'twr',val=0.0, desc='Required total thrust-weight ratio if > 0.\nDo not set TWR > 0 during optimization or if thrust is being varied.\nInterpret THRUST as thrust-weight ratio for parametric variation if = -1.\nDo not use for optimization.',typeVar='Float')
        self.add_param(strChain+'htvc',val=0.0, desc='Modified horizontal tail volume coefficient.\nIf HTVC > 0., SHT = HTVC * SW * Sqrt(SW/AR) / XL (This overrides any input value for SHT)\nIf HTVC = 1., the horizontal tail volume coefficient calculated from the input values of SHT, SW, AR and XL will be maintained.',typeVar='Float')
        self.add_param(strChain+'vtvc',val=0.0, desc='Modified vertical tail volume coefficient.\nIf VTVC > 0., SVT = VTVC * SW * Sqrt(SW*AR) / XL (This overrides any input value for SVT)\nIf VTVC = 1., the vertical tail volume coefficient calculated from the input values of SVT, SW, AR and XL will be maintained.',typeVar='Float')
        self.add_param(strChain+'pglov',val=0.0, desc='Fixed ratio of glove area to wing area (GLOV/SW).\nIf PGLOV > 0., GLOV will change if SW changes.',typeVar='Float')
        self.add_param(strChain+'fixspn',val=0.0, units='ft', desc='Special Option - Fixed wing span.  If the wing area is being varied or optimized, the wing aspect ratio will be adjusted to maintain a constant span.',typeVar='Float')
        self.add_param(strChain+'fixful',val=0.0, units='lb', desc='Special Option - Fixed mission fuel.  Allows specification of mission fuel.\nSince this fuel is normally a fall out (what is left over after OWE and payload are subtracted from the gross weight), this option requires iterating on the gross weight until the mission fuel = FIXFUL.  Gross weight cannot be an active design variable or used in a parametric variation, and IRW must be 2 in Namelist &MISSIN.',typeVar='Float')



    def FlopsWrapper_input_asclin(self):
        """Container for input:asclin"""
        strChain = 'input:asclin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'sref',val=0.0, units='ft*ft', desc='Wing area on which aerodynamic input is based (Default = SW, Namelist &CONFIN). If different from SW, aerodynamics will be scaled.',typeVar='Float')
        self.add_param(strChain+'tref',val=0.0, units='lb', desc='Engine thrust corresponding to nacelle size used in generating aerodynamic input data (Default = THRUST, Namelist &CONFIN). If different from THRUST, aerodynamic data will be modified.',typeVar='Float')
        self.add_param(strChain+'awetn',val=0.0, desc='Nacelle wetted area/SREF',typeVar='Float')
        self.add_param(strChain+'eltot',val=0.0, units='ft', desc='Total configuration length (Default = fuselage length)',typeVar='Float')
        self.add_param(strChain+'voltot',val=0.0, units='ft*ft*ft', desc='Total configuration volume',typeVar='Float')
        self.add_param(strChain+'awett',val=array([]), desc='Total wetted area/SREF.  For variable geometry aircraft, up to NMP values may be input',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'awetw',val=array([]), desc='Wing wetted area/SREF',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'elw',val=array([]), units='ft', desc='Total length of exposed wing',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'volw',val=array([]), units='ft*ft*ft', desc='Total volume of exposed wing',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'form',val=array([]), desc='Subsonic form factor for total configuration',typeVar='Array',pass_by_obj=True)
        self.add_param(strChain+'eql',val=array([]), units='ft', desc='Equivalent friction length for total baseline configuration.  If EQL is omitted, skin friction drag is computed from component data',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'cdwav',val=array([]), desc='Wave drag coefficients (NMP values)',typeVar='Array,float',pass_by_obj=True)
        self.add_param(strChain+'dcdnac',val=array([]), desc='Delta wave drag coefficients, nacelles on - nacelles off',typeVar='Array,float',pass_by_obj=True)


    def FlopsWrapper_input_aero_data(self):
        """Container for input:aero_data"""
        strChain = 'input:aero_data:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'aerodat',val='',typeVar='Str')


    def FlopsWrapper_input_aerin_Takeoff_Landing(self):
        """Container for input:aerin:Takeoff_Landing"""
        strChain = 'input:aerin:Takeoff_Landing:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'wratio',val=0.0, desc='Ratio of maximum landing weight to maximum takeoff weight (Default = WLDG/GW if WLDG is input, otherwise for supersonic aircraft Default = 1. - .00009*DESRNG, for subsonic aircraft Default = 1. - .00004*DESRNG)',typeVar='Float')
        self.add_param(strChain+'vappr',val=150.0, units='nmi', desc='Maximum allowable landing approach velocity',typeVar='Float')
        self.add_param(strChain+'flto',val=12000.0, units='ft', desc='Maximum allowable takeoff field length',typeVar='Float')
        self.add_param(strChain+'flldg',val=0.0, units='ft', desc='Maximum allowable landing field length',typeVar='Float')
        self.add_param(strChain+'cltom',val=2.0, desc='Maximum CL in takeoff configuration',typeVar='Float')
        self.add_param(strChain+'clldm',val=3.0, desc='Maximum CL in landing configuration',typeVar='Float')
        self.add_param(strChain+'clapp',val=0.0, desc='Approach CL',typeVar='Float')
        self.add_param(strChain+'dratio',val=1.0, desc='Takeoff and landing air density ratio',typeVar='Float')
        self.add_param(strChain+'elodss',val=0.0, desc='Lift-Drag ratio for second segment climb (Default is internally computed)',typeVar='Float')
        self.add_param(strChain+'elodma',val=0.0, desc='Lift-Drag ratio for missed approach climb (Default is internally computed)',typeVar='Float')
        self.add_param(strChain+'thrss',val=0.0, units='lb', desc='Thrust per baseline engine for second segment climb (Default = THRUST, Namelist &CONFIN)',typeVar='Float')
        self.add_param(strChain+'thrma',val=0.0, units='lb', desc='Thrust per baseline engine for missed approach climb (Default = THRSS)',typeVar='Float')
        self.add_param(strChain+'throff',val=0.0, units='lb', desc='Thrust per baseline engine for takeoff (Default = THRSS)',typeVar='Float')


    def FlopsWrapper_input_aerin_Internal_Aero(self):
        """Container for input:aerin:Internal_Aero"""
        strChain = 'input:aerin:Internal_Aero:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cam',val=0.0, desc='Maximum camber at 70% semispan, percent of local chord',typeVar='Float')
        self.add_param(strChain+'sbase',val=0.0, units='ft*ft', desc='Aircraft base area (total exit cross-section area minus inlet capture areas for internally mounted engines)',typeVar='Float')
        self.add_param(strChain+'aitek',val=1.0, desc='Airfoil technology parameter.  Use 1 for conventional wing and 2 for advanced technology wing',typeVar='Float')
        self.add_param(strChain+'modaro',val=0,optionsVal=(0,1), desc='Data tables in EDET are to be modified, Namelist &ARIDE will be read in', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'fcldes',val=-1.0, desc='Fixed design lift coefficient.  If input, overrides design CL computed by EDET.',typeVar='Float')
        self.add_param(strChain+'fmdes',val=-1.0, desc='Fixed design Mach number.  If input, overrides design Mach number computed by EDET.',typeVar='Float')
        self.add_param(strChain+'xllam',val=0,optionsVal=(0,1), desc='Use 0 for Turbulent flow and 1 for Laminar Flow', aliases=('Turbulent', 'Laminar'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'truw',val=0.0, desc='Percent LF wing upper surface',typeVar='Float')
        self.add_param(strChain+'trlw',val=0.0, desc='Percent LF wing low surface',typeVar='Float')
        self.add_param(strChain+'truh',val=0.0, desc='Percent LF horizontal tail upper surface',typeVar='Float')
        self.add_param(strChain+'trlh',val=0.0, desc='Percent LF horizontal tail lower surface',typeVar='Float')
        self.add_param(strChain+'truv',val=0.0, desc='Percent LF vertical tail upper surface',typeVar='Float')
        self.add_param(strChain+'trlv',val=0.0, desc='Percent LF vertical tail lower surface',typeVar='Float')
        self.add_param(strChain+'trub',val=0.0, desc='Percent LF fuselage upper surface',typeVar='Float')
        self.add_param(strChain+'trlb',val=0.0, desc='Percent LF fuselage lower surface',typeVar='Float')
        self.add_param(strChain+'trun',val=0.0, desc='Percent LF nacelle upper surface',typeVar='Float')
        self.add_param(strChain+'trln',val=0.0, desc='Percent LF nacelle lower surface',typeVar='Float')
        self.add_param(strChain+'truc',val=0.0, desc='Percent LF canard upper surface',typeVar='Float')
        self.add_param(strChain+'trlc',val=0.0, desc='Percent LF canard lower surface',typeVar='Float')
        self.add_param(strChain+'e',val=1.0, desc='Aerodynamic efficiency factor: use 1 for normal wing efficiency; normal wing efficiency modified for taper ratio and aspect ratio plus E if < 0; Otherwise, normal wing efficiency multiplied by E',typeVar='Float')
        self.add_param(strChain+'swetw',val=1.0, units='ft*ft', desc='Wing wetted area',typeVar='Float')
        self.add_param(strChain+'sweth',val=1.0, units='ft*ft', desc='Horizontal tail wetted area',typeVar='Float')
        self.add_param(strChain+'swetv',val=1.0, units='ft*ft', desc='Vertical tail wetted area',typeVar='Float')
        self.add_param(strChain+'swetf',val=1.0, units='ft*ft', desc='Fuselage wetted area',typeVar='Float')
        self.add_param(strChain+'swetn',val=1.0, units='ft*ft', desc='Nacelle wetted area',typeVar='Float')
        self.add_param(strChain+'swetc',val=1.0, units='ft*ft', desc='Canard wetted area',typeVar='Float')


    def FlopsWrapper_input_aerin_Basic(self):
        """Container for input:aerin:Basic"""
        strChain = 'input:aerin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'myaero',val=0,optionsVal=(0,1,2,3,4), desc='Controls type of user-supplied aerodynamic data\n= 0, Drag polars are computed internally\n= 1, Aerodynamic Data will be read in\n= 2, Scalable Aerodynamic Data will be input (Namelist &ASCLIN required)\n= 3, Special parabolic Aerodynamic Data format (Namelist &RFHIN required)\n= 4, Use aerodynamic response surface - available only in DOSS version', aliases=('Internal', 'Fixed input', 'Scalable input', 'Parabolic', 'Response surface'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'iwave',val=0,optionsVal=(0,1), desc='Controls Wave Drag Data input type\n= 1, Input Wave Drag Data will be formatted\n= 0, Otherwise', aliases=('No', 'Yes'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'fwave',val=1.0, desc='Wave drag factor - multiplies input values of wave drag from formatted aerodynamic data or Namelist &ASCLIN',typeVar='Float')
        self.add_param(strChain+'itpaer',val=2,optionsVal=(1,2,3), desc='Aerodynamic data interpolation switch\n= 1, Linear - Use if aerodynamic data is irregular.  This is usually indicated by strange climb, descent or cruise profiles.\n= 2, Parabolic\n= 3, Parabolic interpolation for CL, linear interpolation for Mach number and altitude.', aliases=('Linear', 'Parabolic', 'Combination'),typeVar='Enum',pass_by_obj=True)
        self.add_param(strChain+'ibo',val=0,optionsVal=(0,1), desc='Format indicator for input aerodynamic matrices\n= 1, A new line is started for each Mach number for Cards 4 and for each altitude for Cards 8\n= 0, Data is continuous, 10 to a line', aliases=('Continuous', '1 Mach/line'),typeVar='Enum',pass_by_obj=True)




    def add_rerun(self):
        """ Method to add a rerun* group to the list of input variables.  This method
        can be invoked multiple times to add as many rerun* groups as desired.
        The first group added is input:rerun0, the second is input:rerun1, etc.
        An additional missin group and mission definition file are also created
        within the new group.  Local var self:nrern0 keeps track of the number of
        groups added."""

        name = "rerun" + str(self.nrern0)
        self.nrern0 += 1
        self.npcons0.append(0)
        #comp = VariableTree()
        self.add_param('input:'+name+':desrng',val=-1,units="nmi.s")
        self.add_param('input:'+name+':mywts', val=-1 )
        self.add_param('input:'+name+':rampwt', val=-1., units="lb" )
        self.add_param('input:'+name+':dowe', val=-1., units="lb" )
        self.add_param('input:'+name+':paylod', val=-1., units="lb" )
        self.add_param('input:'+name+':fuemax', val=-1., units="lb" )
        self.add_param('input:'+name+':itakof', val=-1 )
        self.add_param('input:'+name+':iland', val=-1 )
        self.add_param('input:'+name+':nopro', val=-1 )
        self.add_param('input:'+name+':noise', val=-1 )
        self.add_param('input:'+name+':icost', val=-1 )
        self.add_param('input:'+name+':wsr', val=-1. )
        self.add_param('input:'+name+':twr', val=-1. )
        self.add_param('input:'+name+':iplrng', val=-999,typeVar='Int' )




        self.add_param('input:'+name+':missin:Basic:indr', val=-999)
        self.add_param('input:'+name+':missin:Basic:fact', val=-999.)
        self.add_param('input:'+name+':missin:Basic:fleak', val=-999.)
        self.add_param('input:'+name+':missin:Basic:fcdo', val=-999.)
        self.add_param('input:'+name+':missin:Basic:fcdi', val=-999.)
        self.add_param('input:'+name+':missin:Basic:fcdsub', val=-999.)
        self.add_param('input:'+name+':missin:Basic:fcdsup', val=-999.)
        self.add_param('input:'+name+':missin:Basic:iskal', val=-999)
        self.add_param('input:'+name+':missin:Basic:owfact', val=-999.)
        self.add_param('input:'+name+':missin:Basic:iflag', val=-999)
        self.add_param('input:'+name+':missin:Basic:msumpt', val=-999)
        self.add_param('input:'+name+':missin:Basic:dtc', val=-999.)
        self.add_param('input:'+name+':missin:Basic:irw', val=-999)
        self.add_param('input:'+name+':missin:Basic:rtol', val=-999.)
        self.add_param('input:'+name+':missin:Basic:nhold', val=-999)
        self.add_param('input:'+name+':missin:Basic:iata', val=-999)
        self.add_param('input:'+name+':missin:Basic:tlwind', val=-999.)
        self.add_param('input:'+name+':missin:Basic:dwt', val=-999.)
        self.add_param('input:'+name+':missin:Basic:offdr', array([]))
        self.add_param('input:'+name+':missin:Basic:idoq', val=-999)
        self.add_param('input:'+name+':missin:Basic:nsout', val=-999)
        self.add_param('input:'+name+':missin:Basic:nsadj', val=-999)
        self.add_param('input:'+name+':missin:Basic:mirror', val=-999)

        
        self.add_param('input:'+name+':missin:Store_Drag:stma',val=array([]))
        self.add_param('input:'+name+':missin:Store_Drag:cdst', val=array([]))
        self.add_param('input:'+name+':missin:Store_Drag:istcl', val=array([]))
        self.add_param('input:'+name+':missin:Store_Drag:istcr', val=array([]))
        self.add_param('input:'+name+':missin:Store_Drag:istde', val=-999)


        self.add_param('input:'+name+':missin:User_Weights:mywts', val=-999)
        self.add_param('input:'+name+':missin:User_Weights:rampwt', val=-999.)
        self.add_param('input:'+name+':missin:User_Weights:dowe', val=-999.)
        self.add_param('input:'+name+':missin:User_Weights:paylod', val=-999.)
        self.add_param('input:'+name+':missin:User_Weights:fuemax', val=-999.)


        self.add_param('input:'+name+':missin:Ground_Operations:takotm', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:taxotm', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:apprtm', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:appfff', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:taxitm', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:ittff', val=-999)
        self.add_param('input:'+name+':missin:Ground_Operations:takoff', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:txfufl', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:ftkofl', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:ftxofl', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:ftxifl', val=-999.)
        self.add_param('input:'+name+':missin:Ground_Operations:faprfl', val=-999.)


        self.add_param('input:'+name+':missin:Turn_Segments:xnz', val=array([]))
        self.add_param('input:'+name+':missin:Turn_Segments:xcl', val=array([]))
        self.add_param('input:'+name+':missin:Turn_Segments:xmach', val=array([]))


        self.add_param('input:'+name+':missin:Climb:nclimb', val=-999)
        self.add_param('input:'+name+':missin:Climb:clmmin', val=array([]))
        self.add_param('input:'+name+':missin:Climb:clmmax', val=array([]))
        self.add_param('input:'+name+':missin:Climb:clamin', val=array([]))
        self.add_param('input:'+name+':missin:Climb:clamax', val=array([]))
        self.add_param('input:'+name+':missin:Climb:nincl', val=array([]))
        self.add_param('input:'+name+':missin:Climb:fwf', val=array([]))
        self.add_param('input:'+name+':missin:Climb:ncrcl', val=array([]))
        self.add_param('input:'+name+':missin:Climb:cldcd', val=array([]))
        self.add_param('input:'+name+':missin:Climb:ippcl', val=array([]))
        self.add_param('input:'+name+':missin:Climb:maxcl', val=array([]))
        self.add_param('input:'+name+':missin:Climb:no', val=array([]))
        self.add_param('input:'+name+':missin:Climb:keasvc', val=-999)
        self.add_param('input:'+name+':missin:Climb:actab', val=array([]))
        self.add_param('input:'+name+':missin:Climb:vctab', val=array([]))
        self.add_param('input:'+name+':missin:Climb:ifaacl', val=-999)
        self.add_param('input:'+name+':missin:Climb:ifaade', val=-999)
        self.add_param('input:'+name+':missin:Climb:nodive', val=-999)
        self.add_param('input:'+name+':missin:Climb:divlim', val=-999.)
        self.add_param('input:'+name+':missin:Climb:qlim', val=-999.)
        self.add_param('input:'+name+':missin:Climb:spdlim', val=-999.)
        self.add_param('input:'+name+':missin:Climb:nql', val=-999)
        self.add_param('input:'+name+':missin:Climb:qlalt', val=array([]))
        self.add_param('input:'+name+':missin:Climb:vqlm', val=array([]))





        self.add_param('input:'+name+':missin:Cruise:ncruse', val=-999)
        self.add_param('input:'+name+':missin:Cruise:ioc', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:crmach', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:cralt', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:crdcd', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:flrcr', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:crmmin', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:crclmx', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:hpmin', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:ffuel', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:fnox', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:ifeath', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:feathf', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:cdfeth', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:dcwt', val=-999.)
        self.add_param('input:'+name+':missin:Cruise:rcin', val=-999.)
        self.add_param('input:'+name+':missin:Cruise:wtbm', val=array([]))
        self.add_param('input:'+name+':missin:Cruise:altbm', val=array([]))


        self.add_param('input:'+name+':missin:Descent:ivs', val=-999)
        self.add_param('input:'+name+':missin:Descent:decl', val=-999.)
        self.add_param('input:'+name+':missin:Descent:demmin', val=-999.)
        self.add_param('input:'+name+':missin:Descent:demmax', val=-999.)
        self.add_param('input:'+name+':missin:Descent:deamin', val=-999.)
        self.add_param('input:'+name+':missin:Descent:deamax', val=-999.)
        self.add_param('input:'+name+':missin:Descent:ninde', val=-999)
        self.add_param('input:'+name+':missin:Descent:dedcd', val=-999.)
        self.add_param('input:'+name+':missin:Descent:rdlim', val=-999.)
        self.add_param('input:'+name+':missin:Descent:ns', val=-999)
        self.add_param('input:'+name+':missin:Descent:keasvd', val=-999)
        self.add_param('input:'+name+':missin:Descent:adtab', val=array([]))
        self.add_param('input:'+name+':missin:Descent:vdtab', val=array([]))


        self.add_param('input:'+name+':missin:Reserve:irs', val=-999)
        self.add_param('input:'+name+':missin:Reserve:resrfu', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:restrp', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:timmap', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:altran', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:nclres', val=-999)
        self.add_param('input:'+name+':missin:Reserve:ncrres', val=-999)
        self.add_param('input:'+name+':missin:Reserve:sremch', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:eremch', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:srealt', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:erealt', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:holdtm', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:ncrhol', val=-999)
        self.add_param('input:'+name+':missin:Reserve:ihopos', val=-999)
        self.add_param('input:'+name+':missin:Reserve:icron', val=-999)
        self.add_param('input:'+name+':missin:Reserve:thold', val=-999.)
        self.add_param('input:'+name+':missin:Reserve:ncrth', val=-999)



    def generate_input(self):

        paramList = list(self._params_dict.keys())
        
        #These lines to ensure that floats do not get represented as ints in flops input(flops.in)
        '''for param in paramList:
            if 'typeVar' in self._params_dict[param]:
                keyVar = self._params_dict[param]
                if keyVar['typeVar']=='Array,int' and isinstance(keyVar['val'],ndarray):              
                        self._params_dict[param]['val'] = array(self._params_dict[param]['val'],dtype=numpy_int64 ).tolist()
                if (keyVar['typeVar'].lower()=='list' or keyVar['typeVar']=='Array,int')   and isinstance(keyVar['val'],int):              
                        self._params_dict[param]['val'] = array([self._params_dict[param]['val']])


                elif keyVar['typeVar']=='Array,float' and isinstance(keyVar['val'],ndarray):
                        self._params_dict[param]['val'] = array(self._params_dict[param]['val'] ,dtype=numpy_float64)
                elif keyVar['typeVar']=='Float' and isinstance(keyVar['val'],int):
                        self._params_dict[param]['val'] = float(self._params_dict[param]['val'] )'''


        sb = Namelist(self)
        sb.set_filename(self.input_filepath)
        sb.set_title(self.getValue('input:title'))

        #-------------------
        # Namelist &OPTION
        #-------------------

        sb.add_group('OPTION')
        sb.add_comment("\n  ! Program Control, Execution, Analysis and Plot Option Data")

        iopt = self.getValue('input:option:Program_Control:iopt')
        ianal = self.getValue('input:option:Program_Control:ianal')
        ineng = self.getValue('input:option:Program_Control:ineng')
        itakof = self.getValue('input:option:Program_Control:itakof')
        iland = self.getValue('input:option:Program_Control:iland')
        nopro = self.getValue('input:option:Program_Control:nopro')
        noise = self.getValue('input:option:Program_Control:noise')
        icost = self.getValue('input:option:Program_Control:icost')
        ifite = self.getValue('input:option:Program_Control:ifite')
        mywts = self.getValue('input:wtin:Basic:mywts')

        sb.add_container("input:option:Program_Control")

        sb.add_comment("\n  ! Plot files for XFLOPS Graphical Interface Postprocessor (MSMPLOT)")
        sb.add_var("input:option:Plot_Files:ixfl")

        sb.add_comment("\n  ! Takeoff and Climb Profile File for Noise Calculations (NPROF)")
        sb.add_var("input:option:Plot_Files:npfile")

        sb.add_comment("\n  ! Approach and Landing Profile File for Noise Calculations (LPROF)")
        sb.add_var("input:option:Plot_Files:lpfile")

        sb.add_comment("\n  ! Drag Polar Plot File (POLPLOT)")
        sb.add_var("input:option:Plot_Files:ipolp")
        sb.add_var("input:option:Plot_Files:polalt")

        nmach = size(self.getValue('input:option:Plot_Files:pmach'))
        if nmach > 0:
            sb.add_newvar("nmach", nmach)
            sb.add_var("input:option:Plot_Files:pmach")

        sb.add_comment("\n  ! Engine Performance Data Plot File (THRPLOT)")
        sb.add_var("input:option:Plot_Files:ipltth")

        sb.add_comment("\n  ! Design History Plot File (HISPLOT)")
        sb.add_var("input:option:Plot_Files:iplths")

        ipltps = size(self.getValue("input:option:Excess_Power_Plot:pltnz"))
        if ipltps > 0:
            sb.add_comment("\n  ! Excess Power Plot File (PSPLOT)")
            sb.add_newvar("ipltps", ipltps)
            sb.add_container("input:option:Excess_Power_Plot")

        # Plotfile names
        sb.add_comment("\n  ! Plotfile Names")
        if self.getValue("input:option:Plot_Files:cnfile"):
            sb.add_var("input:option:Plot_Files:cnfile")
        if self.getValue("input:option:Plot_Files:msfile"):
            sb.add_var("input:option:Plot_Files:msfile")
        if self.getValue("input:option:Plot_Files:crfile"):
            sb.add_var("input:option:Plot_Files:crfile")
        if self.getValue("input:option:Plot_Files:tofile") :
            sb.add_var("input:option:Plot_Files:tofile")
        if self.getValue("input:option:Plot_Files:nofile"):
            sb.add_var("input:option:Plot_Files:nofile")
        if self.getValue("input:option:Plot_Files:apfile") :
            sb.add_var("input:option:Plot_Files:apfile")
        if self.getValue("input:option:Plot_Files:thfile") :
            sb.add_var("input:option:Plot_Files:thfile ")
        if self.getValue("input:option:Plot_Files:hsfile") :
            sb.add_var("input:option:Plot_Files:hsfile")
        if self.getValue("input:option:Plot_Files:psfile") :
            sb.add_var("input:option:Plot_Files:psfile")

        #-------------------
        # Namelist &WTIN
        #-------------------

        sb.add_group('WTIN')

        sb.add_comment("\n  ! Geometric, Weight, Balance and Inertia Data")
        sb.add_container("input:wtin:Basic")

        sb.add_comment("\n  ! Special Option for Operating Weight Empty Calculations")
        sb.add_container("input:wtin:OEW_Calculations")

        sb.add_comment("\n  ! Wing Data")
        sb.add_container("input:wtin:Wing_Data")

        netaw = size(self.getValue("input:wtin:Detailed_Wing:etaw"))

    

        if netaw > 0:
            sb.add_comment("\n  ! Detailed Wing Data")
            sb.add_newvar("netaw", netaw)
            sb.add_var("input:wtin:Detailed_Wing:etaw")
            sb.add_var("input:wtin:Detailed_Wing:chd")
            sb.add_var("input:wtin:Detailed_Wing:toc")
            sb.add_var("input:wtin:Detailed_Wing:swl")
            sb.add_var("input:wtin:Detailed_Wing:etae")
            sb.add_var("input:wtin:Detailed_Wing:pctl")
            sb.add_var("input:wtin:Detailed_Wing:arref")
            sb.add_var("input:wtin:Detailed_Wing:tcref")
            sb.add_var("input:wtin:Detailed_Wing:nstd")

            pdist = self.getValue("input:wtin:Detailed_Wing:pdist")
            sb.add_var("input:wtin:Detailed_Wing:pdist")
            if pdist < 0.0001:
                sb.add_var("input:wtin:Detailed_Wing:etap")
                sb.add_var("input:wtin:Detailed_Wing:pval")

        sb.add_comment("\n  ! Tails, Fins, Canards")
        sb.add_comment("\n  ! Horizontal Tail Data")
        sb.add_var("input:wtin:Tails_Fins:sht")
        sb.add_var("input:wtin:Tails_Fins:swpht")
        sb.add_var("input:wtin:Tails_Fins:arht")
        sb.add_var("input:wtin:Tails_Fins:trht")
        sb.add_var("input:wtin:Tails_Fins:tcht")
        sb.add_var("input:wtin:Tails_Fins:hht")

        nvert = self.getValue("input:wtin:Tails_Fins:nvert")
        if nvert != 0:
            sb.add_comment("\n  ! Vertical Tail Data")
            sb.add_var("input:wtin:Tails_Fins:nvert")
            sb.add_var("input:wtin:Tails_Fins:svt")
            sb.add_var("input:wtin:Tails_Fins:swpvt")
            sb.add_var("input:wtin:Tails_Fins:arvt")
            sb.add_var("input:wtin:Tails_Fins:trvt")
            sb.add_var("input:wtin:Tails_Fins:tcvt")

        nfin = self.getValue("input:wtin:Tails_Fins:nfin")
        if nfin != 0:
            sb.add_comment("\n  ! Fin Data")
            sb.add_var("input:wtin:Tails_Fins:nfin")
            sb.add_var("input:wtin:Tails_Fins:sfin")
            sb.add_var("input:wtin:Tails_Fins:arfin")
            sb.add_var("input:wtin:Tails_Fins:trfin")
            sb.add_var("input:wtin:Tails_Fins:swpfin")
            sb.add_var("input:wtin:Tails_Fins:tcfin")

        scan = self.getValue("input:wtin:Tails_Fins:scan")
        if scan != 0:
            sb.add_comment("\n  ! Canard Data")
            sb.add_var("input:wtin:Tails_Fins:scan")
            sb.add_var("input:wtin:Tails_Fins:swpcan")
            sb.add_var("input:wtin:Tails_Fins:arcan")
            sb.add_var("input:wtin:Tails_Fins:trcan")
            sb.add_var("input:wtin:Tails_Fins:tccan")

        sb.add_comment("\n  ! Fuselage Data")
        sb.add_container("input:wtin:Fuselage")

        sb.add_comment("\n  ! Landing Gear Data")
        sb.add_container("input:wtin:Landing_Gear")

        sb.add_comment("\n  ! Propulsion System Data")
        sb.add_container("input:wtin:Propulsion")

        sb.add_comment("\n  ! Fuel System Data")
        sb.add_var("input:wtin:Fuel_System:ntank")
        sb.add_var("input:wtin:Fuel_System:fulwmx")
        sb.add_var("input:wtin:Fuel_System:fulden")
        sb.add_var("input:wtin:Fuel_System:fulfmx")
        sb.add_var("input:wtin:Fuel_System:ifufu")
        sb.add_var("input:wtin:Fuel_System:fulaux")
        fmxtot = self.getValue("input:wtin:Fuel_System:fmxtot")
        if fmxtot>-999.:
            sb.add_var("input:wtin:Fuel_System:fmxtot")

        fuscla = self.getValue("input:wtin:Fuel_System:fuscla")
        if fuscla > 0.000001:
            sb.add_comment("\n  ! Special method for scaling wing fuel capacity")
            sb.add_var("input:wtin:Fuel_System:fuelrf")
            sb.add_var("input:wtin:Fuel_System:fswref")
            sb.add_var("input:wtin:Fuel_System:fuscla")
            sb.add_var("input:wtin:Fuel_System:fusclb")

        sb.add_comment("\n  ! Crew and Payload Data")
        sb.add_container("input:wtin:Crew_Payload")

        paylmx = self.getValue("input:wtin:Crew_optional:paylmx")
        if paylmx>-999.:
            sb.add_var("input:wtin:Crew_optional:paylmx")


        sb.add_comment("\n  ! Override Parameters")
        sb.add_container("input:wtin:Override")

        sb.add_comment("\n  ! Center of Gravity (C.G.) Data")
        sb.add_container("input:wtin:Center_of_Gravity")

        inrtia = self.getValue("input:wtin:Inertia:inrtia")
        if inrtia != 0:
            sb.add_comment("\n  ! Inertia Data")
            sb.add_newvar("inrtia", inrtia)
            sb.add_var("input:wtin:Inertia:zht")
            sb.add_var("input:wtin:Inertia:zvt")
            sb.add_var("input:wtin:Inertia:zfin")
            sb.add_var("input:wtin:Inertia:yfin")
            sb.add_var("input:wtin:Inertia:zef")
            sb.add_var("input:wtin:Inertia:yef")
            sb.add_var("input:wtin:Inertia:zea")
            sb.add_var("input:wtin:Inertia:yea")
            sb.add_var("input:wtin:Inertia:zbw")
            sb.add_var("input:wtin:Inertia:zap")
            sb.add_var("input:wtin:Inertia:zrvt")
            sb.add_var("input:wtin:Inertia:ymlg")
            sb.add_var("input:wtin:Inertia:yfuse")
            sb.add_var("input:wtin:Inertia:yvert")
            sb.add_var("input:wtin:Inertia:swtff")
            sb.add_var("input:wtin:Inertia:tcr")
            sb.add_var("input:wtin:Inertia:tct")
            sb.add_var("input:wtin:Inertia:incpay")

            l = size(self.getValue("input:wtin:Inertia:tx"))
            sb.add_newvar("itank", l)
            if l > 0:
                sb.add_var("input:wtin:Inertia:tx")
                sb.add_var("input:wtin:Inertia:ty")
                sb.add_var("input:wtin:Inertia:tz")

            j = size(self.getValue("input:wtin:Inertia:tl"))
            if j > 0:
                sb.add_var("input:wtin:Inertia:tl")
                sb.add_var("input:wtin:Inertia:tw")
                sb.add_var("input:wtin:Inertia:td")

            j = self.getValue("input:wtin:Inertia:tf").shape[0]
            sb.add_newvar("nfcon", j)
            if l*j > 0:
                sb.add_var("input:wtin:Inertia:tf")

        #-------------------
        # Namelist &FUSEIN
        #-------------------

        # Namelist &FUSEIN is only required if XL=0 or IFITE=3.
        xl = self.getValue("input:wtin:Fuselage:xl")
        if xl < 0.0000001 or ifite == 3:

            sb.add_group('FUSEIN')
            sb.add_comment("\n  ! Fuselage Design Data")
            sb.add_container("input:fusein:Basic")
            sb.add_container("input:fusein:BWB")

        #-------------------
        # Namelist &CONFIN
        #-------------------

        sb.add_group('CONFIN')
        sb.add_container("input:confin:Basic")

        # MC Flops wrapper didn't write these out if iopt was less than 3
        # I changed it to match expected behavior when comparing manual FLOPS
        # if iopt >= 3:
        sb.add_comment("\n  ! Objective Function Definition")
        sb.add_container("input:confin:Objective")

        sb.add_comment("\n  ! Design Variables")
        sb.add_var("input:confin:Design_Variables:gw")
        sb.add_var("input:confin:Design_Variables:ar")
        sb.add_var("input:confin:Design_Variables:thrust")
        sb.add_var("input:confin:Design_Variables:sw")
        sb.add_var("input:confin:Design_Variables:tr")
        sb.add_var("input:confin:Design_Variables:sweep")
        sb.add_var("input:confin:Design_Variables:tca")
        sb.add_var("input:confin:Design_Variables:vcmn")
        sb.add_var("input:confin:Design_Variables:ch")
        sb.add_var("input:confin:Design_Variables:varth")
        sb.add_var("input:confin:Design_Variables:rotvel")
        sb.add_var("input:confin:Design_Variables:plr")

        igenen = self.getValue("input:engdin:Basic:igenen")
        if igenen in (1, -2):
            sb.add_comment("\n  ! Engine Design Variables")
            sb.add_var("input:confin:Design_Variables:etit")
            sb.add_var("input:confin:Design_Variables:eopr")
            sb.add_var("input:confin:Design_Variables:efpr")
            sb.add_var("input:confin:Design_Variables:ebpr")
            sb.add_var("input:confin:Design_Variables:ettr")
            sb.add_var("input:confin:Design_Variables:ebla")

        #-------------------
        # Namelist &AERIN
        #-------------------

        sb.add_group('AERIN')

        myaero = self.getValue("input:aerin:Basic:myaero")
        iwave = self.getValue("input:aerin:Basic:iwave")
        if myaero != 0:
            sb.add_comment("\n  ! Externally Computed Aerodynamics")
            sb.add_var("input:aerin:Basic:myaero")
            sb.add_var("input:aerin:Basic:iwave")
            if iwave != 0:
                sb.add_var("input:aerin:Basic:fwave")
            sb.add_var("input:aerin:Basic:itpaer")
            sb.add_var("input:aerin:Basic:ibo")
        else:
            sb.add_comment("\n  ! Internally Computed Aerodynamics")
            sb.add_container("input:aerin:Internal_Aero")

        sb.add_container("input:aerin:Takeoff_Landing")

        #-------------------
        # Namelist &COSTIN
        #-------------------

        # Namelist &COSTIN is only required if ICOST=1.
        if icost != 0:
            sb.add_group('COSTIN')

            sb.add_comment("\n  ! Cost Calculation Data")
            sb.add_container("input:costin:Basic")
            sb.add_comment("\n  ! Mission Performance Data")
            sb.add_container("input:costin:Mission_Performance")
            sb.add_comment("\n  ! Cost Technology Parameters")
            sb.add_container("input:costin:Cost_Technology")

        #-------------------
        # Namelist &ENGDIN
        #-------------------

        # Namelist &ENGDIN is only required in IANAL=3 or 4 or INENG=1.
        if ianal in (3, 4) or ineng == 1:
            sb.add_group('ENGDIN')

            sb.add_comment("\n  ! Engine Deck Control, Scaling and Usage Data")
            sb.add_var("input:engdin:Basic:ngprt")
            sb.add_var("input:engdin:Basic:igenen")
            sb.add_var("input:engdin:Basic:extfac")
            sb.add_var("input:engdin:Basic:fffsub")
            sb.add_var("input:engdin:Basic:fffsup")
            sb.add_var("input:engdin:Basic:idle")
            sb.add_var("input:engdin:Basic:noneg")
            sb.add_var("input:engdin:Basic:fidmin")
            sb.add_var("input:engdin:Basic:fidmax")
            sb.add_var("input:engdin:Basic:ixtrap")
            sb.add_var("input:engdin:Basic:ifill")
            sb.add_var("input:engdin:Basic:maxcr")
            sb.add_var("input:engdin:Basic:nox")

            npcode =  size(self.getValue("input:engdin:Basic:pcode"))
            if npcode > 0:
                sb.add_newvar("npcode", npcode)
                sb.add_var("input:engdin:Basic:pcode")

            sb.add_var("input:engdin:Basic:boost")
            sb.add_var("input:engdin:Basic:igeo")
            sb.add_var("input:engdin:Special_Options:dffac")
            sb.add_var("input:engdin:Special_Options:fffac")

            if igenen in (1, -2):
                j =  size(self.getValue("input:engdin:Special_Options:emach"))
                l =  self.getValue("input:engdin:Special_Options:alt").shape[0]
                if j > 0:
                    # TODO - Find out about fake 2d for new FLOPS double prop
                    # capability.
                    sb.add_var("input:engdin:Special_Options:emach")
                    if l*j > 0:
                        # TODO - Find out about fake 3d for new FLOPS double prop
                        # capability.
                        sb.add_var("input:engdin:Special_Options:alt")

            insdrg =  self.getValue("input:engdin:Special_Options:insdrg")
            if insdrg != 0:
                sb.add_comment("\n  ! Nozzle installation drag using table look-up")
                sb.add_newvar("insdrg", insdrg)
                sb.add_var("input:engdin:Special_Options:nab")
                sb.add_var("input:engdin:Special_Options:nabref")
                sb.add_var("input:engdin:Special_Options:a10")
                sb.add_var("input:engdin:Special_Options:a10ref")
                sb.add_var("input:engdin:Special_Options:a9ref")
                sb.add_var("input:engdin:Special_Options:xnoz")
                sb.add_var("input:engdin:Special_Options:xnref")
                sb.add_var("input:engdin:Special_Options:rcrv")

                # TODO - rawInputFile( cdfile, "ENDRAG" );
                #cdfile.open

            # Write out the eifile. This is a new addition.
            if self.getValue("input:engdin:eifile"):
                sb.add_var("input:engdin:eifile")


            #----------------------
            # Namelist Engine deck
            #----------------------

            # Insert the engine deck into the flops input file

            # If IGENEN=0 the engine deck is part of the input file, otherwise it is an
            # external file.

            engine_deck  = self.getValue("input:engine_deck:engdek")
            if igenen in (0, -2):
                # engine_deck contains the raw engine deck
                sb.add_group(engine_deck)
            else:
                # engine_deck contains the name of the engine deck file
                if engine_deck:
                    sb.add_var("input:engine_deck:engdek")

        #-------------------
        # Namelist &ENGINE
        #-------------------

        # Namelist &ENGINE is only required if IGENEN=-2 or 1.
        if igenen in (-2, 1):

            sb.add_group('ENGINE')

            nginwt =  self.getValue("input:engine:Engine_Weight:nginwt")
            ieng = self.getValue("input:engine:Basic:ieng")

            sb.add_var("input:engine:Basic:ieng")
            sb.add_var("input:engine:Basic:iprint")
            sb.add_var("input:engine:Basic:gendek")
            sb.add_var("input:engine:Basic:ithrot")
            sb.add_var("input:engine:Basic:npab")
            sb.add_var("input:engine:Basic:npdry")
            sb.add_var("input:engine:Basic:xidle")
            sb.add_var("input:engine:Basic:nitmax")

            if self.getValue("input:engine:Basic:xmmax") > 0:
                sb.add_var("input:engine:Basic:xmmax")
            if self.getValue("input:engine:Basic:amax") > 0:
                sb.add_var("input:engine:Basic:amax")
            if self.getValue("input:engine:Basic:xminc") > 0:
                sb.add_var("input:engine:Basic:xminc")
            if self.getValue("input:engine:Basic:ainc") > 0:
                sb.add_var("input:engine:Basic:ainc")
            if self.getValue("input:engine:Basic:qmin") > 0:
                sb.add_var("input:engine:Basic:qmin")
            if self.getValue("input:engine:Basic:qmax") > 0:
                sb.add_var("input:engine:Basic:qmax")

            sb.add_newvar("nginwt", nginwt)
            sb.add_container("input:engine:Noise_Data")

            if self.getValue("input:engine:Design_Point:desfn") > 0:
                sb.add_var("input:engine:Design_Point:desfn")
            if self.getValue("input:engine:Design_Point:xmdes") > 0:
                sb.add_var("input:engine:Design_Point:xmdes")
            if self.getValue("input:engine:Design_Point:xades") > 0:
                sb.add_var("input:engine:Design_Point:xades")

            sb.add_var("input:engine:Design_Point:oprdes")
            sb.add_var("input:engine:Design_Point:fprdes")
            sb.add_var("input:engine:Design_Point:bprdes")
            sb.add_var("input:engine:Design_Point:tetdes")
            sb.add_var("input:engine:Design_Point:ttrdes")
            sb.add_var("input:engine:Other:hpcpr")
            sb.add_var("input:engine:Other:aburn")
            sb.add_var("input:engine:Other:dburn")
            sb.add_var("input:engine:Other:effab")
            sb.add_var("input:engine:Other:tabmax")
            sb.add_var("input:engine:Other:ven")
            sb.add_var("input:engine:Other:costbl")
            sb.add_var("input:engine:Other:fanbl")
            sb.add_var("input:engine:Other:hpext")
            sb.add_var("input:engine:Other:wcool")
            sb.add_var("input:engine:Other:fhv")
            sb.add_var("input:engine:Other:dtce")
            sb.add_var("input:engine:Other:alc")
            sb.add_var("input:engine:Other:year")
            sb.add_comment("\n  ! Installation effects")
            sb.add_var("input:engine:Other:boat")
            sb.add_var("input:engine:Other:ajmax")

            if self.getValue("input:engine:Other:spill"):
                sb.add_comment("\n  ! Installation effects")
                sb.add_var("input:engine:Other:spill")
                sb.add_var("input:engine:Other:lip")
                sb.add_var("input:engine:Other:blmax")
                sb.add_var("input:engine:Other:spldes")
                sb.add_var("input:engine:Other:aminds")
                sb.add_var("input:engine:Other:alinds")

            sb.add_var("input:engine:Other:etaprp")
            sb.add_var("input:engine:Other:shpowa")
            sb.add_comment("\n  ! Engine operating constraints")
            sb.add_var("input:engine:Other:cdtmax")
            sb.add_var("input:engine:Other:cdpmax")
            sb.add_var("input:engine:Other:vjmax")
            sb.add_var("input:engine:Other:stmin")
            sb.add_var("input:engine:Other:armax")
            sb.add_var("input:engine:Other:limcd")

            if nginwt != 0:
                sb.add_comment("\n  ! Engine Weight Calculation Data")
                sb.add_var("input:engine:Engine_Weight:iwtprt")
                sb.add_var("input:engine:Engine_Weight:iwtplt")
                sb.add_var("input:engine:Engine_Weight:gratio")
                sb.add_var("input:engine:Engine_Weight:utip1")
                sb.add_var("input:engine:Engine_Weight:rh2t1")
                sb.add_var("input:engine:Engine_Weight:igvw")
                sb.add_var("input:engine:Engine_Weight:trbrpm")
                sb.add_var("input:engine:Engine_Weight:trban2")
                sb.add_var("input:engine:Engine_Weight:trbstr")
                sb.add_var("input:engine:Engine_Weight:cmpan2")
                sb.add_var("input:engine:Engine_Weight:cmpstr")
                sb.add_var("input:engine:Engine_Weight:vjpnlt")
                sb.add_var("input:engine:Engine_Weight:wtebu")
                sb.add_var("input:engine:Engine_Weight:wtcon")

            if ieng == 101:
                sb.add_var("input:engine:IC_Engine:ncyl")
                sb.add_var("input:engine:IC_Engine:deshp")
                sb.add_var("input:engine:IC_Engine:alcrit")
                sb.add_var("input:engine:IC_Engine:sfcmax")
                sb.add_var("input:engine:IC_Engine:sfcmin")
                sb.add_var("input:engine:IC_Engine:pwrmin")
                sb.add_var("input:engine:IC_Engine:engspd")
                sb.add_var("input:engine:IC_Engine:prpspd")

            if ieng == 101 or igenen == -2 and nginwt > 0:
                sb.add_var("input:engine:IC_Engine:iwc")
                sb.add_var("input:engine:IC_Engine:ecid")
                sb.add_var("input:engine:IC_Engine:ecr")

            if ieng == 101 or igenen == -2:
                sb.add_var("input:engine:IC_Engine:eht")
                sb.add_var("input:engine:IC_Engine:ewid")
                sb.add_var("input:engine:IC_Engine:elen")
                sb.add_var("input:engine:IC_Engine:ntyp")
                sb.add_var("input:engine:IC_Engine:af")
                sb.add_var("input:engine:IC_Engine:cli")
                sb.add_var("input:engine:IC_Engine:blang")
                sb.add_var("input:engine:IC_Engine:dprop")
                sb.add_var("input:engine:IC_Engine:nblade")
                sb.add_var("input:engine:IC_Engine:gbloss")

            nrpm =  size(self.getValue("input:engine:IC_Engine:arrpm"))
            if nrpm > 0:
                sb.add_comment("  ! power curve input data")
                sb.add_newvar("nrpm", nrpm)
                sb.add_var("input:engine:IC_Engine:arrpm")
                sb.add_var("input:engine:IC_Engine:arpwr")
                sb.add_var("input:engine:IC_Engine:arful")
                if self.input.engine.IC_Engine.lfuun != 0:
                    sb.add_var("input:engine:IC_Engine:lfuun")
                    sb.add_var("input:engine:IC_Engine:feng")

            sb.add_var("input:engine:IC_Engine:fprop")
            sb.add_var("input:engine:IC_Engine:fgbox")

            ifile = self.getValue("input:engine:ifile")
            tfile = self.getValue("input:engine:tfile")

            # The name of the engine cycle definition file to be read in is
            # set by the value of if IENG.
            filenames = { 0: "MYCYCL",
                          1: "TURJET",
                          2: "TFNSEP",
                          3: "TFNMIX",
                          4: "TURPRP",
                          5: "TBYPAS",
                          6: "TFNSP3",
                          7: "TFNMX3",
                          8: "TFN3SH",
                          9: "TURJT2",
                          101: "MYCYCL" }
            try:
                ifilNam = filenames[ieng]
            except KeyError:
                msg = "Illegal value %s for input:engine:Basic:IENG" % ieng
                raise KeyError(msg)

            # TODO - rawInputFile( ifile, ifilNam )
            # TODO - rawInputFile( tfile, "ENGTAB" )
            sb.add_newvar("tfile", tfile)
            sb.add_newvar("ifile", ifilNam)

            #-------------------
            # Namelist &NACELL
            #-------------------

            # Namelist &NACELL is only required if NGINWT != 0
            # (note:, still in IGENEN=-2 or 1.)
            if nginwt != 0:

                sb.add_group('NACELL')
                sb.add_comment("\n  ! Data for Computation of Nacelle Weight.")
                sb.add_container("input:nacell")

        #-------------------
        # Namelist &MISSIN
        #-------------------

        # Namelist &MISSIN is only required if IANAL=3

        npcon = self.getValue("input:missin:Basic:npcon")

        if ianal == 3:

            sb.add_group('MISSIN')

            sb.add_comment("\n  ! Performance Controls and Factors and Mission Segment Definition")
            sb.add_var("input:missin:Basic:indr")
            sb.add_var("input:missin:Basic:fact")
            sb.add_var("input:missin:Basic:fleak")
            sb.add_var("input:missin:Basic:fcdo")
            sb.add_var("input:missin:Basic:fcdi")
            sb.add_var("input:missin:Basic:fcdsub")
            sb.add_var("input:missin:Basic:fcdsup")
            sb.add_var("input:missin:Basic:iskal")
            sb.add_var("input:missin:Basic:owfact")
            sb.add_var("input:missin:Basic:iflag")
            sb.add_var("input:missin:Basic:msumpt")
            sb.add_var("input:missin:Basic:dtc")
            sb.add_var("input:missin:Basic:irw")
            sb.add_var("input:missin:Basic:rtol")
            sb.add_var("input:missin:Basic:nhold")
            sb.add_var("input:missin:Basic:iata")
            sb.add_var("input:missin:Basic:tlwind")
            sb.add_var("input:missin:Basic:dwt")

            if size(self.getValue("input:missin:Basic:offdr")) > 0:
                sb.add_var("input:missin:Basic:offdr")

            sb.add_var("input:missin:Basic:idoq")
            sb.add_newvar("npcon", npcon)

            nsout =  self.getValue("input:missin:Basic:nsout")
            if nsout > 0:
                sb.add_comment("\n  ! Combat Radius Mission\n")
                sb.add_newvar("nsout", nsout)
                sb.add_var("input:missin:Basic:nsadj")
                sb.add_var("input:missin:Basic:mirror")

            i =  size(self.getValue("input:missin:Store_Drag:stma"))
            if i > 0:
                sb.add_comment("\n  ! Store Drags")
                sb.add_container("input:missin:Store_Drag")

            sb.add_var("input:missin:User_Weights:mywts")
            if mywts == 1:
                sb.add_comment("\n  ! User-Specified Weights")
                sb.add_var("input:missin:User_Weights:rampwt")
                sb.add_var("input:missin:User_Weights:dowe")
                sb.add_var("input:missin:User_Weights:paylod")
                sb.add_var("input:missin:User_Weights:fuemax")

            sb.add_comment("\n  ! Ground Operations and Takeoff and Approach Allowances")
            sb.add_container("input:missin:Ground_Operations")

            if size(self.getValue("input:missin:Turn_Segments:xnz")) > 0:
                sb.add_var("input:missin:Turn_Segments:xnz")
            if size(self.getValue("input:missin:Turn_Segments:xcl")) > 0:
                sb.add_var("input:missin:Turn_Segments:xcl")
            if size(self.getValue("input:missin:Turn_Segments:xmach")) > 0:
                sb.add_var("input:missin:Turn_Segments:xmach")
           
            nclimb = max( size(self.getValue("input:missin:Climb:clmmin")),
                          size(self.getValue("input:missin:Climb:clmmax")),
                          size(self.getValue("input:missin:Climb:clamax")),
                          size(self.getValue("input:missin:Climb:nincl")),
                          size(self.getValue("input:missin:Climb:fwf")),
                          size(self.getValue("input:missin:Climb:ncrcl")),
                          size(self.getValue("input:missin:Climb:cldcd")),
                          size(self.getValue("input:missin:Climb:ippcl")),
                          size(self.getValue("input:missin:Climb:maxcl")) )

            # TODO - Ask Karl or Jeff about this
            # I've removed ioc and ifeath from this. These are parameters, so
            # their "length" should have nothing to do with how many Cruise
            # Schedules are in the model.
            ncruse = max( size(self.getValue("input:missin:Cruise:crmach")),
                          size(self.getValue("input:missin:Cruise:cralt")),
                          size(self.getValue("input:missin:Cruise:crdcd")),
                          size(self.getValue("input:missin:Cruise:flrcr")),
                          size(self.getValue("input:missin:Cruise:crmmin")),
                          size(self.getValue("input:missin:Cruise:crclmx")),
                          size(self.getValue("input:missin:Cruise:hpmin")),
                          size(self.getValue("input:missin:Cruise:ffuel")),
                          size(self.getValue("input:missin:Cruise:fnox")),
                          size(self.getValue("input:missin:Cruise:feathf")),
                          size(self.getValue("input:missin:Cruise:cdfeth")) )

            nql = size(self.getValue("input:missin:Climb:qlalt"))
            ns = size(self.getValue("input:missin:Descent:adtab"))

            sb.add_comment("\n  ! Climb Schedule Definition")
            sb.add_newvar("nclimb", nclimb)
            sb.add_var("input:missin:Climb:clmmin")
            sb.add_var("input:missin:Climb:clmmax")
            sb.add_var("input:missin:Climb:clamin")
            sb.add_var("input:missin:Climb:clamax")
            sb.add_var("input:missin:Climb:nincl")
            sb.add_var("input:missin:Climb:fwf")
            sb.add_var("input:missin:Climb:ncrcl")
            sb.add_var("input:missin:Climb:cldcd")
            sb.add_var("input:missin:Climb:ippcl")
            sb.add_var("input:missin:Climb:maxcl")
            sb.add_var("input:missin:Climb:keasvc")

            actab = self.getValue("input:missin:Climb:actab")
            no = actab.shape[1]
            if no == 0:
                no = actab.shape[0]
            elif no > 0:
                noval = ""
                for i in range(0, nclimb):
                    if actab.shape[1] > 0:
                        for j in range(0, actab.shape[1]):
                            if actab[i, j] >= 0.0:
                                n = j+1
                                noval += n + ", "
                            else:
                                break
                    else:
                        noval += "0, "

                sb.add_newvar("no", noval)
                sb.add_var("input:missin:Climb:actab")
                sb.add_var("input:missin:Climb:vctab")

            sb.add_var("input:missin:Climb:ifaacl")
            sb.add_var("input:missin:Climb:ifaade")
            sb.add_var("input:missin:Climb:nodive")
            sb.add_var("input:missin:Climb:divlim")
            sb.add_var("input:missin:Climb:qlim")
            sb.add_var("input:missin:Climb:spdlim")
            if nql > 0:
                sb.add_var("input:missin:Climb:qlalt")
                sb.add_var("input:missin:Climb:vqlm")

            sb.add_comment("\n  ! Cruise Schedule Definition\n")
            sb.add_newvar("ncruse", ncruse)
            sb.add_var("input:missin:Cruise:ioc")
            sb.add_var("input:missin:Cruise:crmach")
            sb.add_var("input:missin:Cruise:cralt")
            sb.add_var("input:missin:Cruise:crdcd")
            sb.add_var("input:missin:Cruise:flrcr")
            sb.add_var("input:missin:Cruise:crmmin")
            sb.add_var("input:missin:Cruise:crclmx")
            sb.add_var("input:missin:Cruise:hpmin")
            sb.add_var("input:missin:Cruise:ffuel")
            sb.add_var("input:missin:Cruise:fnox")
            sb.add_var("input:missin:Cruise:ifeath")
            sb.add_var("input:missin:Cruise:feathf")
            sb.add_var("input:missin:Cruise:cdfeth")
            sb.add_var("input:missin:Cruise:dcwt")
            sb.add_var("input:missin:Cruise:rcin")
            if size(self.getValue("input:missin:Cruise:wtbm")) > 0:
                sb.add_var("input:missin:Cruise:wtbm")
            if size(self.getValue("input:missin:Cruise:altbm")) > 0:
                sb.add_var("input:missin:Cruise:altbm")

            sb.add_comment("\n  ! Descent Schedule Definition")
            sb.add_var("input:missin:Descent:ivs")
            sb.add_var("input:missin:Descent:decl")
            sb.add_var("input:missin:Descent:demmin")
            sb.add_var("input:missin:Descent:demmax")
            sb.add_var("input:missin:Descent:deamin")
            sb.add_var("input:missin:Descent:deamax")
            sb.add_var("input:missin:Descent:ninde")
            sb.add_var("input:missin:Descent:dedcd")
            sb.add_var("input:missin:Descent:rdlim")
            sb.add_var("input:missin:Descent:keasvd")
            if ns > 0:
                sb.add_newvar("ns", ns)
                sb.add_var("input:missin:Descent:adtab")
                sb.add_var("input:missin:Descent:vdtab")

            sb.add_container("input:missin:Reserve")

            #----------------------
            # Mission definition
            #----------------------

            mission = self.getValue("input:mission_definition:mission")
            missionjoin = ' '.join(mission)

            for seg in mission:
                sb.add_group(seg)
            
            self.nmseg = missionjoin.count('CLIMB') + missionjoin.count('CRUISE') + \
                         missionjoin.count('REFUEL') + missionjoin.count('RELEASE') + \
                         missionjoin.count('ACCEL') + missionjoin.count('TURN') + \
                         missionjoin.count('COMBAT') + missionjoin.count('HOLD') + \
                         missionjoin.count('DESCENT')
           
        #-------------------
        # Namelist &PCONIN
        #-------------------

        # One or more &PCONIN namelists may have been created by the user.
        #print('cheCKING  PCONIN',npcon,ianal)
        if npcon > 0 and ianal == 3:

            for i in range(0, npcon):

                sb.add_group('PCONIN')
                sb.add_comment("\n  ! Performance Constraint")

                if self.getValue("input:pconin%s:conalt" % (i)) >= 0.:
                    sb.add_var("input:pconin%s:conalt" % (i))
                if self.getValue("input:pconin%s:conmch" % (i)) >= 0.:
                    sb.add_var("input:pconin%s:conmch" % (i))
                if self.getValue("input:pconin%s:connz" % (i)) >= 0.:
                    sb.add_var("input:pconin%s:connz" % (i))
                if self.getValue("input:pconin%s:conpc" % (i)) > -10.:
                    sb.add_var("input:pconin%s:conpc" % (i))
                if self.getValue("input:pconin%s:conlim" % (i)) != -999.:
                    sb.add_var("input:pconin%s:conlim" % (i))
                if self.getValue("input:pconin%s:conaux" % (i)) > -1.:
                    sb.add_var("input:pconin%s:conaux" % (i))
                if self.getValue("input:pconin%s:neo" % (i)) >= 0:
                    sb.add_var("input:pconin%s:neo" % (i))
                if self.getValue("input:pconin%s:icstdg" % (i)) >= 0:
                    sb.add_var("input:pconin%s:icstdg" % (i))
                if self.getValue("input:pconin%s:conwt" % (i)) >= 0.:
                    sb.add_var("input:pconin%s:conwt" % (i))
                if self.getValue("input:pconin%s:iconsg" % (i)) >= 0:
                    sb.add_var("input:pconin%s:iconsg" % (i))
                if self.getValue("input:pconin%s:confm" % (i)) >= 0.:
                    sb.add_var("input:pconin%s:confm" % (i))
                if self.getValue("input:pconin%s:conwta" % (i)) != -999.:
                    sb.add_var("input:pconin%s:conwta" % (i))
                if self.getValue("input:pconin%s:icontp" % (i)) >= 0:
                    sb.add_var("input:pconin%s:icontp" % (i))

        #--------------------
        # Aerodynamic data
        #--------------------

        # Aerodynamic data are placed in the input file if MYAERO > 0.  If MYAERO=3,
        # insert the aerodynamic data after namelist &RFHIN (below), otherwise insert
        # them here.

        if myaero > 0 and myaero != 3 and ianal == 3:

            # aerodat contains the raw aero data
            sb.add_group(self.getValue("input:aero_data:aerodat"))

        #-------------------
        # Namelist &RFHIN
        #-------------------

        # Namelist &RFHIN is only required if MYAERO=3.

        elif myaero == 3:

            sb.add_group('RFHIN')

            mmach = size(self.getValue("input:rfhin:tmach"))
            sb.add_comment("  ! Aerodynamic Data for Parabolic Drag Polars")
            sb.add_newvar("mmach", mmach)
            sb.add_container("input:rfhin")

            # If MYAERO=3, insert the aerodynamic data here.  Otherwise it may have already
            # been inserted above.

            # aerodat contains the raw aero data
            sb.add_group(self.getValue("input:aero_data:aerodat"))


        #-------------------
        # Namelist &ASCLIN
        #-------------------

        # Namelist &ASCLIN is only required if MYAERO=2.

        if myaero == 2:

            sb.add_group('ASCLIN')

            sb.add_comment("  ! Scaling Data for Lift Independent Drag")
            sb.add_var("input:asclin:sref")
            sb.add_var("input:asclin:tref")
            sb.add_var("input:asclin:awetn")
            sb.add_var("input:asclin:eltot")
            sb.add_var("input:asclin:voltot")

            if size(self.getValue("input:asclin:awett")) > 0:
                sb.add_var("input:asclin:awett")
            if size(self.getValue("input:asclin:awetw")) > 0:
                sb.add_var("input:asclin:awetw")
            if size(self.getValue("input:asclin:elw")) > 0:
                sb.add_var("input:asclin:elw")
            if size(self.getValue("input:asclin:volw")) > 0:
                sb.add_var("input:asclin:volw")
            if size(self.getValue("input:asclin:form")) > 0:
                sb.add_var("input:asclin:form")
            if size(self.getValue("input:asclin:eql")) > 0:
                sb.add_var("input:asclin:eql")

            ncdwav = size(self.getValue("input:asclin:cdwav"))
            if ncdwav > 0:
                sb.add_var("input:asclin:cdwav")
                sb.add_var("input:asclin:dcdnac")

        #-------------------
        # Namelist &TOLIN
        #-------------------

        if itakof == 1 or iland == 1 or nopro == 1:

            sb.add_group('TOLIN')

            sb.add_var("input:tolin:Basic:apa")
            sb.add_var("input:tolin:Basic:dtct")
            if self.getValue("input:tolin:Basic:swref") > 0:
                sb.add_var("input:tolin:Basic:swref")
            if self.getValue("input:tolin:Basic:arret") > 0:
                sb.add_var("input:tolin:Basic:arret")
            sb.add_var("input:tolin:Basic:whgt")
            sb.add_var("input:tolin:Basic:alprun")
            sb.add_var("input:tolin:Basic:tinc")
            sb.add_var("input:tolin:Basic:rollmu")
            sb.add_var("input:tolin:Basic:brakmu")
            sb.add_var("input:tolin:Basic:cdgear")
            sb.add_var("input:tolin:Basic:cdeout")
            sb.add_var("input:tolin:Basic:clspol")
            sb.add_var("input:tolin:Basic:cdspol")
            sb.add_var("input:tolin:Basic:incgef")
            sb.add_var("input:tolin:Basic:argef")
            sb.add_var("input:tolin:Basic:itime")

            sb.add_comment("\n  ! Thrust Reverser")
            sb.add_var("input:tolin:Thrust_Reverser:inthrv")
            sb.add_var("input:tolin:Thrust_Reverser:rvfact")
            if size(self.getValue("input:tolin:Thrust_Reverser:velrv")) > 0:
                sb.add_var("input:tolin:Thrust_Reverser:velrv")
                sb.add_var("input:tolin:Thrust_Reverser:thrrv")

            sb.add_var("input:tolin:Thrust_Reverser:tirvrs")
            sb.add_var("input:tolin:Thrust_Reverser:revcut")
            sb.add_var("input:tolin:Thrust_Reverser:clrev")
            sb.add_var("input:tolin:Thrust_Reverser:cdrev")

            sb.add_comment("\n  ! Integration Intervals  (Default values will provide a precision of +/-.25 ft)")
            sb.add_container("input:tolin:Integration_Intervals")

            sb.add_comment("\n  ! Takeoff Data")
            if self.getValue("input:tolin:Takeoff:cltom") > 0:
                sb.add_var("input:tolin:Takeoff:cltom")
            sb.add_var("input:tolin:Takeoff:cdmto")
            sb.add_var("input:tolin:Takeoff:fcdmto")
            sb.add_var("input:tolin:Takeoff:almxto")
            if self.getValue("input:tolin:Takeoff:obsto") > 0:
                sb.add_var("input:tolin:Takeoff:obsto")
            sb.add_var("input:tolin:Takeoff:alpto")
            sb.add_var("input:tolin:Takeoff:clto")
            sb.add_var("input:tolin:Takeoff:cdto")
            sb.add_var("input:tolin:Takeoff:inthto")

            if size(self.getValue("input:tolin:Takeoff:velto")) > 0:
                sb.add_var("input:tolin:Takeoff:velto")
                sb.add_var("input:tolin:Takeoff:thrto")
            if self.getValue("input:tolin:Takeoff:alprot") > -99:
                sb.add_var("input:tolin:Takeoff:alprot")

            sb.add_var("input:tolin:Takeoff:vrotat")
            sb.add_var("input:tolin:Takeoff:vangl")
            sb.add_var("input:tolin:Takeoff:thfact")
            sb.add_var("input:tolin:Takeoff:ftocl")
            sb.add_var("input:tolin:Takeoff:ftocd")
            sb.add_var("input:tolin:Takeoff:igobs")
            sb.add_var("input:tolin:Takeoff:tdelg")
            sb.add_var("input:tolin:Takeoff:tigear")
            sb.add_var("input:tolin:Takeoff:ibal")
            sb.add_var("input:tolin:Takeoff:itxout")

            sb.add_comment("\n  ! Aborted Takeoff Data")
            sb.add_var("input:tolin:Takeoff:pilott")
            sb.add_var("input:tolin:Takeoff:tispa")
            sb.add_var("input:tolin:Takeoff:tibra")
            sb.add_var("input:tolin:Takeoff:tirva")
            sb.add_var("input:tolin:Takeoff:ispol")
            sb.add_var("input:tolin:Takeoff:irev")

            sb.add_comment("\n  ! Landing Data")
            if self.getValue("input:tolin:Landing:clldm") > 0:
                sb.add_var("input:tolin:Landing:clldm")
            sb.add_var("input:tolin:Landing:cdmld")
            if self.getValue("input:tolin:Landing:fcdmld") > 0:
                sb.add_var("input:tolin:Landing:fcdmld")
            sb.add_var("input:tolin:Landing:almxld")
            sb.add_var("input:tolin:Landing:obsld")
            sb.add_var("input:tolin:Landing:alpld")
            sb.add_var("input:tolin:Landing:clld")
            sb.add_var("input:tolin:Landing:cdld")
            sb.add_var("input:tolin:Landing:inthld")
            if size(self.getValue("input:tolin:Landing:velld")) > 0:
                sb.add_var("input:tolin:Landing:velld")
                sb.add_var("input:tolin:Landing:thrld")

            sb.add_var("input:tolin:Landing:thrld")
            if self.getValue("input:tolin:Landing:thdry") > 0:
                sb.add_var("input:tolin:Landing:thdry")
            sb.add_var("input:tolin:Landing:aprhgt")
            sb.add_var("input:tolin:Landing:aprang")
            sb.add_var("input:tolin:Landing:fldcl")
            sb.add_var("input:tolin:Landing:fldcd")
            sb.add_var("input:tolin:Landing:tdsink")
            if self.getValue("input:tolin:Landing:vangld") > 0:
                sb.add_var("input:tolin:Landing:vangld")
            sb.add_var("input:tolin:Landing:noflar")
            sb.add_var("input:tolin:Landing:tispol")
            sb.add_var("input:tolin:Landing:ticut")
            sb.add_var("input:tolin:Landing:tibrak")
            sb.add_var("input:tolin:Landing:acclim")
            if self.getValue("input:tolin:Landing:magrup") > 0:
                sb.add_var("input:tolin:Landing:magrup")

        #-------------------
        # Namelist &PROIN
        #-------------------

        # Namelist &PROIN is only required if NOPRO=1.
        if nopro > 0:

            npol = size(self.getValue("input:proin:dflap"))

            sb.add_group('PROIN')
            sb.add_var("input:proin:npol")

            if npol > 0:
                sb.add_var("input:proin:alpro")
                sb.add_var("input:proin:clpro")
                sb.add_var("input:proin:cdpro")
                sb.add_var("input:proin:dflap")

            sb.add_var("input:proin:ntime")
            sb.add_var("input:proin:ipcmax")
            sb.add_var("input:proin:txf")
            sb.add_var("input:proin:alpmin")
            sb.add_var("input:proin:gamlim")

            inm = self.getValue("input:proin:inm")
            if inm == 1:
                sb.add_var("input:proin:inm")
                sb.add_var("input:proin:iatr")
                sb.add_var("input:proin:fzf")
                sb.add_var("input:proin:thclmb")
                sb.add_var("input:proin:flapid")

        #-------------------
        # Namelist &SEGIN
        #-------------------

        # One or more &SEGIN namelists may have been created by the user.
        #nseg = self.nseg
        if nopro > 0 and self.nseg0 > 0:

            for i in range(0, self.nseg0):

                key    = self.getValue("input:segin%s:key" % (i))
                nflap  = self.getValue("input:segin%s:nflap" % (i))
                ifix   = self.getValue("input:segin%s:ifix" % (i))
                engscl = self.getValue("input:segin%s:engscl" % (i))
                afix   = self.getValue("input:segin%s:afix" % (i))
                gfix   = self.getValue("input:segin%s:gfix" % (i))
                vfix   = self.getValue("input:segin%s:vfix" % (i))
                hstop  = self.getValue("input:segin%s:hstop" % (i))
                dstop  = self.getValue("input:segin%s:dstop" % (i))
                tstop  = self.getValue("input:segin%s:tstop" % (i))
                vstop  = self.getValue("input:segin%s:vstop" % (i))
                hmin   = self.getValue("input:segin%s:hmin" % (i))
                sprate = self.getValue("input:segin%s:sprate" % (i))
                iplr   = self.getValue("input:segin%s:iplr" % (i))
                delt   = self.getValue("input:segin%s:delt" % (i))
                grdaeo = self.getValue("input:segin%s:grdaeo" % (i))
                grdoeo = self.getValue("input:segin%s:grdoeo" % (i))

                sb.add_group('SEGIN')
                sb.add_newvar("key", key)

                if nflap > 0:
                    sb.add_newvar("nflap", nflap)
                if ifix > 0:
                    sb.add_newvar("ifix", ifix)
                if engscl >= 0.:
                    sb.add_newvar("engscl", engscl)
                if afix > -10.:
                    sb.add_newvar("afix", afix)
                if gfix > -10.:
                    sb.add_newvar("gfix", gfix)
                if vfix > 0.:
                    sb.add_newvar("vfix", vfix)
                if hstop > 0.:
                    sb.add_newvar("hstop", hstop)
                if dstop > 0.:
                    sb.add_newvar("dstop", dstop)
                if tstop > 0.:
                    sb.add_newvar("tstop", tstop)
                if vstop > 0.:
                    sb.add_newvar("vstop", vstop)
                if hmin > 0.:
                    sb.add_newvar("hmin", hmin)
                if sprate >= 0.:
                    sb.add_newvar("sprate", sprate)
                if iplr >= 0.:
                    sb.add_newvar("iplr", iplr)
                if delt > 0.:
                    sb.add_newvar("delt", delt)
                if grdaeo > -1.:
                    sb.add_newvar("grdaeo", grdaeo)
                if grdoeo > -1.:
                    sb.add_newvar("grdoeo", grdoeo)

        #-------------------
        # Namelist &NOISIN
        #-------------------

        # Namelist &NOISIN is only required if NOISIN=1.
        if noise == 1:

            sb.add_group('NOISIN')

            sb.add_comment("\n  ! Data for Noise Calculations\n  ! Noise regulation control")
            sb.add_var("input:noisin:Basic:iepn")
            sb.add_var("input:noisin:Basic:depnt")
            sb.add_var("input:noisin:Basic:depns")
            sb.add_var("input:noisin:Basic:depnl")
            sb.add_var("input:noisin:Basic:itrade")

            sb.add_comment("\n  ! Noise sources to be included")
            ijet = self.getValue("input:noisin:Basic:ijet")
            ifan = self.getValue("input:noisin:Basic:ifan")
            icore = self.getValue("input:noisin:Basic:icore")
            iturb = self.getValue("input:noisin:Basic:iturb")
            iprop = self.getValue("input:noisin:Basic:iprop")
            iflap = self.getValue("input:noisin:Basic:iflap")
            iairf = self.getValue("input:noisin:Basic:iairf")
            igear = self.getValue("input:noisin:Basic:igear")
            ishld = self.getValue("input:noisin:Propagation:ishld")
            ignd = self.getValue("input:noisin:Propagation:ignd")
            if ijet > 0:
                sb.add_newvar("ijet", ijet)
            if ifan > 0:
                sb.add_newvar("ifan", ifan)
            if icore > 0:
                sb.add_newvar("icore", icore)
            if iturb > 0:
                sb.add_newvar("iturb", iturb)
            if iprop > 0:
                sb.add_newvar("iprop", iprop)
            if iflap > 0:
                sb.add_newvar("iflap", iflap)
            if iairf > 0:
                sb.add_newvar("iairf", iairf)
            if igear > 0:
                sb.add_newvar("igear", igear)

            sb.add_comment("\n  ! Noise Propagation Corrections")
            sb.add_var("input:noisin:Propagation:isupp")
            sb.add_var("input:noisin:Propagation:idop")
            sb.add_newvar("ignd", ignd)
            sb.add_var("input:noisin:Propagation:iatm")
            sb.add_var("input:noisin:Propagation:iega")
            sb.add_newvar("ishld", ishld)
            sb.add_var("input:noisin:Propagation:deldb")
            sb.add_var("input:noisin:Propagation:heng")
            sb.add_var("input:noisin:Propagation:filbw")
            sb.add_var("input:noisin:Propagation:tdi")
            sb.add_var("input:noisin:Propagation:rh")

            sb.add_comment("\n  ! Observer Locations")
            nob = size(self.getValue("input:noisin:Observers:xo"))
            if nob > 0:
                sb.add_newvar("nob", nob)
                sb.add_var("input:noisin:Observers:xo")
                sb.add_var("input:noisin:Observers:yo")

            sb.add_var("input:noisin:Observers:zo")
            sb.add_var("input:noisin:Observers:ndprt")
            sb.add_var("input:noisin:Observers:ifoot")
            sb.add_var("input:noisin:Observers:igeom")
            if self.getValue("input:noisin:Observers:thrn") > 0:
                sb.add_var("input:noisin:Observers:thrn")

            sb.add_var("input:noisin:Observers:icorr")
            sb.add_var("input:noisin:Observers:tcorxp")

            nparam = size(self.getValue("input:noisin:Engine_Parameters:aepp"))
            if nparam > 0:
                sb.add_comment("\n  ! Engine Noise Parameters")
                sb.add_newvar("nparam", nparam)
                sb.add_container("input:noisin:Engine_Parameters")

            if ijet != 0:
                sb.add_comment("\n  ! Jet Noise Input Data")
                sb.add_var("input:noisin:Jet:inoz")
                sb.add_var("input:noisin:Jet:iplug")
                sb.add_var("input:noisin:Jet:islot")
                sb.add_var("input:noisin:Jet:iaz")
                sb.add_var("input:noisin:Jet:dbaz")
                sb.add_var("input:noisin:Jet:ejdop")
                sb.add_var("input:noisin:Jet:zmdc")
                sb.add_var("input:noisin:Jet:gammac")
                sb.add_var("input:noisin:Jet:gasrc")
                sb.add_var("input:noisin:Jet:annht")
                sb.add_var("input:noisin:Jet:zmdf")
                sb.add_var("input:noisin:Jet:gammap")
                sb.add_var("input:noisin:Jet:gasrf")
                sb.add_var("input:noisin:Jet:annhtf")
                if self.getValue("input:noisin:Jet:dhc") > 0:
                    sb.add_var("input:noisin:Jet:dhc")
                sb.add_var("input:noisin:Jet:dhf")
                sb.add_var("input:noisin:Jet:zl2")
                sb.add_var("input:noisin:Jet:ifwd")
                sb.add_var("input:noisin:Jet:ishock")
                sb.add_var("input:noisin:Jet:zjsupp")

            if ijet == 5:
                sb.add_comment("\n  ! Jet Noise Input Data for MSjet")
                sb.add_container("input:noisin:MSJet")

            if ifan > 0:
                sb.add_comment("\n  ! Fan Noise Data")
                sb.add_var("input:noisin:Fan:igv")
                sb.add_var("input:noisin:Fan:ifd")
                sb.add_var("input:noisin:Fan:iexh")
                sb.add_var("input:noisin:Fan:nfh")

                if self.getValue("input:noisin:Fan:nstg") > 0:
                    sb.add_var("input:noisin:Fan:nstg")

                sb.add_var("input:noisin:Fan:suppin")
                sb.add_var("input:noisin:Fan:suppex")
                sb.add_var("input:noisin:Fan:methtip")
                sb.add_var("input:noisin:Fan:icomb")
                sb.add_var("input:noisin:Fan:decmpt")
                sb.add_var("input:noisin:Fan:gammaf")

                if self.getValue("input:noisin:Fan:nbl") > 0:
                    sb.add_var("input:noisin:Fan:nbl")
                if self.getValue("input:noisin:Fan:nvan") > 0:
                    sb.add_var("input:noisin:Fan:nvan")
                if self.getValue("input:noisin:Fan:fandia") > 0:
                    sb.add_var("input:noisin:Fan:fandia")
                if self.getValue("input:noisin:Fan:fanhub") > 0:
                    sb.add_var("input:noisin:Fan:fanhub")
                if self.getValue("input:noisin:Fan:tipmd") > 0:
                    sb.add_var("input:noisin:Fan:tipmd")

                sb.add_var("input:noisin:Fan:rss")
                sb.add_var("input:noisin:Fan:efdop")
                sb.add_var("input:noisin:Fan:faneff")

                if self.getValue("input:noisin:Fan:nbl2") > 0:
                    sb.add_var("input:noisin:Fan:nbl2")
                if self.getValue("input:noisin:Fan:nvan2") > 0:
                    sb.add_var("input:noisin:Fan:nvan2")
                if self.getValue("input:noisin:Fan:fand2") > 0:
                    sb.add_var("input:noisin:Fan:fand2")
                if self.getValue("input:noisin:Fan:tipmd2") > 0:
                    sb.add_var("input:noisin:Fan:tipmd2")

                sb.add_var("input:noisin:Fan:rss2")
                sb.add_var("input:noisin:Fan:efdop2")
                sb.add_var("input:noisin:Fan:fanef2")

                if self.getValue("input:noisin:Fan:trat") > 0:
                    sb.add_var("input:noisin:Fan:trat")
                if igenen not in [1, -2] and self.getValue("input:noisin:Fan:prat") > 0:
                    sb.add_var("input:noisin:Fan:prat")

            if icore > 0:
                sb.add_comment("\n  ! Core Noise Data")
                sb.add_var("input:noisin:Core:csupp")
                sb.add_var("input:noisin:Core:gamma")
                sb.add_var("input:noisin:Core:imod")
                if self.getValue("input:noisin:Core:dtemd") > 0:
                    sb.add_var("input:noisin:Core:dtemd")
                sb.add_var("input:noisin:Core:ecdop")

            if iturb > 0:
                sb.add_comment("\n  ! Core Noise Data")
                sb.add_var("input:noisin:Turbine:tsupp")
                if self.getValue("input:noisin:Turbine:tbndia") > 0:
                    sb.add_var("input:noisin:Turbine:tbndia")
                sb.add_var("input:noisin:Turbine:gear")
                sb.add_var("input:noisin:Turbine:cs")
                if self.getValue("input:noisin:Turbine:nblr") > 0:
                    sb.add_var("input:noisin:Turbine:nblr")
                sb.add_var("input:noisin:Turbine:ityptb")
                sb.add_var("input:noisin:Turbine:etdop")

            if iprop > 0:
                sb.add_comment("\n  ! Propeller Noise Data")
                sb.add_container("input:noisin:Propeller")

            if ishld > 0:
                sb.add_comment("\n  ! Shielding Effects Data")
                sb.add_container("input:noisin:Shielding")

            if iflap > 0:
                sb.add_comment("\n  ! Flap Noise Data")
                sb.add_container("input:noisin:Flap_Noise")

            if iairf > 0:
                sb.add_comment("\n  ! Flap Noise Data")
                sb.add_container("input:noisin:Airframe")

            if ignd > 0:
                sb.add_comment("\n  ! Ground Reflection Effects Data")
                sb.add_var("input:noisin:Ground_Effects:itone")

                nht = size(self.getValue("input:noisin:Ground_Effects:dk"))
                if nht > 0:
                    sb.add_newvar("nht", nht)
                    sb.add_var("input:noisin:Ground_Effects:dk")

        #-------------------
        # Namelist &SYNTIN
        #-------------------

        # Namelist &SYNTIN is only required if IOPT=3.
        if iopt == 3:

            sb.add_group('SYNTIN')

            if self.getValue("input:syntin:Variables:desrng") > 0:
                sb.add_var("input:syntin:Variables:desrng")
            if self.getValue("input:syntin:Variables:vappr") > 0:
                sb.add_var("input:syntin:Variables:vappr")
            if self.getValue("input:syntin:Variables:flto") > 0:
                sb.add_var("input:syntin:Variables:flto")
            if self.getValue("input:syntin:Variables:flldg")> 0:
                sb.add_var("input:syntin:Variables:flldg")
            

            sb.add_var("input:syntin:Variables:exfcap")
            if igenen == 1:
                if self.getValue("input:syntin:Variables:cdtmax") > 0:
                    sb.add_var("input:syntin:Variables:cdtmax")
                if self.getValue("input:syntin:Variables:cdpmax") > 0:
                    sb.add_var("input:syntin:Variables:cdpmax")
                if self.getValue("input:syntin:Variables:vjmax") > 0:
                    sb.add_var("input:syntin:Variables:vjmax")
                if self.getValue("input:syntin:Variables:stmin") > 0:
                    sb.add_var("input:syntin:Variables:stmin")
                if self.getValue("input:syntin:Variables:armax") > 0:
                    sb.add_var("input:syntin:Variables:armax")

            sb.add_var("input:syntin:Variables:gnox")
            sb.add_var("input:syntin:Variables:roclim")
            sb.add_var("input:syntin:Variables:dhdtlm")
            sb.add_var("input:syntin:Variables:tmglim")
            sb.add_var("input:syntin:Variables:ig")
            sb.add_var("input:syntin:Variables:ibfgs")
            sb.add_var("input:syntin:Variables:itfine")

            sb.add_comment("\n  ! Optimization Control")
            sb.add_var("input:syntin:Optimization_Control:ndd")
            sb.add_var("input:syntin:Optimization_Control:rk")
            sb.add_var("input:syntin:Optimization_Control:fdd")

            if self.getValue("input:syntin:Optimization_Control:nlin") > 0:
                sb.add_var("input:syntin:Optimization_Control:nlin")

            sb.add_var("input:syntin:Optimization_Control:nstep")
            sb.add_var("input:syntin:Optimization_Control:ef")
            sb.add_var("input:syntin:Optimization_Control:eps")
            sb.add_var("input:syntin:Optimization_Control:amult")
            sb.add_var("input:syntin:Optimization_Control:dep")
            sb.add_var("input:syntin:Optimization_Control:accux")
            sb.add_var("input:syntin:Optimization_Control:glm")

            if size(self.getValue("input:syntin:Optimization_Control:gfact")) > 0:
                sb.add_var("input:syntin:Optimization_Control:gfact")

            sb.add_var("input:syntin:Optimization_Control:autscl")
            sb.add_var("input:syntin:Optimization_Control:icent")
            sb.add_var("input:syntin:Optimization_Control:rhomin")
            sb.add_var("input:syntin:Optimization_Control:rhomax")
            sb.add_var("input:syntin:Optimization_Control:rhodel")
            sb.add_var("input:syntin:Optimization_Control:itmax")
            sb.add_var("input:syntin:Optimization_Control:jprnt")
            sb.add_var("input:syntin:Optimization_Control:rdfun")
            sb.add_var("input:syntin:Optimization_Control:adfun")

        #-------------------
        # Namelist &RERUN
        #-------------------

        # One or more &RERUN namelists may have been created by the user.

        #nrerun = self.nrerun
        if self.nrern0 > 0:

            for i in range(0, self.nrern0):

                sb.add_group('RERUN')

                re_desrng = self.getValue("input:rerun%s:desrng" % (i))
                re_mywts  = self.getValue("input:rerun%s:mywts" % (i))
                re_rampwt = self.getValue("input:rerun%s:rampwt" % (i))
                re_dowe   = self.getValue("input:rerun%s:dowe" % (i))
                re_paylod = self.getValue("input:rerun%s:paylod" % (i))
                re_fuemax = self.getValue("input:rerun%s:fuemax" % (i))
                re_itakof = self.getValue("input:rerun%s:itakof" % (i))
                re_iland  = self.getValue("input:rerun%s:iland" % (i))
                re_nopro  = self.getValue("input:rerun%s:nopro" % (i))
                re_noise  = self.getValue("input:rerun%s:noise" % (i))
                re_icost  = self.getValue("input:rerun%s:icost" % (i))
                re_wsr    = self.getValue("input:rerun%s:wsr" % (i))
                re_twr    = self.getValue("input:rerun%s:twr" % (i))
                re_iplrng = self.getValue("input:rerun%s:iplrng" %(i))

                if re_desrng > 0.:
                    sb.add_var("input:rerun%s:desrng" % (i))
                if re_mywts >= 0:
                    sb.add_var("input:rerun%s:mywts" % (i))
                if re_rampwt >= 0.:
                    sb.add_var("input:rerun%s:rampwt" % (i))
                if re_dowe > 0.:
                    sb.add_var("input:rerun%s:dowe" % (i))
                if re_paylod > 0.:
                    sb.add_var("input:rerun%s:paylod" % (i))
                if re_fuemax > 0.:
                    sb.add_var("input:rerun%s:fuemax" % (i))
                if re_itakof == 0:
                    sb.add_var("input:rerun%s:itakof" % (i))
                if re_iland == 0:
                    sb.add_var("input:rerun%s:iland" % (i))
                if re_nopro == 0:
                    sb.add_var("input:rerun%s:nopro" % (i))
                if re_noise == 0:
                    sb.add_var("input:rerun%s:noise" % (i))
                if re_icost == 0:
                    sb.add_var("input:rerun%s:icost" % (i))
                if re_wsr == 0.:
                    sb.add_var("input:rerun%s:wsr" % (i))
                if re_twr == 0.:
                    sb.add_var("input:rerun%s:twr" % (i))
                if re_iplrng > -999:
                    sb.add_var("input:rerun%s:iplrng" %(i))

                re_indr   = self.getValue("input:rerun%s:missin:Basic:indr" % (i))
                re_fact   = self.getValue("input:rerun%s:missin:Basic:fact" % (i))
                re_fleak  = self.getValue("input:rerun%s:missin:Basic:fleak" % (i))
                re_fcdo   = self.getValue("input:rerun%s:missin:Basic:fcdo" % (i))
                re_fcdi   = self.getValue("input:rerun%s:missin:Basic:fcdi" % (i))
                re_fcdsub = self.getValue("input:rerun%s:missin:Basic:fcdsub" % (i))
                re_fcdsup = self.getValue("input:rerun%s:missin:Basic:fcdsup" % (i))
                re_iskal  = self.getValue("input:rerun%s:missin:Basic:iskal" % (i))
                re_owfact = self.getValue("input:rerun%s:missin:Basic:owfact" % (i))
                re_iflag  = self.getValue("input:rerun%s:missin:Basic:iflag" % (i))
                re_msumpt = self.getValue("input:rerun%s:missin:Basic:msumpt" % (i))
                re_dtc    = self.getValue("input:rerun%s:missin:Basic:dtc" % (i))
                re_irw    = self.getValue("input:rerun%s:missin:Basic:irw" % (i))
                re_rtol   = self.getValue("input:rerun%s:missin:Basic:rtol" % (i))
                re_nhold  = self.getValue("input:rerun%s:missin:Basic:nhold" % (i))
                re_iata   = self.getValue("input:rerun%s:missin:Basic:iata" % (i))
                re_tlwind = self.getValue("input:rerun%s:missin:Basic:tlwind" % (i))

                sb.add_group('MISSIN')

                if re_indr != -999:
                    sb.add_var("input:rerun%s:missin:Basic:indr" % (i))
                if re_fact != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fact" % (i))
                if re_fleak != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fleak" % (i))
                if re_fcdo != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fcdo" % (i))
                if re_fcdi != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fcdi" % (i))
                if re_fcdsub != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fcdsub" % (i))
                if re_fcdsup != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:fcdsup" % (i))
                if re_iskal != -999:
                    sb.add_var("input:rerun%s:missin:Basic:iskal" % (i))
                if re_owfact != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:owfact" % (i))
                if re_iflag != -999:
                    sb.add_var("input:rerun%s:missin:Basic:iflag" % (i))
                if re_msumpt != -999:
                    sb.add_var("input:rerun%s:missin:Basic:msumpt" % (i))
                if re_dtc != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:dtc" % (i))
                if re_irw != -999:
                    sb.add_var("input:rerun%s:missin:Basic:irw" % (i))
                if re_rtol != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:rtol" % (i))
                if re_nhold != -999:
                    sb.add_var("input:rerun%s:missin:Basic:nhold" % (i))
                if re_iata != -999:
                    sb.add_var("input:rerun%s:missin:Basic:iata" % (i))
                if re_tlwind != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:tlwind" % (i))

                re_dwt    = self.getValue("input:rerun%s:missin:Basic:dwt" % (i))
                re_offdr  = self.getValue("input:rerun%s:missin:Basic:offdr" % (i))
                re_idoq   = self.getValue("input:rerun%s:missin:Basic:idoq" % (i))
                re_nsout  = self.getValue("input:rerun%s:missin:Basic:nsout" % (i))
                re_nsadj  = self.getValue("input:rerun%s:missin:Basic:nsadj" % (i))
                re_mirror = self.getValue("input:rerun%s:missin:Basic:mirror" % (i))
                re_stma   = self.getValue("input:rerun%s:missin:Store_Drag:stma" % (i))
                re_cdst   = self.getValue("input:rerun%s:missin:Store_Drag:cdst" % (i))
                re_istcl  = self.getValue("input:rerun%s:missin:Store_Drag:istcl" % (i))
                re_istcr  = self.getValue("input:rerun%s:missin:Store_Drag:istcr" % (i))
                re_istde  = self.getValue("input:rerun%s:missin:Store_Drag:istde" % (i))
                re_mywts  = self.getValue("input:rerun%s:missin:User_Weights:mywts" % (i))
                re_rampwt = self.getValue("input:rerun%s:missin:User_Weights:rampwt" % (i))
                re_dowe   = self.getValue("input:rerun%s:missin:User_Weights:dowe" % (i))
                re_paylod = self.getValue("input:rerun%s:missin:User_Weights:paylod" % (i))
                re_fuemax = self.getValue("input:rerun%s:missin:User_Weights:fuemax" % (i))
                re_takotm = self.getValue("input:rerun%s:missin:Ground_Operations:takotm" % (i))
                re_taxotm = self.getValue("input:rerun%s:missin:Ground_Operations:taxotm" % (i))
                re_apprtm = self.getValue("input:rerun%s:missin:Ground_Operations:apprtm" % (i))
                re_appfff = self.getValue("input:rerun%s:missin:Ground_Operations:appfff" % (i))
                re_taxitm = self.getValue("input:rerun%s:missin:Ground_Operations:taxitm" % (i))
                re_ittff  = self.getValue("input:rerun%s:missin:Ground_Operations:ittff" % (i))
                re_takoff = self.getValue("input:rerun%s:missin:Ground_Operations:takoff" % (i))
                re_txfufl = self.getValue("input:rerun%s:missin:Ground_Operations:txfufl" % (i))
                re_ftkofl = self.getValue("input:rerun%s:missin:Ground_Operations:ftkofl" % (i))
                re_ftxofl = self.getValue("input:rerun%s:missin:Ground_Operations:ftxofl" % (i))
                re_ftxifl = self.getValue("input:rerun%s:missin:Ground_Operations:ftxifl" % (i))
                re_faprfl = self.getValue("input:rerun%s:missin:Ground_Operations:faprfl" % (i))
                re_xnz    = self.getValue("input:rerun%s:missin:Turn_Segments:xnz" % (i))
                re_xcl    = self.getValue("input:rerun%s:missin:Turn_Segments:xcl" % (i))
                re_xmach  = self.getValue("input:rerun%s:missin:Turn_Segments:xmach" % (i))
                re_nclimb = self.getValue("input:rerun%s:missin:Climb:nclimb" % (i))
                re_clmmin = self.getValue("input:rerun%s:missin:Climb:clmmin" % (i))
                re_clmmax = self.getValue("input:rerun%s:missin:Climb:clmmax" % (i))
                re_clamin = self.getValue("input:rerun%s:missin:Climb:clamin" % (i))
                re_clamax = self.getValue("input:rerun%s:missin:Climb:clamax" % (i))
                re_nincl  = self.getValue("input:rerun%s:missin:Climb:nincl" % (i))
                re_fwf    = self.getValue("input:rerun%s:missin:Climb:fwf" % (i))
                re_ncrcl  = self.getValue("input:rerun%s:missin:Climb:ncrcl" % (i))
                re_cldcd  = self.getValue("input:rerun%s:missin:Climb:cldcd" % (i))
                re_ippcl  = self.getValue("input:rerun%s:missin:Climb:ippcl" % (i))
                re_maxcl  = self.getValue("input:rerun%s:missin:Climb:maxcl" % (i))
                re_no     = self.getValue("input:rerun%s:missin:Climb:no" % (i))
                re_keasvc = self.getValue("input:rerun%s:missin:Climb:keasvc" % (i))
                re_actab  = self.getValue("input:rerun%s:missin:Climb:actab" % (i))
                re_vctab  = self.getValue("input:rerun%s:missin:Climb:vctab" % (i))
                re_ifaacl = self.getValue("input:rerun%s:missin:Climb:ifaacl" % (i))
                re_ifaade = self.getValue("input:rerun%s:missin:Climb:ifaade" % (i))
                re_nodive = self.getValue("input:rerun%s:missin:Climb:nodive" % (i))
                re_divlim = self.getValue("input:rerun%s:missin:Climb:divlim" % (i))
                re_qlim   = self.getValue("input:rerun%s:missin:Climb:qlim" % (i))
                re_spdlim = self.getValue("input:rerun%s:missin:Climb:spdlim" % (i))
                re_qlalt  = self.getValue("input:rerun%s:missin:Climb:qlalt" % (i))
                re_vqlm   = self.getValue("input:rerun%s:missin:Climb:vqlm" % (i))
                re_ioc    = self.getValue("input:rerun%s:missin:Cruise:ioc" % (i))
                re_crmach = self.getValue("input:rerun%s:missin:Cruise:crmach" % (i))
                re_cralt  = self.getValue("input:rerun%s:missin:Cruise:cralt" % (i))
                re_crdcd  = self.getValue("input:rerun%s:missin:Cruise:crdcd" % (i))
                re_flrcr  = self.getValue("input:rerun%s:missin:Cruise:flrcr" % (i))
                re_crmmin = self.getValue("input:rerun%s:missin:Cruise:crmmin" % (i))
                re_crclmx = self.getValue("input:rerun%s:missin:Cruise:crclmx" % (i))
                re_hpmin  = self.getValue("input:rerun%s:missin:Cruise:hpmin" % (i))
                re_ffuel  = self.getValue("input:rerun%s:missin:Cruise:ffuel" % (i))
                re_fnox   = self.getValue("input:rerun%s:missin:Cruise:fnox" % (i))
                re_ifeath = self.getValue("input:rerun%s:missin:Cruise:ifeath" % (i))
                re_feathf = self.getValue("input:rerun%s:missin:Cruise:feathf" % (i))
                re_cdfeth = self.getValue("input:rerun%s:missin:Cruise:cdfeth" % (i))
                re_dcwt   = self.getValue("input:rerun%s:missin:Cruise:dcwt" % (i))
                re_rcin   = self.getValue("input:rerun%s:missin:Cruise:rcin" % (i))
                re_wtbm   = self.getValue("input:rerun%s:missin:Cruise:wtbm" % (i))
                re_altbm  = self.getValue("input:rerun%s:missin:Cruise:altbm" % (i))
                re_ivs    = self.getValue("input:rerun%s:missin:Descent:ivs" % (i))
                re_decl   = self.getValue("input:rerun%s:missin:Descent:decl" % (i))
                re_demmin = self.getValue("input:rerun%s:missin:Descent:demmin" % (i))
                re_demmax = self.getValue("input:rerun%s:missin:Descent:demmax" % (i))
                re_deamin = self.getValue("input:rerun%s:missin:Descent:deamin" % (i))
                re_deamax = self.getValue("input:rerun%s:missin:Descent:deamax" % (i))
                re_ninde  = self.getValue("input:rerun%s:missin:Descent:ninde" % (i))
                re_dedcd  = self.getValue("input:rerun%s:missin:Descent:dedcd" % (i))
                re_rdlim  = self.getValue("input:rerun%s:missin:Descent:rdlim" % (i))
                re_ns     = self.getValue("input:rerun%s:missin:Descent:ns" % (i))
                re_irs    = self.getValue("input:rerun%s:missin:Reserve:irs" % (i))
                re_resrfu = self.getValue("input:rerun%s:missin:Reserve:resrfu" % (i))
                re_restrp = self.getValue("input:rerun%s:missin:Reserve:restrp" % (i))
                re_timmap = self.getValue("input:rerun%s:missin:Reserve:timmap" % (i))
                re_altran = self.getValue("input:rerun%s:missin:Reserve:altran" % (i))
                re_nclres = self.getValue("input:rerun%s:missin:Reserve:nclres" % (i))
                re_ncrres = self.getValue("input:rerun%s:missin:Reserve:ncrres" % (i))
                re_sremch = self.getValue("input:rerun%s:missin:Reserve:sremch" % (i))
                re_eremch = self.getValue("input:rerun%s:missin:Reserve:eremch" % (i))
                re_srealt = self.getValue("input:rerun%s:missin:Reserve:srealt" % (i))
                re_erealt = self.getValue("input:rerun%s:missin:Reserve:erealt" % (i))
                re_holdtm = self.getValue("input:rerun%s:missin:Reserve:holdtm" % (i))
                re_ncrhol = self.getValue("input:rerun%s:missin:Reserve:ncrhol" % (i))
                re_ihopos = self.getValue("input:rerun%s:missin:Reserve:ihopos" % (i))
                re_icron  = self.getValue("input:rerun%s:missin:Reserve:icron" % (i))
                re_thold  = self.getValue("input:rerun%s:missin:Reserve:thold" % (i))
                re_ncrth  = self.getValue("input:rerun%s:missin:Reserve:ncrth" % (i))

                if re_dwt != -999.:
                    sb.add_var("input:rerun%s:missin:Basic:dwt" % (i))
                if size(re_offdr) > 0:
                    sb.add_var("input:rerun%s:missin:Basic:offdr" % (i))
                if re_idoq != -999:
                    sb.add_var("input:rerun%s:missin:Basic:idoq" % (i))
                if re_nsout != -999:
                    sb.add_var("input:rerun%s:missin:Basic:nsout" % (i))
                if re_nsadj != -999:
                    sb.add_var("input:rerun%s:missin:Basic:nsadj" % (i))
                if re_mirror != -999:
                    sb.add_var("input:rerun%s:missin:Basic:mirror" % (i))
                if size(re_stma) > 0:
                    sb.add_var("input:rerun%s:missin:Store_Drag:stma" % (i))
                if size(re_cdst) > 0:
                    sb.add_var("input:rerun%s:missin:Store_Drag:cdst" % (i))
                if size(re_istcl) > 0:
                    sb.add_var("input:rerun%s:missin:Store_Drag:istcl" % (i))
                if size(re_istcr) > 0:
                    sb.add_var("input:rerun%s:missin:Store_Drag:istcr" % (i))
                if re_istde != -999:
                    sb.add_var("input:rerun%s:missin:Store_Drag:istde" % (i))
                if re_mywts != -999:
                    sb.add_var("input:rerun%s:missin:User_Weights:mywts" % (i))
                if re_rampwt != -999.:
                    sb.add_var("input:rerun%s:missin:User_Weights:rampwt" % (i))
                if re_dowe != -999.:
                    sb.add_var("input:rerun%s:missin:User_Weights:dowe" % (i))
                if re_paylod != -999.:
                    sb.add_var("input:rerun%s:missin:User_Weights:paylod" % (i))
                if re_fuemax != -999.:
                    sb.add_var("input:rerun%s:missin:User_Weights:fuemax" % (i))
                if re_takotm != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:takotm" % (i))
                if re_taxotm != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:taxotm" % (i))
                if re_apprtm != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:apprtm" % (i))
                if re_appfff != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:appfff" % (i))
                if re_taxitm != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:taxitm" % (i))
                if re_ittff != -999:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:ittff" % (i))
                if re_takoff != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:takoff" % (i))
                if re_txfufl != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:txfufl" % (i))
                if re_ftkofl != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:ftkofl" % (i))
                if re_ftxofl != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:ftxofl" % (i))
                if re_ftxifl != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:ftxifl" % (i))
                if re_faprfl != -999.:
                    sb.add_var("input:rerun%s:missin:Ground_Operations:faprfl" % (i))
                if size(re_xnz) > 0:
                    sb.add_var("input:rerun%s:missin:Turn_Segments:xnz" % (i))
                if size(re_xcl) > 0:
                    sb.add_var("input:rerun%s:missin:Turn_Segments:xcl" % (i))
                if size(re_xmach) > 0:
                    sb.add_var("input:rerun%s:missin:Turn_Segments:xmach" % (i))
                if re_nclimb > 0:
                    sb.add_var("input:rerun%s:missin:Climb:nclimb" % (i))
                if size(re_clmmin) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:clmmin" % (i))
                if size(re_clmmax) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:clmmax" % (i))
                if size(re_clamin) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:clamin" % (i))
                if size(re_clamax) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:clamax" % (i))
                if size(re_nincl) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:nincl" % (i))
                if size(re_fwf) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:fwf" % (i))
                if size(re_ncrcl) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:ncrcl" % (i))
                if size(re_cldcd) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:cldcd" % (i))
                if size(re_ippcl) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:ippcl" % (i))
                if size(re_maxcl) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:maxcl" % (i))
                if size(re_no) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:no" % (i))
                if re_keasvc != -999:
                    sb.add_var("input:rerun%s:missin:Climb:keasvc" % (i))
                if size(re_actab) > 0:
                    sb.add_var2d("input:rerun%s:missin:Climb:actab" % (i))
                if size(re_vctab) > 0:
                    sb.add_var2d("input:rerun%s:missin:Climb:vctab" % (i))
                if re_ifaacl != -999:
                    sb.add_var("input:rerun%s:missin:Climb:ifaacl" % (i))
                if re_ifaade != -999:
                    sb.add_var("input:rerun%s:missin:Climb:ifaade" % (i))
                if re_nodive != -999:
                    sb.add_var("input:rerun%s:missin:Climb:nodive" % (i))
                if re_divlim != -999.:
                    sb.add_var("input:rerun%s:missin:Climb:divlim" % (i))
                if re_qlim != -999.:
                    sb.add_var("input:rerun%s:missin:Climb:qlim" % (i))
                if re_spdlim != -999.:
                    sb.add_var("input:rerun%s:missin:Climb:spdlim" % (i))
                if size(re_qlalt) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:qlalt" % (i))
                if size(re_vqlm) > 0:
                    sb.add_var("input:rerun%s:missin:Climb:vqlm" % (i))
                if size(re_ioc) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:ioc" % (i))
                if size(re_crmach) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:crmach" % (i))
                if size(re_cralt) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:cralt" % (i))
                if size(re_crdcd) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:crdcd" % (i))
                if size(re_flrcr) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:flrcr" % (i))
                if size(re_crmmin) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:crmmin" % (i))
                if size(re_crclmx) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:crclmx" % (i))
                if size(re_hpmin) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:hpmin" % (i))
                if size(re_ffuel) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:ffuel" % (i))
                if size(re_fnox) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:fnox" % (i))
                if size(re_ifeath) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:ifeath" % (i))
                if size(re_feathf) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:feathf" % (i))
                if size(re_cdfeth) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:cdfeth" % (i))
                if re_dcwt != -999.:
                    sb.add_var("input:rerun%s:missin:Cruise:dcwt" % (i))
                if re_rcin != -999.:
                    sb.add_var("input:rerun%s:missin:Cruise:rcin" % (i))
                if size(re_wtbm) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:wtbm" % (i))
                if size(re_altbm) > 0:
                    sb.add_var("input:rerun%s:missin:Cruise:altbm" % (i))
                if re_ivs != -999:
                    sb.add_var("input:rerun%s:missin:Descent:ivs" % (i))
                if re_decl != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:decl" % (i))
                if re_demmin != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:demmin" % (i))
                if re_demmax != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:demmax" % (i))
                if re_deamin != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:deamin" % (i))
                if re_deamax != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:deamax" % (i))
                if re_ninde != -999:
                    sb.add_var("input:rerun%s:missin:Descent:ninde" % (i))
                if re_dedcd != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:dedcd" % (i))
                if re_rdlim != -999.:
                    sb.add_var("input:rerun%s:missin:Descent:rdlim" % (i))

                ns = size(self.getValue("input:rerun%s:missin:Descent:adtab" % (i)))
                if  ns > 0:
                    sb.add_comment("\n  ! Input Descent Schedule\n")
                    sb.add_newvar('ns', ns)
                    sb.add_var("input:rerun%s:missin:Descent:keasvd" % (i))
                    sb.add_var("input:rerun%s:missin:Descent:adtab" % (i))
                    sb.add_var("input:rerun%s:missin:Descent:vdtab" % (i))

                if re_irs != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:irs" % (i))
                if re_resrfu != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:resrfu" % (i))
                if re_restrp != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:restrp" % (i))
                if re_timmap != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:timmap" % (i))
                if re_altran != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:altran" % (i))
                if re_nclres != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:nclres" % (i))
                if re_ncrres != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:ncrres" % (i))
                if re_sremch != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:sremch" % (i))
                if re_eremch != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:eremch" % (i))
                if re_srealt != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:srealt" % (i))
                if re_erealt != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:erealt" % (i))
                if re_holdtm != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:holdtm" % (i))
                if re_ncrhol != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:ncrhol" % (i))
                if re_ihopos != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:ihopos" % (i))
                if re_icron != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:icron" % (i))
                if re_thold != -999.:
                    sb.add_var("input:rerun%s:missin:Reserve:thold" % (i))
                if re_ncrth != -999:
                    sb.add_var("input:rerun%s:missin:Reserve:ncrth" % (i))


                sb.add_newvar("NPCON", self.npcons0[i])

                # Insert the new mission definition.
                #infile = self.getValue("input:rerun%s:mission" % (i)).open()
                #mission = infile.read()
                #infile.close()
                #sb.add_comment(mission)

                # Get the mission definition

                mission = self.getValue("input:rerun%s:mission_definition" % i)

                for seg in mission:
                    sb.add_group(seg)

                # Insert the &PCONIN namelists
                for j in range(0, self.npcons0[i]):

                    re_conalt = self.getValue("input:rerun%s:pconin%s:conalt" % (i, j))
                    re_conmch = self.getValue("input:rerun%s:pconin%s:conmch" % (i, j))
                    re_connz  = self.getValue("input:rerun%s:pconin%s:connz" % (i, j))
                    re_conpc  = self.getValue("input:rerun%s:pconin%s:conpc" % (i, j))
                    re_conlim = self.getValue("input:rerun%s:pconin%s:conlim" % (i, j))
                    re_conaux = self.getValue("input:rerun%s:pconin%s:conaux" % (i, j))
                    re_neo    = self.getValue("input:rerun%s:pconin%s:neo" % (i, j))
                    re_icstdg = self.getValue("input:rerun%s:pconin%s:icstdg" % (i, j))
                    re_conwt  = self.getValue("input:rerun%s:pconin%s:conwt" % (i, j))
                    re_iconsg = self.getValue("input:rerun%s:pconin%s:iconsg" % (i, j))
                    re_confm  = self.getValue("input:rerun%s:pconin%s:confm" % (i, j))
                    re_conwta = self.getValue("input:rerun%s:pconin%s:conwta" % (i, j))
                    re_icontp = self.getValue("input:rerun%s:pconin%s:icontp" % (i, j))

                    sb.add_group('PCONIN')

                    if  re_conalt >= 0.:
                        sb.add_newvar("CONALT", re_conalt)
                    if  re_conmch >= 0.:
                        sb.add_newvar("CONMCH", re_conmch)
                    if  re_connz >= 0.:
                        sb.add_newvar("CONNZ", re_connz)
                    if  re_conpc > -10.:
                        sb.add_newvar("CONPC", re_conpc)
                    if  re_conlim != -999.:
                        sb.add_newvar("CONLIM", re_conlim)
                    if  re_conaux > -1.:
                        sb.add_newvar("CONAUX", re_conaux)
                    if  re_neo >= 0:
                        sb.append("NEO", re_neo)
                    if  re_icstdg >= 0:
                        sb.add_newvar("ICSTDG", re_icstdg)
                    if  re_conwt >= 0.:
                        sb.add_newvar("CONWT", re_conwt)
                    if  re_iconsg >= 0:
                        sb.add_newvar("ICONSG", re_iconsg)
                    if  re_confm >= 0.:
                        sb.add_newvar("CONFM", re_confm)
                    if  re_conwta != -999.:
                        sb.add_newvar("CONWTA", re_conwta)
                    if  re_icontp >= 0:
                        sb.add_newvar("ICONTP", re_icontp)

        # Generate the input file for FLOPS


        sb.generate()

    def parse_output(self):
        """Parses the FLOPS output file(s) and populates the component
        outputs with the data.
        """

        out = FileParser()
        #out.set_file(self.stdout)
        out.set_file(self.output_filepath)



        # Check for namelist read error
        # Throw new Exception for fatal errors
        # Continue processing for FLOPS failures (may want to return error
        # codes to optimizers sometime in the future)
        out.set_delimiters(" ")

        try:
            out.mark_anchor("ERROR READING NAMELIST")
        except RuntimeError:
            pass
        else:
            self.assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error during FLOPS execution.\n %s' % out.transfer_line(0))

        out.reset_anchor()
        try:
            out.mark_anchor("ERROR READING AERODYNAMIC")
        except RuntimeError:
            pass
        else:
            assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error during FLOPS execution.\n %s' % out.transfer_line(0))

        out.reset_anchor()
        try:
            out.mark_anchor("* * * ENGINE DECK MISSING * * *")
        except RuntimeError:
            pass
        else:
            self.assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error during FLOPS execution.\n %s' % out.transfer_line(0) + \
                  '\n\nCheck links from "Engine" to "Flops". Make sure EIFILE' + \
                  'points to an existing file (default is "ENGDECK.txt" in UserDir.\n\n*****************')

        out.reset_anchor()
        try:
            out.mark_anchor("* * * ONLY ONE ALTITUDE FOR MACH NUMBER")
        except RuntimeError:
            pass
        else:
            self.assignValueOutput('output:ERROR',out.transfer_line(0))

            # TODO - Why does MC wrapper do this?
            # commented out for now
            #self.output.Performance.range = 0.
            #self.output.Performance.rampwt = 0.
            #self.output.Performance.fuel = 0.

            raise RuntimeError('Error during FLOPS execution.\n %s' % ERROR)

        out.reset_anchor()
        try:
            out.mark_anchor("* * * ILLEGAL DATA IN ENGINE DECK * * *")
        except RuntimeError:
            pass
        else:
            assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error during FLOPS execution.\n %s' % ERROR)

        out.reset_anchor()
        try:
            #out.mark_anchor("ERROR READING MISSION DEFINITION DATA FROM UNIT")
            # Loosened this up to find any read error; i've found others
            out.mark_anchor("ERROR READING")
        except RuntimeError:
            pass
        else:
            assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error reading a file during FLOPS execution.\n %s' % ERROR)

        out.reset_anchor()
        try:
            out.mark_anchor("ERROR IN SEGMENT INPUT DATA")
        except RuntimeError:
            pass
        else:
            assignValueOutput('output:ERROR',out.transfer_line(0))
            raise RuntimeError('Error during FLOPS execution.\n %s' % ERROR)


        # Modified this section Fri Mar  5 15:05:09 EST 2010
        # there could be failures that recover during optimization

        iopt = self.getValue("input:option:Program_Control:iopt")

        out.reset_anchor()
        try:
            if iopt != 3:
                out.mark_anchor("TITLE, BEGIN OUTPUT OF RESULTS")
            else:
                out.mark_anchor("FINAL ANALYSIS")

        except RuntimeError:

            # Check invalid results
            errorArray = [
               "* * * ENGINE DECK MISSING * * *",
               "NO WEIGHT AVAILABLE FOR FUEL",
               "FAILURE FOR CLIMB SEGMENT",
               "FAILURE FOR CRUISE CONDITION",
               "FAILURE FOR DESCENT SEGMENT",
               "ANALYSIS COULD NOT RECOVER",
               "INITIAL DESIGN UNACCEPTABLE"
               ]
            descArray = [
               "Check links from \"Engine\" to \"Flops\". Make sure EIFILE points to an existing file (default is \"ENGDECK.txt\" in UserDir",
               "Try increasing gross weight (confin.variables.GW1)",
               "Try increasing thrust and/or wing area and see flops.man",
               "Try increasing thrust and/or wing area and see flops.man",
               "Check thrust at flight idle. May need to set IDLE to 1 and see flops.man",
               "Try tweaking SYNTIN inputs to resolve this (AnalysisControl.syntin.control). Also check for other nonfatal failures like failed missed approach climb criterion.",
               "Make sure any initial design variable are within the upper and lower bounds"
               ]

            for i in range(0, size(errorArray)):
                try:
                    out.reset_anchor()
                    out.mark_anchor(errorArray[i])
                    assignValueOutput('output:ERROR',out.transfer_line(0))
                    assignValueOutput('output:HINT' ,descArray[i])
                    self.assignValueOutput("output:Performance:range",0.)
                    self.assignValueOutput("output:Performance:rampwt",0.)
                    self.assignValueOutput("output:Performance:fuel",0.)
                    break
                except RuntimeError:
                    assignValueOutput('output:ERROR','None')
                    assignValueOutput('output:HINT' ,'n/a')


        iopt   = self.getValue("input:option:Program_Control:iopt")
        ianal  = self.getValue("input:option:Program_Control:ianal")
        ifite  = self.getValue("input:option:Program_Control:ifite")
        mywts  = self.getValue("input:wtin:Basic:mywts")
        inrtia = self.getValue("input:wtin:Inertia:inrtia")
        msumpt = self.getValue("input:missin:Basic:msumpt")
        noffdr = size(self.getValue("input:missin:Basic:offdr"))

        out.reset_anchor()

        if ifite == 3:
            out.mark_anchor("PRESSURIZED CABIN DIMENSIONS FOR A")


            self.assignValueOutput("output:Geometry:BWB:xlp", out.transfer_var(1, 5))
            self.assignValueOutput("output:Geometry:BWB:xlw", out.transfer_var(2, 6))
            self.assignValueOutput("output:Geometry:BWB:wf ", out.transfer_var(3, 5))
            self.assignValueOutput("output:Geometry:BWB:acabin", out.transfer_var(4, 4))
            self.assignValueOutput("output:Geometry:BWB:nbaw", out.transfer_var(5, 5))
            self.assignValueOutput("output:Geometry:BWB:bayw", out.transfer_var(6, 5))
            self.assignValueOutput("output:Geometry:BWB:nlava", out.transfer_var(7, 5))
            self.assignValueOutput("output:Geometry:BWB:ngally", out.transfer_var(8, 5))
            self.assignValueOutput("output:Geometry:BWB:nclset", out.transfer_var(9, 5))
            self.assignValueOutput("output:Geometry:BWB:xl", out.transfer_var(10, 5))
            self.assignValueOutput("output:Geometry:BWB:df", out.transfer_var(11, 5))

        out.reset_anchor()
        out.mark_anchor("FUSELAGE DATA")

        self.assignValueOutput("output:Geometry:xl" ,out.transfer_var(2, 4))
        self.assignValueOutput("output:Geometry:wf",out.transfer_var(3, 4))
        self.assignValueOutput("output:Geometry:df", out.transfer_var(4, 4))
        self.assignValueOutput("output:Geometry:xlp",out.transfer_var(6, 5))

        out.reset_anchor()
        out.mark_anchor( "CREW AND PAYLOAD DATA" )

        if ifite != 1:
            self.assignValueOutput("output:Payload:npf", out.transfer_var(1, 5))
            self.assignValueOutput("output:Payload:npb", out.transfer_var(2, 4))
            self.assignValueOutput("output:Payload:npt", out.transfer_var(3, 4))
            self.assignValueOutput("output:Payload:nstu", out.transfer_var(4, 3))
            self.assignValueOutput("output:Payload:ngalc", out.transfer_var(5, 4))
            self.assignValueOutput("output:Payload:wppass", out.transfer_var(7, 5))
            self.assignValueOutput("output:Payload:bpp", out.transfer_var(8, 5))
            self.assignValueOutput("output:Payload:cargow",out.transfer_var(9, 5))
            self.assignValueOutput("output:Payload:cargof",out.transfer_var(10, 5))
        else:
            self.assignValueOutput("output:Payload:cargow", out.transfer_var(2, 6))
            self.assignValueOutput("output:Payload:cargof", out.transfer_var(3, 6))

        out.reset_anchor()
        out.mark_anchor( "CARGO AND BAGGAGE CONTAIN." )
        self.assignValueOutput("output:Payload:wcon", out.transfer_var(0, 6))

        if mywts == 0:
            out.reset_anchor()
            out.mark_anchor( "CREW AND BAGGAGE-FLIGHT" )
            self.assignValueOutput("output:Payload:nflcr",out.transfer_var(0, 4))
            if ifite != 1:
                self.assignValueOutput("output:Payload:nstuag", out.transfer_var(1, 2))

        if iopt == 3:
            # In optimization mode, find the last design mission
            nos = 0
            while True:
                try:
                    out.reset_anchor()
                    out.mark_anchor( "#OBJ/VAR/CONSTR SUMMARY",
                                  noffdr+nos+1+self.nrern0 )
                except RuntimeError:
                    break
                else:
                    nos += 1

            nit = noffdr + nos
        else:
            nit = nos = 1

        if nit > 0:

            # Read output from the weights module

            if mywts == 0:

                out.reset_anchor()
                try:
                    out.mark_anchor( "WING SPAN               ", nos)
                except RuntimeError:
                    ndd = self.getValue("input:syntin:Optimization_Control:ndd")
                    if ndd == 0:
                        msg = "\n\n***************** \n\n"
                        msg += "There was only one iteration in optimization mode \n\n"
                        msg += "and we happen to be looking for the final solution, which isn't there. \n\n"
                        msg += "ndd = %" % ndd + "\n\n"
                        msg += "Try setting flops.input.syntin.Optimization_Control.ndd to 3 or 4.\n\n"
                        msg += "*****************"
                        raise RuntimeError(msg)
                    else:
                        msg = "\n\n***************** \n\n"
                        msg += "There was only one iteration in optimization mode \n\n"
                        msg += "and we happen to be looking for the final solution, which isn't there. \n\n"
                        msg += "Something is wrong here and someone needs to figure it out before we can proceed.\n\n"
                        msg += "*****************"
                        raise RuntimeError(msg)

                self.assignValueOutput("output:Geometry:span", out.transfer_var(0, 3))
                self.assignValueOutput("output:Geometry:glov", out.transfer_var(1, 4))
                self.assignValueOutput("output:Geometry:sht", out.transfer_var(3, 4))
                self.assignValueOutput("output:Geometry:svt", out.transfer_var(5, 4))
                self.assignValueOutput("output:Geometry:xnac", out.transfer_var(8, 3))
                self.assignValueOutput("output:Geometry:dnac", out.transfer_var(9, 3))
                self.assignValueOutput("output:Geometry:xmlg", out.transfer_var(11, 5))
                self.assignValueOutput("output:Geometry:xnlg", out.transfer_var(12, 5))

                self.assignValueOutput("output:Weight:wldg", out.transfer_var(14, 4))
                self.assignValueOutput("output:Weight:fultot",out.transfer_var(19, 4))
                self.assignValueOutput("output:Weight:exsful", out.transfer_var(20, 4))

                out.reset_anchor()
                out.mark_anchor( "WING BENDING FACTOR", nos)

                self.assignValueOutput("output:Weight:Wing:w", out.transfer_var(0, 4))
                self.assignValueOutput("output:Weight:Wing:ew", out.transfer_var(1, 5))
                self.assignValueOutput("output:Weight:Wing:w1", out.transfer_var(4, 3))
                self.assignValueOutput("output:Weight:Wing:w2", out.transfer_var(5, 3))
                self.assignValueOutput("output:Weight:Wing:w3", out.transfer_var(6, 3))

                        # Read mass and balance summary data

                out.reset_anchor()
                out.mark_anchor( "MASS AND BALANCE SUMMARY", nos)

                if ifite == 1:
                    self.assignValueOutput("output:Weight:frwi",out.transfer_keyvar("WING ",2))
                    self.assignValueOutput("output:Weight:frht",out.transfer_keyvar("HORIZONTAL TAIL ",2))
                    self.assignValueOutput("output:Weight:frvt",out.transfer_keyvar("VERTICAL TAIL ",2))
                    self.assignValueOutput("output:Weight:frfin",out.transfer_keyvar("VERTICAL FIN ",2))
                    self.assignValueOutput("output:Weight:frcan",out.transfer_keyvar("CANARD ",2))
                    self.assignValueOutput("output:Weight:frfu",out.transfer_keyvar("FUSELAGE ",2))
                    self.assignValueOutput("output:Weight:wlg",out.transfer_keyvar("LANDING GEAR ",2))
                    self.assignValueOutput("output:Weight:frna",out.transfer_keyvar("NACELLE (AIR INDUCTION) ",2))
                    self.assignValueOutput("output:Weight:wengt",out.transfer_keyvar("ENGINES ",2))
                    self.assignValueOutput("output:Weight:wthr",out.transfer_keyvar("THRUST REVERSERS ",2))
                    self.assignValueOutput("output:Weight:wpmisc",out.transfer_keyvar("MISCELLANEOUS SYSTEMS ",2))
                    self.assignValueOutput("output:Weight:wfsys",out.transfer_keyvar("FUEL SYSTEM-TANKS AND PLUMBING ",2))
                    self.assignValueOutput("output:Weight:frsc",out.transfer_keyvar("SURFACE CONTROLS ",2))
                    self.assignValueOutput("output:Weight:wapu",out.transfer_keyvar("AUXILIARY POWER ",2))
                    self.assignValueOutput("output:Weight:win",out.transfer_keyvar("INSTRUMENTS ",2))
                    self.assignValueOutput("output:Weight:whyd",out.transfer_keyvar("HYDRAULICS ",2))
                    self.assignValueOutput("output:Weight:welec",out.transfer_keyvar("ELECTRICAL ",2))
                    self.assignValueOutput("output:Weight:wavonc",out.transfer_keyvar("AVIONICS ",2))
                    self.assignValueOutput("output:Weight:wfurn",out.transfer_keyvar("FURNISHINGS AND EQUIPMENT ",2))
                    self.assignValueOutput("output:Weight:wac",out.transfer_keyvar("AIR CONDITIONING ",2))
                    self.assignValueOutput("output:Weight:wai",out.transfer_keyvar("AUXILIARY GEAR ",2))
                    self.assignValueOutput("output:Weight:wempty",out.transfer_keyvar(" WEIGHT EMPTY ",2))
                    self.assignValueOutput("output:Weight:wflcrbw",out.transfer_keyvar("CREW AND BAGGAGE-FLIGHT,", 3))
                    self.assignValueOutput("output:Weight:wuf",out.transfer_keyvar("UNUSABLE FUEL ",2))
                    self.assignValueOutput("output:Weight:woil",out.transfer_keyvar("ENGINE OIL ",2))
                    self.assignValueOutput("output:Weight:wsrv",out.transfer_keyvar("AMMUNITION, ETC. ",2))
                    self.assignValueOutput("output:Weight:wbomb",out.transfer_keyvar("AUXILIARY TANKS ",2))
                    self.assignValueOutput("output:Weight:dowe",out.transfer_keyvar("OPERATING WEIGHT  ",2))
                    self.assignValueOutput("output:Weight:zfw",out.transfer_keyvar("ZERO FUEL WEIGHT ",2))
                else:
                    self.assignValueOutput("output:Weight:frwi",out.transfer_keyvar("WING ",2))
                    self.assignValueOutput("output:Weight:frht",out.transfer_keyvar("HORIZONTAL TAIL ",2))
                    self.assignValueOutput("output:Weight:frvt",out.transfer_keyvar("VERTICAL TAIL ",2))
                    self.assignValueOutput("output:Weight:frfin",out.transfer_keyvar("VERTICAL FIN ",2))
                    self.assignValueOutput("output:Weight:frcan",out.transfer_keyvar("CANARD ",2))
                    self.assignValueOutput("output:Weight:frfu",out.transfer_keyvar("FUSELAGE ",2))
                    self.assignValueOutput("output:Weight:wlg",out.transfer_keyvar("LANDING GEAR ",2))
                    self.assignValueOutput("output:Weight:frna",out.transfer_keyvar("NACELLE (AIR INDUCTION) ",2))
                    self.assignValueOutput("output:Weight:wengt",out.transfer_keyvar("ENGINES ",2))
                    self.assignValueOutput("output:Weight:wthr",out.transfer_keyvar("THRUST REVERSERS ",2))
                    self.assignValueOutput("output:Weight:wpmisc",out.transfer_keyvar("MISCELLANEOUS SYSTEMS ",2))
                    self.assignValueOutput("output:Weight:wfsys",out.transfer_keyvar("FUEL SYSTEM-TANKS AND PLUMBING ",2))
                    self.assignValueOutput("output:Weight:frsc",out.transfer_keyvar("SURFACE CONTROLS ",2))
                    self.assignValueOutput("output:Weight:wapu",out.transfer_keyvar("AUXILIARY POWER ",2))
                    self.assignValueOutput("output:Weight:win",out.transfer_keyvar("INSTRUMENTS ",2))
                    self.assignValueOutput("output:Weight:whyd",out.transfer_keyvar("HYDRAULICS ",2))
                    self.assignValueOutput("output:Weight:welec",out.transfer_keyvar("ELECTRICAL ",2))
                    self.assignValueOutput("output:Weight:wavonc",out.transfer_keyvar("AVIONICS ",2))
                    self.assignValueOutput("output:Weight:wfurn",out.transfer_keyvar("FURNISHINGS AND EQUIPMENT ",2))
                    self.assignValueOutput("output:Weight:wac",out.transfer_keyvar("AIR CONDITIONING ",2))
                    self.assignValueOutput("output:Weight:wai",out.transfer_keyvar("ANTI-ICING ",2))
                    self.assignValueOutput("output:Weight:wempty",out.transfer_keyvar(" WEIGHT EMPTY ",2))
                    self.assignValueOutput("output:Weight:wflcrbw",out.transfer_keyvar("CREW AND BAGGAGE-FLIGHT,", 3))
                    self.assignValueOutput("output:Weight:wwstuab",out.transfer_keyvar("-CABIN, ", 3))
                    self.assignValueOutput("output:Weight:wuf",out.transfer_keyvar("UNUSABLE FUEL ",2))
                    self.assignValueOutput("output:Weight:woil",out.transfer_keyvar("ENGINE OIL ",2))
                    self.assignValueOutput("output:Weight:wsrv",out.transfer_keyvar("PASSENGER SERVICE ",2))
                    self.assignValueOutput("output:Weight:dowe",out.transfer_keyvar("OPERATING WEIGHT  ",2))
                    self.assignValueOutput("output:Weight:zfw",out.transfer_keyvar("ZERO FUEL WEIGHT ",2))

                # Read inertia data

                if inrtia > 0:
                    out.reset_anchor()
                    out.mark_anchor( "#  INERTIA DATA FOR AIRCRAFT", nos)

                    nfcon = self.getValue("input:wtin:Inertia:tf").shape[0]

                    self.assignValueOutput("output:Weight:Inertia:cgx",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:cgy",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:cgz",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:ixxroll",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:ixxptch",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:ixxyaw",zeros(1+nfcon))
                    self.assignValueOutput("output:Weight:Inertia:ixz",zeros(1+nfcon))

                    out.reset_anchor()
                    out.mark_anchor( " AIRCRAFT OWE OR ZFW", 1)
                    self.assignValueOutput("output:Weight:Inertia:cgx",out.transfer_var(0, 6),index=0)
                    self.assignValueOutput("output:Weight:Inertia:cgy",out.transfer_var(0, 7),index=0)
                    self.assignValueOutput("output:Weight:Inertia:cgz",out.transfer_var(0, 8),index=0)

                    out.reset_anchor()
                    out.mark_anchor( " AIRCRAFT OWE OR ZFW",2)
                    self.assignValueOutput("output:Weight:Inertia:ixxroll",out.transfer_var(0, 5),index=0)
                    self.assignValueOutput("output:Weight:Inertia:ixxptch",out.transfer_var(0, 6),index=0)
                    self.assignValueOutput("output:Weight:Inertia:ixxyaw",out.transfer_var(0, 7),index=0)
                    self.assignValueOutput("output:Weight:Inertia:ixz",out.transfer_var(0, 8),index=0)

                    out.reset_anchor()
                    if nfcon > 0:
                        for i in range(1, nfcon+1):
                            out.mark_anchor( "INERTIA DATA FOR FUEL CONDITION" )

                            out.mark_anchor( " TOTAL WEIGHT " )
                            self.assignValueOutput("output:Weight:Inertia:cgx",out.transfer_var(0, 4),index=i)
                            self.assignValueOutput("output:Weight:Inertia:cgy",out.transfer_var(0, 5),index=i)
                            self.assignValueOutput("output:Weight:Inertia:cgz",out.transfer_var(0, 6),index=i)

                            out.mark_anchor( " TOTAL AIRCRAFT " )
                            self.assignValueOutput("output:Weight:Inertia:ixxroll",out.transfer_var(0, 3),index=i)
                            self.assignValueOutput("output:Weight:Inertia:ixxptch",out.transfer_var(0, 4),index=i)
                            self.assignValueOutput("output:Weight:Inertia:ixxyaw",out.transfer_var(0, 5),index=i)
                            self.assignValueOutput("output:Weight:Inertia:ixz",out.transfer_var(0, 6),index=i)

            else:

                # set weights to zero
                self.assignValueOutput("output:Geometry:span",0.0)
                self.assignValueOutput("output:Geometry:glov",0.0)
                self.assignValueOutput("output:Geometry:sht",0.0)
                self.assignValueOutput("output:Geometry:svt",0.0)
                self.assignValueOutput("output:Geometry:xnac",0.0)
                self.assignValueOutput("output:Geometry:dnac",0.0)
                self.assignValueOutput("output:Geometry:xmlg",0.0)
                self.assignValueOutput("output:Geometry:xnlg",0.0)
                self.assignValueOutput("output:Weight:wldg",0.0)
                self.assignValueOutput("output:Weight:fultot",0.0)
                self.assignValueOutput("output:Weight:exsful",0.0)
                self.assignValueOutput("output:Weight:frwi",0.0)
                self.assignValueOutput("output:Weight:frht",0.0)
                self.assignValueOutput("output:Weight:frvt",0.0)
                self.assignValueOutput("output:Weight:frfin",0.0)
                self.assignValueOutput("output:Weight:frcan",0.0)
                self.assignValueOutput("output:Weight:frfu",0.0)
                self.assignValueOutput("output:Weight:wlg",0.0)
                self.assignValueOutput("output:Weight:frna",0.0)
                self.assignValueOutput("output:Weight:wengt",0.0)
                self.assignValueOutput("output:Weight:wthr",0.0)
                self.assignValueOutput("output:Weight:wpmisc",0.0)
                self.assignValueOutput("output:Weight:wfsys",0.0)
                self.assignValueOutput("output:Weight:frsc",0.0)
                self.assignValueOutput("output:Weight:wapu",0.0)
                self.assignValueOutput("output:Weight:win",0.0)
                self.assignValueOutput("output:Weight:whyd",0.0)
                self.assignValueOutput("output:Weight:welec",0.0)
                self.assignValueOutput("output:Weight:wavonc",0.0)
                self.assignValueOutput("output:Weight:wfurn",0.0)
                self.assignValueOutput("output:Weight:wac",0.0)
                self.assignValueOutput("output:Weight:wai",0.0)
                self.assignValueOutput("output:Weight:wempty",0.0)
                self.assignValueOutput("output:Weight:wflcrbw",0.0)
                self.assignValueOutput("output:Weight:wwstuab",0.0)
                self.assignValueOutput("output:Weight:wuf",0.0)
                self.assignValueOutput("output:Weight:woil",0.0)
                self.assignValueOutput("output:Weight:wsrv",0.0)
                self.assignValueOutput("output:Weight:dowe",0.0)
                self.assignValueOutput("output:Weight:zfw",0.0)
                self.assignValueOutput("output:Weight:wbomb",0.0)

                # inertia data
                self.assignValueOutput("output:Weight:Inertia:cgx",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:cgy",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:cgz",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:ixxroll",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:ixxptch",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:ixxyaw",zeros(0))
                self.assignValueOutput("output:Weight:Inertia:ixz",zeros(0))

            # Read performance contraints summary
         
            if self.npcon0 > 0 and ianal == 3:
                out.reset_anchor()
                out.mark_anchor( "PERFORMANCE CONSTRAINT SUMMARY", nos)

                out.set_delimiters("columns")
                self.assignValueOutput("output:Performance:Constraints:constraint",out.transfer_array(4, 16, 3+self.npcon0, 29))
                self.assignValueOutput("output:Performance:Constraints:value",out.transfer_array(4, 32, 3+self.npcon0, 40))
                self.assignValueOutput("output:Performance:Constraints:units",out.transfer_array(4, 41, 3+self.npcon0, 47))
                self.assignValueOutput("output:Performance:Constraints:limit",out.transfer_array(4, 48, 3+self.npcon0, 56))

                weight = out.transfer_array(4, 56, 3+self.npcon0, 65)


                if isinstance(weight[0], str):
                    self.assignValueOutput("output:Performance:Constraints:location",out.transfer_array(4, 58, 3+self.npcon0, 87))
                else:
                    self.assignValueOutput("output:Performance:Constraints:location",array([]))
                    self.assignValueOutput("output:Performance:Constraints:weight", weight)
                    self.assignValueOutput("output:Performance:Constraints:mach",out.transfer_array(4, 66, 3+self.npcon0, 74))
                    self.assignValueOutput("output:Performance:Constraints:alt",out.transfer_array(4, 75, 3+self.npcon0, 85))
                    self.assignValueOutput("output:Performance:Constraints:g",out.transfer_array(4, 86, 3+self.npcon0, 98))

                out.set_delimiters(" ")

            # Read sizing and performance results

            if ianal == 3:
                out.reset_anchor()
                out.mark_anchor( "CONFIGURATION DATA AFTER RESIZING (IF ANY)", nit)

                self.assignValueOutput("output:Weight:dowe",out.transfer_var(2, 4))
                self.assignValueOutput("output:Weight:paylod",out.transfer_var(3,2))
                self.assignValueOutput("output:Weight:fuel",out.transfer_var(4, 3))
                self.assignValueOutput("output:Weight:rampwt",out.transfer_var(5, 3))
                self.assignValueOutput("output:Weight:wsr",out.transfer_var(8, 3))
                self.assignValueOutput("output:Weight:thrso",out.transfer_var(10, 4))
                self.assignValueOutput("output:Weight:esf",out.transfer_var(11, 4))
                self.assignValueOutput("output:Weight:twr",out.transfer_var(12, 3))

                self.assignValueOutput("output:Performance:thrso", self.getValueOutput("output:Weight:thrso"))
                self.assignValueOutput("output:Performance:esf", self.getValueOutput("output:Weight:esf"))

            # Read detailed flight segment summary

            if ianal == 3 and msumpt > 0:
                out.reset_anchor()
                out.mark_anchor( "DETAILED FLIGHT SEGMENT SUMMARY")

                for i in range(0, self.nmseg):
                    if i < 9:
                        out.mark_anchor( "SEGMENT  " + str(i+1) + "   ")
                    else:
                        out.mark_anchor( "SEGMENT " + str(i+1) + "   " )

                    self.assignValueOutput("output:Performance:Segments:segment",out.transfer_var(0, 3),i)
                    self.assignValueOutput("output:Performance:Segments:weights",out.transfer_var(5, 1),i)
                    self.assignValueOutput("output:Performance:Segments:alts",out.transfer_var(5,2),i)
                    self.assignValueOutput("output:Performance:Segments:machs",out.transfer_var(5, 3),i)
                    self.assignValueOutput("output:Performance:Segments:thrusts",out.transfer_var(5, 7),i)
                    self.assignValueOutput("output:Performance:Segments:ex_pow",out.transfer_var(5,9),i)
                    self.assignValueOutput("output:Performance:Segments:lods",out.transfer_var(5, 12),i)
                    self.assignValueOutput("output:Performance:Segments:totmaxs",out.transfer_var(6, 6),i)
                    self.assignValueOutput("output:Performance:Segments:sfcs",out.transfer_var(6, 7),i)
                    self.assignValueOutput("output:Performance:Segments:engparms",out.transfer_var(6, 13),i)

                    # This seems a bit klugey, but it actually works.
                    j = 0
                    while True:
                        try:
                            self.assignValueOutput("output:Performance:Segments:weighte",out.transfer_var(j+5, 1),i)
                            self.assignValueOutput("output:Performance:Segments:alte",out.transfer_var(j+5,2),i)
                            self.assignValueOutput("output:Performance:Segments:mache",out.transfer_var(j+5, 3),i)
                            self.assignValueOutput("output:Performance:Segments:thruste",out.transfer_var(j+5, 7),i)
                            self.assignValueOutput("output:Performance:Segments:lode",out.transfer_var(j+5, 12),i)
                            self.assignValueOutput("output:Performance:Segments:totmaxe",out.transfer_var(j+6, 6),i)
                            self.assignValueOutput("output:Performance:Segments:sfce",out.transfer_var(j+6, 7),i)
                            self.assignValueOutput("output:Performance:Segments:engparme",out.transfer_var(j+6, 13),i)

                        except ValueError:
                            break

                        j += 3

                # Read the mission summary

                out.reset_anchor()
                out.mark_anchor( "M I S S I O N   S U M M A R Y", nos)

                self.assignValueOutput("output:Performance:taxofl",out.transfer_var(5, 4))

            # Read the objective, variable and constraint summary

            out.reset_anchor()
            out.mark_anchor( "#OBJ/VAR/CONSTR SUMMARY", nos)
            out.set_delimiters("columns")

            # Changed based on Karl's fix to bug I reported
            if ianal == 3:

                self.assignValueOutput("output:Performance:fuel",out.transfer_var(3, 1, 10))
                self.assignValueOutput("output:Performance:range",out.transfer_var(3, 11, 17))
                self.assignValueOutput("output:Performance:vapp",out.transfer_var(3, 18, 23))

                # TODO - Again, there's got to be a better way
                try:
                    self.assignValueOutput("output:Performance:faroff",out.transfer_var(3, 24, 30))
                except(RuntimeError, IndexError):
                    self.assignValueOutput("output:Performance:faroff", 1.0e10)

                self.assignValueOutput("output:Performance:farldg",out.transfer_var(3, 31, 37))
                self.assignValueOutput("output:Performance:amfor",out.transfer_var(3, 38, 45))
                self.assignValueOutput("output:Performance:ssfor",out.transfer_var(3, 46, 53))

                self.assignValueOutput("output:Geometry:ar",out.transfer_var(3, 65, 70))
                self.assignValueOutput("output:Geometry:sw",out.transfer_var(3, 80, 87))
                self.assignValueOutput("output:Geometry:tr",out.transfer_var(3, 88, 93))
                self.assignValueOutput("output:Geometry:sweep",out.transfer_var(3, 94, 99))
                self.assignValueOutput("output:Geometry:tca",out.transfer_var(3, 100, 106))

                if self.getValue("input:wtin:Basic:vmmo") > 0.:
                    self.assignValueOutput("output:Performance:vmmo", self.getValue("input:wtin:Basic:vmmo"))
                else:
                    self.assignValueOutput("output:Performance:vmmo",out.transfer_var(3, 107, 112))

            if self.getValueOutput("output:Weight:fuel") == 0.:
                self.assignValueOutput("output:Weight:fuel",out.transfer_var(3, 1, 10))

            if self.getValueOutput("output:Weight:rampwt") == 0.:
                self.assignValueOutput("output:Weight:rampwt",out.transfer_var(3, 54, 64))

            if self.getValueOutput("output:Weight:thrso") == 0.:
                self.assignValueOutput("output:Weight:thrso",out.transfer_var(3, 72, 78))
                #self.assignValueOutput("output:Weight:thrsop",self.getValueOutput("output:Performance:thrso"))

            if self.getValueOutput("output:Weight:wsr") == 0.:
                self.assignValueOutput("output:Weight:wsr",out.transfer_var(3, 121, 126))

            if self.getValueOutput("output:Weight:twr") == 0.:
                self.assignValueOutput("output:Weight:twr",out.transfer_var(3, 127, 132))

            out.set_delimiters(" ")

            # Read off-design mission data

            if ianal == 3:

                ndim = 1 + noffdr + self.nrern0
                self.assignValueOutput("output:Econ:sl",zeros(ndim))
                self.assignValueOutput("output:Econ:blockt",zeros(ndim))
                self.assignValueOutput("output:Econ:blockf",zeros(ndim))
                self.assignValueOutput("output:Econ:blockNx",zeros(ndim))
                self.assignValueOutput("output:Econ:wpayl",zeros(ndim))
                self.assignValueOutput("output:Econ:wgross",zeros(ndim))
                self.assignValueOutput("output:Econ:range",zeros(ndim))
                self.assignValueOutput("output:Econ:vapp",zeros(ndim))
                self.assignValueOutput("output:Econ:faroff",zeros(ndim))
                self.assignValueOutput("output:Econ:farldg",zeros(ndim))
                self.assignValueOutput("output:Econ:amfor",zeros(ndim))
                self.assignValueOutput("output:Econ:ssfor",zeros(ndim))

                for i in range(0, ndim):

                    out.reset_anchor()
                    out.mark_anchor( "CONFIGURATION DATA AFTER RESIZING", (nos-1)*(1 + noffdr) + 1 + i)

                    self.assignValueOutput("output:Econ:wpayl",out.transfer_var(3,2),i)
                    self.assignValueOutput("output:Econ:wgross",out.transfer_var(5, 3),i)

                    out.mark_anchor( "DESIGN RANGE" )
                    self.assignValueOutput("output:Econ:sl",out.transfer_var(0, 3),i)

                    out.mark_anchor( "BLOCK TIME =" )
                    self.assignValueOutput("output:Econ:blockt",out.transfer_var(0, 4),i)
                    self.assignValueOutput("output:Econ:blockf",out.transfer_var(1, 4),i)
                    self.assignValueOutput("output:Econ:blockNx",out.transfer_var(2, 6),i)

                    out.mark_anchor( "#OBJ/VAR/CONSTR SUMMARY" );

                    out.set_delimiters("columns")
                    self.assignValueOutput("output:Econ:range",out.transfer_var(3, 11, 17),i)
                    self.assignValueOutput("output:Econ:vapp",out.transfer_var(3, 18, 23),i)

                    try:
                        self.assignValueOutput("output:Econ:faroff",out.transfer_var(3, 24, 30),i)
                    except (RuntimeError, IndexError):
                        self.assignValueOutput("output:Econ:faroff",1.0e10,i)

                    self.assignValueOutput("output:Econ:farldg",out.transfer_var(3, 31, 37),i)
                    self.assignValueOutput("output:Econ:amfor",out.transfer_var(3, 38, 45),i)
                    self.assignValueOutput("output:Econ:ssfor",out.transfer_var(3, 46, 53),i)

                    out.set_delimiters(" ")






    def load_model(self , filename):
        """Loads the FLOPS model from an existing input file"""
        """Needed to initialize namelist"""

        sb = Namelist(self)

        sb.set_filename(filename)


       # Where each namelist goes in the component
        rule_dict = { "OPTION" : ["input:option:Program_Control", \
                                  "input:option:Plot_Files", \
                                  "input:option:Excess_Power_Plot"],
                      "WTIN" : [ "input:wtin:Basic", \
                                 "input:wtin:Center_of_Gravity", \
                                 "input:wtin:Crew_Payload", \
                                 "input:wtin:Crew_optional", \
                                 "input:wtin:Detailed_Wing", \
                                 "input:wtin:Fuel_System", \
                                 "input:wtin:Fuselage", \
                                 "input:wtin:Inertia", \
                                 "input:wtin:Landing_Gear", \
                                 "input:wtin:OEW_Calculations", \
                                 "input:wtin:Override", \
                                 "input:wtin:Propulsion", \
                                 "input:wtin:Tails_Fins", \
                                 "input:wtin:Wing_Data"],
                      "CONFIN" : ["input:confin:Basic", \
                                  "input:confin:Design_Variables", \
                                  "input:confin:Objective"],
                      "AERIN" : ["input:aerin:Basic", \
                                 "input:aerin:Internal_Aero", \
                                 "input:aerin:Takeoff_Landing"],
                      "ENGDIN" : ["input:engdin", \
                                  "input:engdin:Basic", \
                                  "input:engdin:Special_Options"],
                      "MISSIN" : ["input:missin:Basic", \
                                  "input:missin:Climb", \
                                  "input:missin:Cruise", \
                                  "input:missin:Descent", \
                                  "input:missin:Ground_Operations", \
                                  "input:missin:Reserve", \
                                  "input:missin:Store_Drag", \
                                  "input:missin:Turn_Segments", \
                                  "input:missin:User_Weights", \
                                  "input:parent"],
                      "TOLIN" : ["input:tolin:Basic", \
                                 "input:tolin:Integration_Intervals", \
                                 "input:tolin:Landing", \
                                 "input:tolin:Takeoff", \
                                 "input:tolin:Thrust_Reverser"],
                      "NOISIN" : ["input:noisin:Airframe", \
                                  "input:noisin:Basic", \
                                  "input:noisin:Core", \
                                  "input:noisin:Engine_Parameters", \
                                  "input:noisin:Fan", \
                                  "input:noisin:Flap_Noise", \
                                  "input:noisin:Ground_Effects", \
                                  "input:noisin:Jet", \
                                  "input:noisin:MSJet", \
                                  "input:noisin:Observers", \
                                  "input:noisin:Propagation", \
                                  "input:noisin:Propeller", \
                                  "input:noisin:Shielding", \
                                  "input:noisin:Turbine"],
                      "COSTIN" : ["input:costin:Basic", \
                                  "input:costin:Cost_Technology", \
                                  "input:costin:Mission_Performance"],
                      "FUSEIN" : ["input:fusein:Basic", \
                                  "input:fusein:BWB"],
                      "ENGINE" : ["input:engine", \
                                  "input:engine:Basic", \
                                  "input:engine:Design_Point", \
                                  "input:engine:Engine_Weight", \
                                  "input:engine:IC_Engine", \
                                  "input:engine:Noise_Data", \
                                  "input:engine:Other"],
                      "SYNTIN" : ["input:syntin", \
                                  "input:syntin:Variables", \
                                  "input:syntin:Optimization_Control"],
                      "ASCLIN" : ["input:asclin"],
                      "NACELL" : ["input:nacell"],
                      "PROIN"  : ["input:proin"]
                    }
        # Some variables aren't exposed in the OpenMDAO wrapper (e.g., array
        # sizes which aren't needed explicitly.)
        ignore = ["netaw", "itank", "nob", "nparam", "nfcon", "npcon"]

        sb.parse_file()
    

        self.assignValue('input:title',sb.title)

        empty_groups, unlisted_groups, unlinked_vars = \
                    sb.load_model(rule_dict, ignore)

        # The pconin groups are problematic, and have not been filled because
        # they aren't created yet. We can parse the unlisted_groups to see
        # which ones are in the input-file, and then add them to the component.

        # Rerun, Segin, and Pconin groups also do not have unique names. We give
        # them unique names in OpenMDAO.

        num_mission = 0
        if size(unlisted_groups) > 0:
            #for i, group in unlisted_groups.iteritems():
            for i,group in iter(unlisted_groups.items()):
            
                if group.lower().count('pconin'):
                    
                    self.add_pconin()
                    rule_dict = { "PCONIN" : ["input:pconin"+str(self.npcon0-1)] }
                

                    ne, nu, nv = sb.load_model(rule_dict, ignore, i)
                    for var in nv:
                        unlinked_vars.append(var)
                   
                   
                elif group.lower().count('rerun'):

                    self.add_rerun()
                    stem = "input:rerun"+str(self.nrern0-1)
                    rule_dict = { "RERUN" : [stem] }

                    ne, nu, nv = sb.load_model(rule_dict, ignore, i)
                    for var in nv:
                        unlinked_vars.append(var)

                elif group.lower().count('segin'):

                    self.add_segin()
                    stem = "input:segin"+str(self.nseg0-1)
                    rule_dict = { "SEGIN" : [stem] }

                    ne, nu, nv = sb.load_model(rule_dict, ignore, i)
                    for var in nv:
                        unlinked_vars.append(var)

                # Hopefully the missin namelist always follows its associated
                # rerun group.

                elif group.lower().count('missin'):

                    rule_dict = { "MISSIN" : [stem+":missin:Basic",
                                              stem+":missin:Store_Drag",
                                              stem+":missin:User_Weights",
                                              stem+":missin:Ground_Operations",
                                              stem+":missin:Turn_Segments",
                                              stem+":missin:Climb",
                                              stem+":missin:Cruise",
                                              stem+":missin:Descent",
                                              stem+":missin:Reserve",] }

                    ne, nu, nv = sb.load_model(rule_dict, ignore, i)
                    for var in nv:
                        unlinked_vars.append(var)

                    num_mission += 1

            self.assignValue('input:missin:Basic:npcon',self.npcon0)
        # Mission segments are also a challenge.
        # The remaining empty groups should be mission segments or comments.

        missions = []
        if size(empty_groups) > 0:

            in_mission = False
            for group in empty_groups.values():

                group_name = group.strip().split(" ")[0]

                if group_name.lower() == 'start':
                    missions.append('START')
                    in_mission = True
                elif group_name.lower() == 'end':
                    missions.append('END')
                    in_mission = False
                elif in_mission == True:

                    groups = ['climb', 'cruise', 'refuel', 'release', 'accel', \
                              'turn', 'combat', 'hold', 'descent']

                    if group_name.lower() in groups:
                        missions.append(group.upper())
                    else:
                        print("Warning: Ignoring unknonwn mission %s" % group)

            # Fist, handle the standard run missions
            mission_count = 0
            mission_start = 0
            mission_end = 0
            for i, mission in enumerate(missions):
                if mission == 'END':
                    mission_end = i
                    mission_count += i+1
                    break

            #self.input.mission_definition.mission = missions[:mission_end+1]
            self.assignValue('input:mission_definition:mission',missions[:mission_end+1])

            # Next, handle the missions in the Rerun groups
            for j in range(0,self.nrern0):
                name = "rerun" + str(j)
                mission_start = mission_end+1
                for i, mission in enumerate(missions[mission_start:]):
                    if mission == 'END':
                        mission_end = i+mission_start
                        mission_count += i+1
                        break
                '''self.set("input:%s:mission_definition" % name, \
                           missions[mission_start:mission_end+1])'''
                self.add_param("input:%s:mission_definition" % name,val=missions[mission_start:mission_end+1])


        # Certain data files are sometimes jammed into the input file. We have
        # to jump through some hoops to detect and import this information.

        ndecks = 0
        #getValue(self,'input:engdin:Basic:igenen')
        #exit()

        #if self.input.engdin:Basic:igenen in (0, -2):
        if self.getValue('input:engdin:Basic:igenen') in (0,-2):
            found = False
            engine_deck = ""
            for i, group in enumerate(sb.groups):

                if group.lower().strip() == 'engdin':
                    found = True

                elif found == True:

                    if size(sb.cards[i]) > 0:
                        break

                    engine_deck += '%s\n' % group
                    ndecks += 1

            self.assignValue("input:engine_deck:engdek", engine_deck)

        # Aero deck seems to fall after the mission segements
        if self.getValue('input:aerin:Basic:myaero') > 0 and \
           self.getValue('input:aerin:Basic:myaero') != 3 and \
           self.getValue('input:option:Program_Control:ianal') == 3:

            found = False
            aerodat = ""
            for i, group in enumerate(sb.groups):

                if group.lower().strip() == 'end':
                    found = True

                elif found == True:

                    if size(sb.cards[i]) > 0:
                        break

                    aerodat += '%s\n' % group
                    ndecks += 1

            #self.input.aero_data.aerodat = aerodat
            self.assignValue('input:aero_data:aerodat',aerodat)
        # Post process some stuff, mostly arrays 2D arrays that come over as 1D

        #tf = self.input:wtin:Inertia:tf
        tf = self.getValue('input:wtin:Inertia:tf')
        # TODO: tf can be input with 1st dim greater than one. Need to find out
        # how that is written / parsed.

        if tf.shape[0] > 0:
            #self.set('input:wtin:Inertia:tf', array([tf]))
            self.assignValue('input:wtin:Inertia:tf',array([tf]))      

        # Report diagnostics and raise any exceptions.

        print( "Empty Groups: %d, Unhandled Groups: %d, Unlinked Vars: %d" % \
              (size(empty_groups)-size(missions)-ndecks, \
               size(unlisted_groups)-self.getValue("input:missin:Basic:npcon")-self.nrern0-self.nseg0-num_mission, \
               size(unlinked_vars)))
      
        '''Initializing all the output (unknown) variables'''
        self.loadOutputVars()

