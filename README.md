# NanoAOD skimming code

## First installation on lxplus

### Set up recent CMSSW release 

-Tested in 10_6_28_patch1 but 10_6_30 should work as well - there's no strong dependence on the version

```shell
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
```
- You should get this WARNING message if you are on lxplus

```shell
WARNING: Developer's area is created for non-production architecture slc7_amd64_gcc820. Production architecture for this release is slc7_amd64_gcc700.
```

### NanoAOD-tools installation

-Tools for working with NanoAOD

```shell
cd $CMSSW_BASE/src
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
cmsenv
scram b
```

### Clone this git repo

```shell
cd $CMSSW_BASE/src
git clone git@github.com:cms-hnl/nanoaod-skim.git
```

## Command to run at each login

```shell
cd $CMSSW_BASE/src
cmsenv
```