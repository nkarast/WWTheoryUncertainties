#!/usr/bin/env python
#
#
# @file addbdt.py
#
# script to add TMVA BDT score to an ntuple (in a friend tree)
#
# if the MVA friend tree exists already, it will be updated with
# a new BDT branch, in which a version number is automatically appended
# to the branch name iff that branch exists
#

import tempfile
import os
import sys
import random
import string
import warnings
import gzip

os.environ['LD_LIBRARY_PATH'] += ':%s/TMVA/lib'%(os.environ['PWD'])

from array import array
from glob import glob
from optparse import OptionParser
from commands import getstatusoutput as shell
from lxml import etree as xmlparser

warnings.filterwarnings("ignore", category=RuntimeWarning) 

def usage():
    print 'addbdt --input=/path/to/file.root --xml=/path/to/weights.xml --name=BDT [--tree=HWWTree --force=False --output=/path/to/output.root]'
    sys.exit(-1)

parser = OptionParser()
parser.add_option('-i', '--input', dest='inputfile', default='', help='input file')
parser.add_option('-t', '--tree', dest='tree', default='HWWTree', help='name of input tree')
parser.add_option('-x', '--xml', dest='xml', default='', help='TMVA weights definition')
parser.add_option('-n', '--name', dest='name', default='BDT', help='name of BDT weight branch')
parser.add_option('-f', '--force', dest='force', action='store_true', default=False, help='ignore warning')
parser.add_option('-o', '--output', dest='outputfile', default='', help='optional output file (if not specified, add MVA information to input file)')
parser.add_option('-a', '--alias', dest='aliasfile', default=None, help='.py file containing branch alias definitions')
parser.add_option('-c', '--cuts', dest='cuts', default=None, help='selection cuts for events to process')
parser.add_option('-m', '--maxevents', dest='maxevents', type='int', default=-1, help='maximum number of events to process')

(options, args) = parser.parse_args()

if options.inputfile=='' or options.name=='':
    usage()

if options.maxevents == -1:
    options.maxevents = float('inf')

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT
roofile = ROOT.TFile.Open
rootree = ROOT.TTree

# ----------- ============ ----------- ============ ----------- ============ -----------

if os.path.exists('TMVA'): ## use local TMVA build if available
    ROOT.gSystem.AddIncludePath(' -ITMVA ')
    for lib in glob('TMVA/lib/*.so'):
        ROOT.gSystem.Load(lib)
    ROOT.gROOT.ProcessLine('.x TMVA/test/TMVAlogon.C')
else: ## use TMVA shipped with ROOT 
    if 'ROOTSYS' not in os.environ:
        print 'ERROR cannot find ROOT installation'
        sys.exit(-1)
    ROOT.gSystem.Load('libTMVA')
    ROOT.gROOT.ProcessLine('.x %s/tmva/test/TMVAlogon.C'%(os.environ['ROOTSYS']))

