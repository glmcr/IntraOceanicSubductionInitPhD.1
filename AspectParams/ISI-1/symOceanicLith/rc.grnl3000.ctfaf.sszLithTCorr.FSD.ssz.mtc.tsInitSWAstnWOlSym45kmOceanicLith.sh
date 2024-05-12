#!/bin/bash
##SBATCH --mail-user=you@some.email.address
##SBATCH --mail-type=BEGIN
##SBATCH --mail-type=END
##SBATCH --mail-type=FAIL
##SBATCH --mail-type=REQUEUE
##SBATCH --mail-type=ALL
##SBATCH --account=def-cagui22

## OK SBATCH --nodes=6
## OK SBATCH --ntasks-per-node=64
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --mem=48G
##SBATCH --time=00-47:35
##SBATCH --time=00-12:35
#SBATCH --time=00-06:35
#SBATCH --chdir=/scratch/gimer47/Crunch/Aspect/ISI-1

export OMP_NUM_THREADS=1
#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

#---
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3

srun /home/gimer47/Dev/GH/aspect-fork/builds/moMTCOnSides.sszOcMTC.sszLithTCorr.pMPa.LUSICompoParticles.MTC.diffExpTh/aspect.release \
/home/gimer47/Dev/AspectParamsFiles/ISI-1/symOceanicLith/rc.grnl3000.ctfaf.sszLithTCorr.FSD.ssz.mtc.tsInitSWAstnWOlSym45kmOceanicLith.prm
