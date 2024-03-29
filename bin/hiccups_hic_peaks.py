#!/usr/bin/env python

from __future__ import division
import argparse, sys, logging, logging.handlers

import numpy as np
from scipy import sparse
from sklearn import isotonic

def getargs():
    ## Construct an ArgumentParser object for command-line arguments
    parser = argparse.ArgumentParser(usage = '%(prog)s <-O output> [options]',
                                     description = 'Local Peak Calling for Hi-C Data',
                                     formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # Output
    parser.add_argument('-O', '--output', help = 'Output prefix.')
    parser.add_argument('--logFile', default = 'HICCUPS.log', help = 'Logging file name.')
    
    group_1 = parser.add_argument_group(title = 'Relate to Hi-C data:')
    group_1.add_argument('-p', '--path', default = '.',
                         help = 'Path to Hi-C data')
    group_1.add_argument('-R', '--resolution', default = 10000, type = int,
                         help = 'Resolution of the binned data')
    group_1.add_argument('-C', '--chroms', nargs = '*', default = ['#', 'X'],
                         help = 'Which chromosomes to read. Specially, "#" stands'
                         ' for chromosomes with numerical labels. "--chroms" with zero argument'
                         ' will generate an empty list, in which case all chromosome data will'
                         ' be loaded.')
    
    ## About the algorithm
    group_2 = parser.add_argument_group(title = 'Algorithm Parameters:')
    group_2.add_argument('--pw', type = int, default = 2, help = 'Width of the interaction '
                         'region surrounding the peak. According to experience, we set it'
                         ' to 1 at 20 kb, 2 at 10 kb, and 4 at 5 kb.')
    group_2.add_argument('--ww', type = int, default = 5, help = 'The size of the donut '
                         'sampled. Set it to 3 at 20 kb, 5 at 10 kb, and 7 at 5 kb.')
    group_2.add_argument('--maxww', type = int, default = 20, help = 'Maximum donut size.')
    group_2.add_argument('--siglevel', type = float, default = 0.1, help = 'Significant Level.')
    group_2.add_argument('--maxapart', type = int, default = 10000000, help = 'Maximum genomic'
                         ' distance between two loci.')
    
    ## Parse the command-line arguments
    commands = sys.argv[1:]
    if not commands:
        commands.append('-h')
    args = parser.parse_args(commands)
    
    return args, commands

def run():
     # Parse Arguments
    args, commands = getargs()
    # Improve the performance if you don't want to run it
    if commands[0] not in ['-h', '--help']:
        ## Root Logger Configuration
        logger = logging.getLogger()
        # Logger Level
        logger.setLevel(10)
        console = logging.StreamHandler()
        filehandler = logging.handlers.RotatingFileHandler(args.logFile,
                                                           maxBytes = 100000,
                                                           backupCount = 5)
        # Set level for Handlers
        console.setLevel('INFO')
        filehandler.setLevel('DEBUG')
        # Customizing Formatter
        formatter = logging.Formatter(fmt = '%(name)-14s %(levelname)-7s @ %(asctime)s: %(message)s',
                                      datefmt = '%m/%d/%y %H:%M:%S')
        
        console.setFormatter(formatter)
        filehandler.setFormatter(formatter)
        # Add Handlers
        logger.addHandler(console)
        logger.addHandler(filehandler)
        
        ## Logging for argument setting
        arglist = ['# ARGUMENT LIST:',
                   '# output file prefix = %s' % args.output,
                   '# HiC Data Path = %s' % args.path,
                   '# chromosomes = %s' % args.chroms,
                   '# data resolution = %s' % args.resolution,
                   '# Peak window width = %s' % args.pw,
                   '# Donut size = %s' % args.ww,
                   '# Maximum donut size = %s' % args.maxww,
                   '# Significant Level = %s' % args.siglevel,
                   '# Genomic distance range = %s' % [args.ww * args.resolution, args.maxapart]
                   ]
        
        argtxt = '\n'.join(arglist)
        logger.info('\n' + argtxt)
        
        # Package Dependencies
        from mirnylib.numutils import completeIC
        
        logger.info('Locating Hi-C data ...')
        Lib = np.load(args.path)
        
        logger.info('Calling Peaks ...')
        OF = open('.'.join([args.output, 'peaks', 'txt']), 'wb')
        head = '\t'.join(['chromLabel', 'loc_1', 'loc_2', 'IF', 'D-Enrichment', 'D-pvalue', 'D-qvalue',
                          'LL-Enrichment', 'LL-pvalue', 'LL-qvalue']) + '\n'
        OF.write(head)
        
        for key in Lib.files:
            if ((not args.chroms) or (key.isdigit() and '#' in args.chroms) or (key in args.chroms)):
                logger.info('Chromosome %s ...', key)
                sparseH = Lib[key].reshape(1)[0]
                triuH = sparseH.toarray()
                H = triuH + triuH.T - np.diag(triuH.diagonal()) # Symmetric Matrix
                del sparseH, triuH # Release Memory
                logger.info('Perform ICE ...')
                cHeatMap, biases = completeIC(H, returnBias = True)
                logger.info('Done!')
                
                logger.info('Customize Sparse Matrix ...')
                chromLen = H.shape[0]
                num = args.maxapart // args.resolution + args.maxww + 1
                Diags = [np.diagonal(H, i) for i in np.arange(num)]
                M = sparse.diags(Diags, np.arange(num), format = 'csr')
                x = np.arange(args.ww, num)
                y = []
                cDiags = []
                for i in x:
                    diag = np.diagonal(cHeatMap, i)
                    y.append(diag.mean())
                    cDiags.append(diag)
                cM = sparse.diags(cDiags, x, format = 'csr')
                IR = isotonic.IsotonicRegression(increasing = 'auto')
                IR.fit(x, y)
                
                del H, cHeatMap
                
                Donuts, LL = pcaller(M, cM, biases, IR, chromLen, Diags, cDiags, num,
                                     pw = args.pw, ww = args.ww, sig = args.siglevel,
                                     maxww = args.maxww, maxapart = args.maxapart,
                                     res = args.resolution)
                                                                
                for i in Donuts:
                    lineFormat = '%s\t%d\t%d\t%.4g\t%.4g\t%.4g\t%.4g\t%.4g\t%.4g\t%.4g\n'
                    contents = (key,) + i + Donuts[i] + LL[i][1:]
                    line = lineFormat % contents
                    OF.write(line)
                    
        OF.flush()
        OF.close()
                            
        logger.info('Done!')

def pcaller(M, cM, biases, IR, chromLen, Diags, cDiags, num, pw = 2, ww = 5, sig = 0.05, maxww = 20,
            maxapart = 2000000, res = 10000):
    
    # Necessary Modules
    from scipy.stats import poisson
    from statsmodels.sandbox.stats.multicomp import multipletests
    
    logger = logging.getLogger()
    
    extDiags = {}
    for w in range(ww, maxww + 1):
        temp = []
        for i in xrange(num):
            OneDArray = Diags[i]
            extODA = np.zeros(chromLen - i + w*2)
            extODA[w:-w] = OneDArray
            temp.append(extODA)
        extDiags[w] = temp
    
    x = np.arange(ww, num)
    predictE = IR.predict(x)
    predictE[predictE < 0] = 0
    EDiags = []
    for i in xrange(x.size):
        OneDArray = np.ones(chromLen - x[i]) * predictE[i]
        EDiags.append(OneDArray)
    
    EM = sparse.diags(EDiags, x, format = 'csr')
    
    extCDiags = {}
    extEDiags = {}
    for w in range(ww, maxww + 1):
        tempC = []
        tempE = []
        for i in xrange(x.size):
            extODA_E = np.zeros(chromLen - x[i] + w*2)
            extODA_E[w:-w] = EDiags[i]
            tempE.append(extODA_E)
            extODA_C = np.zeros(chromLen - x[i] + w*2)
            extODA_C[w:-w] = cDiags[i]
            tempC.append(extODA_C)
        extCDiags[w] = tempC
        extEDiags[w] = tempE
    
    ps = 2 * pw + 1 # Peak Size
    
    Pool_Diags = {}
    Pool_EDiags = {}
    Pool_cDiags = {}
    Offsets_Diags = {}
    Offsets_EDiags = {}
    
    for w in range(ww, maxww + 1):
        ws = 2 * w + 1 # Window size
        ss = range(ws)
        Pool_Diags[w] = {}
        Pool_EDiags[w] = {}
        Pool_cDiags[w] = {}
        Offsets_Diags[w] = {}
        Offsets_EDiags[w] = {}
        for i in ss:
            for j in ss:
                Pool_Diags[w][(i,j)] = []
                Pool_EDiags[w][(i,j)] = []
                Pool_cDiags[w][(i,j)] = []
                Offsets_Diags[w][(i,j)] = np.arange(num) + (i - j)
                Offsets_EDiags[w][(i,j)] = x + (i - j)
                for oi in np.arange(num):
                    if Offsets_Diags[w][(i,j)][oi] >= 0:
                        starti = i
                        endi = i + chromLen - Offsets_Diags[w][(i,j)][oi]
                    else:
                        starti = i - Offsets_Diags[w][(i,j)][oi]
                        endi = starti + chromLen + Offsets_Diags[w][(i,j)][oi]
                    Pool_Diags[w][(i,j)].append(extDiags[w][oi][starti:endi])
                for oi in xrange(x.size):
                    if Offsets_EDiags[w][(i,j)][oi] >= 0:
                        starti = i
                        endi = i + chromLen - Offsets_EDiags[w][(i,j)][oi]
                    else:
                        starti = i - Offsets_EDiags[w][(i,j)][oi]
                        endi = starti + chromLen + Offsets_EDiags[w][(i,j)][oi]
                    Pool_EDiags[w][(i,j)].append(extEDiags[w][oi][starti:endi])
                    Pool_cDiags[w][(i,j)].append(extCDiags[w][oi][starti:endi])
                
    ## Peak Calling ...    
    xi, yi = M.nonzero()
    Mask = ((yi - xi) >= ww) & ((yi - xi) <= (maxapart // res))
    xi = xi[Mask]
    yi = yi[Mask]
    flocals = ['K', 'Y']
    bSV = {}; bEV = {}
    for fl in flocals:
        bSV[fl] = np.zeros(xi.size)
        bEV[fl] = np.zeros(xi.size)
    
    logger.info('Observed Contact Number: %d', xi.size)
    
    RefIdx = np.arange(xi.size)
    RefMask = np.ones_like(xi, dtype = bool)
    
    iniNum = xi.size
    
    logger.info('Two local neighborhoods, two expected matrices ...')
    for w in range(ww, maxww + 1):
        ws = 2 * w + 1
        bS = {}; bE = {}
        for fl in flocals:
            bS[fl] = sparse.csr_matrix((chromLen, chromLen))
            bE[fl] = sparse.csr_matrix((chromLen, chromLen))
        Reads = sparse.csr_matrix((chromLen, chromLen))
        logger.info('    Current window width: %s' % w)
        P1 = set([(i,j) for i in range(w-pw, ps+w-pw) for j in range(w-pw, ps+w-pw)]) # Center Peak Region
        P_1 = set([(i,j) for i in range(w+1, ws) for j in range(w)])
        P_2 = set([(i,j) for i in range(w+1, ps+w-pw) for j in range(w-pw, w)])
        P2 = P_1 - P_2 # Lower-left Region
        
        for key in Pool_Diags[w]:
            if (key[0] != w) and (key[1] != w) and (key not in P1) and (key not in P2):
                bS['K'] = bS['K'] + sparse.diags(Pool_cDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
                bE['K'] = bE['K'] + sparse.diags(Pool_EDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
            if key in P2:
                bS['K'] = bS['K'] + sparse.diags(Pool_cDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
                bE['K'] = bE['K'] + sparse.diags(Pool_EDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
                bS['Y'] = bS['Y'] + sparse.diags(Pool_cDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
                bE['Y'] = bE['Y'] + sparse.diags(Pool_EDiags[w][key], Offsets_EDiags[w][key], format = 'csr')
                Reads = Reads + sparse.diags(Pool_Diags[w][key], Offsets_Diags[w][key], format = 'csr')
                
        Txi = xi[RefIdx]
        Tyi = yi[RefIdx]
        RNums = np.array(Reads[Txi, Tyi]).ravel()
        EIdx = RefIdx[RNums >= 16]
        logger.info('    Valid Contact Number: %d', EIdx.size)
        Valid_Ratio = EIdx.size/float(iniNum)
        logger.info('    Valid Contact Ratio: %.3f', Valid_Ratio)
        Exi = xi[EIdx]
        Eyi = yi[EIdx]
        for fl in flocals:
            bSV[fl][EIdx] = np.array(bS[fl][Exi, Eyi]).ravel()
            bEV[fl][EIdx] = np.array(bE[fl][Exi, Eyi]).ravel()
                
        RefIdx = RefIdx[RNums < 16]
            
        iniNum = RefIdx.size
        
        if Valid_Ratio < 0.1:
            logger.info('    Ratio of valid contact is too small, break the loop ...')
            break
        
        logger.info('    Continue ...')
        logger.info('    %d Contacts will get into next loop ...', RefIdx.size)
    
    RefMask[RefIdx] = False
    
    Mask = (bEV['K'] != 0) & (bEV['Y'] != 0) & RefMask
    xi = xi[Mask]
    yi = yi[Mask]
    bRV = {}
    for fl in flocals:
        bRV[fl] = bSV[fl][Mask] / bEV[fl][Mask]
    
    bR = {}
    for fl in flocals:
        bR[fl] = sparse.csr_matrix((chromLen, chromLen))
        bR[fl][xi, yi] = bRV[fl]
    
    ## Corrected Expected Matrix
    cEM = {}
    for fl in flocals:
        cEM[fl] = EM.multiply(bR[fl])
    
    logger.info('Poisson Models and Benjamini-Hochberg Correcting for lambda chunks ...')
    Description = {'K': 'Donut backgrounds', 'Y': 'Lower-left backgrounds'}
    xpos = {}; ypos = {}; Ovalues = {}; Evalues = {}
    Fold = {}; pvalues = {}; qvalues = {}
    gaps = set(np.where(np.array(M.sum(axis=1)).ravel() == 0)[0])
    for fl in flocals:
        logger.info('    %s ...', Description[fl])
        xi, yi = cEM[fl].nonzero()
        Evalues[fl] = np.array(cEM[fl][xi, yi]).ravel() * biases[xi] * biases[yi]
        Mask = (Evalues[fl] > 0)
        Evalues[fl] = Evalues[fl][Mask]
        xi = xi[Mask]
        yi = yi[Mask]
        Ovalues[fl] = np.array(M[xi, yi]).ravel()
        Fold[fl] =  Ovalues[fl] / Evalues[fl]
        logger.info('    Valid contact number: %d', xi.size)
        
        pvalue = np.ones(xi.size)
        qvalue = np.ones(xi.size)
        
        logger.info('    Lambda chunking ...')
        chunks = lambdachunk(Evalues[fl])
        logger.info('    Number of chunks: %d', len(chunks))
        for chunk in chunks:
            logger.debug('        lv: %.4g, rv: %.4g, Num: %d', chunk[0], chunk[1], chunk[2].size)
            if chunk[2].size > 0:
                Poiss = poisson(chunk[1])
                logger.debug('        Assign P values ...')
                chunkP = 1 - Poiss.cdf(Ovalues[fl][chunk[2]])
                pvalue[chunk[2]] = chunkP
                logger.debug('        Multiple testing ...')
                cResults = multipletests(chunkP, alpha = sig, method = 'fdr_bh')
                cP = cResults[1] # Corrected Pvalue
                qvalue[chunk[2]] = cP
            else:
                logger.debug('        Skipping ...')
        
        reject = qvalue <= sig
        qvalue = qvalue[reject]
        pvalue = pvalue[reject]
        Ovalues[fl] = Ovalues[fl][reject]
        Evalues[fl] = Evalues[fl][reject]
        Fold[fl] = Fold[fl][reject]
        xi = xi[reject]
        yi = yi[reject]
        
        logger.info('    Remove Gap Effects ...')
        
        if len(gaps) > 0:
            fIdx = []
            for i in xrange(xi.size):
                lower = (xi[i] - 5) if (xi[i] > 5) else 0
                upper = (xi[i] + 5) if ((xi[i] + 5) < chromLen) else (chromLen - 1)
                cregion_1 = range(lower, upper)
                lower = (yi[i] - 5) if (yi[i] > 5) else 0
                upper = (yi[i] + 5) if ((yi[i] + 5) < chromLen) else (chromLen - 1)
                cregion_2 = range(lower, upper)
                cregion = set(cregion_1) | set(cregion_2)
                intersect = cregion & gaps
                if len(intersect) == 0:
                    fIdx.append(i)
        
            xi = xi[fIdx]
            yi = yi[fIdx]
            Ovalues[fl] = Ovalues[fl][fIdx]
            pvalue = pvalue[fIdx]
            qvalue = qvalue[fIdx]
            Fold[fl] = Fold[fl][fIdx]
            Evalues[fl] = Evalues[fl][fIdx]
        
        xpos[fl] = xi
        ypos[fl] = yi
        pvalues[fl] = pvalue
        qvalues[fl] = qvalue
    
    logger.info('Combine two local filters ...')
    
    preDonuts = dict(zip(zip(xpos['K']*res, ypos['K']*res), zip(Ovalues['K'], Fold['K'], pvalues['K'], qvalues['K'])))
    preLL = dict(zip(zip(xpos['Y']*res, ypos['Y']*res), zip(Ovalues['Y'], Fold['Y'], pvalues['Y'], qvalues['Y'])))
    
    commonPos = set(preDonuts.keys()) & set(preLL.keys())
    Donuts = {}; LL = {}
    for pos in commonPos:
        Donuts[pos] = preDonuts[pos]
        LL[pos] = preLL[pos]
    
    return Donuts, LL

def lambdachunk(E):
    
    numbin = np.int(np.ceil(np.log(E.max()) / np.log(2) * 3 + 1))
    Pool = []
    for i in xrange(1, numbin + 1):
        if i == 1:
            lv = 0; rv = 1
        else:
            lv = np.power(2, ((i - 2)/3.))
            rv = np.power(2, ((i - 1)/3.))
        idx = np.where((E > lv) & (E < rv))[0]
        Pool.append((lv, rv, idx))
    
    return Pool
    

if __name__ == '__main__':
    run()