# pylint: disable-msg=C0111,C0103

import unittest
import os
import sys
import shutil

# Append the path above us, so that we can run the test even if we don't
# have the package installed.
import sys
sys.path.append("../")
#from flops_wrapper.flops_wrapper import FlopsWrapper
from flops_wrapper import FlopsWrapper
from openmdao.core.problem import Problem
from openmdao.core.group import Group
from compareDump import editFile



class FLOPSWrapperTestCase(unittest.TestCase):

    def setUp(self):
        """this setup function will be called before each test in this class"""
        pass

    def tearDown(self):
        """this teardown function will be called after each test"""

        for filename in ['flops.inp', 'flops.out', 'flops.err', 
                                    'flops.dump','FPex4',
                                    'temp_openmado.dump',
                                    'edited_temp_openmado.dump',
                                     'edited_Old.dump']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_FLOPS_cases(self):

        dirname = os.path.abspath(os.path.dirname(__file__))

        basename = os.getcwd()
        os.chdir(dirname)

        try:
            for num in range(1,7):
    
                startfile_name = 'xflp%s.in' % num
                infile_name = 'xflp%s_openmdao.in' % num
                outfile_name = 'xflp%s_openmdao.out' % num
                dumpfile_name = 'xflp%s_openmdao.dump' % num
                top = Problem()
                top.root = Group()
                top.root.add('my_flops',FlopsWrapper())

                #top.root.my_flops.load_model(testFile)    
                flops_comp = top.root.my_flops

                #flops_comp = FlopsWrapper()
    
                # Check input file generation
    
                flops_comp.load_model(startfile_name)
                flops_comp.generate_input()
                top.setup(check=False)

                with open(infile_name, 'r') as inp:
                    result1 = inp.readlines()
                with open('flops.inp', 'r') as inp:
                    result2 = inp.readlines()
                lnum = 1
                for line1, line2 in zip(result1, result2):

                    try:
                        self.assertEqual(line1, line2)

                    except AssertionError as err:
                        raise AssertionError("line %d doesn't match file %s: %s"
                                             % (lnum, infile_name, err))
                    lnum += 1
                        
                # Check output file parsing
    
                shutil.copyfile(outfile_name, 'flops.out')

                flops_comp.parse_output()

                #generate temporary dump file for OpenMDAO
                tempdump_name = 'temp_openmado.dump'
                tempdump= open(tempdump_name,'w')    
                mydumpVar(flops_comp,out_stream=tempdump)
                tempdump.close()
            
                #edit output files so that they are suitable for comparison



                #edit old openmdao dump file
                replace= ['npcon','input.missin.Basic.npcon']
                ignoreKey=['ERROR','HINT','<flops_wrapper','derivative_exec_count','directory','env_vars',
                                    'exec_count','force_fd','poll_delay', 'resources', 'return_code', 'timed_out', 'timeout',
                                    'itername', 'missing_deriv_policy','npcons','nrerun','nseg','<open']
                editFile(dumpfile_name,'edited_old.dump',ignoreKey,replace)     

                #edit generated openmdao dump file
                replace=['','']
                ignoreKey=['thrsop','ERROR','HINT']
                editFile(tempdump_name,'edited_'+tempdump_name,ignoreKey,replace)     


                with open('edited_old.dump', 'r') as inp:
                    result1 = inp.readlines()
                with open('edited_'+tempdump_name, 'r') as inp:
                    result2 = inp.readlines()
    
                lnum = 1
                for line1, line2 in zip(result1, result2):
                    # Omit lines with objects, because memory location differs
                    if 'object at' not in line1:
                        try:
                            self.assertEqual(line1, line2)
                        except AssertionError as err:
                            raise AssertionError("line %d doesn't match file %s: %s"
                                                 % (lnum, dumpfile_name, err))
                        lnum += 1

        finally:
            os.chdir(basename)
def mydumpVar(local_comp, out_stream=sys.stdout):
    """
    Writes a formated dump of this `Component` to file.

    Args
    ----

    out_stream : an open file, optional
        Where output is written.  Defaults to sys.stdout.

    """

    ulabel, plabel, uvecname, pvecname = 'u', 'p', 'unknowns', 'params'

    uvec = getattr(local_comp, uvecname)
    pvec = getattr(local_comp, pvecname)


    for v in sorted(pvec):


        inval = ' \''+v.replace(":",'.')+'\':'+' \''+str(pvec[v]).replace("\n","\\n")+'\',\n'
        out_stream.write( inval)


    for v in sorted(uvec):
        outval = ' \''+v.replace(":",'.')+'\':'+' \''+str(uvec[v]).replace("\n","\\n")+'\',\n'
        out_stream.write(outval)


    out_stream.flush()

if __name__ == "__main__":
    unittest.main()
