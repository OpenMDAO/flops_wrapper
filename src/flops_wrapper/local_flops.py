import os
import sys
#wrapper for flops executable
def flopsH(inputName,outputName,flops_exec='flops'):
    #print('Running FLOPS',inputName,'>',outputName)
    os.system(flops_exec+' <'+inputName+'>'+outputName)


if __name__ == "__main__":

    input_filename = sys.argv[2]
    output_filename = sys.argv[3]
    exec_command = sys.argv[1]
    flopsH(input_filename, output_filename,flops_exec=exec_command)

