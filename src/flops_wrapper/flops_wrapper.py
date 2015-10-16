from __future__ import print_function

#from namelist_util import Namelist
from openmdao.util.namelist_util import Namelist, ToBool

from openmdao.core import Component
from openmdao.components import ExternalCode
from numpy import int64 as numpy_int64
from numpy import float64 as numpy_float64
from numpy import str as numpy_str
from numpy import zeros, array
from openmdao.core.problem import Problem
from openmdao.core.group import Group





    
class FlopsWrapper(ExternalCode):
    """Wrapper for FlopsWrapper"""
    ERROR = {'val':'none','iotype':'out', 'desc':'Error message for FLOPS failures'}
    HINT = {'val':'none', 'iotype':'out', 'desc':'Hint for resolving error'}
    npcon =0# {'val':0, 'iotype':'in', 'desc':'Number of PCONIN namelists to be created'}
    nseg = {'val':0, 'iotype':'in', 'desc':'Number of SEGIN namelists to be created'}
    nrerun = {'val':0, 'iotype':'in', 'desc':'Number of RERUN namelists to be created'}
    npcons = {'iotype':'in', 'dtype':numpy_int64, 'desc':'Number of PCONIN ' +
                   'namelists to be created with each RERUN namelist'}


    def assignValue(self,variable,value):
            #support the modification of input variables before calling setup
            #comp -> component
            # variable is  a string
            if hasattr(self.params, 'keys'):
                self.params[variable]=value
            else:
                self._params_dict[variable]['val']=value

    def getValue(self,variable):
            #support the modification of input variables before calling setup
            #comp -> component

            if hasattr(self.params, 'keys'):
                val = self.params[variable]
            else:
                val = self._params_dict[variable]['val']
            return val


    def __init__(self):
        '''Constructor for the FlopsWrapper component'''
        super(FlopsWrapper,self).__init__()
        self.add_param('input:title',val='none',typeVar='Str')#adding title for namecards
        self.loadInputVars()
        #top = Problem()
        #top.root =  Group()
        #top.root.add('my_flops',self)
        #top.setup(check=False)

        # External Code public variables

        self.input_filepath = 'flops.inp'
        self.output_filepath = 'flops.out'
        self.stderr = 'flops.err'

        self.options['external_input_files'] = [self.input_filepath]
        self.options['external_output_files'] = [self.output_filepath]
        self.options['command'] = ['flops',self.input_filepath,self.output_filepath]

        """self.external_files = [
            FileMetadata(path=self.stdin, input=True),
            FileMetadata(path=self.stdout),
            FileMetadata(path=self.stderr),
        ]"""


        # This stuff is global in the Java wrap.
        # These are used when adding and removing certain segments.
        self.nseg0 = 0
        self.npcon0 = 0
        self.nrern0 = 0
        self.npcons0 = []
        self.npcons0.append(0)
        self.nmseg = 0

    def generate_input(self):
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

        sb.add_container("input.option.Program_Control")

        sb.add_comment("\n  ! Plot files for XFLOPS Graphical Interface Postprocessor (MSMPLOT)")
        sb.add_var("input:option:Plot_Files:ixfl")

        sb.add_comment("\n  ! Takeoff and Climb Profile File for Noise Calculations (NPROF)")
        sb.add_var("input:option:Plot_Files:npfile")

        sb.add_comment("\n  ! Drag Polar Plot File (POLPLOT)")
        sb.add_var("input:option:Plot_Files:ipolp")
        sb.add_var("input:option:Plot_Files:polalt")








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





    def FlopsWrapper_input_wtin_Wing_Data(self):
        """Container for input:wtin:Wing_Data"""
        strChain = 'input:wtin:Wing_Data:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'span',val=0.0, units='ft', desc='Wing span (optional, see &CONFIN - SW and AR)',typerVar='Float')
        self.add_param(strChain+'dih',val=0.0, units='deg', desc='Wing dihedral (positive) or anhedral (negative) angle',typerVar='Float')
        self.add_param(strChain+'flapr',val=0.3330, desc='Flap ratio -- ratio of total movable wing surface area (flaps, elevators, spoilers, etc.) to wing area',typerVar='Float')
        self.add_param(strChain+'glov',val=0.0, units='ft*ft', desc='Total glove and bat area beyond theoretical wing',typerVar='Float')
        self.add_param(strChain+'varswp',val=0.0, desc='Fraction of wing variable sweep weight penalty = 0., Fixed-geometry wing = 1., Full variable-sweep wing',typerVar='Float')
        self.add_param(strChain+'fcomp',val=0.0, desc='Decimal fraction of amount of composites used in wing structure = 0., No composites = 1., Maximum use of composites, approximately equivalent to FRWI1=.6, FRWI2=.83, FRWI3=.7 (Not necessarily all composite) This only applies to the wing.  Use override parameters for other components such as FRHT=.75, FRVT=.75, FRFU=.82, FRLGN=.85, FRLGM=.85, FRNA=.8',typerVar='Float')
        self.add_param(strChain+'faert',val=0.0, desc='Decimal fraction of amount of aeroelastic tailoring used in design of wing = 0., No aeroelastic tailoring = 1., Maximum aeroelastic tailoring',typerVar='Float')
        self.add_param(strChain+'fstrt',val=0.0, desc='Wing strut-bracing factor = 0., No wing strut = 1., Full benefit from strut bracing',typerVar='Float')


    def FlopsWrapper_input_wtin_Tails_Fins(self):
        """Container for input:wtin:Tails_Fins"""
        strChain = 'input:wtin:Tails_Fins:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'sht',val=0.0, units='ft*ft', desc='Horizontal tail theoretical area',typerVar='Float')
        self.add_param(strChain+'swpht',val=-100.0, units='deg', desc='Horizontal tail 25% chord sweep angle (Default = SWEEP, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'arht',val=-100.0, desc='Horizontal tail theoretical aspect ratio (Default = AR/2, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'trht',val=-100.0, desc='Horizontal tail theoretical taper ratio (Default = TR, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'tcht',val=0.0, desc='Thickness-chord ratio for the horizontal tail (Default = TCA, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'hht',val=-100.0, desc='Decimal fraction of vertical tail span where horizontal tail is mounted = 0. for body mounted (Default for transports with all engines on the wing and for fighters) = 1. for T tail (Default for transports with multiple engines on the fuselage)',typerVar='Float')
        self.add_param(strChain+'nvert',val=1, desc='Number of vertical tails',typerVar='Int')
        self.add_param(strChain+'svt',val=0.0, units='ft*ft', desc='Vertical tail theoretical area (per tail)',typerVar='Float')
        self.add_param(strChain+'swpvt',val=-100.0, units='deg', desc='Vertical tail sweep angle at 25% chord (Default = SWPHT)',typerVar='Float')
        self.add_param(strChain+'arvt',val=-100.0, desc='Vertical tail theoretical aspect ratio (Default = ARHT/2)',typerVar='Float')
        self.add_param(strChain+'trvt',val=-100.0, desc='Vertical tail theoretical taper ratio (Default = TRHT)',typerVar='Float')
        self.add_param(strChain+'tcvt',val=0.0, desc='Thickness-chord ratio for the vertical tail (Default = TCHT)',typerVar='Float')
        self.add_param(strChain+'nfin',val=0, desc='Number of fins',typerVar='Int')
        self.add_param(strChain+'sfin',val=0.0, units='ft*ft', desc='Vertical fin theoretical area',typerVar='Float')
        self.add_param(strChain+'arfin',val=-100.0, desc='Vertical fin theoretical aspect ratio',typerVar='Float')
        self.add_param(strChain+'trfin',val=-100.0, desc='Vertical fin theoretical taper ratio',typerVar='Float')
        self.add_param(strChain+'swpfin',val=-100.0, units='deg', desc='Vertical fin sweep angle at 25% chord',typerVar='Float')
        self.add_param(strChain+'tcfin',val=0.0, desc='Vertical fin thickness - chord ratio',typerVar='Float')
        self.add_param(strChain+'scan',val=0.0, units='ft*ft', desc='Canard theoretical area',typerVar='Float')
        self.add_param(strChain+'swpcan',val=-100.0, units='deg', desc='Canard sweep angle at 25% chord',typerVar='Float')
        self.add_param(strChain+'arcan',val=-100.0, desc='Canard theoretical aspect ratio',typerVar='Float')
        self.add_param(strChain+'trcan',val=-100.0, desc='Canard theoretical taper ratio',typerVar='Float')
        self.add_param(strChain+'tccan',val=0.0, desc='Canard thickness-chord ratio (Default = TCHT)',typerVar='Float')


    def FlopsWrapper_input_wtin_Propulsion(self):
        """Container for input:wtin:Propulsion"""
        strChain = 'input:wtin:Propulsion:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'new',val=0, desc='Number of wing mounted engines',typerVar='Int')
        self.add_param(strChain+'nef',val=0, desc='Number of fuselage mounted engines',typerVar='Int')
        self.add_param(strChain+'thrso',val=0.0, units='lb', desc='Rated thrust of baseline engine as described in Engine Deck (Default = THRUST, see &CONFIN)',typerVar='Float')
        self.add_param(strChain+'weng',val=0.0, units='lb', desc='Weight of each baseline engine or bare engine if WINL and WNOZ (below) are supplied (Default = THRSO/5.5 for transports and THRSO/8 for fighters)',typerVar='Float')
        self.add_param(strChain+'eexp',val=1.15, desc='Engine weight scaling parameter\nW(Engine) = WENG*(THRUST/THRSO)**EEXP\nIf EEXP is less than 0.3,\nW(Engine) = WENG + (THRUST-THRSO)*EEXP',typerVar='Float')
        self.add_param(strChain+'winl',val=0.0, units='lb', desc='Inlet weight for baseline engine if not included in WENG above',typerVar='Float')
        self.add_param(strChain+'einl',val=1.0, desc='Inlet weight scaling exponent\nW(Inlet) = WINL*(THRUST/THRSO)**EINL',typerVar='Float')
        self.add_param(strChain+'wnoz',val=0.0, units='lb', desc='Nozzle weight for baseline engine if not included in WENG above',typerVar='Float')
        self.add_param(strChain+'enoz',val=1.0, desc='Nozzle weight scaling exponent\nW(Nozzle) = WNOZ*(THRUST/THRSO)**ENOZ',typerVar='Float')
        self.add_param(strChain+'xnac',val=0.0, units='ft', desc='Average length of baseline engine nacelles.  Scaled by SQRT(THRUST/THRSO)',typerVar='Float')
        self.add_param(strChain+'dnac',val=0.0, units='ft', desc='Average diameter of baseline engine nacelles.  Scaled by SQRT(THRUST/THRSO)',typerVar='Float')
        self.add_param(strChain+'wpmisc',val=0.0, desc='Additional miscellaneous propulsion system weight or fraction of engine weight if < 1.  This is added to the engine control and starter weight and may be overridden if WPMSC is input.',typerVar='Float')


    def FlopsWrapper_input_wtin_Override(self):
        """Container for input:wtin:Override"""
        strChain = 'input:wtin:Override:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'frwi',val=1.0, desc='Total wing weight - fixed weight overrides FRWI1, FRWI2, FRWI3, FRWI4 below, scale factor is cumulative \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n \n',typerVar='Float')
        self.add_param(strChain+'frwi1',val=1.0, desc='First term in wing weight equation - loosely corresponds to bending material weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n',typerVar='Float')
        self.add_param(strChain+'frwi2',val=1.0, desc='Second term in wing weight equation - loosely corresponds to control surfaces, spars and ribs \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component\n',typerVar='Float')
        self.add_param(strChain+'frwi3',val=1.0, desc='Third term in wing weight equation - miscellaneous, just because it',typerVar='Float')
        self.add_param(strChain+'frwi4',val=1.0, desc='Fourth term in wing weight equation - miscellaneous, just because it',typerVar='Float')
        self.add_param(strChain+'frht',val=1.0, desc='Horizontal tail weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frvt',val=1.0, desc='Vertical tail weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frfin',val=1.0, desc='Wing vertical fin weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frcan',val=1.0, desc='Canard weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frfu',val=1.0, desc='Fuselage weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frlgn',val=1.0, desc='Landing gear weight, nose \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frlgm',val=1.0, desc='Landing gear weight, main \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frna',val=1.0, desc='Total weight of nacelles and/or air induction system \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wthr',val=0.0, desc='Total weight of thrust reversers\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wpmsc',val=1.0, desc='Weight of miscellaneous propulsion systems such as engine controls, starter and wiring \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wfsys',val=1.0, desc='Weight of fuel system \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'frsc',val=1.0, desc='Surface controls weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wapu',val=1.0, desc='Auxiliary power unit weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'win',val=1.0, desc='Instrument Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'whyd',val=1.0, desc='Hydraulics Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'welec',val=1.0, desc='Electrical Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wavonc',val=1.0, desc='Avionics Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'warm',val=0.0, desc='Armament Group weight - includes thermal protection system or armor and fixed weapons\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wfurn',val=1.0, desc='Furnishings Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wac',val=1.0, desc='Air Conditioning Group weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wai',val=1.0, desc='Transports: Anti-icing Group weight\n            Fighters:   Auxiliary gear \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wuf',val=1.0, desc='Weight of unusable fuel \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'woil',val=1.0, desc='Engine oil weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wsrv',val=1.0, desc='Transports: Passenger service weight\n             Fighters: Ammunition and nonfixed weapons weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wcon',val=1.0, desc='Transports: Cargo and baggage container weight Fighters:   Miscellaneous operating items weight If < 0.5, as a fraction of Gross Weight \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wauxt',val=1.0, desc='Auxiliary fuel tank weight (Fighters only) \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wflcrb',val=1.0, desc='Total weight of flight crew and baggage\n           (Defaults:  Transports    - 225.*NFLCR\n           Fighters      - 215.*NFLCR\n           Carrier-based - 180.*NFLCR)\n           \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'wstuab',val=1.0, desc='Total weight of cabin crew and baggage (Default = 155.*NSTU + 200.*NGALC) \n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')
        self.add_param(strChain+'ewmarg',val=0.0, desc='Empty weight margin (Special Option) - delta weight added to Weight Empty.  If abs(EWMARG) < 5., it is interpreted as a fraction of calculated Weight Empty.  May be positive or negative\n < 0., negative of starting weight which will be modified as appropriate during optimization or parametric variation\n \n = 0., no weight for that component\n \n > 0. but < 5., scale factor applied to internally computed weight\n \n > 5., actual fixed weight for component',typerVar='Float')


    def FlopsWrapper_input_wtin_OEW_Calculations(self):
        """Container for input:wtin:OEW_Calculations:"""
        strChain = 'input:wtin:OEW_Calculations:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ispowe',val=0,optionsVal=(0,1), desc='= 0, Normal FLOPS weight equations will be used\n= 1, Special equation for Operating Weight Empty will be used:\n            \n            OWE = SPWTH*THRUST + SPWSW*SW + SPWGW*GW + SPWCON\n            \n            Structures group weights will be scaled to meet the calculated OWE.\n            \n            = 2, Use response surface for weights - available only in DOSS version', aliases=('Normal FLOPS', 'Special eqn for OEW'),typerVar='Enum')
        self.add_param(strChain+'spwth',val=2.2344, units='lb/lb', desc='Multiplier for thrust/engine in special equation for Operating Weight Empty\nSPWTH = \n                                  AIRFLOWref\n(PODsclr + dOEWsclr) * ------------\n                               SLSTHRUSTref\n            ',typerVar='Float')
        self.add_param(strChain+'spwsw',val=9.5, units='psf', desc='Multiplier for wing area in special equation for Operating Weight Empty',typerVar='Float')
        self.add_param(strChain+'spwgw',val=0.104087, units='lb/lb', desc='Multiplier for gross weight in special equation for Operating Weight Empty\nSPWGW = \n            MTOWsclr+OEWgrwth*MTOWgrwth\n        -----------------------------------\n            1. + MTOWgrowth\n\n',typerVar='Float')
        self.add_param(strChain+'spwcon',val=38584.0, units='lb', desc='Constant weight term in special equation for Operating Weight Empty\n            \nSPWCON = OEWuncycled\n            - MTOWscalar*MTOWuncycled\n            - WINGscalar*SWref\n            - (PODscalar + dOEWscalar)\n            *AIRFLOWref\n',typerVar='Float')


    def FlopsWrapper_input_wtin_Landing_Gear(self):
        """Container for input:wtin:Landing_Gear"""
        strChain = 'input:wtin:Landing_Gear:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xmlg',val=0.0, units='inch', desc='Length of extended main landing gear oleo (Default is computed internally)',typerVar='Float')
        self.add_param(strChain+'xnlg',val=0.0, units='inch', desc='Length of extended nose landing gear oleo (Default is computed internally)',typerVar='Float')
        self.add_param(strChain+'wldg',val=0.0, units='lb', desc='Design landing weight (if WRATIO is input in Namelist &AERIN, WLDG = GW*WRATIO) See Namelist &AERIN for WRATIO defaults.',typerVar='Float')
        self.add_param(strChain+'mldwt',val=0,optionsVal=(1,0), desc='= 1, The design landing weight is set to the end of descent weight for the main mission plus DLDWT.  Use only if IRW = 1 in Namelist &MISSIN.  = 0, The design landing weight is determined by WLDG above or WRATIO in Namelist &AERIN',typerVar='Enum')
        self.add_param(strChain+'dldwt',val=0.0, units='lb', desc='Delta landing weight for MLDWT = 1',typerVar='Float')
        self.add_param(strChain+'carbas',val=0.0, desc='Carrier based aircraft switch, affects weight of flight crew, avionics and nose gear = 1., Carrier based = 0., Land based',typerVar='Float')


    def FlopsWrapper_input_wtin_Inertia(self):
        """Container for input:wtin:Inertia"""
        strChain = 'input:wtin:Inertia:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inrtia',val=0,optionsVal=(1,0), desc='= 1, Aircraft inertias will be calculated = 0, Otherwise', aliases=('Calculate', 'Do not calculate'),typerVar='Enum')
        self.add_param(strChain+'zht',val=0.0, units='inch', desc='Vertical C.G. of the horizontal tail (optional)',typerVar='Float')
        self.add_param(strChain+'zvt',val=0.0, units='inch', desc='Vertical C.G. of the vertical tail (optional)',typerVar='Float')
        self.add_param(strChain+'zfin',val=0.0, units='inch', desc='Vertical C.G. of the vertical fin (optional)',typerVar='Float')
        self.add_param(strChain+'yfin',val=0.0, units='inch', desc='Lateral C.G. of the vertical fin (optional)',typerVar='Float')
        self.add_param(strChain+'zef',val=0.0, units='inch', desc='Vertical C.G. of two forward mounted engines (optional)',typerVar='Float')
        self.add_param(strChain+'yef',val=0.0, units='inch', desc='Lateral C.G. of two forward mounted engines (optional, may be input as a fraction of the semispan)',typerVar='Float')
        self.add_param(strChain+'zea',val=0.0, units='inch', desc='Vertical C.G. of one or two aft mounted engines (optional)',typerVar='Float')
        self.add_param(strChain+'yea',val=0.0, units='inch', desc='Lateral C.G. of one or two aft mounted engines (optional, may be input as a fraction of the semispan)',typerVar='Float')
        self.add_param(strChain+'zbw',val=0.0, units='inch', desc='Lowermost point of wing root airfoil section',typerVar='Float')
        self.add_param(strChain+'zap',val=0.0, units='inch', desc='Vertical C.G. of Auxiliary Power Unit (optional)',typerVar='Float')
        self.add_param(strChain+'zrvt',val=0.0, units='inch', desc='Vertical datum line (Water Line) of vertical tail theoretical root chord (optional, if blank assumes at maximum height of fuselage)',typerVar='Float')
        self.add_param(strChain+'ymlg',val=0.0, units='inch', desc='Lateral C.G. of extended main landing gear',typerVar='Float')
        self.add_param(strChain+'yfuse',val=0.0, units='inch', desc='Lateral C.G. of outboard fuselage if there is more than one fuselage',typerVar='Float')
        self.add_param(strChain+'yvert',val=0.0, units='inch', desc='Lateral C.G. of outboard vertical tail if there is more than one vertical tail',typerVar='Float')
        self.add_param(strChain+'swtff',val=0.0, desc='Gross fuselage wetted area (Default = internally computed)',typerVar='Float')
        self.add_param(strChain+'tcr',val=0.0, desc='Wing root thickness-chord ratio (Default = TOC(0) or TCA in &CONFIN)',typerVar='Float')
        self.add_param(strChain+'tct',val=0.0, desc='Wing tip thickness-chord ratio (Default = TOC(NETAW) or TCA in &CONFIN)',typerVar='Float')
        self.add_param(strChain+'incpay',val=0,optionsVal=(1,0), desc='For inertia calculations, all mission fuel is placed in "tanks." \n \n = 1, Include passengers, passenger baggage, and cargo in the fuselage and contents for inertia calculations. \n \n = 0, For inertia calculations, all payload (passengers, passenger baggage, and cargo) are placed in "tanks" like the fuel', aliases=('Passengers-etc in fuse', 'All payload in tanks'),typerVar='Enum')
        self.add_param(strChain+'tx',val=array([]), units='inch', desc='x coordinates of the centroid of the Ith tank',typerVar='Array')
        self.add_param(strChain+'ty',val=array([]), units='inch', desc='y coordinates of the centroid of the Ith tank',typerVar='Array')
        self.add_param(strChain+'tz',val=array([]), units='inch', desc='z coordinates of the centroid of the Ith tank',typerVar='Array')
        self.add_param(strChain+'tl',val=array([]), desc='Length of the Ith tank (optional, used only in calculating I0',typerVar='Array')
        self.add_param(strChain+'tw',val=array([]), desc='Width of the Ith tank (optional, used only in calculating I0',typerVar='Array')
        self.add_param(strChain+'td',val=array([]), desc='Depth of the Ith tank (optional, used only in calculating I0',typerVar='Array')
        self.add_param(strChain+'tf',val=array([]), units='lb', desc='Weight of fuel (or payload) in Ith tank for the Jth fuel condition NOTE: Dimensions are [J,I]',typerVar='Array')


    def FlopsWrapper_input_wtin_Fuselage(self):
        """Container for input:wtin:Fuselage"""
        strChain = 'input:wtin:Fuselage:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'nfuse',val=1, desc='Number of fuselages',typerVar='Int')
        self.add_param(strChain+'xl',val=0.0, units='ft', desc='Fuselage total length (See Fuselage Design Data)',typerVar='Float')
        self.add_param(strChain+'wf',val=0.0, units='ft', desc='Maximum fuselage width',typerVar='Float')
        self.add_param(strChain+'df',val=0.0, units='ft', desc='Maximum fuselage depth',typerVar='Float')
        self.add_param(strChain+'xlp',val=0.0, units='ft', desc='Length of passenger compartment (Default is internally computed)',typerVar='Float')


    def FlopsWrapper_input_wtin_Fuel_System(self):
        """Container for input:wtin:Fuel_System"""
        strChain = 'input:wtin:Fuel_System:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ntank',val=7, desc='Number of fuel tanks',typerVar='Int')
        self.add_param(strChain+'fulwmx',val=-1.0, units='lb', desc='Total fuel capacity of wing.  The default is internally calculated from:\n \n                             TCA * SW**2         TR\n FULWMX = FWMAX * ---------- * ( 1 - -------- )\n                                SPAN         (1+TR)**2\n \n Where the default value of FWMAX is 23.  If FULWMX is input < 50, it is interpreted as FWMAX and the above equation is used.  This equation is also used for scaling when the wing area, t/c, aspect ratio, or taper ratio is varied or optimized.\n \n Alternatively,  FULWMX = FUELRF + FUSCLA*(SW**1.5 - FSWREF**1.5)\n + FUSCLB*(SW - FSWREF)\n',typerVar='Float')
        self.add_param(strChain+'fulden',val=1.0, desc='Fuel density ratio for alternate fuels compared to jet fuel (typical density of 6.7 lb/gal), used in the calculation of FULWMX (if FULWMX is not input) and in the calculation of fuel system weight.',typerVar='Float')
        self.add_param(strChain+'fuelrf',val=0.0, units='lb', desc='Fuel capacity at FSWREF for alternate method',typerVar='Float')
        self.add_param(strChain+'fswref',val=-1.0, units='ft*ft', desc='Reference wing area for alternate method (Default = SW in Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'fuscla',val=0.0, desc='Alternate fuel capacity scaling method - Factor A',typerVar='Float')
        self.add_param(strChain+'fusclb',val=0.0, desc='Alternate fuel capacity scaling method - Factor B',typerVar='Float')
        self.add_param(strChain+'fulfmx',val=0.0, desc='Total fuel capacity of fuselage (wing ',typerVar='Float')
        self.add_param(strChain+'ifufu',val=0, desc='= 1, Fuselage fuel capacity is adjusted to meet the required fuel capacity for the primary mission.  Use only if IRW = 1 in Namelist &MISSIN, and use with care - some passengers can',typerVar='Int')
        self.add_param(strChain+'fulaux',val=0.0, units='lb', desc='Auxiliary (external) fuel tank capacity (Fighters only)',typerVar='Float')


    def FlopsWrapper_input_wtin_Detailed_Wing(self):
        """Container for input:wtin:Detailed_Wing"""
        strChain = 'input:wtin:Detailed_Wing:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'etaw',val=numpy_float64, desc='Wing station location - fraction of semispan or distance from fuselage centerline.  Typically, goes from 0. to 1.  Input fixed distances (>1.1) are not scaled with changes in span.',typerVar='Array')
        self.add_param(strChain+'chd',val=numpy_float64, desc='Chord length - fraction of semispan or actual chord.   Actual chord lengths (>5.) are not scaled.',typerVar='Array')
        self.add_param(strChain+'toc',val=numpy_float64, desc='Thickness - chord ratio',typerVar='Array')
        self.add_param(strChain+'swl',val=numpy_float64, units='deg', desc='Sweep of load path.  Typically parallel to rear spar tending toward max t/c of airfoil.  The Ith value is used between wing stations I and I+1.',typerVar='Array')
        self.add_param(strChain+'etae',val=array([0.3, 0.6, 0.0, 0.0]), dtype=numpy_float64, desc='Engine locations - fraction of semispan or distance from fuselage centerline.  Actual distances are not scaled with changes in span.  NEW/2 values are input',typerVar='Array')
        self.add_param(strChain+'pctl',val=1.0, desc='Fraction of load carried by defined wing',typerVar='Float')
        self.add_param(strChain+'arref',val=0.0, desc='Reference aspect ratio (Default = AR in &CONFIN)',typerVar='Float')
        self.add_param(strChain+'tcref',val=0.0, desc='Reference thickness-chord ratio (Default = TCA in &CONFIN)',typerVar='Float')
        self.add_param(strChain+'nstd',val=50, desc='Number of integration stations',typerVar='Int')
        self.add_param(strChain+'pdist',val=2.0, desc='Pressure distribution indicator\n= 0., Input distribution - see below\n= 1., Triangular distribution\n= 2., Elliptical distribution\n= 3., Rectangular distribution PDIST is a continuous variable, i.e., a value of 1.5 would be half way between triangular and elliptical.\nCAUTION - the constants in the wing weight calculations were correlated with existing aircraft assuming an elliptical distribution.  Use the default value unless you have a good reason not to.',typerVar='Float')
        self.add_param(strChain+'etap',val=numpy_float64, desc='Fraction of wing semispan',typerVar='Array')
        self.add_param(strChain+'pval',val=numpy_float64, desc='Relative spanwise pressure at ETAP(J)',typerVar='Array')


    def FlopsWrapper_input_wtin_Crew_Payload(self):
        """Container for input:wtin:Crew_Payload"""
        strChain = 'input:wtin:Crew_Payload:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'npf',val=0, desc='Number of first class passengers',typerVar='Int')
        self.add_param(strChain+'npb',val=0, desc='Number of business class passengers',typerVar='Int')
        self.add_param(strChain+'npt',val=0, desc='Number of tourist passengers',typerVar='Int')
        self.add_param(strChain+'nstu',val=-1, desc='Number of flight attendants (optional)',typerVar='Int')
        self.add_param(strChain+'ngalc',val=-1, desc='Number of galley crew (optional)',typerVar='Int')
        self.add_param(strChain+'nflcr',val=-1, desc='Number of flight crew (optional)',typerVar='Int')
        self.add_param(strChain+'wppass',val=165.0, units='lb', desc='Weight per passenger',typerVar='Float')
        self.add_param(strChain+'bpp',val=-1.0, units='lb', desc='Weight of baggage per passenger (Default = 35., or 40. if DESRNG in Namelist &CONFIN > 900., or 44. if DESRNG > 2900.)',typerVar='Float')
        self.add_param(strChain+'cargf',val=0.0, desc='Military cargo aircraft floor factor = 0., Passenger transport\n= 1., Military cargo transport floor',typerVar='Float')
        self.add_param(strChain+'cargow',val=0.0, units='lb', desc='Cargo carried in wing (Weight of wing-mounted external stores for fighters)',typerVar='Float')
        self.add_param(strChain+'cargof',val=0.0, units='lb', desc='Cargo (other than passenger baggage) carried in fuselage (Fuselage external stores for fighters)',typerVar='Float')


    def FlopsWrapper_input_wtin_Center_of_Gravity(self):
        """Container for input:wtin:Center_of_Gravity"""
        strChain = 'input:wtin:Center_of_Gravity:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cgw',val=0.0, units='inch', desc='Longitudinal C.G. of wing',typerVar='Float')
        self.add_param(strChain+'cght',val=0.0, units='inch', desc='Longitudinal C.G. of horizontal tail',typerVar='Float')
        self.add_param(strChain+'cgvt',val=0.0, units='inch', desc='Longitudinal C.G. of vertical tail',typerVar='Float')
        self.add_param(strChain+'cgfin',val=0.0, units='inch', desc='Longitudinal C.G. of wing vertical fins',typerVar='Float')
        self.add_param(strChain+'cgcan',val=0.0, units='inch', desc='Longitudinal C.G. of canard',typerVar='Float')
        self.add_param(strChain+'cgf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage',typerVar='Float')
        self.add_param(strChain+'cglgn',val=0.0, units='inch', desc='Longitudinal C.G. of nose landing gear',typerVar='Float')
        self.add_param(strChain+'cglgm',val=0.0, units='inch', desc='Longitudinal C.G. of main landing gear',typerVar='Float')
        self.add_param(strChain+'cgef',val=0.0, units='inch', desc='Longitudinal C.G. of two forward mounted engines',typerVar='Float')
        self.add_param(strChain+'cgea',val=0.0, units='inch', desc='Longitudinal C.G. of one or two aft mounted engines',typerVar='Float')
        self.add_param(strChain+'cgap',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary power unit',typerVar='Float')
        self.add_param(strChain+'cgav',val=0.0, units='inch', desc='Longitudinal C.G. of avionics group (optional)',typerVar='Float')
        self.add_param(strChain+'cgarm',val=0.0, units='inch', desc='Longitudinal C.G. of armament group - includes thermal protection system or armor and fixed weapons (Default = CGF)',typerVar='Float')
        self.add_param(strChain+'cgcr',val=0.0, units='inch', desc='Longitudinal C.G. of flight crew',typerVar='Float')
        self.add_param(strChain+'cgp',val=0.0, units='inch', desc='Longitudinal C.G. of passengers',typerVar='Float')
        self.add_param(strChain+'cgcw',val=0.0, units='inch', desc='Longitudinal C.G. of wing cargo or external stores',typerVar='Float')
        self.add_param(strChain+'cgcf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage cargo or external stores',typerVar='Float')
        self.add_param(strChain+'cgzwf',val=0.0, units='inch', desc='Longitudinal C.G. of fuselage fuel',typerVar='Float')
        self.add_param(strChain+'cgfwf',val=0.0, units='inch', desc='Longitudinal C.G. of wing fuel in full condition',typerVar='Float')
        self.add_param(strChain+'cgais',val=0.0, units='inch', desc='Longitudinal C.G. of air induction system',typerVar='Float')
        self.add_param(strChain+'cgacon',val=0.0, units='inch', desc='Longitudinal C.G. of air conditioning system',typerVar='Float')
        self.add_param(strChain+'cgaxg',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary gear',typerVar='Float')
        self.add_param(strChain+'cgaxt',val=0.0, units='inch', desc='Longitudinal C.G. of auxiliary tanks',typerVar='Float')
        self.add_param(strChain+'cgammo',val=0.0, units='inch', desc='Longitudinal C.G. of ammunition and nonfixed weapons',typerVar='Float')
        self.add_param(strChain+'cgmis',val=0.0, units='inch', desc='Longitudinal C.G. of miscellaneous operating items',typerVar='Float')


    def FlopsWrapper_input_wtin_Basic(self):
        """Container for input:wtin:Basic"""
        strChain = 'input:wtin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ulf',val=3.75, desc='Structural ultimate load factor',typerVar='Float')
        self.add_param(strChain+'dgw',val=1.0, units='lb', desc='Design gross weight - fraction of GW (see &CONFIN) or weight',typerVar='Float')
        self.add_param(strChain+'vmmo',val=0.0, desc='Maximum operating Mach number (Default = VCMN, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'nwref',val=39,optionsVal=(39,37,33,26), desc='The number of the reference weight for percentage weight output.', aliases=('Ramp weight', 'Zero fuel weight', 'Operating weight empty', 'Weight empty'),typerVar='Enum')
        self.add_param(strChain+'cgrefl',val=0.0, units='inch', desc='Reference length for percentage C.G. location output (Default = XL*12., fuselage length)',typerVar='Float')
        self.add_param(strChain+'cgrefx',val=0.0, units='inch', desc='X - location of start of reference length',typerVar='Float')
        self.add_param(strChain+'mywts',val=0,optionsVal=(0,1), desc='= 0, Weights will be computed\n = 1, Otherwise (See User-Specified Weights, Namelist &MISSIN)', aliases=('Compute weight', 'User-specified'),typerVar='Enum')
        self.add_param(strChain+'hydpr',val=3000.0, units='psi', desc='Hydraulic system pressure',typerVar='Float')
        self.add_param(strChain+'wpaint',val=0.0, units='psf', desc='Weight of paint for all wetted areas',typerVar='Float')
        self.add_param(strChain+'ialtwt',val=0,optionsVal=(0,1), desc='= 1, Alternate weight equations for some components will be used (Special option)\n= 0, Normal FLOPS weight equations will be used', aliases=('Normal', 'Alternate'),typerVar='Enum')




    def FlopsWrapper_input_tolin_Thrust_Reverser(self):
        """Container for input:tolin:Thrust_Reverser"""
        strChain = 'input:tolin:Thrust_Reverser:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inthrv',val=-1, desc='= -1, Use takeoff thrust\n=  0, Input thrust values will be used\n=  1, Input values will be scaled\n>  1, Scaled engine deck for the (INTHRV-1)th power setting will be used',typerVar='Int')
        self.add_param(strChain+'rvfact',val=0.0, desc='Fraction of thrust reversed - net  (Real values should be negative)',typerVar='Float')
        self.add_param(strChain+'velrv',val=numpy_float64, units='ft/s', desc='Velocities for reverse thrust',typerVar='Array')
        self.add_param(strChain+'thrrv',val=numpy_float64, units='lb', desc='Thrust values',typerVar='Array')
        self.add_param(strChain+'tirvrs',val=5.0, units='s', desc='Time after touchdown to reverse thrust',typerVar='Float')
        self.add_param(strChain+'revcut',val=-1000.0, units='nmi', desc='Cutoff velocity for thrust reverser',typerVar='Float')
        self.add_param(strChain+'clrev',val=0.0, desc='Change in lift coefficient due to thrust reverser',typerVar='Float')
        self.add_param(strChain+'cdrev',val=0.0, desc='Change in drag coefficient due to thrust reverser',typerVar='Float')


    def FlopsWrapper_input_tolin_Takeoff(self):
        """Container for input:tolin:Takeoff"""
        strChain = 'input:tolin:Takeoff:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cltom',val=-1.0, desc='Maximum CL for takeoff (Default, see &AERIN)',typerVar='Float')
        self.add_param(strChain+'cdmto',val=0.0, desc='Minimum CD for takeoff, typically, this is the drag coefficient at zero lift',typerVar='Float')
        self.add_param(strChain+'fcdmto',val=0.3, desc='Fraction of CDMTO due to wing',typerVar='Float')
        self.add_param(strChain+'almxto',val=25.0, units='deg', desc='Maximum angle of attack during takeoff',typerVar='Float')
        self.add_param(strChain+'obsto',val=-1.0, units='ft', desc='Takeoff obstacle height (Defaults, Transport = 35., Fighter = 50.)',typerVar='Float')
        self.add_param(strChain+'alpto',val=array([-100.0]), dtype=numpy_float64, units='deg', desc='Angles of attack for takeoff polar',typerVar='Array')
        self.add_param(strChain+'clto',val=array([-100.0]), dtype=numpy_float64, desc='Lift coefficients for takeoff polar.  These are not generated internally',typerVar='Array')
        self.add_param(strChain+'cdto',val=array([-100.0]), dtype=numpy_float64, desc='Drag coefficients for takeoff polar.  These are not generated internally',typerVar='Array')
        self.add_param(strChain+'inthto',val=0, desc='= 0, Input thrust values will be used\n= 1, The input values will be scaled\n> 1, Scaled engine data deck for the (INTHTO-1)th power setting will be used',typerVar='Int')
        self.add_param(strChain+'velto',val=numpy_float64, units='ft/s', desc='Velocities for takeoff thrust',typerVar='Array')
        self.add_param(strChain+'thrto',val=numpy_float64, units='lb', desc='Thrust values',typerVar='Array')
        self.add_param(strChain+'alprot',val=-100.0, desc='Maximum angle of attack during rotation phase of takeoff (Default = ALMXTO)',typerVar='Float')
        self.add_param(strChain+'vrotat',val=1.05, desc='Minimum rotation start speed, knots or fraction of Vstall',typerVar='Float')
        self.add_param(strChain+'vangl',val=2.0, units='deg/s', desc='Rotation rate',typerVar='Float')
        self.add_param(strChain+'thfact',val=1.0, desc='Thrust multiplier for input or extracted thrust data',typerVar='Float')
        self.add_param(strChain+'ftocl',val=1.0, desc='Factor for takeoff lift.  Also applied to drag polars input in &PROIN',typerVar='Float')
        self.add_param(strChain+'ftocd',val=1.0, desc='Factor for takeoff drag.  Also applied to drag polars input in &PROIN',typerVar='Float')
        self.add_param(strChain+'igobs',val=0,optionsVal=(0,1), desc='Gear retraction switch', aliases=('Liftoff + TDELG', 'Obstacle + TDELG'),typerVar='Enum')
        self.add_param(strChain+'tdelg',val=0.0, units='s', desc='Time delay after liftoff/obstacle before start of landing gear retraction',typerVar='Float')
        self.add_param(strChain+'tigear',val=2.0, units='s', desc='Time required to retract landing gear.  Landing gear drag is reduced using a cosine function.',typerVar='Float')
        self.add_param(strChain+'ibal',val=1,optionsVal=(1,2,0), desc='Option to compute balanced field length', aliases=('pre-1998 FAA rules', 'post-1998 FAA rules', 'Do not compute'),typerVar='Enum')
        self.add_param(strChain+'itxout',val=0,optionsVal=(1,0), desc='Weight to use for takeoff field length calculations', aliases=('Ramp weight - taxi out fuel', 'Ramp weight'),typerVar='Enum')
        self.add_param(strChain+'pilott',val=1.0, units='s', desc='Actual pilot reaction time from engine failure to brake application.  Spoilers, brakes, and thrust reversal are assumed to become effective and engine cutback occurs at PILOTT + 2 seconds after engine failure.',typerVar='Float')
        self.add_param(strChain+'tispa',val=0.0, units='s', desc='Not currently used',typerVar='Float')
        self.add_param(strChain+'tibra',val=0.0, units='s', desc='Not currently used',typerVar='Float')
        self.add_param(strChain+'tirva',val=0.0, units='s', desc='Not currently used',typerVar='Float')
        self.add_param(strChain+'ispol',val=1,optionsVal=(0,1), desc='Option for spoiler use during aborted takeoff', aliases=('Not used', 'Used'),typerVar='Enum')
        self.add_param(strChain+'irev',val=1,optionsVal=(0,1,2), desc='Option for thrust reversal during aborted takeoff', aliases=('Not used', 'Only if all engines operational', 'Always used'),typerVar='Enum')


    def FlopsWrapper_input_tolin_Landing(self):
        """Container for input:tolin:Landing"""
        strChain = 'input:tolin:Landing:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'clldm',val=-1.0, desc='Maximum CL for landing (Default, see &AERIN)',typerVar='Float')
        self.add_param(strChain+'cdmld',val=0.0, desc='Minimum CD for landing',typerVar='Float')
        self.add_param(strChain+'fcdmld',val=-1.0, desc='Fraction of CDMLD due to wing (Default = FCDMTO)',typerVar='Float')
        self.add_param(strChain+'almxld',val=25.0, units='deg', desc='Maximum angle of attack during landing',typerVar='Float')
        self.add_param(strChain+'obsld',val=50.0, units='ft', desc='Landing obstacle height',typerVar='Float')
        self.add_param(strChain+'alpld',val=numpy_float64, units='deg', desc='Angles of attack for landing polar',typerVar='Array')
        self.add_param(strChain+'clld',val=numpy_float64, desc='Lift coefficients for landing polar.  These are not generated internally',typerVar='Array')
        self.add_param(strChain+'cdld',val=numpy_float64, desc='Drag coefficients for landing polar.  These are not generated internally',typerVar='Array')
        self.add_param(strChain+'inthld',val=0, desc='= 0, Input thrust values will be used\n= 1, The input values will be scaled\n> 1, Scaled engine data deck will be used',typerVar='Int')
        self.add_param(strChain+'velld',val=numpy_float64, units='ft/s', desc='Velocities for landing',typerVar='Array')
        self.add_param(strChain+'thrld',val=numpy_float64, units='lb', desc='Thrust values',typerVar='Array')
        self.add_param(strChain+'thdry',val=-1.0, units='lb', desc='Maximum dry thrust at missed appproach for fighters (Default = takeoff thrust)',typerVar='Float')
        self.add_param(strChain+'aprhgt',val=100.0, units='ft', desc='Height above ground for start of approach',typerVar='Float')
        self.add_param(strChain+'aprang',val=-3.0, units='deg', desc='Approach flight path angle',typerVar='Float')
        self.add_param(strChain+'fldcl',val=1.0, desc='Factor for landing lift',typerVar='Float')
        self.add_param(strChain+'fldcd',val=1.0, desc='Factor for landing drag',typerVar='Float')
        self.add_param(strChain+'tdsink',val=0.0, units='ft/s', desc='Sink rate at touchdown (Must be positive if input)',typerVar='Float')
        self.add_param(strChain+'vangld',val=0.0, units='deg/s', desc='Flare rate (Default = VANGL)',typerVar='Float')
        self.add_param(strChain+'noflar',val=0,optionsVal=(1,0), desc='Option for flare during landing.  If no flare, sink rate at touchdown is the approach sink rate with ground effects.', aliases=('No flare', 'Flare'),typerVar='Enum')
        self.add_param(strChain+'tispol',val=2.0, units='s', desc='Time after touchdown to spoiler actuation',typerVar='Float')
        self.add_param(strChain+'ticut',val=3.0, units='s', desc='Time after touchdown to cut back of engines to zero thrust',typerVar='Float')
        self.add_param(strChain+'tibrak',val=4.0, units='s', desc='Time after touchdown to brake application',typerVar='Float')
        self.add_param(strChain+'acclim',val=16.0, units='ft/(s*s)', desc='Deceleration limit',typerVar='Float')
        self.add_param(strChain+'magrup',val=-1,optionsVal=(1,0,-1), desc='Missed approach landing gear switch', aliases=('Gear up during missed approach', 'Gear down during missed approach', 'Use default'),typerVar='Enum')


    def FlopsWrapper_input_tolin_Integration_Intervals(self):
        """Container for input:tolin:Integration_Intervals"""
        strChain = 'input:tolin:Integration_Intervals:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'delvto',val=4.0, units='ft/s', desc='Velocity step during ground run',typerVar='Float')
        self.add_param(strChain+'deltro',val=0.2, units='s', desc='Time step during rotation',typerVar='Float')
        self.add_param(strChain+'deltcl',val=0.2, units='s', desc='Time step during climbout',typerVar='Float')
        self.add_param(strChain+'delhap',val=10.0, units='ft', desc='Altitude step during approach',typerVar='Float')
        self.add_param(strChain+'deldfl',val=10.0, units='ft', desc='Distance step during flare',typerVar='Float')
        self.add_param(strChain+'deltrn',val=0.25, units='s', desc='Time step during runout',typerVar='Float')


    def FlopsWrapper_input_tolin_Basic(self):
        """Container for input:tolin:Basic"""
        strChain = 'input:tolin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'apa',val=0.0, units='ft', desc='Airport altitude',typerVar='Float')
        self.add_param(strChain+'dtct',val=0.0, units='degC', desc='Delta temperature from standard day.  (This parameter is independent from the DTC in Namelist &MISSIN and DTCE in Namelist &ENGINE.)',typerVar='Float')
        self.add_param(strChain+'swref',val=-1.0, units='ft*ft', desc='Wing area on which takeoff and landing drag polars are based (Default = SW, Namelist &CONFIN). If different from SW, polars will be scaled.',typerVar='Float')
        self.add_param(strChain+'arret',val=-1.0, desc='Wing aspect ratio on which takeoff and landing drag polars are based (Default = AR, Namelist &CONFIN). If different from AR, polars will be modified.',typerVar='Float')
        self.add_param(strChain+'whgt',val=8.0, units='ft', desc='Wing height above ground',typerVar='Float')
        self.add_param(strChain+'alprun',val=0.0, units='deg', desc='Angle of attack on ground',typerVar='Float')
        self.add_param(strChain+'tinc',val=0.0, units='deg', desc='Thrust incidence on ground',typerVar='Float')
        self.add_param(strChain+'rollmu',val=0.025, desc='Coefficient of rolling friction',typerVar='Float')
        self.add_param(strChain+'brakmu',val=0.3, desc='Coefficient of friction, brakes on',typerVar='Float')
        self.add_param(strChain+'cdgear',val=0.0, desc='Landing gear drag coefficient',typerVar='Float')
        self.add_param(strChain+'cdeout',val=0.0, desc='Delta drag coefficient due to engine out condition.  Includes effect of stopped or windmilling engine and the trim drag associated with compensating for asymmetric thrust.',typerVar='Float')
        self.add_param(strChain+'clspol',val=0.0, desc='Spoiler delta lift coefficient (Should be negative)',typerVar='Float')
        self.add_param(strChain+'cdspol',val=0.0, desc='Spoiler delta drag coefficient',typerVar='Float')
        self.add_param(strChain+'incgef',val=1,optionsVal=(1,0), desc='Ground effects switch', aliases=('Ground effects', 'No ground effects'),typerVar='Enum')
        self.add_param(strChain+'argef',val=1.0, desc='Aspect ratio factor for ground effects',typerVar='Float')
        self.add_param(strChain+'itime',val=0,optionsVal=(1,0), desc='Detailed takeoff and landing profiles print option', aliases=('Print', 'No print'),typerVar='Enum')




    def FlopsWrapper_input_syntin_Variables(self):
        """Container for input:syntin:Variables"""
        strChain = 'input:syntin:Variables:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'desrng',val=-1.0, desc='Design range, n.mi. (or endurance, min.). See INDR in Namelist &MISSIN (Overrides input in Namelist &CONFIN).',typerVar='Float')
        self.add_param(strChain+'vappr',val=-1.0, units='nmi', desc='Maximum allowable landing approach velocity (Overrides input in Namelist &AERIN)',typerVar='Float')
        self.add_param(strChain+'flto',val=-1.0, units='ft', desc='Maximum allowable takeoff field length (Overrides input in Namelist &AERIN)',typerVar='Float')
        self.add_param(strChain+'flldg',val=-1.0, units='ft', desc='Maximum allowable landing field length (Overrides input in Namelist &AERIN)',typerVar='Float')
        self.add_param(strChain+'exfcap',val=0.0, units='lb', desc='Minimum allowable excess fuel capacity',typerVar='Float')
        self.add_param(strChain+'cdtmax',val=-1.0, units='degR', desc='Maximum allowable compressor discharge temperature (Overrides input in Namelist &ENGINE',typerVar='Float')
        self.add_param(strChain+'cdpmax',val=-1.0, units='psi', desc='Maximum allowable compressor discharge pressure (Overrides input in Namelist &ENGINE',typerVar='Float')
        self.add_param(strChain+'vjmax',val=-1.0, units='ft/s', desc='Maximum allowable jet velocity (Overrides input in Namelist &ENGINE',typerVar='Float')
        self.add_param(strChain+'stmin',val=-1.0, units='lb/lb/s', desc='Minimum allowable specific thrust (Overrides input in Namelist &ENGINE',typerVar='Float')
        self.add_param(strChain+'armax',val=-1.0, desc='Maximum allowable ratio of the bypass area to the core area of a mixed flow turbofan (Overrides input in Namelist &ENGINE',typerVar='Float')
        self.add_param(strChain+'gnox',val=0.0, units='lb', desc='Maximum allowable NOx emissions',typerVar='Float')
        self.add_param(strChain+'roclim',val=100.0, units='ft/min', desc='Minimum allowable potential rate of climb during climb segments',typerVar='Float')
        self.add_param(strChain+'dhdtlm',val=100.0, units='ft/min', desc='Minimum allowable actual rate of climb during climb segments',typerVar='Float')
        self.add_param(strChain+'tmglim',val=0.1, desc='Minimum allowable thrust margin, (Thrust-Drag)/Drag, during climb segments',typerVar='Float')
        self.add_param(strChain+'ig',val=numpy_int64, desc='= 1, Ith behavioral constraint is used in optimization\n= 0, Otherwise',typerVar='Array')
        self.add_param(strChain+'ibfgs',val=1,optionsVal=(0,1,2,3,4,5), desc='Search algorithm for optimization', aliases=('Davidon-Fletcher-Powell', 'Broyden-Fletcher-Goldfarb-Shano', 'Conjugate Gradient (Polak-Ribiere)', 'Steepest Descent', 'Univariate Search', 'Kreisselmeier-Steinhauser with DFP'),typerVar='Enum')
        self.add_param(strChain+'itfine',val=0,optionsVal=(1,0), desc='Option to set IRW = 1 for final analysis', aliases=('Yes', 'No'),typerVar='Enum')


    def FlopsWrapper_input_syntin_Optimization_Control(self):
        """Container for input:syntin:Optimization_Control"""
        strChain = 'input:syntin:Optimization_Control:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ndd',val=0, desc='Number of drawdowns (Defaults to analysis only - no optimization is performed.  Suggested value = 3 or 4)',typerVar='Int')
        self.add_param(strChain+'rk',val=0.0, desc='Initial value of RK (Default internally computed)',typerVar='Float')
        self.add_param(strChain+'fdd',val=0.2, desc='RK multiplier for successive drawdowns',typerVar='Float')
        self.add_param(strChain+'nlin',val=-1, desc='Maximum number of gradients per drawdown (Default = number of active design variables times 2)',typerVar='Int')
        self.add_param(strChain+'nstep',val=20, desc='Maximum number of steps per one-dimensional minimization (Default = 20)',typerVar='Int')
        self.add_param(strChain+'ef',val=3.0, desc='Limits one-dimensional minimization step size to EF times previous step',typerVar='Float')
        self.add_param(strChain+'eps',val=0.001, desc='Fraction of initial design variable value used as a finite difference delta',typerVar='Float')
        self.add_param(strChain+'amult',val=10.0, desc='The initial step in a one-dimensional search is controlled by the design variable value times EPS times AMULT',typerVar='Float')
        self.add_param(strChain+'dep',val=0.001, desc='One-dimensional search convergence criterion on step size as a fraction of move distance',typerVar='Float')
        self.add_param(strChain+'accux',val=3.0e-4, desc='One-dimensional search convergence criterion on step size as a fraction of initial design variable value',typerVar='Float')
        self.add_param(strChain+'glm',val=0.0, desc='Value of G at which constraint switches to quadratic extended form, a value of .002 is recommended',typerVar='Float')
        self.add_param(strChain+'gfact',val=numpy_float64, desc='Scaling factor for each behavioral constraint',typerVar='Array')
        self.add_param(strChain+'autscl',val=1.0, desc='Design variable scale factor exponent.  Scale factors for design variables default to VALUE ** AUTSCL',typerVar='Float')
        self.add_param(strChain+'icent',val=0,optionsVal=(0,1), desc='Type of differencing to be used in gradient calculations', aliases=('Forward', 'Central'),typerVar='Enum')
        self.add_param(strChain+'rhomin',val=0.0, desc='Starting value for RHO, a scalar multiplying factor used in the KS function.  (Default is computed internally)',typerVar='Float')
        self.add_param(strChain+'rhomax',val=300.0, desc='Maximum value for RHO',typerVar='Float')
        self.add_param(strChain+'rhodel',val=0.0, desc='RHO increment (Default is computed internally)',typerVar='Float')
        self.add_param(strChain+'itmax',val=30, desc='Maximum number of iterations',typerVar='Int')
        self.add_param(strChain+'jprnt',val=2, desc='KS module print control\n= 0, No output from the KS module\n= 999, Maximum output',typerVar='Int')
        self.add_param(strChain+'rdfun',val=0.01, desc='If the relative change in the KS function is less than RDFUN for three consecutive iterations, optimization is terminated.',typerVar='Float')
        self.add_param(strChain+'adfun',val=0.001, desc='If the absolute change in the KS function is less than ADFUN for three consecutive iterations, optimization is terminated.',typerVar='Float')




    def FlopsWrapper_input_rfhin(self):
        """Container for input:rfhin"""
        strChain = 'input:rfhin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'tmach',val=numpy_float64, desc='Mach numbers in increasing order',typerVar='Array')
        self.add_param(strChain+'cdmin',val=numpy_float64, desc='Minimum drag for each Mach number.\nThe lift dependent drag coefficient for the Ith Mach number is computed from:\n\nCD = CDMIN(I) + CK(I) * [CL - CLB(I)] ** 2\n+ C1SW(I) * (SW/REFAS - REFBS) ** EXPS\n+ C1TH(I) * (THRUST/REFAT - REFBT) ** EXPT\n\nwhere SW and THRUST are the current values for the wing area and for the thrust per engine, and CL is the lift coefficient.',typerVar='Array')
        self.add_param(strChain+'ck',val=numpy_float64, desc='Drag-due-to-lift factors for each Mach number',typerVar='Array')
        self.add_param(strChain+'clb',val=numpy_float64, desc='Lift coefficients corresponding to each CDMIN',typerVar='Array')
        self.add_param(strChain+'c1sw',val=numpy_float64, desc='Coefficient for wing area term for each Mach number.  May be a drag coefficient or D/Q depending on the values of REFAS, REFBS and EXPS.',typerVar='Array')
        self.add_param(strChain+'c1th',val=numpy_float64, desc='Coefficient for thrust term for each Mach number.  May be a drag coefficient or D/Q depending on the values of REFAT, REFBT and EXPT.',typerVar='Array')
        self.add_param(strChain+'refas',val=1.0, desc='Wing area reference value',typerVar='Float')
        self.add_param(strChain+'refbs',val=0.0, desc='Wing area base value',typerVar='Float')
        self.add_param(strChain+'exps',val=1.0, desc='Wing area term exponent',typerVar='Float')
        self.add_param(strChain+'refat',val=1.0, desc='Thrust reference value',typerVar='Float')
        self.add_param(strChain+'refbt',val=0.0, desc='Thrust base value',typerVar='Float')
        self.add_param(strChain+'expt',val=1.0, desc='Thrust term exponent',typerVar='Float')


    def FlopsWrapper_input_proin(self):
        """Container for input:proin"""
        strChain = 'input:proin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'npol',val=0, desc='Number of drag polars to be printed out (Default = size of dflap)',typerVar='Int')
        self.add_param(strChain+'alpro',val=numpy_float64, units='deg', desc='Angles of attack for each drag polar',typerVar='Array')
        self.add_param(strChain+'clpro',val=numpy_float64, desc='Lift coefficients for each drag polar',typerVar='Array')
        self.add_param(strChain+'cdpro',val=numpy_float64, desc='Drag coefficients for each drag polar',typerVar='Array')
        self.add_param(strChain+'dflap',val=array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), dtype=numpy_float64, units='deg', desc='Flap deflection corresponding to each drag polar.  Used only for output',typerVar='Array')
        self.add_param(strChain+'ntime',val=0,optionsVal=(1,0), desc='Option for printing detailed takeoff and climb profiles for noise', aliases=('Print', 'No print'),typerVar='Enum')
        self.add_param(strChain+'ipcmax',val=1, desc='Maximum engine power code (This variable could be used, for example, to limit takeoff and climb to dry power settings on an afterburning engine.)',typerVar='Int')
        self.add_param(strChain+'keas',val=0,optionsVal=(1,0), desc='Type of velocity given by VFIX in namelist &SEGIN', aliases=('Knots equivalent airspeed (keas)', 'True airspeed'),typerVar='Enum')
        self.add_param(strChain+'txf',val=-1.0, units='lb', desc='Fuel used in taxiing out to runway (Default is computed in mission analysis)',typerVar='Float')
        self.add_param(strChain+'alpmin',val=0.0, units='deg', desc='Minimum angle of attack during climb segment',typerVar='Float')
        self.add_param(strChain+'gamlim',val=0.0, units='deg', desc='Minimum flight path angle during fixed angle of attack segments',typerVar='Float')
        self.add_param(strChain+'inm',val=0,optionsVal=(1,0), desc='Option to generate data files necessary for transporting FLOPS takeoff and climb profile data to the FAA Integrated Noise Model (INM) program', aliases=('Generate', 'Do not generate'),typerVar='Enum')
        self.add_param(strChain+'iatr',val=0,optionsVal=(1,0), desc='Automatic thrust restoration indicator option (INM=1, has no effect of takeoff and climb profile)', aliases=('ATR', 'No ATR'),typerVar='Enum')
        self.add_param(strChain+'fzf',val=1.25, desc='Maneuver speed factor (INM=1)',typerVar='Float')
        self.add_param(strChain+'thclmb',val=-1.0, desc='Climb throttle setting (INM=1)',typerVar='Float')
        self.add_param(strChain+'flapid',val=numpy_str, desc='Six character label for each of the NPOL input drag polars, for example, "gearup"',typerVar='Array')


    def FlopsWrapper_input_option_Program_Control(self):
        """Container for input:option:Program_Control"""
        strChain = 'input:option:Program_Control:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'mprint',val=1,optionsVal=(0,1), desc='Print control \n = 0, Print only 3-5 line summary for each analysis. Usually used only for contour plots (IOPT = 4) \n = 1, Normal output for all analyses', aliases=('Short Summary', 'Normal'),typerVar='Enum')
        self.add_param(strChain+'iopt',val=1,optionsVal=(1,2,3,4), desc='Execution Type', aliases=('Analysis', 'Parametric Variation', 'Optimization', 'Contour or Thumbprint plot'),typerVar='Enum')
        self.add_param(strChain+'ianal',val=3,optionsVal=(1,2,3,4), desc='Analysis Type', aliases=('Weights', 'Weights and Aerodynamics', 'Full Analysis', 'Propulsion'),typerVar='Enum')
        self.add_param(strChain+'ineng',val=0,optionsVal=(0,1), desc='Force engine Data Read', aliases=('If necessary', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'itakof',val=0,optionsVal=(0,1), desc='Detailed takeoff', aliases=('No', 'Yes (Namelist &TOLIN required)'),typerVar='Enum')
        self.add_param(strChain+'iland',val=0,optionsVal=(0,1), desc='Detailed landing', aliases=('No', 'Yes (Namelist &TOLIN required)'),typerVar='Enum')
        self.add_param(strChain+'nopro',val=0,optionsVal=(0,1), desc='Generate takeoff and climb profiles (Namelists &TOLIN &PROIN and &SEGIN required)', aliases=('No', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'noise',val=0,optionsVal=(0,1,2), desc='Calculate noise', aliases=('No', 'Yes (Namelist &COSTIN required)', 'Yes for final analysis only'),typerVar='Enum')
        self.add_param(strChain+'icost',val=0,optionsVal=(0,1), desc='Calculate costs', aliases=('No', 'Yes (Namelist &COSTIN required)'),typerVar='Enum')
        self.add_param(strChain+'ifite',val=0,optionsVal=(0,1,2,3), desc='Weight equations', aliases=('Transports', 'Fighter/attack', 'General aviation', 'Blended wing body'),typerVar='Enum')


    def FlopsWrapper_input_option_Plot_Files(self):
        """Container for input:option:Plot_Files"""
        strChain = 'input:option:Plot_Files:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ixfl',val=0,optionsVal=(0,1), desc='Generate mission summary plot files', aliases=('No', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'npfile',val=0,optionsVal=(0,1,2), desc='Output takeoff and climb profiles for use with ANOPP preprocessor (andin)', aliases=('No', 'Yes', 'XFlops'),typerVar='Enum')
        self.add_param(strChain+'ipolp',val=0,optionsVal=(0,1,2), desc='Drag polar plot data', aliases=('None', 'Drag polars at existing Mach numbers', 'User specified Mach numbers'),typerVar='Enum')
        self.add_param(strChain+'polalt',val=0.0, units='ft', desc='Altitude for drag polar plots',typerVar='Float')
        self.add_param(strChain+'pmach',val=numpy_float64, desc='Mach numbers for drag polar plot data',typerVar='Array')
        self.add_param(strChain+'ipltth',val=0,optionsVal=(0,1,2), desc='Generate engine plot data', aliases=('None', 'Initial engine', 'Final scaled engine'),typerVar='Enum')
        self.add_param(strChain+'iplths',val=0,optionsVal=(0,1), desc='Design history plot data', aliases=('No', 'Yes'),typerVar='Enum')
        '''        
        nfile = Str(desc='Contour or thumbprint plot data filename')
        msfile = Str(desc='Mission summary data filename')
        crfile = Str(desc='Cruise schedule summary data filename')
        tofile = Str(desc='Takeoff and landing aerodynamic and thrust data filename')
        nofile = Str(desc='Takeoff and climb profile data filename')
        apfile = Str(desc='Drag polar plot data filename')
        thfile = Str(desc='Engine plot data filename')
        hsfile = Str(desc='Design history plot filename')
        psfile = Str(desc='Excess power and load factor plot data filename')
        '''

    def FlopsWrapper_input_option_Excess_Power_Plot(self):
        """Container for input:option:Excess_Power_Plot"""
        strChain = 'input:option:Excess_Power_Plot:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xmax',val=0.9, desc='Maximum Mach number for plots',typerVar='Float')
        self.add_param(strChain+'xmin',val=0.3, desc='Minimum Mach number for plots',typerVar='Float')
        self.add_param(strChain+'xinc',val=0.2, desc='Mach number increment for plots',typerVar='Float')
        self.add_param(strChain+'ymax',val=40000.0, units='ft', desc='Maximum altitude for plots',typerVar='Float')
        self.add_param(strChain+'ymin',val=0.0, units='ft', desc='Minimum altitude for plots',typerVar='Float')
        self.add_param(strChain+'yinc',val=10000.0, units='ft', desc='Altitude increment for plots',typerVar='Float')
        self.add_param(strChain+'pltnz',val=numpy_float64, desc='Nz at which Ps contours are plotted (or Nz)',typerVar='Array')
        self.add_param(strChain+'pltpc',val=numpy_float64, desc='Engine power (fraction if =< 1; else setting)',typerVar='Array')
        self.add_param(strChain+'ipstdg',val=numpy_int64, desc='Store drag schedule (see Namelist &MISSIN)',typerVar='Array')
        self.add_param(strChain+'pltwt',val=numpy_float64, units='lb', desc='Fixed weight',typerVar='Array')
        self.add_param(strChain+'ipltsg',val=numpy_int64, desc='Weight at start of mission segment IPLTSG is used',typerVar='Array')
        self.add_param(strChain+'pltfm',val=numpy_float64, desc='Fraction of fuel burned',typerVar='Array')
        self.add_param(strChain+'pltwta',val=numpy_float64, units='lb', desc='Delta weight',typerVar='Array')




    def FlopsWrapper_input_noisin_Turbine(self):
        """Container for input:noisin:Turbine"""
        strChain = 'input:noisin:Turbine:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'tsupp',val=numpy_float64, desc='Turbine suppression spectrum',typerVar='Array')
        self.add_param(strChain+'tbndia',val=-1.0, units='ft', desc='Diameter of last-stage turbine',typerVar='Float')
        self.add_param(strChain+'gear',val=1.0, desc='Gear ratio:  turbine RPM/fan RPM',typerVar='Float')
        self.add_param(strChain+'cs',val=0.0, desc='Stator chord to rotor spacing ratio',typerVar='Float')
        self.add_param(strChain+'nblr',val=-1, desc='Number of last stage rotor blades',typerVar='Int')
        self.add_param(strChain+'ityptb',val=0,optionsVal=(1,0), desc='Type of exit plane', aliases=('Turbofans', 'Turbojets or coplanar exits'),typerVar='Enum')
        self.add_param(strChain+'etdop',val=4.0, desc='Exponent on source motion (Doppler) amplification on turbine noise',typerVar='Float')


    def FlopsWrapper_input_noisin_Shielding(self):
        """Container for input:noisin:Shielding"""
        strChain = 'input:noisin:Shielding:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'iuotw',val=0,optionsVal=(1,0), desc='Engine location relative to wing', aliases=('Over the wing', 'Under the wing'),typerVar='Enum')
        self.add_param(strChain+'sfuse',val=10.0, desc='Maximum fuselage shielding',typerVar='Float')
        self.add_param(strChain+'swide',val=60.0, units='deg', desc='Degrees of arc where fuselage shielding is greater than SFUSE/e',typerVar='Float')
        self.add_param(strChain+'swing',val=10.0, desc='Maximum wing shielding for over-the-wing engine',typerVar='Float')
        self.add_param(strChain+'smx',val=90.0, units='deg', desc='Angle in flyover plane of maximum over-the-wing shielding',typerVar='Float')
        self.add_param(strChain+'cfuse',val=10.0, units='ft', desc='Characteristic fuselage dimension (such as diameter)',typerVar='Float')
        self.add_param(strChain+'cwing',val=10.0, units='ft', desc='Characteristic wing dimension (such as chord)',typerVar='Float')


    def FlopsWrapper_input_noisin_Propeller(self):
        """Container for input:noisin:Propeller"""
        strChain = 'input:noisin:Propeller:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'nb',val=0, desc='Number of blades per propeller',typerVar='Int')
        self.add_param(strChain+'bldia',val=0.0, units='ft', desc='Diameter of propeller',typerVar='Float')
        self.add_param(strChain+'blarea',val=0.0, units='ft*ft', desc='Total blade area for one side of propeller',typerVar='Float')
        self.add_param(strChain+'gearp',val=1.0, desc='Ratio of propeller rpm / engine rpm',typerVar='Float')
        self.add_param(strChain+'epdop',val=1.0, desc='Exponent on source motion (Doppler) amplification on propeller noise',typerVar='Float')
        self.add_param(strChain+'blth',val=0.0, units='ft', desc='Blade thickness at 70% span',typerVar='Float')
        self.add_param(strChain+'blch',val=0.0, units='ft', desc='Blade chord at 70% span',typerVar='Float')
        self.add_param(strChain+'blattk',val=0.0, units='deg', desc='Blade angle of attack at 70% span',typerVar='Float')
        self.add_param(strChain+'dharm',val=0.5, desc='Rate of decrease in harmonic level beyond tenth, dB/harmonic',typerVar='Float')
        self.add_param(strChain+'nph',val=10, desc='Number of harmonics of BDF desired',typerVar='Int')
        self.add_param(strChain+'ivor',val=1,optionsVal=(1,0), desc='Calculate vortex noise component', aliases=('Vortex noise', 'No vortex noise'),typerVar='Enum')
        self.add_param(strChain+'irot',val=1,optionsVal=(1,0), desc='Calculate rotational noise component', aliases=('Rotational noise', 'No rotational noise'),typerVar='Enum')
        self.add_param(strChain+'ipdir',val=0,optionsVal=(1,0), desc='Apply Boeing directivity correction', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'psupp',val=numpy_float64, desc='Propeller noise suppression spectrum',typerVar='Array')


    def FlopsWrapper_input_noisin_Propagation(self):
        """Container for input:noisin:Propagation"""
        strChain = 'input:noisin:Propagation:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'isupp',val=0,optionsVal=(1,0), desc='Apply suppression spectra to each source for which they are supplied', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'idop',val=0,optionsVal=(1,0), desc='Apply Doppler frequency and intensity correction to total noise', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'ignd',val=0,optionsVal=(0,1,2), desc='Ground reflection option', aliases=('None', 'Perfect reflection', 'Putnam method'),typerVar='Enum')
        self.add_param(strChain+'iatm',val=0,optionsVal=(0,1,2), desc='Atmospheric absorption correction', aliases=('None', 'SAE ARP 866', 'Bass & Shields'),typerVar='Enum')
        self.add_param(strChain+'iega',val=0,optionsVal=(1,0), desc='Extra ground attenuation', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'ishld',val=0,optionsVal=(1,0), desc='Shielding of fan, jet, core, turbine and propeller sources', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'deldb',val=20.0, desc='Number of dB down from the peak noise level to cut off printing of noise time histories',typerVar='Float')
        self.add_param(strChain+'heng',val=0.0, units='ft', desc='Height of engine above ground during taxi',typerVar='Float')
        self.add_param(strChain+'filbw',val=1.0, desc='Fraction of filter bandwidth with a gain of 1',typerVar='Float')
        self.add_param(strChain+'tdi',val=1.0, units='s', desc='Reception time increment',typerVar='Float')
        self.add_param(strChain+'rh',val=70.0, desc='Ambient relative humidity',typerVar='Float')


    def FlopsWrapper_input_noisin_Observers(self):
        """Container for input:noisin:Observers"""
        strChain = 'input:noisin:Observers:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'xo',val=numpy_float64, units='ft', desc='X-coordinates of observers',typerVar='Array')
        self.add_param(strChain+'yo',val=numpy_float64, units='ft', desc='Y-coordinates of observers',typerVar='Array')
        self.add_param(strChain+'zo',val=0.0, units='ft', desc='Height of all observers above the ground',typerVar='Float')
        self.add_param(strChain+'ndprt',val=1,optionsVal=(1,0), desc='Print observer noise histories',typerVar='Enum')
        self.add_param(strChain+'ifoot',val=0,optionsVal=(1,0), desc='Print noise levels of input observers in countour format to file NSPLOT for subsequent plotting of the noise footprint', aliases=('Print', 'No print'),typerVar='Enum')
        self.add_param(strChain+'igeom',val=0,optionsVal=(1,0), desc='Print geometric relations of aircraft/observer at each time point', aliases=('Print', 'No print'),typerVar='Enum')
        self.add_param(strChain+'thrn',val=-1.0, units='lb', desc='Thrust of baseline engine.  Geometry data and engine parameter arrays will be scaled accordingly (Default=THRSO, Namelist &WTIN)',typerVar='Float')
        self.add_param(strChain+'icorr',val=0,optionsVal=(1,0), desc='Apply corrections to engine parameters to correct for ambient conditions', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'tcorxp',val=1.0, desc='Exponent for core temperature correction in engine parameter arrays',typerVar='Float')


    def FlopsWrapper_input_noisin_MSJet(self):
        """Container for input:noisin:MSJet"""
        strChain = 'input:noisin:MSJet:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'iy9',val=1,optionsVal=(1,2,3,4,5,6), desc='Type of nozzle', aliases=('Convergent conical', 'Single multitube', 'Single multichute', 'Dual convergent conical', 'Dual, multitube on outer', 'Dual, multichute/spoke on outer'),typerVar='Enum')
        self.add_param(strChain+'n',val=1, desc='Number of tubes (IY9=2,5) or elements (IY9=3,6)',typerVar='Int')
        self.add_param(strChain+'rp',val=0.0, units='ft', desc='Centerbody plug radius (IY9=2,3,5,6)',typerVar='Float')
        self.add_param(strChain+'b9',val=0.0, units='deg', desc='Tube centerline cant angle (IY9-2,5)\nChute/spoke exit cant angle (IY9=3,6)',typerVar='Float')
        self.add_param(strChain+'dt',val=0.0, units='inch', desc='Tube diameter (IY9=2,5)',typerVar='Float')
        self.add_param(strChain+'z5',val=0.0, desc='Number of rows of tubes, counting center tube (if present) as zero (IY9=2,5)',typerVar='Float')
        self.add_param(strChain+'s1j',val=0.0, desc='Tube centerline spacing to tube diameter ratio (IY9=2,5)',typerVar='Float')
        self.add_param(strChain+'a6',val=0.0, desc='Ratio of ejector inlet area to nozzle (total or annulus) area (input zero for no ejector) (IY9=2,3,5,6)',typerVar='Float')
        self.add_param(strChain+'zl9',val=0.0, desc='Ratio of ejector length to suppressor nozzle equivalent diameter (IY9=2,3,5,6)',typerVar='Float')
        self.add_param(strChain+'a',val=numpy_float64, desc='A(0): Ejector treatment faceplate thickness, in\nA(1): Ejector treatment hole diameter, in\nA(2): Ejector treatment cavity depth, in\nA(3): Ejector treatment open area ratio\n(IY9=2,3,5,6)',typerVar='Array')

    # TODO - rr and rx are units of 'Rayl' (rayleigh)
        self.add_param(strChain+'rr',val=numpy_float64, desc='Ejector treatment specific resistance (59 values required) (IY9=2,3,5,6)',typerVar='Array')
        self.add_param(strChain+'rx',val=numpy_float64, desc='Ejector treatment specific reactance (59 values required) (IY9=2,3,5,6)',typerVar='Array')
        self.add_param(strChain+'r4',val=0.0, units='inch', desc='Outer circumferential flow dimension (IY9=3,6)',typerVar='Float')
        self.add_param(strChain+'r6',val=0.0, units='inch', desc='Inner circumferential flow dimension (IY9=3,6)',typerVar='Float')
        self.add_param(strChain+'ss',val=0.0, units='inch', desc='Outer circumferential element dimension (IY9=3,6)',typerVar='Float')
        self.add_param(strChain+'dn',val=0.0, units='ft', desc='Nozzle outer diameter',typerVar='Float')
        self.add_param(strChain+'aa',val=0.0, desc='Unknown variable',typerVar='Float')
        self.add_param(strChain+'nflt',val=1, desc='Unknown variable',typerVar='Int')
        self.add_param(strChain+'htr',val=0.0, desc='Unknown variable',typerVar='Float')
        self.add_param(strChain+'nst',val=1, desc='Unknown variable',typerVar='Int')


    def FlopsWrapper_input_noisin_Jet(self):
        """Container for input:noisin:Jet"""
        strChain = 'input:noisin:Jet:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'inoz',val=0,optionsVal=(1,0), desc='Type of nozzle', aliases=('Coaxial', 'Circular'),typerVar='Enum')
        self.add_param(strChain+'iplug',val=0,optionsVal=(1,0), desc='Plug nozzle on primary', aliases=('Plug', 'No plug'),typerVar='Enum')
        self.add_param(strChain+'islot',val=0,optionsVal=(1,0), desc='Slot nozzle on primary', aliases=('Slot nozzle', 'No slot'),typerVar='Enum')
        self.add_param(strChain+'iaz',val=0,optionsVal=(1,0), desc='Azimuthal correction for nozzle geometry', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'dbaz',val=0.0, desc='Noise reduction due to nozzle geometry at phi = 75 degrees, used only if IAZ = 1',typerVar='Float')
        self.add_param(strChain+'ejdop',val=1.0, desc='Exponent on source motion (Doppler) amplification on shock noise only.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'zmdc',val=1.0, desc='Core (primary) jet design Mach number.  Used for application of non-ideally expanded shock noise.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'gammac',val=-1.0, desc='Core (primary) jet exhaust gamma Used for IJET=1,2,6 (Default = 1.4)',typerVar='Float')
        self.add_param(strChain+'gasrc',val=-1.0, units='(ft*lb)/(lb*degR)', desc='Core exhaust gas constant, Used for IJET=1,2 (Default = 53.35)',typerVar='Float')
        self.add_param(strChain+'annht',val=0.0, units='ft', desc='Core nozzle annulus height.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'zmdf',val=1.0, desc='Fan (secondary) jet design Mach number.  Used for application of non-ideally expanded shock noise.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'gammap',val=-1.0, desc='Fan (secondary) jet exhaust gamma Used for IJET=1,2 (Default = GAMMAF)',typerVar='Float')
        self.add_param(strChain+'gasrf',val=53.35, units='(ft*lb)/(lb*degR)', desc='Fan exhaust gas constant.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'annhtf',val=0.0, units='ft', desc='Fan nozzle annulus height.  Used for IJET=1,2',typerVar='Float')
        self.add_param(strChain+'dhc',val=-1.0, units='ft', desc='Core nozzle hydraulic diameter.  Used for IJET=3,4',typerVar='Float')
        self.add_param(strChain+'dhf',val=0.0, units='ft', desc='Fan nozzle hydraulic diameter.  Used for IJET=3,4',typerVar='Float')
        self.add_param(strChain+'zl2',val=0.0, units='ft', desc='Axial distance from the outer exit plane to the exit plane of the inner nozzle.  Used for IJET=3,4',typerVar='Float')
        self.add_param(strChain+'ifwd',val=0,optionsVal=(1,0), desc='Forward velocity effects on source.  Used for IJET=1,2,3,4,5', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'ishock',val=1,optionsVal=(1,0), desc='Calculate shock noise.  Used for IJET=1,2,3,4,5', aliases=('Shock noise', 'No shock'),typerVar='Enum')
        self.add_param(strChain+'zjsupp',val=numpy_float64, desc='Jet suppression spectrum.  Used for IJET=1,2,3,4,5',typerVar='Array')


    def FlopsWrapper_input_noisin_Ground_Effects(self):
        """Container for input:noisin:Ground_Effects"""
        strChain = 'input:noisin:Ground_Effects:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'itone',val=0,optionsVal=(1,0), desc='1/3-octave bands exceeding adjacent bands by 3 dB or more are approximated as tones', aliases=('Yes', 'No'),typerVar='Enum')
        #self.add_param(strChain+'nht',val=0, desc='Number of heights to be used to approximate a distributed source by multiple sources',typerVar='Int')
        self.add_param(strChain+'dk',val=numpy_float64, units='ft', desc='Heights of multiple sources from source center',typerVar='Array')


    def FlopsWrapper_input_noisin_Flap_Noise(self):
        """Container for input:noisin:Flap_Noise"""
        strChain = 'input:noisin:Flap_Noise:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ilnoz',val=0,optionsVal=(2,1,0), desc='Nozzle type', aliases=('Coaxial, mixed flow', 'Coaxial, separate flow', 'Circular'),typerVar='Enum')
        self.add_param(strChain+'insens',val=0,optionsVal=(1,0), desc='Configuration with noise levels insensitive to flap angle', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'ac1',val=0.0, units='ft*ft', desc='Core (primary) nozzle area',typerVar='Float')
        self.add_param(strChain+'af1',val=0.0, units='ft*ft', desc='Fan (secondary) nozzle area',typerVar='Float')
        self.add_param(strChain+'bpr',val=0.0, desc='Bypass ratio, for mixed flow coaxial nozzle',typerVar='Float')
        self.add_param(strChain+'wingd',val=0.0, desc='Ratio of wing chord to total nozzle diameter, used for large BPR designs when WINGD < 3',typerVar='Float')
        self.add_param(strChain+'flsupp',val=numpy_float64, desc='Flap noise suppression spectrum',typerVar='Array')
        self.add_param(strChain+'eldop',val=0.0, desc='Exponent on source motion (Doppler) amplification on flap noise',typerVar='Float')


    def FlopsWrapper_input_noisin_Fan(self):
        """Container for input:noisin:Fan"""
        strChain = 'input:noisin:Fan:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'igv',val=0,optionsVal=(1,0), desc='Inlet guide vane option', aliases=('Inlet guide vane', 'No IGV'),typerVar='Enum')
        self.add_param(strChain+'ifd',val=0,optionsVal=(1,0), desc='Inlet flow distortion option during ground run', aliases=('Inlet flow distortion', 'No distortion'),typerVar='Enum')
        self.add_param(strChain+'iexh',val=2,optionsVal=(0,1,2), desc='Fan inlet, exhaust noise options', aliases=('Inlet only', 'Exhaust only', 'Both inlet & exhaust'),typerVar='Enum')
        self.add_param(strChain+'nfh',val=10, desc='Number of harmonics to be considered in blade-passing tone',typerVar='Int')
        self.add_param(strChain+'nstg',val=-1, desc='Number of fan stages',typerVar='Int')
        self.add_param(strChain+'suppin',val=numpy_float64, desc='Fan inlet suppression spectrum',typerVar='Array')
        self.add_param(strChain+'suppex',val=numpy_float64, desc='Fan exhaust suppression spectrum',typerVar='Array')
        self.add_param(strChain+'methtip',val=1,optionsVal=(1,2,3), desc='Method for calculation of relative tip Mach number', aliases=('ANOPP method', 'Clark', 'Use ATIPM'),typerVar='Enum')
        self.add_param(strChain+'icomb',val=1,optionsVal=(1,0), desc='Option to include combination tones if relative tip Mach number is supersonic', aliases=('Combination tones', 'No combination tones'),typerVar='Enum')
        self.add_param(strChain+'decmpt',val=0.0, desc='Decrement to apply to combination tones',typerVar='Float')
        self.add_param(strChain+'gammaf',val=1.4, desc='Gamma of fan air',typerVar='Float')
        self.add_param(strChain+'nbl',val=-1, desc='Number of fan blades',typerVar='Int')
        self.add_param(strChain+'nvan',val=-1, desc='Number of stator vanes',typerVar='Int')
        self.add_param(strChain+'fandia',val=-1.0, units='ft', desc='Fan diameter',typerVar='Float')
        self.add_param(strChain+'fanhub',val=-1.0, units='ft', desc='Fan hub diameter',typerVar='Float')
        self.add_param(strChain+'tipmd',val=-1.0, desc='Design relative tip Mach number',typerVar='Float')
        self.add_param(strChain+'rss',val=100.0, desc='Rotor-stator spacing in percent',typerVar='Float')
        self.add_param(strChain+'efdop',val=4.0, desc='Exponent on source motion (Doppler) amplification on fan noise',typerVar='Float')
        self.add_param(strChain+'faneff',val=0.88, desc='Constant first stage fan efficiency, < 1.0.  Overridden by AFANEF',typerVar='Float')
        self.add_param(strChain+'nbl2',val=-1, desc='Number of fan blades for second stage (Default = NBL)',typerVar='Int')
        self.add_param(strChain+'nvan2',val=-1, desc='Number of stator vanes for second stage (Default = NVAN)',typerVar='Int')
        self.add_param(strChain+'fand2',val=-1.0, units='ft', desc='Fan diameter for second stage (Default = FANDIA)',typerVar='Float')
        self.add_param(strChain+'tipmd2',val=-1.0, desc='Design relative tip Mach number for second stage (Default = TIPMD)',typerVar='Float')
        self.add_param(strChain+'rss2',val=-1.0, desc='Rotor-stator spacing in percent for second stage (Default = RSS)',typerVar='Float')
        self.add_param(strChain+'efdop2',val=-1.0, desc='Exponent on source motion (Doppler) amplification on second stage fan noise (Default = EFDOP)',typerVar='Float')
        self.add_param(strChain+'fanef2',val=0.88, desc='Constant second stage fan efficiency, < 1.0.  Overridden by AFANF2',typerVar='Float')
        self.add_param(strChain+'trat',val=-1.0, desc='Ratio of second stage temperature rise (DELT2) to that of first stage.  Either TRAT or PRAT is used to calculate DELT2.',typerVar='Float')
        self.add_param(strChain+'prat',val=1.0, desc='Ratio of second stage fan pressure ratio to that of first stage',typerVar='Float')


    def FlopsWrapper_input_noisin_Engine_Parameters(self):
        """Container for input:noisin:Engine_Parameters"""
        strChain = 'input:noisin:Engine_Parameters:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'aepp',val=numpy_float64, desc='Throttle settings as a fraction of net thrust',typerVar='Array')
        self.add_param(strChain+'avc',val=numpy_float64, units='ft/s', desc='Core/primary exhaust jet velocity (ideally expanded velocity; exclude friction and expansion alterations).  Used for IJET=1,2,3,4,6',typerVar='Array')
        self.add_param(strChain+'avf',val=numpy_float64, units='ft/s', desc='Fan/secondary exhaust jet velocity (ideally expanded velocity; exclude friction and expansion alterations).  Used for IJET=1,2,3,4',typerVar='Array')
        self.add_param(strChain+'atc',val=numpy_float64, units='degR', desc='Core/primary jet exhaust total temperature.  Used for IJET=1,2,3,4,6',typerVar='Array')
        self.add_param(strChain+'atf',val=numpy_float64, units='degR', desc='Fan/secondary jet exhaust total temperature.  Used for IJET=1,2,3,4',typerVar='Array')
        self.add_param(strChain+'aac',val=numpy_float64, units='ft*ft', desc='Core jet nozzle exhaust area.  For IJET=1,2,6, AAC represents exit area; for IJET=3,4, AAC represents throat area.',typerVar='Array')
        self.add_param(strChain+'aaf',val=numpy_float64, units='ft*ft', desc='Fan jet nozzle exhaust area.  For IJET=1 or IJET=2, AAF represents exit area; for IJET=3,4, AAF represents throat area.',typerVar='Array')
        self.add_param(strChain+'adj',val=numpy_float64, units='ft', desc='Core outer diameter; at the equivalent throat if the nozzle is C-D.   Used only for IJET=3,4',typerVar='Array')
        self.add_param(strChain+'adj2',val=numpy_float64, units='ft', desc='Fan outer diameter; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typerVar='Array')
        self.add_param(strChain+'ahj',val=numpy_float64, units='ft', desc='Core annulus height; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typerVar='Array')
        self.add_param(strChain+'ahj2',val=numpy_float64, units='ft', desc='Fan annulus height; at the equivalent throat if the nozzle is C-D.  Used only for IJET=3,4',typerVar='Array')
        self.add_param(strChain+'afuel',val=numpy_float64, units='lb/s', desc='Fuel flow.  Used if ICORE, ITURB=1; and IJET=1,2 and only if calculating GAMMAC and GASRC.',typerVar='Array')
        self.add_param(strChain+'atipm',val=numpy_float64, desc='Fan first-stage relative tip Mach number.  These are approximated if not input.  Used if IFAN=1',typerVar='Array')
        self.add_param(strChain+'atipm2',val=numpy_float64, desc='Fan second-stage relative tip Mach number.  These are approximated if not input.  Used if IFAN=1',typerVar='Array')
        self.add_param(strChain+'awafan',val=numpy_float64, units='lb/s', desc='Total engine airflow.  Used if IFAN=1',typerVar='Array')
        self.add_param(strChain+'adelt',val=numpy_float64, units='degR', desc='Fan temperature rise.  Used if IFAN=1',typerVar='Array')
        self.add_param(strChain+'afpr',val=numpy_float64, desc='Fan pressure ratio.  This is not needed if ADELT is input.  Otherwise, values for ADELT will be calculated using AFANEF and AFANF2 values.',typerVar='Array')
        self.add_param(strChain+'afanef',val=numpy_float64, desc='Fan first-stage efficiency.  These are required if AFPR is supplied rather than ADELT.',typerVar='Array')
        self.add_param(strChain+'afanf2',val=numpy_float64, desc='Fan second-stage efficiency.  These are required if AFPR is supplied rather than ADELT.',typerVar='Array')
        self.add_param(strChain+'arpm',val=numpy_float64, units='rpm', desc='Fan or turbine speed.  Used if IFAN, ITURB=1',typerVar='Array')
        self.add_param(strChain+'awcore',val=numpy_float64, units='lb/s', desc='Burner and turbine airflow.  Used if ICORE or ITURB=1 and IJET=1,2 and only if calculating GAMMAC and GASRC.',typerVar='Array')
        self.add_param(strChain+'ap3',val=numpy_float64, units='psf', desc='Burner inlet pressure.  Used if ICORE=1',typerVar='Array')
        self.add_param(strChain+'at3',val=numpy_float64, units='degR', desc='Burner inlet temperature.  Used if ICORE=1',typerVar='Array')
        self.add_param(strChain+'at4',val=numpy_float64, units='degR', desc='Burner exit static temperature.  These are approximated from the fuel/air ratio if not input.  Used if ICORE=1',typerVar='Array')
        self.add_param(strChain+'aturts',val=numpy_float64, units='ft/s', desc='Turbine last stage rotor relative tip speed.  These are approximated if not input.  Used if ITURB=1',typerVar='Array')
        self.add_param(strChain+'atctur',val=numpy_float64, units='degR', desc='Turbine exit temperature.  These are assumed the same as ATC if not supplied.  Used if ITURB=1',typerVar='Array')
        self.add_param(strChain+'aepwr',val=numpy_float64, units='hp', desc='Horsepower supplied to propeller.  Used if IPROP=1',typerVar='Array')
        self.add_param(strChain+'athrst',val=numpy_float64, units='lb', desc='Propeller thrust.  Used if IPROP=1',typerVar='Array')
        self.add_param(strChain+'amsp9',val=numpy_float64, desc='Nozzle pressure ratio: entance total to ambient static.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amstt3',val=numpy_float64, units='degR', desc='Nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amsa9',val=numpy_float64, units='ft*ft', desc='Nozzle exit area.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amsa7',val=numpy_float64, desc='Nozzle ejector chute area ratio.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amsaa8',val=numpy_float64, units='ft*ft', desc='Inner nozzle flow area.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amstt4',val=numpy_float64, units='degR', desc='Inner nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amsp4',val=numpy_float64, desc='Inner nozzle pressure ratio: entrance total to ambient static.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amstt5',val=numpy_float64, units='degR', desc='Outer nozzle exit total temperature.  Used for M*S code jet predictions, IJET=5',typerVar='Array')
        self.add_param(strChain+'amsp5',val=numpy_float64, desc='Outer nozzle pressure ratio: entrance total to ambient static.  Used for M*S code jet predictions, IJET=5',typerVar='Array')


    def FlopsWrapper_input_noisin_Core(self):
        """Container for input:noisin:Core"""
        strChain = 'input:noisin:Core:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'csupp',val=numpy_float64, desc='Core suppression spectrum',typerVar='Array')
        self.add_param(strChain+'gamma',val=1.4, desc='Specific heat ratio;  required if using AP3 rather than AT3',typerVar='Float')
        self.add_param(strChain+'imod',val=0,optionsVal=(1,0), desc='Use modified core level prediction', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'dtemd',val=-1.0, units='degR', desc='Design turbine temperature drop',typerVar='Float')
        self.add_param(strChain+'ecdop',val=2.0, desc='Exponent on source motion (Doppler) amplification on core noise',typerVar='Float')


    def FlopsWrapper_input_noisin_Basic(self):
        """Container for input:noisin:Basic"""
        strChain = 'input:noisin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'iepn',val=0,optionsVal=(0,1,2), desc='= 0, Stage III\n= 1, Stage III - Delta dB (see DEPNT, DEPNS and DEPNL)\n=2, Find the X-coordinate where the maximum EPNL occurs.  NOB, XO and YO must be input.  YO should be constant.  IEPN=2 is usually used to get a sideline (YO) noise for GA aircraft.', aliases=('Stage III', 'Stage III - Delta', 'Find max. EPNL'),typerVar='Enum')
        self.add_param(strChain+'depnt',val=0.0, desc='Increment below Stage III for takeoff (see IEPN)',typerVar='Float')
        self.add_param(strChain+'depns',val=0.0, desc='Increment below Stage III for sideline (see IEPN).\nIf IEPN=2, DEPNS is the upper limit for sideline noise.',typerVar='Float')
        self.add_param(strChain+'depnl',val=0.0, desc='Increment below Stage III for landing (see IEPN)',typerVar='Float')
        self.add_param(strChain+'itrade',val=0,optionsVal=(1,0), desc='Option to trade 2 dB between sideline and flyover noise', aliases=('Trade', 'No trade'),typerVar='Enum')
        self.add_param(strChain+'ijet',val=0,optionsVal=(0,1,2,3,4,5,6), desc='Jet noise option', aliases=('None', 'Stone/Clark', 'Kresja', 'Stone ALLJET', 'Stone JET181', 'GE M*S', 'SAE A-21 (ANOPP)'),typerVar='Enum')
        self.add_param(strChain+'ifan',val=0,optionsVal=(0,1,2), desc='Fan noise option', aliases=('None', 'Heidmann', 'Gliebe'),typerVar='Enum')
        self.add_param(strChain+'icore',val=0,optionsVal=(0,1), desc='Core noise option', aliases=('None', 'Core noise'),typerVar='Enum')
        self.add_param(strChain+'iturb',val=0,optionsVal=(0,1), desc='Turbine noise option', aliases=('None', 'Turbine noise'),typerVar='Enum')
        self.add_param(strChain+'iprop',val=0,optionsVal=(0,1,2), desc='Propeller noise option', aliases=('None', 'SAE', 'Gutin'),typerVar='Enum')
        self.add_param(strChain+'iflap',val=0,optionsVal=(0,1), desc='Flap noise/Jet-flap impingement noise option', aliases=('None', 'Flap & jet/flap noise'),typerVar='Enum')
        self.add_param(strChain+'iairf',val=0,optionsVal=(0,1), desc='Airframe noise option', aliases=('None', 'Airframe noise'),typerVar='Enum')
        self.add_param(strChain+'igear',val=0,optionsVal=(0,1), desc='Gear box noise option', aliases=('None', 'Approx. gear box noise'),typerVar='Enum')


    def FlopsWrapper_input_noisin_Airframe(self):
        """Container for input:noisin:Airframe"""
        strChain = 'input:noisin:Airframe:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ifl',val=0,optionsVal=(1,0), desc='Include slotted flap noise', aliases=('Slotted flap noise', 'No slotted flap noise'),typerVar='Enum')
        self.add_param(strChain+'nf',val=2, desc='Number of trailing edge flap slots for IFL = 1',typerVar='Int')
        self.add_param(strChain+'pfchd',val=0.25, desc='Average chord for slotted flap, ft or fraction of wing chord.  Used only if IFL = 1',typerVar='Float')
        self.add_param(strChain+'itypw',val=1,optionsVal=(1,2), desc='Type of wing', aliases=('Conventional', 'Delta'),typerVar='Enum')
        self.add_param(strChain+'iclean',val=0,optionsVal=(1,0), desc='Aerodynamically clean aircraft', aliases=('Aerodynamically clean', 'Conventional'),typerVar='Enum')
        self.add_param(strChain+'iwing',val=0,optionsVal=(1,0), desc='Wing, horizontal and vertical tail noise', aliases=('Wing, horiz., vert. tail noise', 'No wing, tail noise'),typerVar='Enum')
        self.add_param(strChain+'islat',val=0,optionsVal=(1,0), desc='Slatted leading edge noise', aliases=('Slatted l.e. noise', 'No slatted l.e. noise'),typerVar='Enum')
        self.add_param(strChain+'ilg',val=0,optionsVal=(1,0), desc='Nose and main landing gear noise', aliases=('Landing gear noise', 'No landing gear noise'),typerVar='Enum')
        self.add_param(strChain+'ng',val=numpy_int64, desc='NG(0):  Number of nose gear trucks\nNG(1):  Number of main gear trucks',typerVar='Array')
        self.add_param(strChain+'nw',val=numpy_int64, desc='NW(0):  Number of wheels per nose gear truck\nNW(1):  Number of wheels per main gear truck',typerVar='Array')
        self.add_param(strChain+'dw',val=numpy_float64, units='ft', desc='DW(0):  Diameter of nose gear tires\nDW(1):  Diameter of main gear tires',typerVar='Array')
        self.add_param(strChain+'cg',val=numpy_float64, desc='CG(0):  Ratio of nose strut length to DW(0)\nCG(1):  Ratio of main strut length to DW(1)',typerVar='Array')





    def FlopsWrapper_input_nacell(self):
        """Container for input:nacell"""
        strChain = 'input:nacell:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'x1r',val=2.06, desc='X1 / R.  If IVAR = -1, X1R is the cowl length divided by the inlet capture radius.',typerVar='Float')
        self.add_param(strChain+'x2r',val=1.58, desc='X2 / R',typerVar='Float')
        self.add_param(strChain+'r1r',val=0.354, desc='R1 / R',typerVar='Float')
        self.add_param(strChain+'r2r',val=0.585, desc='R2 / R',typerVar='Float')
        self.add_param(strChain+'angle',val=7.0, units='deg', desc='Average angle of the subsonic diffuser portion of the inlet between the throat and the engine face',typerVar='Float')
        self.add_param(strChain+'clang',val=0.0, units='deg', desc='Cowl lip angle',typerVar='Float')
        self.add_param(strChain+'mixed',val=-1,optionsVal=(-1,0,1), desc='Inlet compression type indicator\n= -1, Inlet geometry is based solely on the geometry variables described above.\n=  0, Inlet geometry is based in the internal geometry data base for external compression inlets and the given inlet design Mach number.\n=  1, Inlet geometry is based in the internal geometry data base for mixed compression inlets and the given inlet design Mach number', aliases=('Use geometry variables', 'External compression inlet', 'Mixed compression inlet'),typerVar='Enum')
        self.add_param(strChain+'radd',val=3.0, units='inch', desc='Distance from the engine compressor tip to the exterior of the nacelle.  If RADD < 1. the added radial distance is RADD times the compressor tip radius.',typerVar='Float')
        self.add_param(strChain+'xnlod',val=-10.0, desc='Nozzle length / diameter (Default is computed',typerVar='Float')
        self.add_param(strChain+'xnld2',val=-10.0, desc='Fan nozzle length / diameter (Default is computed',typerVar='Float')
        self.add_param(strChain+'inac',val=0,optionsVal=(-5,-4,-3,-2,-1,0,1,2,3,4,5), desc='Nacelle type indicator', aliases=('2-D Bifurcated inlet + axisymmetric nozzle + podded together', '2-D Bifurcated inlet + 2-D nozzle + podded together', '2-D inlet + axisymmetric nozzle + podded together', '2-D + podded together', 'Axisymmetric + podded together', 'None', 'Axisymmetric', '2-D', '2-D inlet + Axisymmetric nozzle', '2-D Bifurcated inlet + 2-D nozzle', '2-D Bifurcated inlet + axisymmetric nozzle'),typerVar='Enum')
        self.add_param(strChain+'ivar',val=1,optionsVal=(-1,0,1,2,3), desc='Inlet variable geometry switch used to estimate weight factor WTCB1', aliases=('Fixed no centerbody', 'Fixed centerbody', 'Translating centerbody', 'Collapsing centerbody', 'Translating & collapsing centerbody'),typerVar='Enum')
        self.add_param(strChain+'nvar',val=0,optionsVal=(0,1,2,3,4), desc='Nozzle variable geometry switch used to estimate weight factor WTNOZ', aliases=('Fixed geometry', 'Variable area throat', 'Variable area exit', 'Variable throat & exit', 'Fixed plug core & fixed fan nozzle'),typerVar='Enum')
        self.add_param(strChain+'wtcb1',val=-10.0, desc='Weighting factor for the inlet centerbody up to the throat.   Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typerVar='Float')
        self.add_param(strChain+'wtcb2',val=-10.0, desc='Weighting factor for the inlet centerbody from the throat to the engine face.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typerVar='Float')
        self.add_param(strChain+'wtint',val=-10.0, desc='Weighting factor for the internal cowl up to the engine face.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typerVar='Float')
        self.add_param(strChain+'wtext',val=-10.0, desc='Weighting factor for the external nacelle.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typerVar='Float')
        self.add_param(strChain+'wtnoz',val=-10.0, desc='Weighting factor for the nozzle.  Multiplied by the surface area of the applicable inlet section to predict inlet weight.  The default is based on the internal materials data base and the maximum cruise Mach number.',typerVar='Float')
        self.add_param(strChain+'h2w',val=1.0, desc='Inlet height to width ratio for 2-D inlets',typerVar='Float')


    def FlopsWrapper_input_mission_definition(self):
        """Container for input:mission_definition"""
        strChain = 'input:mission_definition:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'mission',val='in' ,typeVar='List',other='itype')


    def FlopsWrapper_input_missin_User_Weights(self):
        """Container for input:missin:User_Weights"""
        strChain = 'input:missin:User_Weights:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'mywts',val=0,optionsVal=(0,1), desc='Weight input switch, overrides value input in Namelist &WTIN.', aliases=('Compute weight', 'User-specified'),typerVar='Enum')
        self.add_param(strChain+'rampwt',val=0.0, units='lb', desc='Gross weight before taxi out (Default = DOWE + PAYLOD + FUEMAX)',typerVar='Float')
        self.add_param(strChain+'dowe',val=0.0, units='lb', desc='Fixed operating weight empty',typerVar='Float')
        self.add_param(strChain+'paylod',val=0.0, units='lb', desc='Fixed payload weight',typerVar='Float')
        self.add_param(strChain+'fuemax',val=0.0, units='lb', desc='Total usable fuel weight\nFUEMAX = RAMPWT - DOWE - PAYLOD.\nRequired only if RAMPWT is not input',typerVar='Float')


    def FlopsWrapper_input_missin_Turn_Segments(self):
        """Container for input:missin:Turn_Segments"""
        strChain = 'input:missin:Turn_Segments:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'xnz',val=numpy_float64, units='g', desc='Maximum turn load factor at each Mach number',typerVar='Array')
        self.add_param(strChain+'xcl',val=numpy_float64, desc='Maximum turn lift coefficient at each Mach number',typerVar='Array')
        self.add_param(strChain+'xmach',val=numpy_float64, desc='Mach number array corresponding to both XNZ and XCL',typerVar='Array')


    def FlopsWrapper_input_missin_Store_Drag(self):
        """Container for input:missin:Store_Drag"""
        strChain = 'input:missin:Store_Drag:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'stma',val=numpy_float64, desc='Mach number schedule for store drags.  Store drags can also be assessed in ACCEL and TURN segments of the mission as covered in the Segment Definition Cards section, in PS and NZ plots (see Namelist &OPTION), and in performance constraints (see Namelist &PCONIN)',typerVar='Array')
        self.add_param(strChain+'cdst',val=numpy_float64, desc='Corresponding drag coefficients or D/q',typerVar='Array')
        self.add_param(strChain+'istcl',val=numpy_int64, desc='Store drag condition applied to climb schedule K\n= 0, No store drag for climb schedule K',typerVar='Array')
        self.add_param(strChain+'istcr',val=numpy_int64, desc='Store drag condition applied to cruise schedule K\n= 0, No store drag for cruise schedule K',typerVar='Array')
        self.add_param(strChain+'istde',val=0, desc='Store drag condition applied to descent schedule\n= 0, No store drag for descent schedule',typerVar='Int')


    def FlopsWrapper_input_missin_Reserve(self):
        """Container for input:missin:Reserve"""
        strChain = 'input:missin:Reserve:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'irs',val=2,optionsVal=(1,2,3), desc='Reserve fuel calculation switch', aliases=('Calculated for trip to alternate airport plus RESRFU and/or RESTRP', 'Constant values (RESRFU and/or RESTRP) only', 'Reserve fuel is what is left over after primary mission'),typerVar='Enum')
        self.add_param(strChain+'resrfu',val=0.0, desc='> 1., Fixed reserve fuel, lb\n< 1., Reserve fuel as a fraction of total usable fuel weight',typerVar='Float')
        self.add_param(strChain+'restrp',val=0.0, desc='Reserve fuel as a fraction of total trip fuel weight',typerVar='Float')
        self.add_param(strChain+'timmap',val=0.0, units='min', desc='Missed approach time',typerVar='Float')
        self.add_param(strChain+'altran',val=0.0, units='nmi', desc='Range to alternate airport',typerVar='Float')
        self.add_param(strChain+'nclres',val=1, desc='Climb schedule number used in reserve mission',typerVar='Int')
        self.add_param(strChain+'ncrres',val=1, desc='Cruise schedule number used in reserve mission',typerVar='Int')
        self.add_param(strChain+'sremch',val=-1.0, desc='Start reserve Mach number (Default = CLMMIN[NCLRES])',typerVar='Float')
        self.add_param(strChain+'eremch',val=-1.0, desc='End reserve Mach number (Default = DEMMIN)',typerVar='Float')
        self.add_param(strChain+'srealt',val=-1.0, units='ft', desc='Start reserve altitude (Default = CLAMIN[NCLRES])',typerVar='Float')
        self.add_param(strChain+'erealt',val=-1.0, units='ft', desc='End reserve altitude (Default = DEAMIN)',typerVar='Float')
        self.add_param(strChain+'holdtm',val=0.0, units='min', desc='Reserve holding time',typerVar='Float')
        self.add_param(strChain+'ncrhol',val=0, desc='Cruise schedule number for hold (Default = NCRRES)',typerVar='Int')
        self.add_param(strChain+'ihopos',val=1,optionsVal=(0,1,2), desc='Hold position switch', aliases=('Between main descent and missed approach', 'End of reserve cruise', 'End of reserve descent'),typerVar='Enum')
        self.add_param(strChain+'icron',val=0,optionsVal=(0,1,2), desc='Type of flight to alternate airport', aliases=('Climb-cruise-descend', 'Climb-cruise-beam down to airport', 'Cruise only'),typerVar='Enum')
        self.add_param(strChain+'thold',val=0.0, desc='Used to define a hold segment between main mission descent and missed approach.\n> 1., Reserve holding time, min\n< 1., Fraction of flight time to be used as reserve holding time.  (Effective only if IRW = 1)\n= 0., This option is ignored',typerVar='Float')
        self.add_param(strChain+'ncrth',val=1, desc='Cruise schedule number for THOLD',typerVar='Int')


    def FlopsWrapper_input_missin_Ground_Operations(self):
        """Container for input:missin:Ground_Operations"""
        strChain = 'input:missin:Ground_Operations:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'takotm',val=0.0, units='min', desc='Takeoff time',typerVar='Float')
        self.add_param(strChain+'taxotm',val=0.0, units='min', desc='Taxi out time',typerVar='Float')
        self.add_param(strChain+'apprtm',val=0.0, units='min', desc='Approach time',typerVar='Float')
        self.add_param(strChain+'appfff',val=2.0, desc='Approach fuel flow factor applied to sea level static idle fuel flow',typerVar='Float')
        self.add_param(strChain+'taxitm',val=0.0, units='min', desc='Taxi in time',typerVar='Float')
        self.add_param(strChain+'ittff',val=0, desc='> 0, Engine deck power setting for takeoff (Usually = 1 if specified).  Taxi fuel flow is sea level static idle.\n= 0, Use TAKOFF and TXFUFL.',typerVar='Int')
        self.add_param(strChain+'takoff',val=0.0, units='lb/h', desc='Takeoff fuel flow',typerVar='Float')
        self.add_param(strChain+'txfufl',val=0.0, units='lb/h', desc='Taxi fuel flow',typerVar='Float')
        self.add_param(strChain+'ftkofl',val=0.0, units='lb', desc='Fixed takeoff fuel.  This ovverides the calculated value and is not scaled with engine thrust',typerVar='Float')
        self.add_param(strChain+'ftxofl',val=0.0, units='lb', desc='Fixed taxi out fuel.  This ovverides the calculated value and is not scaled with engine thrust',typerVar='Float')
        self.add_param(strChain+'ftxifl',val=0.0, units='lb', desc='Fixed taxi in fuel.  This ovverides the calculated value and is not scaled with engine thrust',typerVar='Float')
        self.add_param(strChain+'faprfl',val=0.0, units='lb', desc='Fixed approach fuel.  This ovverides the calculated value and is not scaled with engine thrust',typerVar='Float')


    def FlopsWrapper_input_missin_Descent(self):
        """Container for input:missin:Descent"""
        strChain = 'input:missin:Descent:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ivs',val=1,optionsVal=(0,1,2), desc='Descent option switch', aliases=('No descent time or distance or fuel', 'Descend at optimum L/D', 'Descend at constance lift coefficient'),typerVar='Enum')
        self.add_param(strChain+'decl',val=0.8, desc='Descent lift coefficient for IVS = 2',typerVar='Float')
        self.add_param(strChain+'demmin',val=0.3, desc='Minimum Mach number',typerVar='Float')
        self.add_param(strChain+'demmax',val=0.0, desc='Max Mach number (Default = VCMN, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'deamin',val=0.0, units='ft', desc='Minimum altitude',typerVar='Float')
        self.add_param(strChain+'deamax',val=0.0, units='ft', desc='Max altitude (Default = CH, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'ninde',val=31, desc='Number of descent steps',typerVar='Int')
        self.add_param(strChain+'dedcd',val=0.0, desc='Drag coefficient increment applied to descent',typerVar='Float')
        self.add_param(strChain+'rdlim',val=-99999.0, units='ft/min', desc='Limiting or constant rate of descent.  Must be negative',typerVar='Float')
        self.add_param(strChain+'ns',val=0, desc='Number of altitudes for q limit schedule (Default = 0 - QLIM is used, Maximum = 20 )',typerVar='Int')
        self.add_param(strChain+'keasvd',val=0,optionsVal=(0,1), desc='= 1, VDTAB is in knots equivalent airspeed (keas)\n\n= 0, VDTAB is true airspeed or Mach number (Default)', aliases=('VDTAB is Mach number', 'VDTAB in knots'),typerVar='Enum')
        self.add_param(strChain+'adtab',val=numpy_float64, units='ft', desc='Descent altitude schedule.  If only part of the descent profile is specified, the portion of the profile outside the energy range defined by values of ADTAB and VDTAB will be optimized for the descent schedule.',typerVar='Array')
        self.add_param(strChain+'vdtab',val=numpy_float64, desc='Descent speed schedule, kts or Mach number',typerVar='Array')


    def FlopsWrapper_input_missin_Cruise(self):
        """Container for input:missin:Cruise"""
        strChain = 'input:missin:Cruise:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ncruse',val=1, desc='Number of cruise schedules to be defined (Default = 1, Maximum = 6, Include reserve cruise)',typerVar='Int')
        self.add_param(strChain+'ioc',val=1, optionsVal='(0,1,2,3,4,5,6,7,8,9,10)', aliases=('Opt. alt. and Mach for specific range', 'Fixed Mach + opt. alt. for specific range', 'Fixed Mach at input max. alt. or cruise ceiling', 'Fixed alt. + opt. Mach for specific range', 'Fixed alt. + opt. Mach for endurance (min. fuel flow)', 'Fixed alt. + constant lift coefficient (CRCLMX)', 'Fixed Mach + opt. alt. for endurance', 'Opt. Mach and alt. for endurance', 'Max. Mach at input fixed alt.', 'Max. Mach at opt. alt.', 'Fixed Mach + constant lift coefficient (CRCLMX'), desc='Cruise option switch',typeVar='List')
        self.add_param(strChain+'crmach',val=array([0.0]), dtype=numpy_float64, desc='Maximum or fixed Mach number (or velocity, kts) (Default = VCMN, Namelist &CONFIN)',typerVar='Array')
        self.add_param(strChain+'cralt',val=array([-1.0]), dtype=numpy_float64, units='ft', desc='Maximum or fixed altitude (Default = CH, Namelist &CONFIN)',typerVar='Array')
        self.add_param(strChain+'crdcd',val=array([0.0]), dtype=numpy_float64, desc='Drag coefficient increment',typerVar='Array')
        self.add_param(strChain+'flrcr',val=array([1.0]), dtype=numpy_float64, desc='Specific range factor for long range cruise Mach number - used if IOC = 3',typerVar='Array')
        self.add_param(strChain+'crmmin',val=array([0.0]), dtype=numpy_float64, desc='Minimum Mach number',typerVar='Array')
        self.add_param(strChain+'crclmx',val=array([0.0]), dtype=numpy_float64, desc='Maximum or fixed lift coefficient',typerVar='Array')
        self.add_param(strChain+'hpmin',val=array([1000.0]), dtype=numpy_float64, units='ft', desc='Minimum cruise altitude.\nFor fixed Mach number cruise schedules, HPMIN can be used to enforce a dynamic pressure (Q) limit.',typerVar='Array')
        self.add_param(strChain+'ffuel',val=array([1.0]), dtype=numpy_float64, desc='Fuel factor in cruise profile optimization',typerVar='Array')
        self.add_param(strChain+'fnox',val=array([0.0]), dtype=numpy_float64, desc='NOx emissions factor in cruise profile optimization.\nSince for supersonic engines the NOx emissions are on the order of 1 - 3 percent of fuel, FNOX should be relatively large (30. - 100.) to get comparable weighting.',typerVar='Array')
        self.add_param(strChain+'ifeath',val=0, optionsVal='(1,0,-1)', desc='Cruise feathering option', aliases=('Engines may be feathered', 'No feathering', 'Engines must be feathered'),typeVar='List')
        self.add_param(strChain+'feathf',val=array([0.5]), dtype=numpy_float64, desc='Fraction of engines remaining after feathering',typerVar='Array')
        self.add_param(strChain+'cdfeth',val=array([0.0]), dtype=numpy_float64, desc='Drag coefficient increase due to feathered engines',typerVar='Array')
        self.add_param(strChain+'dcwt',val=1.0, units='lb', desc='Weight increment used to compute cruise tables (Default = the greater of 1. or DWT/20)',typerVar='Float')
        self.add_param(strChain+'rcin',val=100.0, units='ft/min', desc='Instantaneous rate of climb for ceiling calculation',typerVar='Float')
        self.add_param(strChain+'wtbm',val=numpy_float64, desc='Array of weights for specification of max. allowable altitude for low sonic boom configurations (must be in ascending order) Since linear interpolation/extrapolation is used, data should cover the entire expected weight range.',typerVar='Array')
        self.add_param(strChain+'altbm',val=numpy_float64, units='ft', desc='Corresponding array of maximum altitudes',typerVar='Array')


    def FlopsWrapper_input_missin_Climb(self):
        """Container for input:missin:Climb"""
        strChain = 'input:missin:Climb:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nclimb',val=1, desc='Number of climb schedules to be defined (Default = 1, Maximum = 4, Include reserve climb)',typerVar='Int')
        self.add_param(strChain+'clmmin',val=array([0.3]), dtype=numpy_float64, desc='Minimum Mach number for each climb schedule.\nNote: Separate climb schedules are not required if the only changes are in the minimum or maximum Mach number or altitude.  Just make sure all climbs are bracketed.',typerVar='Array')
        self.add_param(strChain+'clmmax',val=array([0.0]), dtype=numpy_float64, desc='Maximum Mach number (Default = VCMN, Namelist &CONFIN).\nNote: Separate climb schedules are not required if the only changes are in the minimum or maximum Mach number or altitude.  Just make sure all climbs are bracketed.',typerVar='Array')
        self.add_param(strChain+'clamin',val=array([0.0]), dtype=numpy_float64, units='ft', desc='Minimum altitude',typerVar='Array')
        self.add_param(strChain+'clamax',val=array([0.0]), dtype=numpy_float64, units='ft', desc='Maximum altitude (Default = CH, Namelist &CONFIN)',typerVar='Array')
        self.add_param(strChain+'nincl',val=array([31]), dtype=numpy_int64, desc='Number of climb steps',typerVar='Array')
        self.add_param(strChain+'fwf',val=array([-0.0010]), dtype=numpy_float64, desc='Climb profile optimization function control parameter.  Recommended aircraft in parentheses.\n=  1., minimum fuel-to-distance profile (Subsonic transports, do NOT use for supersonic transports)\n=  0., minimum time-to-distance profile (Interceptors only)\n1. > FWF > 0., combination of the above\n= -.001, minimum time-to-climb profile (Fighters)\n= -1., minimum fuel-to-climb profile (Supersonic transports, Subsonic transports)\n-1. < FWF < -.001, combination of the above',typerVar='Array')
        self.add_param(strChain+'ncrcl',val=array([1]), dtype=numpy_int64, desc='Number of the cruise schedule to be used in fuel- or time-to-distance profile climb optimization comparisons',typerVar='Array')
        self.add_param(strChain+'cldcd',val=array([0.0]), dtype=numpy_float64, desc='Drag coefficient increment applied to each climb schedule.  If coefficient varies with Mach number, see ISTCL above.',typerVar='Array')
        self.add_param(strChain+'ippcl',val=array([1]), dtype=numpy_int64, desc='Number of power settings to be considered for climb.  Program will select the most efficient.  Should be used only with afterburning engines for minimum fuel climb profiles.',typerVar='Array')
        self.add_param(strChain+'maxcl',val=array([1]), dtype=numpy_int64, desc='Maximum power setting used for climb',typerVar='Array')
        self.add_param(strChain+'actab',val=zeros(shape=(0,0)), dtype=numpy_float64, units='ft', desc='Altitude schedule.  If not input, climb profile will be optimized',typerVar='Array')
        self.add_param(strChain+'vctab',val=zeros(shape=(0,0)), dtype=numpy_float64, units='nmi', desc='Climb speed schedule.  If not input, climb profile will be optimized',typerVar='Array')
        self.add_param(strChain+'keasvc',val=0,optionsVal=(1,0), desc='Type of velocity input in VCTAB', aliases=('Knots equivalent airspeed (keas)', 'True airspeed or Mach no.'),typerVar='Enum')
        self.add_param(strChain+'ifaacl',val=1,optionsVal=(0,1,2), desc='Climb speed limit option', aliases=('Optimum speed', 'Max. 250 knots CAS below 10,000 ft', 'Climb to 250 kcas at 1500 ft then SPDLIM at 10,000 ft'),typerVar='Enum')
        self.add_param(strChain+'ifaade',val=-1,optionsVal=(-1,0,1), desc='Descent speed limit option', aliases=('Use default', 'Optimum speed', 'Max. 250 knots CAS below 10,000 ft'),typerVar='Enum')
        self.add_param(strChain+'nodive',val=0,optionsVal=(0,1), desc='Rate of climb limit option', aliases=('Optimum altitude at each energy level', 'Min. rate of climb limit enfored'),typerVar='Enum')
        self.add_param(strChain+'divlim',val=0.0, units='ft/min', desc='Minimum allowable rate of climb or descent.\nEnforced only if NODIVE = 1, may be negative to allow a shallow dive during climb.',typerVar='Float')
        self.add_param(strChain+'qlim',val=0.0, units='psf', desc='Constant dynamic pressure limit.  Applied at all climb and descent points not covered by the variable dynamic pressure limit below.',typerVar='Float')
        self.add_param(strChain+'spdlim',val=0.0, desc='Maximum speed at 10,000 ft, used only for IFAACL = 2, kts or Mach number  (Default is computed from\n  a) the variable dynamic pressure limit below, if applicable,\n  b) QLIM above, if QLIM > 0., or\n  c) a dynamic pressure of 450 psf, in that order)',typerVar='Float')
        self.add_param(strChain+'nql',val=0, desc='Number of altitudes for q limit schedule (Default = 0 - QLIM is used, Maximum = 20 )',typerVar='Int')
        self.add_param(strChain+'qlalt',val=numpy_float64, units='ft', desc='Altitudes, in increasing order, for variable dynamic pressure limit schedule',typerVar='Array')
        self.add_param(strChain+'vqlm',val=numpy_float64, units='psf', desc='Corresponding dynamic pressure limits',typerVar='Array')


    def FlopsWrapper_input_missin_Basic(self):
        """Container for input:missin:Basic"""
        strChain = 'input:missin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'indr',val=0,optionsVal=(0,1), desc='= 0, DESRNG is design range in n.mi.\n= 1, DESRNG is endurance in minutes', aliases=('Range', 'Endurance'),typerVar='Enum')
        self.add_param(strChain+'fact',val=1.0, desc='Factor to increase or decrease fuel flows.  Cumulative with FFFSUB and FFFSUP in Namelist &ENGDIN.',typerVar='Float')
        self.add_param(strChain+'fleak',val=0.0, units='lb/h', desc='Constant delta fuel flow',typerVar='Float')
        self.add_param(strChain+'fcdo',val=1.0, desc='Factor to increase or decrease lift-independent drag coefficients',typerVar='Float')
        self.add_param(strChain+'fcdi',val=1.0, desc='Factor to increase or decrease lift-dependent drag coefficients',typerVar='Float')
        self.add_param(strChain+'fcdsub',val=1.0, desc='Factor to increase or decrease all subsonic drag coefficients.  Cumulative with FCDO and FCDI.',typerVar='Float')
        self.add_param(strChain+'fcdsup',val=1.0, desc='Factor to increase or decrease all supersonic drag coefficients.  Cumulative with FCDO and FCDI.',typerVar='Float')
        self.add_param(strChain+'iskal',val=1,optionsVal=(1,0), desc='Special option used to turn off engine scaling using THRUST/THRSO', aliases=('Scale engine', 'No scaling'),typerVar='Enum')
        self.add_param(strChain+'owfact',val=1.0, desc='Factor for increasing or decreasing OWE',typerVar='Float')
        self.add_param(strChain+'iflag',val=0,optionsVal=(0,1,2,3), desc='Mission print option', aliases=('Mission summary only', 'Plus cruise', 'Plus climb & descent', 'Plus scaled engine'),typerVar='Enum')
        self.add_param(strChain+'msumpt',val=0,optionsVal=(1,0), desc='Option to calculate and print detailed mission summary', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'dtc',val=0.0, units='degC', desc='Deviation from standard day temperature (See also DTCT in Namelist &TOLIN and DTCE in Namelist &ENGINE.  These temperature deviations are independent.)',typerVar='Float')
        self.add_param(strChain+'irw',val=2,optionsVal=(1,2), desc='Range/weight calculation option', aliases=('Range fixed-calculate ramp weight', 'Ramp weight fixed-calculate range'),typerVar='Enum')
        self.add_param(strChain+'rtol',val=0.001, units='nmi', desc='Tolerance in range calculation for IRW = 1',typerVar='Float')
        self.add_param(strChain+'nhold',val=0, desc='Special option - Time for segment NHOLD (which must be a Hold Segment) is adjusted until the specified range is met for the input ramp weight.  Note - IRW must be 1',typerVar='Int')
        self.add_param(strChain+'iata',val=1,optionsVal=(1,0), desc='Option to adjust range for ATA Traffic Allowance', aliases=('Yes', 'No'),typerVar='Enum')
        self.add_param(strChain+'tlwind',val=0.0, units='nmi', desc='Velocity of tail wind (Input negative value for head wind)',typerVar='Float')
        self.add_param(strChain+'dwt',val=1.0, units='lb', desc='Gross weight increment for performance tables (Default is internally computed)',typerVar='Float')
        self.add_param(strChain+'offdr',val=numpy_float64, units='nmi', desc='Off design range.  Note: This simply performs the defined mission with the sized airplane with a different design range.  If more changes are desired or if additional analyses are required (e.g., cost analysis), use Namelist &RERUN.  If OFFDR is used with a cost analysis, costs will be computed for the last design range.',typerVar='Array')
        self.add_param(strChain+'idoq',val=0,optionsVal=(1,0), desc='Form for drag increments', aliases=('D/q', 'Drag coefficients'),typerVar='Enum')
        self.add_param(strChain+'nsout',val=0, desc='Last segment number in outbound leg (Combat Radius Mission - Iterates until outbound leg and inbound leg are equal.  IRW must be equal to 2, and there must be at least two cruise segments).  If NSOUT = 0, radius is not calculated',typerVar='Int')
        self.add_param(strChain+'nsadj',val=0, desc='Cruise segment in outbound leg to be adjusted for radius calculation (Default = NSOUT).  Note: Make sure that the NSADJ Cruise segment is terminated on total rather than segment distance in the Mission Definition Data.',typerVar='Int')
        self.add_param(strChain+'mirror',val=0, desc='Cruise segment in inbound leg to be set equal to segment NSADJ  (if MIRROR = 0, only total leg lengths are forced to be equal).  This option would be used for a high-low-low-high mission where the dash in and dash out are unknown but must be equal to each other.  NSADJ would be the dash in segment number, and MIRROR would be the dash out segment number.',typerVar='Int')


    def FlopsWrapper_input_fusein_Basic(self):
        """Container for input:fusein:Basic"""
        strChain = 'input:fusein:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'fpitch',val=0.0, units='inch', desc='Seat pitch for the first class passengers',typerVar='Float')
        self.add_param(strChain+'nfabr',val=0, desc='Number of first class passengers abreast',typerVar='Int')
        self.add_param(strChain+'bpitch',val=0.0, units='inch', desc='Seat pitch for business class passengers',typerVar='Float')
        self.add_param(strChain+'nbabr',val=0, desc='Number of business class passengers abreast',typerVar='Int')
        self.add_param(strChain+'tpitch',val=0.0, units='inch', desc='Seat pitch for tourist class passengers',typerVar='Float')
        self.add_param(strChain+'ntabr',val=0, desc='Number of tourist class passengers abreast',typerVar='Int')


    def FlopsWrapper_input_fusein_BWB(self):
        """Container for input:fusein:BWB"""
        strChain = 'input:fusein:BWB:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'osspan',val=0.0, units='ft', desc='Outboard semispan (Default = ETAW(NETAW), required if ETAW(NETAW) is less than or equal to 1.0 and IFITE = 3 and NETAW > 1)\nThis variable is used if a detailed wing outboard panel (See Detailed Wing Data in Namelist $WTIN) is being added to a BWB fuselage.',typerVar='Float')
        self.add_param(strChain+'tipchd',val=0.0, units='ft', desc='Wing tip chord (Default = 0.06*Wing span)\nThis variable is used if the wing outer panel is defined as a trapezoid attached to the BWB cabin.',typerVar='Float')
        self.add_param(strChain+'nesob',val=0, desc='Wing eta station number for outboard side of body.  If this variable is greater than 1, the detailed wing definition is assumed to include the cabin.  Weight calculations for the outboard wing start at this eta station. (If = 0, the detailed outboard wing is added to the cabin as indicated above.)',typerVar='Int')
        self.add_param(strChain+'acabin',val=0.0, units='ft*ft', desc='Fixed area of passenger cabin for blended wing body transports (Default is internally computed based on passenger data)',typerVar='Float')
        self.add_param(strChain+'xlw',val=0.0, units='ft', desc='Fixed length of side wall.\nThis is the outboard wall of the passenger cabin and is used to define the outboard wing root chord.',typerVar='Float')
        self.add_param(strChain+'xlwmin',val=0.0, units='ft', desc='Minimum side wall length.  The typical value of 38.5 ft is based on a required maximum depth at the side wall of 8.25 ft divided by a fuselage thickness/chord ratio of 0.15 and 70 percent of the resulting wing root chord of 55 ft.',typerVar='Float')
        self.add_param(strChain+'nbay',val=0, desc='Fixed number of bays',typerVar='Int')
        self.add_param(strChain+'nbaymx',val=0, desc='Maximum number of bays',typerVar='Int')
        self.add_param(strChain+'bayw',val=0.0, units='ft', desc='Fixed bay width',typerVar='Float')
        self.add_param(strChain+'baywmx',val=0.0, units='ft', desc='Maximum bay width',typerVar='Float')
        self.add_param(strChain+'swple',val=45.0, units='deg', desc='Sweep angle of the leading edge of the passenger cabin',typerVar='Float')
        self.add_param(strChain+'cratio',val=0.0, desc='Fixed ratio of the centerline length to the cabin width (XLP/WF)',typerVar='Float')
        self.add_param(strChain+'tcf',val=0.0, desc='Fuselage thickness/chord ratio (Default = TCA, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'tcsob',val=0.0, desc='Fuselage thickness/chord ratio at side of body (Default = TCF)',typerVar='Float')
        self.add_param(strChain+'rspchd',val=0.0, desc='Rear spar percent chord for BWB fuselage and wing (Default = 70 percent)',typerVar='Float')
        self.add_param(strChain+'rspsob',val=0.0, desc='Rear spar percent chord for BWB fuselage at side of body (Default = 70 percent)',typerVar='Float')



    def FlopsWrapper_input_engine_deck(self):
        """Container for input:engine_deck"""
        strChain = 'input:engine_deck:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'engdek',val='',typeVar='Str')


    def FlopsWrapper_input_engine_Other(self):
        """Container for input:engine:Other"""
        strChain = 'input:engine:Other:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'hpcpr',val=5.0, desc='Pressure ratio of the high pressure (third) compressor (Only used if there are three compressor components)',typerVar='Float')
        self.add_param(strChain+'aburn' ,val=False, desc='True if there is an afterburner',typeVar='Bool')
        self.add_param(strChain+'dburn',val=False, desc='True if there is a duct burner (Separate flow turbofans only).  ABURN and DBURN cannot both be true.',typeVar='Bool')
        self.add_param(strChain+'effab',val=0.85, desc='Afterburner/duct burner efficiency',typerVar='Float')
        self.add_param(strChain+'tabmax',val=3500.0, units='degR', desc='Maximum afterburner/duct burner temperature',typerVar='Float')
        self.add_param(strChain+'ven',val=False, desc='True if the exhaust nozzle has a variable flow area.  The nozzle flow area is automatically allowed to vary for cases when the afterburner or duct burner is on.',typoVar='Bool')
        self.add_param(strChain+'costbl',val=1.0, units='lb/s', desc='Customer high pressure compressor bleed',typerVar='Float')
        self.add_param(strChain+'fanbl',val=0.0, desc='Fan bleed fraction, only used for bypass engines',typerVar='Float')
        self.add_param(strChain+'hpext',val=200.0, units='hp', desc='Customer power extraction',typerVar='Float')
        self.add_param(strChain+'wcool',val=-1.0e-4, desc='Turbine cooling flow as a fraction of high pressure compressor mass flow. The cooling flow defaults to the value in the engine cycle definition file. If WCOOL is input greater than or equal to zero the default will be overridden.\nIf WCOOL > 1., the turbine cooling flow fraction required to bring the turbine inlet temperature down to WCOOL will be computed.',typerVar='Float')
        self.add_param(strChain+'fhv',val=18500.0, units='Btu/lb', desc='Fuel heating value',typerVar='Float')
        self.add_param(strChain+'dtce',val=0.0, units='degC', desc='Deviation from standard day temperature.  The deviation, as used in the cycle analysis module, is DTCE at sea level and varies to zero at ALC (see below). The design point is at standard temperature.',typerVar='Float')
        self.add_param(strChain+'alc',val=10000.0, units='ft', desc='The altitude at which DTCE (see above) becomes zero.',typerVar='Float')
        self.add_param(strChain+'year',val=1985.0, desc='Technology availability date used to estimate compressor polytropic efficiency',typerVar='Float')
        self.add_param(strChain+'boat',val=False, desc='True to include boattail drag',typeVar='Bool')
        self.add_param(strChain+'ajmax',val=0.0, units='ft*ft', desc='Nozzle reference area for boattail drag.  Used only if BOAT = true.  Default is the largest of\n1) 1.1 times the inlet capture area\n2) Nozzle exit area at the inlet design point\n3) Estimated engine frontal area\n4) Estimated nozzle entrance area\nor\nIf nacelle weight and geometry calculations are\nperformed (see NGINWT below) AJMAX is set to the\nnacelle cross-sectional area at the customer connect. \nor\nIf AJMAX is less than zero, the cruise design point\nnozzle exit area multiplied by the absolute value\nof AJMAX is used as the reference.',typerVar='Float')
        self.add_param(strChain+'spill',val=False, desc='True to include spillage and lip drag in engine performance data',typeVar='Bool')
        self.add_param(strChain+'lip',val =False, desc='Compute inlet cowl lip drag.  Used only if SPILL = true',typeVar='Bool')
        self.add_param(strChain+'blmax',val=-1.0, desc='Inlet bleed flow fraction of total flow at the inlet design point (Default = .016 * AMINDS**1.5).  Used only if SPILL = true',typerVar='Float')
        self.add_param(strChain+'spldes',val=0.01, desc='Inlet design spillage fraction.  Used only if SPILL = true',typerVar='Float')
        self.add_param(strChain+'aminds',val=0.0, desc='Inlet design Mach number (Default = XMMAX).  Used only if SPILL = true',typerVar='Float')
        self.add_param(strChain+'alinds',val=0.0, units='ft', desc='Inlet design altitude (Default = AMAX).  Used only if SPILL = true',typerVar='Float')
        self.add_param(strChain+'etaprp',val=0.84, desc='Maximum propeller efficiency (Turboprops only). The actual propeller efficiency is based on an internal schedule of efficiency versus Mach number with the maximum efficiency (ETAPRP) occurring at a Mach number of 0.80.  To use the Hamilton Standard Method set ETAPRP=1 and input the propeller characteristics as defined under ',typerVar='Float')
        self.add_param(strChain+'shpowa',val=60.0, units='hp/(lb/s)', desc='Design point shaft horsepower divided by the design point core airflow',typerVar='Float')
        self.add_param(strChain+'cdtmax',val=99999.0, units='degR', desc='Maximum allowable compressor discharge temperature',typerVar='Float')
        self.add_param(strChain+'cdpmax',val=99999.0, units='psi', desc='Maximum allowable compressor discharge pressure',typerVar='Float')
        self.add_param(strChain+'vjmax',val=99999.0, units='ft/s', desc='(IENG < 100) Maximum allowable jet velocity\n(IENG > 100) Propeller tip speed',typerVar='Float')
        self.add_param(strChain+'stmin',val=1.0, units='lb/lb/s', desc='Minimum allowable specific thrust',typerVar='Float')
        self.add_param(strChain+'armax',val=99999.0, desc='Maximum allowable ratio of the bypass area to the core area of a mixed flow turbofan',typerVar='Float')
        self.add_param(strChain+'limcd',val=1,optionsVal=(0,1,2), desc='Switch to use the compressor discharge temperature and pressure limits only for optimization.', aliases=('Limit at cruise design Mach and altitude only for optimization', 'Limit at all points in envelope', 'Limit max. compressor discharge temp. everywhere'),typerVar='Enum')


    def FlopsWrapper_input_engine_Noise_Data(self):
        """Container for input:engine:Noise_Data"""
        strChain = 'input:engine:Noise_Data:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nprint',val=0,optionsVal=(-1,0,1,2), desc='Noise data print control', aliases=('Print compressor operating line', 'No print', 'Print to ANOPP', 'Print to FOOTPR'),typerVar='Enum')
        #self.add_param(strChain+'ivat',val=0,optionsVal=(0,1), desc='Flag for variable exit area low pressure turbine.  Used only for estimating LPT exit area when NPRINT=1', aliases=('Fixed', 'Variable'),typerVar='Enum')
        self.add_param(strChain+'jet',val=-1,optionsVal=(-1,0,1,2,3,4,5,6), desc='FOOTPR input data generation control', aliases=('No noise data', 'No jet noise', 'Stone/Clark', 'Kresja', 'Stone ALLJET', 'Stone JET181', 'GE M*S', 'SAE A-21'),typerVar='Enum')
        self.add_param(strChain+'ftmach',val=0.0, desc='Mach number to calculate FOOTPR input data',typerVar='Float')
        self.add_param(strChain+'ftalt',val=0.0, desc='Altitude to calculate FOOTPR input data',typerVar='Float')


    def FlopsWrapper_input_engine_IC_Engine(self):
        """Container for input:engine:IC_Engine"""
        strChain = 'input:engine:IC_Engine:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ncyl',val=4, desc='Number of cylinders',typerVar='Int')
        self.add_param(strChain+'deshp',val=180.0, units='hp', desc='Baseline engine power',typerVar='Float')
        self.add_param(strChain+'alcrit',val=0.0, units='ft', desc='Critical turbocharger altitude.  The altitude to which turbocharged IC engines are able to maintain DESHP',typerVar='Float')
        self.add_param(strChain+'sfcmax',val=0.52, units='lb/h/hp', desc='Brake specific fuel consumption at maximum power',typerVar='Float')
        self.add_param(strChain+'sfcmin',val=0.4164, units='lb/h/hp', desc='Minimum brake specific fuel consumption or SFC',typerVar='Float')
        self.add_param(strChain+'pwrmin',val=0.65, desc='Fraction of maximum power where SFCMIN occurs. If NRPM > 0 and PWRMIN > 1 then PWRMIN is the rotational speed where SFCMIN occurs (recommend PWRMIN > 1 if SFCMIN is less than about 0.4',typerVar='Float')
        self.add_param(strChain+'engspd',val=2700.0, units='1/min', desc='Maximum engine crankshaft speed',typerVar='Float')
        self.add_param(strChain+'prpspd',val=2700.0, units='1/min', desc='Maximum propeller shaft speed',typerVar='Float')
        self.add_param(strChain+'iwc',val=0,optionsVal=(0,1), desc='Cooling system', aliases=('Air cooled', 'Water cooled'),typerVar='Enum')
        self.add_param(strChain+'ecid',val=361.0, units='inch*inch*inch', desc='Engine displacement',typerVar='Float')
        self.add_param(strChain+'ecr',val=8.5, desc='Engine compression ratio',typerVar='Float')
        self.add_param(strChain+'eht',val=19.96, units='inch', desc='Engine envelope height',typerVar='Float')
        self.add_param(strChain+'ewid',val=33.37, units='inch', desc='Engine envelope width',typerVar='Float')
        self.add_param(strChain+'elen',val=31.83, units='inch', desc='Engine envelope length',typerVar='Float')
        self.add_param(strChain+'ntyp',val=2,optionsVal=(1,2,3,4,5,6), desc='Propeller type indicator', aliases=('Fixed pitch', 'Variable pitch', 'Variable pitch + full feathering', 'Variable pitch + full feathering + deicing', 'Variable pitch + full feathering + deicing w/reverse', 'Ducted fan'),typerVar='Enum')
        self.add_param(strChain+'af',val=87.6, desc='Activity factor',typerVar='Float')
        self.add_param(strChain+'cli',val=0.569, desc='Integrated design lift coefficient',typerVar='Float')
        self.add_param(strChain+'blang',val=20.0, units='deg', desc='Blade angle for fixed pitch propeller',typerVar='Float')
        self.add_param(strChain+'dprop',val=6.375, units='ft', desc='Propeller diameter',typerVar='Float')
        self.add_param(strChain+'nblade',val=0, desc='Number of blades',typerVar='Int')
        self.add_param(strChain+'gbloss',val=0.02, desc='Gearbox losses, fraction. If PRPSPD = ENGSPD, there are no losses.',typerVar='Float')
        self.add_param(strChain+'arrpm',val=numpy_float64, units='rpm', desc='Rotational speed (descending order)',typerVar='Array')
        self.add_param(strChain+'arpwr',val=numpy_float64, units='hp', desc='Engine shaft power at ARRPM(I)',typerVar='Array')
        self.add_param(strChain+'arful',val=numpy_float64, desc='Engine fuel requirements at ARRPM(I) (Required only if LFUUN is not equal to zero)',typerVar='Array')
        self.add_param(strChain+'lfuun',val=0,optionsVal=(0,1,2,3), desc='Fuel input type indicator', aliases=('Fuel flows are computed from SFCMAX SFCMIN and PWRMIN', 'Brake specific fuel consumption values are input in ARFUL', 'Actual fuel flows are input in ARFUL (lb/hr)', 'Actual fuel flows are input in ARFUL (gal/hr)'),typerVar='Enum')
        self.add_param(strChain+'feng',val=1.0, desc='Scale factor on engine weight',typerVar='Float')
        self.add_param(strChain+'fprop',val=1.0, desc='Scale factor on propeller weight',typerVar='Float')
        self.add_param(strChain+'fgbox',val=1.0, desc='Scale factor on gear box weight',typerVar='Float')


    def FlopsWrapper_input_engine_Engine_Weight(self):
        """Container for input:engine:Engine_Weight"""
        strChain = 'input:engine:Engine_Weight:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'nginwt',val=0,optionsVal=(-4,-3,-2,-1,0,1,2,3,4,5), desc='Switch for engine weight calculations.   Use the negative value to calculate the weight for the initial design and then scale engine weights and dimensions with airflow.  Zero or a negative value should always be used during optimization with engine cycle design variables.  (IENG > 100 options in parentheses)', aliases=('-Engine + inlet + nacelle + nozzle', '-Engine + inlet + nacelle', '-Engine and inlet', '-Engine only', 'None', 'Engine only (Total prop. system)', 'Engine and inlet (Propeller)', 'Engine + inlet + nacelle (Propeller + cowl + mounts)', 'Engine + inlet + nacelle + nozzle ( Propeller + cowl + mounts + exhaust)', '(Propeller + cowl + mounts + exhaust + alternator)'),typerVar='Enum')
        self.add_param(strChain+'iwtprt',val=1,optionsVal=(0,1,2,3,4), desc='Printout control for engine weight calculations.  Printout is on file OFILE.', aliases=('No output', 'Print component weights and dimensions', 'Print component design details', 'Plus initial and final optimization data', 'Print component details at each iteration'),typerVar='Enum')
        self.add_param(strChain+'iwtplt',val=0,optionsVal=(-4,-3,-2,-1,0,1,2,3,4), desc='PostScript plot control for engine (and nacelle) schematics on file PLTFIL.  If the negative value is input, only the final design will be plotted.',typerVar='Enum')
        self.add_param(strChain+'gratio',val=1.0, desc='Ratio of the RPM of the low pressure compressor to the RPM of the connected fan',typerVar='Float')
        self.add_param(strChain+'utip1',val=0.0, units='ft/s', desc='Tip speed of the first compressor (or fan) in the flow.  Default is based on YEAR, engine type, and other design considerations.',typerVar='Float')
        self.add_param(strChain+'rh2t1',val=0.0, desc='Hub to tip radius ratio of the first compressor (or fan) in the flow.  Default is based on YEAR, engine type, and other design considerations.',typerVar='Float')
        self.add_param(strChain+'igvw',val=0,optionsVal=(-2,-1,0,1,2), desc='Flag for compressor inlet guide vanes', aliases=('Variable-no fan IGV', 'Fixed-no fan IGV', 'None', 'Fixed', 'Variable'),typerVar='Enum')
        self.add_param(strChain+'trbrpm',val=0.0, units='rpm', desc='The rotational speed of any free turbine.  TRBAN2 is used to set the free turbine rotational speed if TRBRPM is not input. TRBRPM overrides TRBAN2.',typerVar='Float')
        self.add_param(strChain+'trban2',val=0.0, units='(inch*inch)/(min*min)', desc='Maximum allowable AN**2 for turbine components.  The input value is the actual maximum divided by 10**10.  AN**2 is the flow area multiplied by the rotational speed squared.  The default is based on year.',typerVar='Float')
        self.add_param(strChain+'trbstr',val=15000.0, units='psi', desc='Turbine usable stress lower limit.  Normally when component weights are predicted, the usable stress is a function of operating conditions.  For turbine components, this can be unusually low because cooling effects are not accounted for.',typerVar='Float')
        self.add_param(strChain+'cmpan2',val=0.0, units='(inch*inch)/(min*min)', desc='Maximum allowable AN**2 for compressor components.  The input value is the actual maximum divided by 10**10.  AN**2 is the flow area multiplied by the rotational speed squared.  The default is based on year.',typerVar='Float')
        self.add_param(strChain+'cmpstr',val=25000.0, units='psi', desc='Requested compressor usable stress.  This forces a change in compressor material when the current (lower temperature) material starts to run out of strength as temperature increases.',typerVar='Float')
        self.add_param(strChain+'vjpnlt',val=0.0, units='lb', desc='Weight penalty factor for a suppressor to reduce the core jet velocity to 1500 ft/sec',typerVar='Float')
        self.add_param(strChain+'wtebu',val=0.2, desc='Fraction for weight of engine build up unit (pylon, mounting hardware, etc)',typerVar='Float')
        self.add_param(strChain+'wtcon',val=0.05, desc='Fraction for weight of engine controls',typerVar='Float')


    def FlopsWrapper_input_engine_Design_Point(self):
        """Container for input:engine:Design_Point"""
        strChain = 'input:engine:Design_Point:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'desfn',val=0.0, units='lb', desc='Engine design point net dry thrust (Default = THRUST, Namelist &CONFIN).  Do not use the default for afterburning engines since THRUST is the maximum wet thrust rating.  The maximum wet (afterburning) thrust for the generated engine is transferred back to THRSO for scaling with THRUST.',typerVar='Float')
        self.add_param(strChain+'xmdes',val=-9999.0, desc='Engine optimization point Mach number (Default = VCMN, Namelist &CONFIN).  XMDES and XADES are used for propulsion only analyses (IANAL = 4).',typerVar='Float')
        self.add_param(strChain+'xades',val=-9999.0, units='ft', desc='Engine optimization point altitude (Default = CH, Namelist &CONFIN).  If XADES < 0., it is interpreted as the negative of the design point dynamic pressure (psf), and the altitude is back-calculated with a minimum of 0.',typerVar='Float')
        self.add_param(strChain+'oprdes',val=25.0, desc='Overall pressure ratio',typerVar='Float')
        self.add_param(strChain+'fprdes',val=1.5, desc='Fan pressure ratio (turbofans only)',typerVar='Float')
        self.add_param(strChain+'bprdes',val=0.0, desc='Bypass ratio (Turbofans only, Default is computed based on OPRDES, FPRDES, TTRDES, XMDES and ALDES).  If BPRDES < -1, then the bypass ratio is computed such that the ratio of the fan to core jet velocities equals the absolute value of BPRDES.  For turbine bypass engines, BPRDES must be input and is defined as the fraction of compressor exit airflow that is bypassed around the main burner and the turbine.  If both EBPR and BPRDES are zero, the optimum bypass ratio is computed at the design Mach number and altitude (XMDES, XADES).',typerVar='Float')
        self.add_param(strChain+'tetdes',val=2500.0, units='degR', desc='Engine design point turbine entry temperature',typerVar='Float')
        self.add_param(strChain+'ttrdes',val=1.0, desc='Engine throttle ratio defined as the ratio of the maximum allowable turbine inlet temperature divided by the design point turbine inlet temperature.  If TTRDES is greater than TETDES, it is assumed to be the maximum allowable turbine inlet temperature.',typerVar='Float')


    def FlopsWrapper_input_engine_Basic(self):
        """Container for input:engine:Basic"""
        strChain = 'input:engine:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ieng',val=1,optionsVal=(0,1,2,3,4,5,6,7,8,9,101), desc='Engine cycle definition input file indicator', aliases=('User-defined', 'Turbojet', 'Separate flow turbofan w/ 2 compressors', 'Mixed flow turbofan w/ 2 compressors', 'Turboprop', 'Turbine bypass', 'Separate flow turofan w/ 3 compressors', 'Mixed flow turbofan w/ 3 compressors', '3-spool separate flow turbofan w/ 3 compressors', '2-spool turbojet', 'IC engine'),typerVar='Enum')
        self.add_param(strChain+'iprint',val=1, desc='Engine cycle analysis printout control.  Printout is on file OFILE',typerVar='Int')
        self.add_param(strChain+'gendek' ,val=False, desc='Engine data will be saved on the file designated by EOFILE as an Engine Deck for future use',typeVar='Bool')
        self.add_param(strChain+'ithrot',val=1,optionsVal=(0,1,2), desc='Controls frequency of part power data generation', aliases=('All Mach-altitude combos', 'Max. altitude for each Mach', 'Max. altitude for max. Mach'),typerVar='Enum')
        self.add_param(strChain+'npab',val=0, desc='Maximum number of afterburning throttle settings for each Mach-altitude combination',typerVar='Int')
        self.add_param(strChain+'npdry',val=15, desc='Maximum number of dry (non-afterburning) throttle settings',typerVar='Int')
        self.add_param(strChain+'xidle',val=0.05, desc='Fraction of maximum dry thrust used as a cutoff for part power throttle settings',typerVar='Float')
        self.add_param(strChain+'nitmax',val=50, desc='Maximum iterations per point',typerVar='Int')
        self.add_param(strChain+'xmmax',val=-1.0, desc='Max Mach number (Default = VCMN, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'amax',val=-1.0, units='ft', desc='Max altitude (Default = CH, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'xminc',val=0.2, desc='Mach number increment (Default = .2)',typerVar='Float')
        self.add_param(strChain+'ainc',val=5000.0, units='ft', desc='Altitude increment (Default = 5000.)',typerVar='Float')
        self.add_param(strChain+'qmin',val=150.0, units='psf', desc='Minimum dynamic pressure',typerVar='Float')
        self.add_param(strChain+'qmax',val=1200.0, units='psf', desc='Maximum dynamic pressure',typerVar='Float')


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
        self.add_param(strChain+'dffac',val=0.0, desc='Fuel flow scaling constant term.\nThe engine fuel flow scale factor for ENGSKAL = THRUST/THRSO is\nENGSKAL*[1. + DFFAC + FFFAC*(1. - ENGSKAL)]',typerVar='Float')
        self.add_param(strChain+'fffac',val=0.0, desc='Fuel flow scaling linear term.\nThe engine fuel flow scale factor for ENGSKAL = THRUST/THRSO is\nENGSKAL*[1. + DFFAC + FFFAC*(1. - ENGSKAL)]',typerVar='Float')
        self.add_param(strChain+'emach',val=numpy_float64, desc='Array of Mach numbers in descending order at which engine data are to be generated (Default computed internally, Do not zero fill)',typerVar='Array')
        self.add_param(strChain+'alt',val=zeros(shape=(0,0)), dtype=numpy_float64, units='ft', desc='Arrays of altitudes in descending order, one set for each Mach number, at which engine data are to be generated (Default computed internally, do not zero fill).  Altitudes and numbers of altitudes do not have to be consistent between Mach numbers.',typerVar='Array')
        self.add_param(strChain+'insdrg',val=0,optionsVal=(0,1,2,3), desc='Nozzle installation drag scaling switch', aliases=('No drag scaling', 'Scale with A10', 'Calculate using A10', 'Calculate for Cd=0 at A9=A9ref'),typerVar='Enum')
        self.add_param(strChain+'nab',val=6969, desc='Table number in CDFILE to be used for afterbody drag',typerVar='Int')
        self.add_param(strChain+'nabref',val=6969, desc='Table number in CDFILE to be used for reference afterbody drag',typerVar='Int')
        self.add_param(strChain+'a10',val=0.0, units='inch*inch', desc='Maximum nozzle area (Required if INSDRG > 0)',typerVar='Float')
        self.add_param(strChain+'a10ref',val=0.0, units='inch*inch', desc='Reference maximum nozzle area (Required if INSDRG > 0)',typerVar='Float')
        self.add_param(strChain+'a9ref',val=0.0, units='inch*inch', desc='Reference nozzle exit area (Required if INSDRG = 3)',typerVar='Float')
        self.add_param(strChain+'xnoz',val=0.0, units='inch', desc='Nozzle length (Required if INSDRG > 0)',typerVar='Float')
        self.add_param(strChain+'xnref',val=0.0, units='inch', desc='Reference nozzle length (Required if INSDRG > 0)',typerVar='Float')
        self.add_param(strChain+'rcrv',val=-1.0, desc='Nozzle radius of curvature parameter (Triggers special nozzle drag option)',typerVar='Float')


    def FlopsWrapper_input_engdin_Basic(self):
        """Container for input:engdin:Basic"""
        strChain = 'input:engdin:Basic:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'ngprt',val=1,optionsVal=(0,1,2), desc='Print engine data tables', aliases=('No printout', 'Print tables', 'Print sorted tables'),typerVar='Enum')
        self.add_param(strChain+'igenen',val=0,optionsVal=(-3,-2,-1,0,1), desc='Switch indicating source of Engine Deck', aliases=('Response surfaces', 'External file (horsepower/rpm/fuel flow', 'External file (thrust/fuel flow)', 'Follows namelist &ENGDIN', 'Engine deck to be generated'),typerVar='Enum')
        self.add_param(strChain+'extfac',val=1.0, desc='Slope factor for extrapolating engine fuel flows for thrust levels above the maximum for that Mach number and altitude',typerVar='Float')
        self.add_param(strChain+'fffsub',val=1.0, desc='Fuel flow factor for all subsonic engine points',typerVar='Float')
        self.add_param(strChain+'fffsup',val=1.0, desc='Fuel flow factor for all supersonic engine points',typerVar='Float')
        self.add_param(strChain+'idle',val=0, desc='> 0, Flight idle data will be internally generated with zero thrust and an extrapolated fuel flow.  The fuel flow must be at least FIDMIN times the fuel flow at power setting number IDLE and no more than FIDMAX times the fuel flow at power setting number IDLE.  If NONEG (below) = 0 and negative thrusts exist, an idle power setting is not generated.\n= 0, The lowest input power setting is assumed to be flight idle (Not recommended.  Results will be more consistent with IDLE > 0)',typerVar='Int')
        self.add_param(strChain+'noneg',val=0,optionsVal=(1,0), desc='Option for using points in the Engine Deck with negative thrust', aliases=('Ignore', 'Use all points'),typerVar='Enum')
        self.add_param(strChain+'fidmin',val=0.08, desc='Minimum fraction of the fuel flow at power setting number IDLE for generated flight idle fuel flows',typerVar='Float')
        self.add_param(strChain+'fidmax',val=1.0, desc='Maximum fraction of the fuel flow at power setting number IDLE for generated flight idle fuel flows',typerVar='Float')
        self.add_param(strChain+'ixtrap',val=1, desc='Option for extrapolation of engine data beyond altitudes provided in input data, which may result in radically improved SFC',typerVar='Int')
        self.add_param(strChain+'ifill',val=2, desc='Option for filling in part power data\n=0, No part power data will be generated\n> 0, Part power cruise data will be filled in for Mach-altitude points for which IFILL (or fewer) thrust levels have been input\nFor NPCODE > 1, data will be filled in for each specified power code that is not input for each Mach-altitude point.',typerVar='Int')
        self.add_param(strChain+'maxcr',val=2, desc='Maximum power setting used for cruise',typerVar='Int')
        self.add_param(strChain+'nox',val=0,optionsVal=(0,1,2,3), desc='Option for NOx emissions data.  If IGENEN=-2, NOx emissions data are replaced with engine shaft speed, rpm', aliases=('Do not use', 'Indices in engine deck or generated', 'Emissions lb/hr in engine deck', 'Another parameter in engine deck'),typerVar='Enum')
        self.add_param(strChain+'pcode',val=numpy_float64, desc='Power codes to be used in sorting the Engine Deck.  Values correspond to thrust levels in descending order, i.e., climb, maximum continuous, part power cruise settings, and flight idle.  Actual values are arbitrary (they are just used as labels), but only points in the Engine Deck with corresponding values for PC will be used.',typerVar='Array')
        self.add_param(strChain+'boost',val=0.0, desc='> 0., Scale factor for boost engine to be added to baseline engine for takeoff and climb.  Climb thrust of the boost engine in the Engine Deck must be artificially increased by 100,000.\n= 0., No boost engine',typerVar='Float')
        self.add_param(strChain+'igeo',val=0,optionsVal=(0,1), desc='Engine deck altitude type', aliases=('Geometric', 'Geopotential-will be converted'),typerVar='Enum')


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
        self.add_param(strChain+'desmch',val=0.0, desc='Design Mach number (Default = VCMN, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'dprsmx',val=0.0, units='psf', desc='Maximum dynamic pressure (Default = 460. * DESMCH)',typerVar='Float')
        self.add_param(strChain+'veloc',val=0.0, units='mi/h', desc='Cruise velocity (Default = 660. * DESMCH)',typerVar='Float')
        self.add_param(strChain+'blockf',val=0.9, units='lb', desc='Block fuel, or fraction of aircraft fuel capacity  (Default = 0.90 * (FULWMX+FULFMX), Namelist &WTIN)',typerVar='Float')
        self.add_param(strChain+'blockt',val=0.0, units='h', desc='Block time (Default = DESRNG/VELOC + 0.65)',typerVar='Float')


    def FlopsWrapper_input_costin_Cost_Technology(self):
        """Container for input:costin:Cost_Technology"""
        strChain = 'input:costin:Cost_Technology:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'fafrd',val=1.0, desc='Technology factor on Airframe R&D',typerVar='Float')
        self.add_param(strChain+'fenrd',val=1.0, desc='Technology factor on Engine R&D',typerVar='Float')
        self.add_param(strChain+'fmac',val=1.0, desc='Technology factor on Air conditioning',typerVar='Float')
        self.add_param(strChain+'fmai',val=1.0, desc='Technology factor on Anti-icing',typerVar='Float')
        self.add_param(strChain+'fmapu',val=1.0, desc='Technology factor on Auxiliary power unit',typerVar='Float')
        self.add_param(strChain+'fmav',val=1.0, desc='Technology factor on Avionics',typerVar='Float')
        self.add_param(strChain+'fmbody',val=1.0, desc='Technology factor on Fuselage',typerVar='Float')
        self.add_param(strChain+'fmcomp',val=1.0, desc='Technology factor on Composite materials (applied to the wing, tails, fuselage, and nacelles)',typerVar='Float')
        self.add_param(strChain+'fmel',val=1.0, desc='Technology factor on Electrical systems',typerVar='Float')
        self.add_param(strChain+'fmeng',val=1.0, desc='Technology factor on Engine',typerVar='Float')
        self.add_param(strChain+'fmensy',val=1.0, desc='Technology factor on Engine systems',typerVar='Float')
        self.add_param(strChain+'fmfcs',val=1.0, desc='Technology factor on Surface controls',typerVar='Float')
        self.add_param(strChain+'fmfeq',val=1.0, desc='Technology factor on Furnishings and equipment',typerVar='Float')
        self.add_param(strChain+'fmfusy',val=1.0, desc='Technology factor on Fuel systems',typerVar='Float')
        self.add_param(strChain+'fmgear',val=1.0, desc='Technology factor on Landing gear',typerVar='Float')
        self.add_param(strChain+'fmhyd',val=1.0, desc='Technology factor on Hydraulic systems',typerVar='Float')
        self.add_param(strChain+'fmins',val=1.0, desc='Technology factor on Instruments',typerVar='Float')
        self.add_param(strChain+'fmnac',val=1.0, desc='Technology factor on Nacelles',typerVar='Float')
        self.add_param(strChain+'fmpnm',val=1.0, desc='Technology factor on Pneumatics',typerVar='Float')
        self.add_param(strChain+'fmtail',val=1.0, desc='Technology factor on Tail',typerVar='Float')
        self.add_param(strChain+'fmtrv',val=1.0, desc='Technology factor on Thrust reversers',typerVar='Float')
        self.add_param(strChain+'fmwing',val=1.0, desc='Technology factor on Wing',typerVar='Float')
        self.add_param(strChain+'foac',val=1.0, desc='Technology factor on Air conditioning',typerVar='Float')
        self.add_param(strChain+'foai',val=1.0, desc='Technology factor on Anti-icing',typerVar='Float')
        self.add_param(strChain+'foapu',val=1.0, desc='Technology factor on Auxiliary power unit',typerVar='Float')
        self.add_param(strChain+'foav',val=1.0, desc='Technology factor on Avionics',typerVar='Float')
        self.add_param(strChain+'fobody',val=1.0, desc='Technology factor on Fuselage',typerVar='Float')
        self.add_param(strChain+'focomp',val=1.0, desc='Technology factor on Composite materials',typerVar='Float')
        self.add_param(strChain+'foel',val=1.0, desc='Technology factor on Electrical systems',typerVar='Float')
        self.add_param(strChain+'fofcs',val=1.0, desc='Technology factor on Flight control system',typerVar='Float')
        self.add_param(strChain+'fofeq',val=1.0, desc='Technology factor on Furnishings and equipment',typerVar='Float')
        self.add_param(strChain+'fofusy',val=1.0, desc='Technology factor on Fuel systems',typerVar='Float')
        self.add_param(strChain+'fogear',val=1.0, desc='Technology factor on Landing gear',typerVar='Float')
        self.add_param(strChain+'fohyd',val=1.0, desc='Technology factor on Hydraulic systems',typerVar='Float')
        self.add_param(strChain+'foins',val=1.0, desc='Technology factor on Instruments',typerVar='Float')
        self.add_param(strChain+'fonac',val=1.0, desc='Technology factor on Nacelles',typerVar='Float')
        self.add_param(strChain+'fopnm',val=1.0, desc='Technology factor on Pneumatics',typerVar='Float')
        self.add_param(strChain+'foprop',val=1.0, desc='Technology factor on Propulsion system',typerVar='Float')
        self.add_param(strChain+'fowing',val=1.0, desc='Technology factor on Wing',typerVar='Float')
        self.add_param(strChain+'feacsr',val=1.0, desc='Technology factor on Aircraft servicing',typerVar='Float')
        self.add_param(strChain+'fecfee',val=1.0, desc='Technology factor on Aircraft control fee',typerVar='Float')
        self.add_param(strChain+'fecrw',val=1.0, desc='Technology factor on Flight crew',typerVar='Float')
        self.add_param(strChain+'fedep',val=1.0, desc='Technology factor on Depreciation',typerVar='Float')
        self.add_param(strChain+'feflta',val=1.0, desc='Technology factor on Flight attendants',typerVar='Float')
        self.add_param(strChain+'feins',val=1.0, desc='Technology factor on Insurance',typerVar='Float')
        self.add_param(strChain+'felabr',val=1.0, desc='Technology factor on R&D labor rate',typerVar='Float')
        self.add_param(strChain+'feldfe',val=1.0, desc='Technology factor on Landing fee',typerVar='Float')
        self.add_param(strChain+'femain',val=1.0, desc='Technology factor on Maintenance hours',typerVar='Float')


    def FlopsWrapper_input_costin_Basic(self):
        """Container for input:costin:Basic"""
        strChain = 'input:costin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ac',val=350.0, units='lb/min', desc='Airconditioning total pack air flow',typerVar='Float')
        self.add_param(strChain+'apuflw',val=400.0, units='lb/min', desc='Auxiliary power unit flow rate',typerVar='Float')
        self.add_param(strChain+'apushp',val=170.0, units='hp', desc='Auxiliary power unit shaft horsepower',typerVar='Float')
        self.add_param(strChain+'depper',val=14.0, units='year', desc='Depreciation period',typerVar='Float')
        self.add_param(strChain+'devst',val=1980.0, units='year', desc='Development start time',typerVar='Float')
        self.add_param(strChain+'dlbur',val=2.0, desc='Direct labor burden factor',typerVar='Float')
        self.add_param(strChain+'dyear',val=1986, desc='Desired year for dollar calculations',typerVar='Int')
        self.add_param(strChain+'epr',val=20.0, desc='Engine pressure ratio at sea level static',typerVar='Float')
        self.add_param(strChain+'fafmsp',val=0.1, desc='Spares factor for production airframes',typerVar='Float')
        self.add_param(strChain+'fare',val=0.0, units='USD/pax/mi', desc='Fare (Triggers calculation of return on investment)',typerVar='Float')
        self.add_param(strChain+'fengsp',val=0.3, desc='Spares factor for production engines',typerVar='Float')
        self.add_param(strChain+'fppft',val=0.5, desc='Spares factor for prototype and flight test engines',typerVar='Float')
        self.add_param(strChain+'fuelpr',val=0.5, units='USD/galUS', desc='Fuel price',typerVar='Float')
        self.add_param(strChain+'hydgpm',val=150.0, desc='Gallon per minute flow of hydraulic pumps',typerVar='Float')
        self.add_param(strChain+'iacous',val=0,optionsVal=(0,1), desc='Acoustic treatment in nacelle', aliases=('No', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'ibody',val=0,optionsVal=(0,1), desc='Body type indicator', aliases=('Narrow', 'Wide'),typerVar='Enum')
        self.add_param(strChain+'icirc',val=1,optionsVal=(1,2), desc='Circuit indicator - fire detection', aliases=('Single', 'Dual'),typerVar='Enum')
        self.add_param(strChain+'icorev',val=1,optionsVal=(0,1), desc='Thrust reverser', aliases=('No core reverser', 'Core reverser'),typerVar='Enum')
        self.add_param(strChain+'icostp',val=1,optionsVal=(1,2,3,4,5), desc='Type of cost calculation desired', aliases=('Life cycle cost (LCC)', 'Acquisition cost', 'Direct operating cost (DOC)', 'Indirect operating cost (IOC)', 'Operating cost only (DOC + IOC - Depreciation)'),typerVar='Enum')
        self.add_param(strChain+'idom',val=1,optionsVal=(1,2), desc='Operation type indicator', aliases=('Domestic', 'International'),typerVar='Enum')
        self.add_param(strChain+'imux',val=0,optionsVal=(0,1), desc='Multiplex indicator', aliases=('No multiplex', 'Multiplex'),typerVar='Enum')
        self.add_param(strChain+'inozz',val=1,optionsVal=(1,2,3,4,5), desc='Nozzle type indicator', aliases=('Translating sleeve', 'Simple target w/ separate flow nozzle', 'Simple target w/ mixed flow nozzle', 'Separate flow exhaust w/o thrust reverser', 'Short duct w/o thrust reverser'),typerVar='Enum')
        self.add_param(strChain+'ipflag',val=1,optionsVal=(0,1), desc='Print controller for Cost Module', aliases=('Print major elements', 'Print details'),typerVar='Enum')
        self.add_param(strChain+'irad',val=1,optionsVal=(0,1), desc='Indicator to include research and development', aliases=('Ignore R&D costs', 'Include R&D costs'),typerVar='Enum')
        self.add_param(strChain+'irange',val=1,optionsVal=(0,1,2), desc='Range indicator', aliases=('Short', 'Medium', 'Long'),typerVar='Enum')
        self.add_param(strChain+'ispool',val=0,optionsVal=(0,1), desc='Auxiliary power unit complexity indicator', aliases=('Single spool fixed vane', 'Double spool variable vane APU'),typerVar='Enum')
        self.add_param(strChain+'itran',val=0,optionsVal=(0,1), desc='Cargo/baggage transfer operation indicator', aliases=('No transfer', 'Transfer'),typerVar='Enum')
        self.add_param(strChain+'iwind',val=0,optionsVal=(0,1), desc='Windshield type indicator', aliases=('Flat', 'Curved'),typerVar='Enum')
        self.add_param(strChain+'kva',val=200.0, desc='KVA rating of full-time generators',typerVar='Float')
        self.add_param(strChain+'lf',val=55.0, desc='Passenger load factor',typerVar='Float')
        self.add_param(strChain+'life',val=14.0, desc='Number of years for Life Cycle Cost calculation',typerVar='Float')
        self.add_param(strChain+'napu',val=1, desc='Number of auxiliary power units',typerVar='Int')
        self.add_param(strChain+'nchan',val=1,optionsVal=(1,2,3), desc='Number of autopilot channels',typerVar='Enum')
        self.add_param(strChain+'nfltst',val=2, desc='Number of flight test aircraft',typerVar='Int')
        self.add_param(strChain+'ngen',val=3,optionsVal=(3,4), desc='Number of inflight operated generators',typerVar='Enum')
        self.add_param(strChain+'nins',val=0, desc='Number of inertial navigation systems',typerVar='Int')
        self.add_param(strChain+'npod',val=4, desc='Number of podded engines',typerVar='Int')
        self.add_param(strChain+'nprotp',val=2, desc='Number of prototype aircraft',typerVar='Int')
        self.add_param(strChain+'pctfc',val=10.0, desc='Percent of seats for first class',typerVar='Float')
        self.add_param(strChain+'plmqt',val=1984.0, units='year', desc='Planned MQT (150-hour Model Qualification Test or FAA certification)',typerVar='Float')
        self.add_param(strChain+'prorat',val=15.0, desc='Manufacturers',typerVar='Float')
        self.add_param(strChain+'prproc',val=0.0, desc='Prior number of engines procured',typerVar='Float')
        self.add_param(strChain+'q',val=100.0, desc='Airframe production quantities',typerVar='Float')
        self.add_param(strChain+'resid',val=2.0, desc='Residual value at end of lifetime',typerVar='Float')
        self.add_param(strChain+'roi',val=10.0, desc='Return on investment (Triggers calculation of required fare)',typerVar='Float')
        self.add_param(strChain+'sfc',val=0.6, units='lb/h/lb', desc='Engine specific fuel consumption',typerVar='Float')
        self.add_param(strChain+'taxrat',val=0.33, desc='Corporate tax rate for ROI calculations',typerVar='Float')
        self.add_param(strChain+'temp',val=1800.0, units='degF', desc='Maximum turbine inlet temperature',typerVar='Float')




    def FlopsWrapper_input_confin_Objective(self):
        """Container for input:confin:Objective"""
        strChain = 'input:confin:Objective:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'ofg',val=0.0, desc='Objective function weighting factor for gross weight \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'off',val=1.0, desc='Objective function weighting factor for mission fuel \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofm',val=0.0, desc='Objective function weighting factor for Mach*(L/D), should be negative to maximize \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofr',val=0.0, desc='Objective function weighting factor for Range, should be negative to maximize. \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofc',val=0.0, desc='Objective function weighting factor for Cost \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'osfc',val=0.0, desc='Objective function weighting factor for Specific Fuel Consumption at the engine design point.  Generally used only for engine design cases (IANAL = 4). \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofnox',val=0.0, desc='Objective function weighting factor for NOx emissions \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofnf',val=0.0, desc='Objective function weighting factor for flyover noise (used primarily for contour plots) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofns',val=0.0, desc='Objective function weighting factor for sideline noise (used primarily for contour plots) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofnfom',val=0.0, desc='Objective function weighting factor for noise figure of merit \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'oarea',val=0.0, desc='Objective function weighting factor for area of noise footprint (not implemented) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')
        self.add_param(strChain+'ofh',val=0.0, desc='Objective function weighting factor for hold time for segment NHOLD (See Namelist &MISSIN) \nThe function that is minimized is\n \n OBJ = OFG*GW \n + OFF*Fuel \n + OFM*VCMN*(Lift/Drag) \n + OFR*Range + OFC*Cost \n + OSFC*SFC \n + OFNOX*NOx \n + OFNF*(Flyover Noise) \n + OFNS*(Sideline Noise) \n + OFNFOM*(Noise Figure of Merit) \n + OFH*(Hold Time for Segment NHOLD)',typerVar='Float')


    def FlopsWrapper_input_confin_Design_Variables(self):
        """Container for input:confin:Design_Variables"""
        strChain = 'input:confin:Design_Variables:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'gw',val=numpy_float64, units='lb', desc='GW(0)=Ramp weight (Required.  If IRW = 1, a good initial guess must be input.)\nGW(1)=Activity status, active if > 0\nGW(2)=Lower bound\nGW(3)=Upper bound\nGW(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'ar',val=numpy_float64, desc='AR(0)=Wing aspect ratio\nAR(1)=Activity status, active if > 0\nAR(2)=Lower bound\nAR(3)=Upper bound\nAR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'thrust',val=numpy_float64, units='lb', desc='THRUST(0)=Maximum rated thrust per engine, or thrust-weight ratio if TWR = -1.\nTHRUST(1)=Activity status, active if > 0\nTHRUST(2)=Lower bound\nTHRUST(3)=Upper bound\nTHRUST(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'sw',val=numpy_float64, units='ft*ft', desc='SW(0)=Reference wing area, or wing loading if WSR = -1.\nSW(1)=Activity status, active if > 0\nSW(2)=Lower bound\nSW(3)=Upper bound\nSW(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'tr',val=numpy_float64, desc='TR(0)=Taper ratio of the wing (Required)\nTR(1)=Activity status, active if > 0\nTR(2)=Lower bound\nTR(3)=Upper bound\nTR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'sweep',val=numpy_float64, units='deg', desc='SWEEP(0)=Quarter-chord sweep angle of the wing (Required)\nSWEEP(1)=Activity status, active if > 0\nSWEEP(2)=Lower bound\nSWEEP(3)=Upper bound\nSWEEP(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'tca',val=numpy_float64, desc='TCA(0)=Wing thickness-chord ratio (weighted average) (Required)\nTCA(1)=Activity status, active if > 0\nTCA(2)=Lower bound\nTCA(3)=Upper bound\nTCA(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'vcmn',val=numpy_float64, desc='VCMN(0)=Cruise Mach number (Required)\nVCMN(1)=Activity status, active if > 0\nVCMN(2)=Lower bound\nVCMN(3)=Upper bound\nVCMN(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'ch',val=numpy_float64, units='ft', desc='CH(0)=Maximum cruise altitude (Required)\nCH(1)=Activity status, active if > 0\nCH(2)=Lower bound\nCH(3)=Upper bound\nCH(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'varth',val=numpy_float64, desc='VARTH(0)=Thrust derating factor for takeoff noise Fraction of full thrust used in takeoff\nVARTH(1)=Activity status, active if > 0\nVARTH(2)=Lower bound\nVARTH(3)=Upper bound\nVARTH(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'rotvel',val=numpy_float64, desc='ROTVEL(0)=Rotation velocity for takeoff noise abatement (default is minimum required to meet takeoff performance constraints)\nROTVEL(1)=Activity status, active if > 0\nROTVEL(2)=Lower bound\nROTVEL(3)=Upper bound\nROTVEL(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'plr',val=numpy_float64, desc='PLR(0)=Thrust fraction after programmed lapse rate (default thrust is specified in each segment)\nPLR(1)=Activity status, active if > 0\nPLR(2)=Lower bound\nPLR(3)=Upper bound\nPLR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'etit',val=numpy_float64, units='degR', desc='ETIT(0)=Engine design point turbine entry temperature\nETIT(1)=Activity status, active if > 0\nETIT(2)=Lower bound\nETIT(3)=Upper bound\nETIT(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'eopr',val=numpy_float64, desc='EOPR(0)=Overall pressure ratio\nEOPR(1)=Activity status, active if > 0\nEOPR(2)=Lower bound\nEOPR(3)=Upper bound\nEOPR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'efpr',val=numpy_float64, desc='EFPR(0)=Fan pressure ratio (turbofans only)\nEFPR(1)=Activity status, active if > 0\nEFPR(2)=Lower bound\nEFPR(3)=Upper bound\nEFPR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'ebpr',val=numpy_float64, desc='EBPR(0)=Bypass ratio (turbofans only)\nEBPR(1)=Activity status, active if > 0\nEBPR(2)=Lower bound\nEBPR(3)=Upper bound\nEBPR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'ettr',val=numpy_float64, desc='ETTR(0)=Engine throttle ratio defined as the ratio of the maximum allowable turbine inlet temperature divided by the design point turbine inlet temperature.\nIf ETTR is greater than ETIT, it is assumed to be the maximum allowable turbine inlet temperature.\nETTR(1)=Activity status, active if > 0\nETTR(2)=Lower bound\nETTR(3)=Upper bound\nETTR(4)=Optimization scale factor',typerVar='Array')
        self.add_param(strChain+'ebla',val=numpy_float64, units='deg', desc='EBLA(0)=Blade angle for fixed pitch propeller\nEBLA(1)=Activity status, active if > 0\nEBLA(2)=Lower bound\nEBLA(3)=Upper bound\nEBLA(4)=Optimization scale factor',typerVar='Array')


    def FlopsWrapper_input_confin_Basic(self):
        """Container for input:confin:Basic"""
        strChain = 'input:confin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'desrng',val=0.0, desc='Design range (or endurance).  See INDR in Namelist &MISSIN)\nRequired - if IRW = 2 in Namelist &MISSIN, the range is computed, but a reasonable guess must still be input',typerVar='Float')
        self.add_param(strChain+'wsr',val=0.0, desc='Required wing loading if > 0.\nDo not set WSR > 0 during optimization or if wing area is being varied.\nInterpret SW as wing loading for parametric variation if = -1.\nDo not use for optimization.',typerVar='Float')
        self.add_param(strChain+'twr',val=0.0, desc='Required total thrust-weight ratio if > 0.\nDo not set TWR > 0 during optimization or if thrust is being varied.\nInterpret THRUST as thrust-weight ratio for parametric variation if = -1.\nDo not use for optimization.',typerVar='Float')
        self.add_param(strChain+'htvc',val=0.0, desc='Modified horizontal tail volume coefficient.\nIf HTVC > 0., SHT = HTVC * SW * Sqrt(SW/AR) / XL (This overrides any input value for SHT)\nIf HTVC = 1., the horizontal tail volume coefficient calculated from the input values of SHT, SW, AR and XL will be maintained.',typerVar='Float')
        self.add_param(strChain+'vtvc',val=0.0, desc='Modified vertical tail volume coefficient.\nIf VTVC > 0., SVT = VTVC * SW * Sqrt(SW*AR) / XL (This overrides any input value for SVT)\nIf VTVC = 1., the vertical tail volume coefficient calculated from the input values of SVT, SW, AR and XL will be maintained.',typerVar='Float')
        self.add_param(strChain+'pglov',val=0.0, desc='Fixed ratio of glove area to wing area (GLOV/SW).\nIf PGLOV > 0., GLOV will change if SW changes.',typerVar='Float')
        self.add_param(strChain+'fixspn',val=0.0, units='ft', desc='Special Option - Fixed wing span.  If the wing area is being varied or optimized, the wing aspect ratio will be adjusted to maintain a constant span.',typerVar='Float')
        self.add_param(strChain+'fixful',val=0.0, units='lb', desc='Special Option - Fixed mission fuel.  Allows specification of mission fuel.\nSince this fuel is normally a fall out (what is left over after OWE and payload are subtracted from the gross weight), this option requires iterating on the gross weight until the mission fuel = FIXFUL.  Gross weight cannot be an active design variable or used in a parametric variation, and IRW must be 2 in Namelist &MISSIN.',typerVar='Float')



    def FlopsWrapper_input_asclin(self):
        """Container for input:asclin"""
        strChain = 'input:asclin:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'sref',val=0.0, units='ft*ft', desc='Wing area on which aerodynamic input is based (Default = SW, Namelist &CONFIN). If different from SW, aerodynamics will be scaled.',typerVar='Float')
        self.add_param(strChain+'tref',val=0.0, units='lb', desc='Engine thrust corresponding to nacelle size used in generating aerodynamic input data (Default = THRUST, Namelist &CONFIN). If different from THRUST, aerodynamic data will be modified.',typerVar='Float')
        self.add_param(strChain+'awetn',val=0.0, desc='Nacelle wetted area/SREF',typerVar='Float')
        self.add_param(strChain+'eltot',val=0.0, units='ft', desc='Total configuration length (Default = fuselage length)',typerVar='Float')
        self.add_param(strChain+'voltot',val=0.0, units='ft*ft*ft', desc='Total configuration volume',typerVar='Float')
        self.add_param(strChain+'awett',val=numpy_float64, desc='Total wetted area/SREF.  For variable geometry aircraft, up to NMP values may be input',typerVar='Array')
        self.add_param(strChain+'awetw',val=numpy_float64, desc='Wing wetted area/SREF',typerVar='Array')
        self.add_param(strChain+'elw',val=numpy_float64, units='ft', desc='Total length of exposed wing',typerVar='Array')
        self.add_param(strChain+'volw',val=numpy_float64, units='ft*ft*ft', desc='Total volume of exposed wing',typerVar='Array')
        self.add_param(strChain+'form',val=numpy_float64, desc='Subsonic form factor for total configuration',typerVar='Array')
        self.add_param(strChain+'eql',val=numpy_float64, units='ft', desc='Equivalent friction length for total baseline configuration.  If EQL is omitted, skin friction drag is computed from component data',typerVar='Array')
        self.add_param(strChain+'cdwav',val=numpy_float64, desc='Wave drag coefficients (NMP values)',typerVar='Array')
        self.add_param(strChain+'dcdnac',val=numpy_float64, desc='Delta wave drag coefficients, nacelles on - nacelles off',typerVar='Array')


    def FlopsWrapper_input_aero_data(self):
        """Container for input:aero_data"""
        strChain = 'input:aero_data:'

        # OpenMDAO Public Variables
        self.add_param(strChain+'aerodat',val='',typeVar='Str')


    def FlopsWrapper_input_aerin_Takeoff_Landing(self):
        """Container for input:aerin:Takeoff_Landing"""
        strChain = 'input:aerin:Takeoff_Landing:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'wratio',val=0.0, desc='Ratio of maximum landing weight to maximum takeoff weight (Default = WLDG/GW if WLDG is input, otherwise for supersonic aircraft Default = 1. - .00009*DESRNG, for subsonic aircraft Default = 1. - .00004*DESRNG)',typerVar='Float')
        self.add_param(strChain+'vappr',val=150.0, units='nmi', desc='Maximum allowable landing approach velocity',typerVar='Float')
        self.add_param(strChain+'flto',val=12000.0, units='ft', desc='Maximum allowable takeoff field length',typerVar='Float')
        self.add_param(strChain+'flldg',val=0.0, units='ft', desc='Maximum allowable landing field length',typerVar='Float')
        self.add_param(strChain+'cltom',val=2.0, desc='Maximum CL in takeoff configuration',typerVar='Float')
        self.add_param(strChain+'clldm',val=3.0, desc='Maximum CL in landing configuration',typerVar='Float')
        self.add_param(strChain+'clapp',val=0.0, desc='Approach CL',typerVar='Float')
        self.add_param(strChain+'dratio',val=1.0, desc='Takeoff and landing air density ratio',typerVar='Float')
        self.add_param(strChain+'elodss',val=0.0, desc='Lift-Drag ratio for second segment climb (Default is internally computed)',typerVar='Float')
        self.add_param(strChain+'elodma',val=0.0, desc='Lift-Drag ratio for missed approach climb (Default is internally computed)',typerVar='Float')
        self.add_param(strChain+'thrss',val=0.0, units='lb', desc='Thrust per baseline engine for second segment climb (Default = THRUST, Namelist &CONFIN)',typerVar='Float')
        self.add_param(strChain+'thrma',val=0.0, units='lb', desc='Thrust per baseline engine for missed approach climb (Default = THRSS)',typerVar='Float')
        self.add_param(strChain+'throff',val=0.0, units='lb', desc='Thrust per baseline engine for takeoff (Default = THRSS)',typerVar='Float')


    def FlopsWrapper_input_aerin_Internal_Aero(self):
        """Container for input:aerin:Internal_Aero"""
        strChain = 'input:aerin:Internal_Aero:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'cam',val=0.0, desc='Maximum camber at 70% semispan, percent of local chord',typerVar='Float')
        self.add_param(strChain+'sbase',val=0.0, units='ft*ft', desc='Aircraft base area (total exit cross-section area minus inlet capture areas for internally mounted engines)',typerVar='Float')
        self.add_param(strChain+'aitek',val=1.0, desc='Airfoil technology parameter.  Use 1 for conventional wing and 2 for advanced technology wing',typerVar='Float')
        self.add_param(strChain+'modaro',val=0,optionsVal=(0,1), desc='Data tables in EDET are to be modified, Namelist &ARIDE will be read in', aliases=('No', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'fcldes',val=-1.0, desc='Fixed design lift coefficient.  If input, overrides design CL computed by EDET.',typerVar='Float')
        self.add_param(strChain+'fmdes',val=-1.0, desc='Fixed design Mach number.  If input, overrides design Mach number computed by EDET.',typerVar='Float')
        self.add_param(strChain+'xllam',val=0,optionsVal=(0,1), desc='Use 0 for Turbulent flow and 1 for Laminar Flow', aliases=('Turbulent', 'Laminar'),typerVar='Enum')
        self.add_param(strChain+'truw',val=0.0, desc='Percent LF wing upper surface',typerVar='Float')
        self.add_param(strChain+'trlw',val=0.0, desc='Percent LF wing low surface',typerVar='Float')
        self.add_param(strChain+'truh',val=0.0, desc='Percent LF horizontal tail upper surface',typerVar='Float')
        self.add_param(strChain+'trlh',val=0.0, desc='Percent LF horizontal tail lower surface',typerVar='Float')
        self.add_param(strChain+'truv',val=0.0, desc='Percent LF vertical tail upper surface',typerVar='Float')
        self.add_param(strChain+'trlv',val=0.0, desc='Percent LF vertical tail lower surface',typerVar='Float')
        self.add_param(strChain+'trub',val=0.0, desc='Percent LF fuselage upper surface',typerVar='Float')
        self.add_param(strChain+'trlb',val=0.0, desc='Percent LF fuselage lower surface',typerVar='Float')
        self.add_param(strChain+'trun',val=0.0, desc='Percent LF nacelle upper surface',typerVar='Float')
        self.add_param(strChain+'trln',val=0.0, desc='Percent LF nacelle lower surface',typerVar='Float')
        self.add_param(strChain+'truc',val=0.0, desc='Percent LF canard upper surface',typerVar='Float')
        self.add_param(strChain+'trlc',val=0.0, desc='Percent LF canard lower surface',typerVar='Float')
        self.add_param(strChain+'e',val=1.0, desc='Aerodynamic efficiency factor: use 1 for normal wing efficiency; normal wing efficiency modified for taper ratio and aspect ratio plus E if < 0; Otherwise, normal wing efficiency multiplied by E',typerVar='Float')
        self.add_param(strChain+'swetw',val=1.0, units='ft*ft', desc='Wing wetted area',typerVar='Float')
        self.add_param(strChain+'sweth',val=1.0, units='ft*ft', desc='Horizontal tail wetted area',typerVar='Float')
        self.add_param(strChain+'swetv',val=1.0, units='ft*ft', desc='Vertical tail wetted area',typerVar='Float')
        self.add_param(strChain+'swetf',val=1.0, units='ft*ft', desc='Fuselage wetted area',typerVar='Float')
        self.add_param(strChain+'swetn',val=1.0, units='ft*ft', desc='Nacelle wetted area',typerVar='Float')
        self.add_param(strChain+'swetc',val=1.0, units='ft*ft', desc='Canard wetted area',typerVar='Float')


    def FlopsWrapper_input_aerin_Basic(self):
        """Container for input:aerin:Basic"""
        strChain = 'input:aerin:Basic:'

    # OpenMDAO Public Variables
        self.add_param(strChain+'myaero',val=0,optionsVal=(0,1,2,3,4), desc='Controls type of user-supplied aerodynamic data\n= 0, Drag polars are computed internally\n= 1, Aerodynamic Data will be read in\n= 2, Scalable Aerodynamic Data will be input (Namelist &ASCLIN required)\n= 3, Special parabolic Aerodynamic Data format (Namelist &RFHIN required)\n= 4, Use aerodynamic response surface - available only in DOSS version', aliases=('Internal', 'Fixed input', 'Scalable input', 'Parabolic', 'Response surface'),typerVar='Enum')
        self.add_param(strChain+'iwave',val=0,optionsVal=(0,1), desc='Controls Wave Drag Data input type\n= 1, Input Wave Drag Data will be formatted\n= 0, Otherwise', aliases=('No', 'Yes'),typerVar='Enum')
        self.add_param(strChain+'fwave',val=1.0, desc='Wave drag factor - multiplies input values of wave drag from formatted aerodynamic data or Namelist &ASCLIN',typerVar='Float')
        self.add_param(strChain+'itpaer',val=2,optionsVal=(1,2,3), desc='Aerodynamic data interpolation switch\n= 1, Linear - Use if aerodynamic data is irregular.  This is usually indicated by strange climb, descent or cruise profiles.\n= 2, Parabolic\n= 3, Parabolic interpolation for CL, linear interpolation for Mach number and altitude.', aliases=('Linear', 'Parabolic', 'Combination'),typerVar='Enum')
        self.add_param(strChain+'ibo',val=0,optionsVal=(0,1), desc='Format indicator for input aerodynamic matrices\n= 1, A new line is started for each Mach number for Cards 4 and for each altitude for Cards 8\n= 0, Data is continuous, 10 to a line', aliases=('Continuous', '1 Mach/line'),typerVar='Enum')




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
       
        '''comp.add('desrng', Float(-1., units="nmi/s" ))
        comp.add('mywts', Int(-1 ))
        comp.add('rampwt', Float(-1., units="lb" ))
        comp.add('dowe', Float(-1., units="lb" ))
        comp.add('paylod', Float(-1., units="lb" ))
        comp.add('fuemax', Float(-1., units="lb" ))
        comp.add('itakof', Int(-1 ))
        comp.add('iland', Int(-1 ))
        comp.add('nopro', Int(-1 ))
        comp.add('noise', Int(-1 ))
        comp.add('icost', Int(-1 ))
        comp.add('wsr', Float(-1. ))
        comp.add('twr', Float(-1. ))

        comp.add('missin', VarTree(VariableTree()))
        comp.missin.add('Basic', VarTree(VariableTree()))
        comp.missin.Basic.add('indr', Int(-999 ))
        comp.missin.Basic.add('fact', Float(-999. ))
        comp.missin.Basic.add('fleak', Float(-999. ))
        comp.missin.Basic.add('fcdo', Float(-999. ))
        comp.missin.Basic.add('fcdi', Float(-999. ))
        comp.missin.Basic.add('fcdsub', Float(-999. ))
        comp.missin.Basic.add('fcdsup', Float(-999. ))
        comp.missin.Basic.add('iskal', Int(-999 ))
        comp.missin.Basic.add('owfact', Float(-999. ))
        comp.missin.Basic.add('iflag', Int(-999 ))
        comp.missin.Basic.add('msumpt', Int(-999 ))
        comp.missin.Basic.add('dtc', Float(-999. ))
        comp.missin.Basic.add('irw', Int(-999 ))
        comp.missin.Basic.add('rtol', Float(-999. ))
        comp.missin.Basic.add('nhold', Int(-999 ))
        comp.missin.Basic.add('iata', Int(-999 ))
        comp.missin.Basic.add('tlwind', Float(-999. ))
        comp.missin.Basic.add('dwt', Float(-999. ))
        comp.missin.Basic.add('offdr', Array(dtype=numpy_float64 ))
        comp.missin.Basic.add('idoq', Int(-999 ))
        comp.missin.Basic.add('nsout', Int(-999 ))
        comp.missin.Basic.add('nsadj', Int(-999 ))
        comp.missin.Basic.add('mirror', Int(-999 ))

        comp.missin.add('Store_Drag', VarTree(VariableTree()))
        comp.missin.Store_Drag.add('stma', Array(dtype=numpy_float64 ))
        comp.missin.Store_Drag.add('cdst', Array(dtype=numpy_float64 ))
        comp.missin.Store_Drag.add('istcl', Array(dtype=numpy_float64 ))
        comp.missin.Store_Drag.add('istcr', Array(dtype=numpy_float64 ))
        comp.missin.Store_Drag.add('istde', Int(-999 ))

        comp.missin.add('User_Weights', VarTree(VariableTree()))
        comp.missin.User_Weights.add('mywts', Int(-999 ))
        comp.missin.User_Weights.add('rampwt', Float(-999. ))
        comp.missin.User_Weights.add('dowe', Float(-999. ))
        comp.missin.User_Weights.add('paylod', Float(-999. ))
        comp.missin.User_Weights.add('fuemax', Float(-999. ))

        comp.missin.add('Ground_Operations', VarTree(VariableTree()))
        comp.missin.Ground_Operations.add('takotm', Float(-999. ))
        comp.missin.Ground_Operations.add('taxotm', Float(-999. ))
        comp.missin.Ground_Operations.add('apprtm', Float(-999. ))
        comp.missin.Ground_Operations.add('appfff', Float(-999. ))
        comp.missin.Ground_Operations.add('taxitm', Float(-999. ))
        comp.missin.Ground_Operations.add('ittff', Int(-999 ))
        comp.missin.Ground_Operations.add('takoff', Float(-999. ))
        comp.missin.Ground_Operations.add('txfufl', Float(-999. ))
        comp.missin.Ground_Operations.add('ftkofl', Float(-999. ))
        comp.missin.Ground_Operations.add('ftxofl', Float(-999. ))
        comp.missin.Ground_Operations.add('ftxifl', Float(-999. ))
        comp.missin.Ground_Operations.add('faprfl', Float(-999. ))

        comp.missin.add('Turn_Segments', VarTree(VariableTree()))
        comp.missin.Turn_Segments.add('xnz', Array(dtype=numpy_float64 ))
        comp.missin.Turn_Segments.add('xcl', Array(dtype=numpy_float64 ))
        comp.missin.Turn_Segments.add('xmach', Array(dtype=numpy_float64 ))

        comp.missin.add('Climb', VarTree(VariableTree()))
        comp.missin.Climb.add('nclimb', Int(-999))
        comp.missin.Climb.add('clmmin', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('clmmax', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('clamin', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('clamax', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('nincl', Array(dtype=numpy_int64 ))
        comp.missin.Climb.add('fwf', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('ncrcl', Array(dtype=numpy_int64 ))
        comp.missin.Climb.add('cldcd', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('ippcl', Array(dtype=numpy_int64 ))
        comp.missin.Climb.add('maxcl', Array(dtype=numpy_int64 ))
        comp.missin.Climb.add('no', Array(dtype=numpy_int64 ))
        comp.missin.Climb.add('keasvc', Int(-999 ))
        comp.missin.Climb.add('actab', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('vctab', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('ifaacl', Int(-999 ))
        comp.missin.Climb.add('ifaade', Int(-999 ))
        comp.missin.Climb.add('nodive', Int(-999 ))
        comp.missin.Climb.add('divlim', Float(-999. ))
        comp.missin.Climb.add('qlim', Float(-999. ))
        comp.missin.Climb.add('spdlim', Float(-999. ))
        comp.missin.Climb.add('nql', Int(-999 ))
        comp.missin.Climb.add('qlalt', Array(dtype=numpy_float64 ))
        comp.missin.Climb.add('vqlm', Array(dtype=numpy_float64 ))

        comp.missin.add('Cruise', VarTree(VariableTree()))
        comp.missin.Cruise.add('ncruse', Int(-999 ))
        comp.missin.Cruise.add('ioc', Array(dtype=numpy_int64 ))
        comp.missin.Cruise.add('crmach', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('cralt', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('crdcd', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('flrcr', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('crmmin', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('crclmx', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('hpmin', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('ffuel', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('fnox', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('ifeath', Array(dtype=numpy_int64 ))
        comp.missin.Cruise.add('feathf', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('cdfeth', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('dcwt', Float(-999. ))
        comp.missin.Cruise.add('rcin', Float(-999. ))
        comp.missin.Cruise.add('wtbm', Array(dtype=numpy_float64 ))
        comp.missin.Cruise.add('altbm', Array(dtype=numpy_float64 ))

        comp.missin.add('Descent', VarTree(VariableTree()))
        comp.missin.Descent.add('ivs', Int(-999 ))
        comp.missin.Descent.add('decl', Float(-999. ))
        comp.missin.Descent.add('demmin', Float(-999. ))
        comp.missin.Descent.add('demmax', Float(-999. ))
        comp.missin.Descent.add('deamin', Float(-999. ))
        comp.missin.Descent.add('deamax', Float(-999. ))
        comp.missin.Descent.add('ninde', Int(-999 ))
        comp.missin.Descent.add('dedcd', Float(-999. ))
        comp.missin.Descent.add('rdlim', Float(-999. ))
        comp.missin.Descent.add('ns', Int(-999 ))
        comp.missin.Descent.add('keasvd', Int(-999 ))
        comp.missin.Descent.add('adtab', Array(dtype=numpy_float64 ))
        comp.missin.Descent.add('vdtab', Array(dtype=numpy_float64 ))

        comp.missin.add('Reserve', VarTree(VariableTree()))
        comp.missin.Reserve.add('irs', Int(-999 ))
        comp.missin.Reserve.add('resrfu', Float(-999. ))
        comp.missin.Reserve.add('restrp', Float(-999. ))
        comp.missin.Reserve.add('timmap', Float(-999. ))
        comp.missin.Reserve.add('altran', Float(-999. ))
        comp.missin.Reserve.add('nclres', Int(-999 ))
        comp.missin.Reserve.add('ncrres', Int(-999 ))
        comp.missin.Reserve.add('sremch', Float(-999. ))
        comp.missin.Reserve.add('eremch', Float(-999. ))
        comp.missin.Reserve.add('srealt', Float(-999. ))
        comp.missin.Reserve.add('erealt', Float(-999. ))
        comp.missin.Reserve.add('holdtm', Float(-999. ))
        comp.missin.Reserve.add('ncrhol', Int(-999 ))
        comp.missin.Reserve.add('ihopos', Int(-999 ))
        comp.missin.Reserve.add('icron', Int(-999 ))
        comp.missin.Reserve.add('thold', Float(-999. ))
        comp.missin.Reserve.add('ncrth', Int(-999 ))

        # New mission definition defaults to the original one
        comp.add('mission_definition', List(iotype='in'))
        comp.mission_definition = self.input.mission_definition.mission

        self.input.add(name, VarTree(comp))'''


  

       
      
    



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
        if len(unlisted_groups) > 0:
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


        # Mission segments are also a challenge.
        # The remaining empty groups should be mission segments or comments.

        missions = []
        if len(empty_groups) > 0:

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
                '''self.set("input:%s.mission_definition" % name, \
                           missions[mission_start:mission_end+1])'''
                self.add_param("input:%s:mission_definition" % name,val=missions[mission_start:mission_end+1])


        # Certain data files are sometimes jammed into the input file. We have
        # to jump through some hoops to detect and import this information.

        ndecks = 0
        #getValue(self,'input:engdin:Basic:igenen')
        #exit()

        #if self.input.engdin.Basic.igenen in (0, -2):
        if self.getValue('input:engdin:Basic:igenen') in (0,-2):
            found = False
            engine_deck = ""
            for i, group in enumerate(sb.groups):

                if group.lower().strip() == 'engdin':
                    found = True

                elif found == True:

                    if len(sb.cards[i]) > 0:
                        break

                    engine_deck += '%s\n' % group
                    ndecks += 1

            self.input.engine_deck.engdek = engine_deck

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

                    if len(sb.cards[i]) > 0:
                        break

                    aerodat += '%s\n' % group
                    ndecks += 1

            #self.input.aero_data.aerodat = aerodat
            self.assignValue('input:aero_data:aerodat',aerodat)
        # Post process some stuff, mostly arrays 2D arrays that come over as 1D

        #tf = self.input.wtin.Inertia.tf
        tf = self.getValue('input:wtin:Inertia:tf')
        # TODO: tf can be input with 1st dim greater than one. Need to find out
        # how that is written / parsed.

        if tf.shape[0] > 0:
            #self.set('input.wtin.Inertia.tf', array([tf]))
            self.assignValues('input:wtin:Inertia:tf',array([tf]))      

        # Report diagnostics and raise any exceptions.
        print( "Empty Groups: %d, Unhandled Groups: %d, Unlinked Vars: %d" % \
              (len(empty_groups)-len(missions)-ndecks, \
               len(unlisted_groups)-self.npcon-self.nrern0-self.nseg0-num_mission, \
               len(unlinked_vars)))

  













testFile = './test/xflp1.in'


#top.root.my_flops.load_model(testFile)
        #top = Problem()
        #top.root =  Group()
        #top.root.add('my_flops',self)
        #top.setup(check=False)
top = Problem()
top.root = Group()
top.root.add('my_flops',FlopsWrapper())
#top.setup(check=False)
top.root.my_flops.load_model(testFile)

top.root.my_flops.generate_input()


