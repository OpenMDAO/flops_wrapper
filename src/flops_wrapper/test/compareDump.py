# routine to check component.dump from


def editFile(file1,fileNameOut,keyIgnore,replace):
    fileIn1 = open(file1,'r')
    fileOut = open(fileNameOut,'w')
    newLine = []
    for line1 in fileIn1:
        if any(s in line1 for s in keyIgnore):
            pass
        elif replace[0] in line1:
                newLine.append(line1.replace(replace[0],replace[1]))
        else:
            newLine.append(line1.replace('\"','\''))
    lineList = sorted(newLine)
    for item in lineList:
        fileOut.write(item)
    fileIn1.close()
    fileOut.close()



'''replace= ['npcon','input.missin.Basic.npcon']
ignoreKey=['ERROR','HINT','<flops_wrapper','derivative_exec_count','directory','env_vars',
                    'exec_count','force_fd','poll_delay', 'resources', 'return_code', 'timed_out', 'timeout',
                     'itername', 'missing_deriv_policy','npcons','nrerun','nseg','<open']
check('xflp6_openmdao.dump','tt1.txt',ignoreKey,replace)'''
