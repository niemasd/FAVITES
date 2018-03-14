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
from gzip import open as gopen
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
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def get_edge_list():
        args = []
        for arg in PANGEA_ARGS:
            val = getattr(GC,arg)
            if isinstance(val,str):
                val = val.strip()
                if len(val) == 0 and arg.split('_')[1].strip() == 'seed': # if no seed given, randomly generate
                    from random import randint
                    val = str(randint(0,32767))
                if len(val) != 0:
                    args.append("%s='%s'" % (arg.split('_')[1],val))
            else:
                args.append("%s=%s" % (arg.split('_')[1],val))
        orig_dir = getcwd()
        makedirs(PANGEA_path, exist_ok=True)
        chdir(PANGEA_path)
        f = open(PANGEA_command_script,'w')
        f.write("library(PANGEA.HIV.sim)\n")
        f.write("outdir <- getwd()\n")
        f.write("pipeline.args <- sim.regional.args(")
        if GC.random_number_seed is not None:
            f.write("seed=%d,"%GC.random_number_seed)
            GC.random_number_seed += 1
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
        f.write('#!/usr/bin/env bash\n%s' % script_str)
        f.close()
        check_output(['./%s' % script], stderr=open('%s_output.log' % script,'w'))
        archive = None
        for archive in glob('*_INTERNAL.zip'):
            break
        assert archive is not None, "PANGEA failed to run successfully"
        z = ZipFile(archive, 'r')
        internal = [item for item in z.namelist() if item.endswith('_SIMULATED_INTERNAL.R')][0]
        f = open(internal,'wb')
        f.write(z.read(internal))
        f.close()
        f = open(PANGEA_trans_net_script,'w')
        f.write("library(PANGEA.HIV.sim)\n")
        f.write("load('%s')\n" % internal)
        f.write("trans <- df.trms[,c('IDTR','IDREC','TIME_TR')]\n")
        f.write("write.table(trans[order(trans$TIME_TR),], file='%s', append=FALSE, sep='\\t', row.names=FALSE, col.names=FALSE, quote=FALSE)" % PANGEA_trans_file)
        f.close()
        check_output([GC.Rscript_path,PANGEA_trans_net_script], stderr=open(devnull,'w'))
        GC.PANGEA_TRANSMISSION_NETWORK = [i.strip().split() for i in open(PANGEA_trans_file) if len(i.strip()) > 0]
        chdir(orig_dir)
        for archive in glob('%s/*_SIMULATED_SEQ.zip' % PANGEA_path):
            break
        z = ZipFile(archive, 'r')
        fasta_files = [item for item in z.namelist() if item.endswith('.fa')]
        f = gopen("error_free_files/sequence_data.fasta.gz",'wb',9)
        for fasta in fasta_files:
            ending = '_%s.fasta' % fasta.split('_')[-1].split('.')[0]
            seqs = GC.parseFASTA(z.read(fasta).decode('ascii').splitlines())
            for seqID in seqs:
                f.write(('>%s\n%s\n' % (seqID,seqs[seqID])).encode())
        f.write(b'\n'); f.close()
        archive = None
        for archive in glob('%s/*_SIMULATED_TREE.zip' % PANGEA_path):
            break
        assert archive is not None, "PANGEA failed to run successfully"
        z = ZipFile(archive, 'r')
        trees = [item for item in z.namelist() if item.endswith('.newick')]
        for tree in trees:
            f = gopen("error_free_files/phylogenetic_trees/%s.gz" % tree,'wb',9)
            to_write = z.read(tree)
            if isinstance(to_write, bytes):
                f.write(to_write)
            else:
                f.write(to_write.encode())
            f.write(b'\n'); f.close()
        return []
