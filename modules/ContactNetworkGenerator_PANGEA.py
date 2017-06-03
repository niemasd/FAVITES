#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from glob import glob
from os.path import expanduser
from os import chdir,getcwd,makedirs,devnull
from subprocess import check_output
from zipfile import ZipFile

PANGEA_path = "PANGEA_files"
PANGEA_command_script = 'FAVITES_PANGEA_COMMAND.R'
PANGEA_trans_net_script = 'FAVITES_EXTRACT_TRANSMISSION_NETWORK.R'
PANGEA_trans_file = "FAVITES_TRANSMISSION_NETWORK.txt"
PANGEA_ARGS = ["pangea_yr.start", "pangea_yr.end", "pangea_seed", "pangea_s.INC.recent", "pangea_s.INC.recent.len", "pangea_s.PREV.min", "pangea_s.PREV.max", "pangea_s.PREV.base", "pangea_s.INTERVENTION.start", "pangea_s.INTERVENTION.mul", "pangea_s.ARCHIVAL.n", "pangea_s.MODEL", "pangea_s.PREV.max.n", "pangea_s.INTERVENTION.prop", "pangea_epi.model", "pangea_epi.acute", "pangea_epi.intervention", "pangea_epi.dt", "pangea_epi.import", "pangea_root.edge.fixed", "pangea_v.N0tau", "pangea_v.r", "pangea_v.T50", "pangea_wher.mu", "pangea_wher.sigma", "pangea_bwerm.mu", "pangea_bwerm.sigma", "pangea_er.gamma", "pangea_er.gtr", "pangea_sp.prop.of.sexactive", "pangea_report.prop.recent", "pangea_dbg.GTRparam", "pangea_dbg.rER", "pangea_index.starttime.mode", "pangea_startseq.mode", "pangea_seqtime.mode"]

class ContactNetworkGenerator_PANGEA(ContactNetworkGenerator):
    def init():
        assert "ContactNetwork_PANGEA" in str(MF.modules['ContactNetwork']), "Must use ContactNetwork_PANGEA module"
        assert "ContactNetworkGenerator_PANGEA" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PANGEA module"
        assert "EndCriteria_Instant" in str(MF.modules['EndCriteria']), "Must use EndCriteria_Instant module"
        assert "NodeEvolution_PANGEA" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_PANGEA module"
        assert "NodeAvailability_PANGEA" in str(MF.modules['NodeAvailability']), "Must use NodeAvailability_PANGEA module"
        assert "NumBranchSample_All" in str(MF.modules['NumBranchSample']), "Must use NumBranchSample_All module"
        assert "NumTimeSample_PANGEA" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_PANGEA module"
        assert "PostValidation_Dummy" in str(MF.modules['PostValidation']), "Must use PostValidation_Dummy module"
        assert "SeedSelection_PANGEA" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PANGEA module"
        assert "SeedSequence_PANGEA" in str(MF.modules['SeedSequence']), "Must use SeedSequence_PANGEA module"
        assert "SequenceEvolution_PANGEA" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_PANGEA module"
        assert "SourceSample_PANGEA" in str(MF.modules['SourceSample']), "Must use SourceSample_PANGEA module"
        assert "TimeSample_PANGEA" in str(MF.modules['TimeSample']), "Must use TimeSample_PANGEA module"
        assert "TransmissionNodeSample_PANGEA" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PANGEA module"
        assert "TransmissionTimeSample_PANGEA" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PANGEA module"

    def get_edge_list():
        args = []
        for arg in PANGEA_ARGS:
            val = getattr(GC,arg)
            if isinstance(val,str):
                val = val.strip()
                if len(val) != 0:
                    args.append(arg.split('_')[1] + "='" + val + "'")
            else:
                args.append(arg.split('_')[1] + "=" + str(val))
        orig_dir = getcwd()
        makedirs(PANGEA_path)
        chdir(PANGEA_path)
        f = open(PANGEA_command_script,'w')
        f.write("library(PANGEA.HIV.sim)\n")
        f.write("outdir <- getwd()\n")
        f.write("pipeline.args <- sim.regional.args(")
        f.write(', '.join(args))
        f.write(")\ncat(sim.regional(outdir, pipeline.args=pipeline.args))")
        f.close()
        try:
            check_output([GC.Rscript_path,PANGEA_command_script], stderr=open(devnull,'w'))
        except FileNotFoundError:
            chdir(GC.START_DIR)
            assert False, "Rscript executable was not found"
        for script in glob('*.sh'):
            break
        script_str = open(script,'r').read()
        f = open(script,'w')
        f.write('#!/usr/bin/env bash\n' + script_str)
        f.close()
        check_output(['./' + script], stderr=open(script + '_output.log','w'))
        for archive in glob('*_INTERNAL.zip'):
            break
        z = ZipFile(archive, 'r')
        internal = [item for item in z.namelist() if item.endswith('_SIMULATED_INTERNAL.R')][0]
        f = open(internal,'wb')
        f.write(z.read(internal))
        f.close()
        f = open(PANGEA_trans_net_script,'w')
        f.write("library(PANGEA.HIV.sim)\n")
        f.write("load('" + internal + "')\n")
        f.write("trans <- df.trms[,c('IDTR','IDREC','TIME_TR')]\n")
        f.write("write.table(trans[order(trans$TIME_TR),], file='" + PANGEA_trans_file + "', append=FALSE, sep='\\t', row.names=FALSE, col.names=FALSE, quote=FALSE)")
        f.close()
        check_output([GC.Rscript_path,PANGEA_trans_net_script], stderr=open(devnull,'w'))
        GC.PANGEA_TRANSMISSION_NETWORK = [i.strip().split() for i in open(PANGEA_trans_file) if len(i.strip()) > 0]
        chdir(orig_dir)
        for archive in glob(PANGEA_path + '/*_SIMULATED_SEQ.zip'):
            break
        z = ZipFile(archive, 'r')
        fasta_files = [item for item in z.namelist() if item.endswith('.fa')]
        for fasta in fasta_files:
            ending = '_' + fasta.split('_')[-1].split('.')[0] + '.fasta'
            seqs = GC.parseFASTA(z.read(fasta).decode('ascii').splitlines())
            for seqID in seqs:
                f = open("error_free_files/sequence_data/seqs_" + seqID.split('|')[0] + ending, 'w')
                f.write('>' + seqID + '\n' + seqs[seqID] + '\n')
                f.close()
        for archive in glob(PANGEA_path + '/*_SIMULATED_TREE.zip'):
            break
        z = ZipFile(archive, 'r')
        trees = [item for item in z.namelist() if item.endswith('.newick')]
        for tree in trees:
            f = open("error_free_files/phylogenetic_trees/" + tree, 'wb')
            f.write(z.read(tree))
            f.close()
        return []