wsrc = '''\
#include "TMVA/Reader.h"

#include "TString.h"
#include "TObjArray.h"

#include <vector>
#include <map>
#include <iostream>

#define MAX_NUM_MVA 25

namespace TMVATools
{
  TMVA::Reader* myReader[MAX_NUM_MVA] = { 0x0 };
  float p__data[100];
  
  std::string p__method[MAX_NUM_MVA];
  
  TMVA::Reader* loadReader(const char* method, const char* wts_file, const char* variables, unsigned imva = 0, const char* delim=":")
  {
    if(imva > MAX_NUM_MVA)
    {
      std::cerr << "ERROR cannot allocate more than [" << MAX_NUM_MVA << "] MVA\'s" << std::endl;
      return NULL;
    }

    if(myReader[imva] != 0x0)
    {
      std::cerr << "WARNING deleting existing MVA with index [" << imva << "]" << std::endl;
      delete myReader[imva];
    }
    
    myReader[imva] = new TMVA::Reader("!Color:!Silent");
    
    TObjArray* list = TString(variables).Tokenize(delim);
    for(unsigned int il = 0; il < (unsigned) list->GetEntries(); ++il)
    {
      myReader[imva]->AddVariable(((TObjString*)list->At(il))->GetString().Data(), &(p__data[il]));
    }
    p__method[imva] = method;
    myReader[imva]->BookMVA(method, wts_file);
    delete list;
    
    return myReader[imva];
  }
  
  double evaluateMVA(unsigned imva, double a, double b = 0, double c = 0, 
		      double d = 0, double e = 0, double f = 0, double g = 0, 
		      double h = 0, double i = 0, double j = 0, double k = 0, 
		      double l = 0, double m = 0, double n = 0, double o = 0, 
		      double p = 0, double q = 0, double r = 0, double s = 0, 
		      double t = 0, double u = 0, double v = 0, double w = 0, 
		      double x = 0, double y = 0, double z = 0)
  {
    unsigned ic = 0;
    p__data[ic++] = float(a);    
    p__data[ic++] = float(b);
    p__data[ic++] = float(c);    
    p__data[ic++] = float(d);
    p__data[ic++] = float(e);    
    p__data[ic++] = float(f);
    p__data[ic++] = float(g);    
    p__data[ic++] = float(h);
    p__data[ic++] = float(i);    
    p__data[ic++] = float(j);
    p__data[ic++] = float(k);    
    p__data[ic++] = float(l);
    p__data[ic++] = float(m);    
    p__data[ic++] = float(n);
    p__data[ic++] = float(o);       
    p__data[ic++] = float(p);
    p__data[ic++] = float(q);    
    p__data[ic++] = float(r);
    p__data[ic++] = float(s);    
    p__data[ic++] = float(t);
    p__data[ic++] = float(u);    
    p__data[ic++] = float(v);
    p__data[ic++] = float(w); 
    p__data[ic++] = float(x); 
    p__data[ic++] = float(y); 
    p__data[ic++] = float(z); 
    
    // for(ic = 0; ic < 15; ++ic) { std::cout << p__data[ic] << " "; }
    // std::cout << endl;
    
    if(myReader[imva] != 0x0)
      return (myReader[imva]->EvaluateMVA(p__method[imva].c_str()));
    
    return -1;
  }
}
'''

hndl, tmpname = tempfile.mkstemp(suffix='.C', dir='/tmp')
hndl = open(tmpname, 'w')
hndl.write(wsrc)
hndl.close()
gROOT.ProcessLine('.L %s+g'%(tmpname))

__bdts = {  }

class treedef:
    def __init__(self, index, args, exprs):
        self.index = index
        self.args = args
        self.exprs = exprs

class xmlreader:
    def __init__(self, fn, ownfile=False):
        self._fn  = fn
        self._ownfile = ownfile
    def __del__(self):
        if self._ownfile:
            s,o = shell('rm -rf %s'%(self._fn))
    def __str__(self):
        return self._fn
    def handle(self):
        if self._fn.endswith('.gz'): return gzip.open(self._fn,'rb')
        else:                        return open(self._fn,'r')
    def buffer(self):
        hndl, fn = tempfile.mkstemp(prefix='bdt', suffix='.xml', dir='/tmp')
        hndl = open(fn, 'w')
        hndl.write(self.handle().read())
        hndl.close()
        return xmlreader(fn, True)

def loadBDTFromXML(weightsfn, name, aliases=None):
    global __bdts
    if name in __bdts:
        print 'WARNING overriding existing definition for', name
    xmlfile = xmlreader(weightsfn)
    xmlbuff = xmlfile.buffer()
    rootnode = xmlparser.parse(xmlfile.handle())
    mvavars = map(lambda x: x.replace('&gt;', '>').replace('&lt;', '<'), [ ele.attrib['Label'] for ele in rootnode.xpath('//Variable') ])
    mvaexpr = map(lambda x: x.replace('&gt;', '>').replace('&lt;', '<'), [ ele.attrib['Title'] for ele in rootnode.xpath('//Variable') ])
    if aliases != None:
        for k,v in aliases.items():
            mvaexpr = [ v if x == k else x for x in mvaexpr ]
    mvaargs = ','.join(mvaexpr) ## << variable expressions in HWWTree
    __bdts[name] = treedef(len(__bdts), mvaargs, mvaexpr)
    reader = ROOT.TMVATools.loadReader(name, str(xmlbuff), '|'.join(mvavars), __bdts[name].index, '|')
    return reader

