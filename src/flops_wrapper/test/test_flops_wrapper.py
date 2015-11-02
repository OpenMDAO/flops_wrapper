# pylint: disable-msg=C0111,C0103

import unittest
import os
import sys
import shutil

# Append the path above us, so that we can run the test even if we don't
# have the package installed.


#from flops_wrapper.flops_wrapper import FlopsWrapper
import sys
sys.path.append("../")
from flops_wrapper import FlopsWrapper
from openmdao.core.problem import Problem
from openmdao.core.group import Group
from openmdao.recorders.dump_recorder import DumpRecorder

class FLOPSWrapperTestCase(unittest.TestCase):

    def setUp(self):
        """this setup function will be called before each test in this class"""
        pass

    def tearDown(self):
        """this teardown function will be called after each test"""

        for filename in ['flops.inp', 'flops.out', 'flops.err', 'flops.dump', 'FPex4']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_FLOPS_cases(self):

        dirname = os.path.abspath(os.path.dirname(__file__))

        basename = os.getcwd()
        os.chdir(dirname)

        try:
            for num in range(1, 7):
                startfile_name = 'xflp%s.in' % num
                infile_name = 'xflp%s_openmdao.in' % num
                outfile_name = 'xflp%s_openmdao.out' % num
                dumpfile_name = 'xflp%s_openmdao.dump' % num
                top = Problem()
                top.root = Group()
                top.root.add('flops_comp',FlopsWrapper())
                flops_comp = top.root.flops_comp    
         
    
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
    
                '''with open('flops.dump', 'w') as out:
                    #dump(flops_comp, stream=out, recurse=True)'''
                dumpFile = open('flops.dump','w')
                simple_dump(flops_comp,out_stream=dumpFile)
                dumpFile.close()

                with open(dumpfile_name, 'r') as inp:
                    result1 = inp.readlines()
                with open('flops.dump', 'r') as inp:
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

def simple_dump(comp, out_stream=sys.stdout):
    # The current dump function in Components only dumps the outputs
    """
    Writes a formated dump of this `Component` to file.

    Args
    ----

    out_stream : an open file, optional
        Where output is written.  Defaults to sys.stdout.

    """

    ulabel, plabel, uvecname, pvecname = 'u', 'p', 'unknowns', 'params'

    uvec = getattr(comp, uvecname)
    pvec = getattr(comp, pvecname)


    for v in sorted(pvec):


        inval = ' \''+v+'\' = '+str(pvec[v])+'\n'
        out_stream.write( inval)


    for v in sorted(uvec):
        outval =  ' \''+v+'\' = '+str(uvec[v])+'\n'
        out_stream.write(outval)


    out_stream.flush()



if __name__ == "__main__":
    unittest.main()
