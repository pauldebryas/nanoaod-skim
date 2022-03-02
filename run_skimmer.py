#!/bin/env python
# pylint: disable=E0401,C0103
import os
from argparse import ArgumentParser
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from NanoSkim.NanoSkim.skimmer import Skimmer

# need to keep this for grid-control
# @FILE_NAMES@

maxEvents = -1

cut_dict = {}
cut_dict["base"] = "nMuon>0"
cut_dict["muon_trigger"] = "(HLT_IsoMu27 || HLT_IsoMu24)"

# REDIRECTOR = "root://xrootd-cms.infn.it//"
REDIRECTOR = "root://cms-xrd-global.cern.ch//"

parser = ArgumentParser(description='Run the NanoAOD skimmer.')
parser.add_argument('inFiles', nargs="+", default="", help="Comma-separated list of input files")
parser.add_argument('--out', action="store", dest="outDir", default="./",
                    help="Output directory")
parser.add_argument('--keepdrop', action="store", dest="keepDropFile",
                    default="keep_and_drop_skim.txt", help="Branches keep and drop file")
parser.add_argument('--isdata', action="store_true", dest="isdata", default=False,
                    help="Whether running on data")
parser.add_argument('--tag', dest='tag', default='skim')
args = parser.parse_args()

# inFiles come as combination of comma- and/or space-separated list
inFiles = ','.join(args.inFiles).replace("\"", "").split(',')
inFiles = [REDIRECTOR+f if f.startswith('/store') else f for f in inFiles]
outputDir = args.outDir
keepDropFile = args.keepDropFile

cuts = '&&'.join(['({})'.format(cut) for cut in cut_dict.values()])

# jetmetUncertainties2017(),
modules = [Skimmer(args.isdata)]

jsonInput = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt' if args.isdata else None

p = PostProcessor(outputDir, inFiles, cuts, outputbranchsel=keepDropFile,
                  modules=modules, provenance=False, fwkJobReport=False,
                  jsonInput=jsonInput, postfix=args.tag)
p.run()



# REDUCE FILE SIZE
# Temporary solution to reduce file size
#   https://hypernews.cern.ch/HyperNews/CMS/get/physTools/3734/1.html
#   https://github.com/cms-nanoAOD/nanoAOD-tools/issues/249
print(">>> Reduce file size...")
import glob
from subprocess import Popen, PIPE, STDOUT, CalledProcessError

outfiles = os.path.join(outputDir, "*%s.root"%args.tag)

def execute(command,dry=False,fatal=True,verb=0):
  """Execute shell command."""
  command = str(command)
  out = ""
  if dry:
    print ">>> Dry run: %r"%(command)
  else:
    if verb>=1:
      print ">>> Executing: %r"%(command)
    try:
      #process = Popen(command.split(),stdout=PIPE,stderr=STDOUT) #,shell=True)
      process = Popen(command,stdout=PIPE,stderr=STDOUT,bufsize=1,shell=True) #,universal_newlines=True
      for line in iter(process.stdout.readline,""):
        if verb>=1: # real time print out (does not work for python scripts without flush)
          print line.rstrip()
        out += line
      process.stdout.close()
      retcode = process.wait()
      ##print 0, process.communicate()
      ##out     = process.stdout.read()
      ##err     = process.stderr.read()
      ##print out
      out = out.strip()
    except Exception as e:
      if verb<1:
        print out #">>> Output: %s"%(out)
      print ">>> Failed: %r"%(command)
      raise e
    if retcode and fatal:
      if verb<1:
        print out
      raise CalledProcessError(retcode,command)
      #raise Exception("Command '%s' ended with return code %s"%(command,retcode)) #,err)
  return out

execute("ls -hlt %s"%(outfiles),verb=2)
for outfile in glob.glob(outfiles):
  ftmp = outfile.replace(".root","_tmp.root")
  execute("haddnano.py %s %s"%(ftmp,outfile),verb=2) # reduce file size
  execute("ls -hlt %s %s"%(ftmp,outfile),verb=2)
  execute("mv %s %s"%(ftmp,outfile),verb=2)
execute("ls -hlt %s"%(outfiles),verb=2)