def getBDTExpression(name):
    if name in __bdts:
        defn = __bdts[name]
        return 'TMVATools::evaluateMVA(%d, %s)'%(defn.index, defn.args)
    return '-1'

dummyweight = -1.0e6

# ----------- ============ ----------- ============ ----------- ============ -----------

if options.outputfile != '':
    ifile = roofile(options.inputfile, 'read')
    ofile = roofile(options.outputfile, 'recreate')
    if ofile == None or ofile.IsZombie():
        raise IOError, 'ERROR: could not open file [%s] for writing'%(options.outputfile)
else:
    ifile = roofile(options.inputfile, 'update')
    ofile = None
itree = ifile.Get(options.tree)
if itree == None:
    print 'FATAL :: tree [%s] not found'%(options.tree)
    sys.exit(-1)

aliases = None
if options.aliasfile != None:
    try:
        execfile(options.aliasfile) ## mod = __import__(options.aliasfile)
    except ImportError, AttributeError:
        print 'ERROR :: could not import aliases'
if aliases != None:
    for br in aliases.values():
        if itree.GetBranch(br) == None:
            print 'WARNING :: alias points to branch [%s] that may not exist'%(br)

loadBDTFromXML(options.xml, 'BDT', aliases)
expr = getBDTExpression('BDT')

print 'INFO :: using BDT expression "%s"'%(expr)

formula = ROOT.TTreeFormula('BDT', expr, itree)
formula.SetQuickLoad(True)

selection = None
if options.cuts != None:
    itree.Draw('>>selected', options.cuts)
    selection = gROOT.FindObject('selected')

## if addflag is set, then need to add new MVA tree as
## friend to the input tree, and re-write the input tree
## to make this persistent
addflag = False

if ofile == None: ## add MVA information to input file
    if ifile.Get('MVA') == None:
        otree = rootree('MVA', 'MVA')
        addflag = True ## adding new MVA tree
    else:
        otree = ifile.Get('MVA')
        addflag = False
else: ## put MVA information in new output file
    otree = rootree('MVA', 'MVA')

# if not addflag: ## disable unused branches (if not re-writing original tree)
#     for br in itree.GetListOfBranches():
#         enable = ((br.GetName() in expr) or (br.GetName() in aliases.values()))
#         print 'DEBUG :: setting branch status of [%s] to [%s]'%(br.GetName(), enable)
#         itree.SetBranchStatus(br.GetName(), enable)

if addflag:
    itree.AddFriend(otree)

iversion = 1
brref = array('d', [0])
brname = options.name

obranch = None
if otree.GetBranch(brname) != None:
    if not options.force:
        ifile.Close()
        print 'WARNING :: will not overwrite existing branch [%s]'%(brname)
        sys.exit()
    else:
        otree.SetBranchStatus(brname, False)
        otree = otree.CloneTree(-1) ## copy over all branches except the one to overwrite
        # while otree.GetBranch(brname) != None:
        #     iversion += 1
        #     brname = options.name + '_v%d'%(iversion)

obranch = otree.Branch(brname, brref, brname + '/D')

print 'INFO :: will process %d entries'%(itree.GetEntries())
if selection != None:
    print 'INFO :: selected %d entries'%(selection.GetN())
sys.stdout.write('[')
sys.stdout.flush()
for ientry in xrange(itree.GetEntries()):
    if ientry >= options.maxevents:
        break
    nb = itree.LoadTree(ientry)
    if nb < 0:
        print 'ERROR :: processing entry failed'
        sys.exit()
    flag = True
    if selection != None:
        flag = selection.Contains(ientry)
    if flag: brref[0] = formula.EvalInstance()
    else:    brref[0] = dummyweight
    if ofile != None or addflag:
        otree.Fill()
    else:
        obranch.Fill()
    if ientry % min(options.maxevents/10, itree.GetEntries()/10) == 0 and ientry > 0:
        sys.stdout.write('#')
        sys.stdout.flush()
sys.stdout.write(']')
sys.stdout.flush()

otree.Write(otree.GetName(), ROOT.TObject.kOverwrite)

if addflag: ## update friend status of input tree
    itree.Write('', ROOT.TObject.kOverwrite) 

ifile.Close()
if ofile != None:
    ofile.Close()

shell('rm -rf %s %s_C.*'%(tmpname, tmpname.replace('.C','')))

print
