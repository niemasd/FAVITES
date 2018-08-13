#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module using the PangeaSim tool to model small-village
HIV epidemics.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from glob import glob
from gzip import open as gopen
from os import chdir,getcwd,makedirs,remove,rmdir
from os.path import expanduser
from subprocess import call,STDOUT

PANGEASIM_OUTPUT_DIR = "PangeaSim_output"

class ContactNetworkGenerator_PangeaSim(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.PangeaSim_Acute = expanduser(GC.PangeaSim_Acute.strip())
        assert GC.PangeaSim_Acute.split('/')[-1] in {'PangeaSim_HighAcute','PangeaSim_LowAcute'}, "PangeaSim_Acute must be either PangeaSim_HighAcute or PangeaSim_LowAcute"
        assert "EndCriteria_PangeaSim" in str(MF.modules['EndCriteria']), "Must use EndCriteria_PangeaSim module"
        assert "SeedSelection_PangeaSim" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PangeaSim module"
        assert "TransmissionNodeSample_PangeaSim" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PangeaSim module"
        assert "TransmissionTimeSample_PangeaSim" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PangeaSim module"

    def get_edge_list():
        orig_dir = getcwd()
        makedirs(PANGEASIM_OUTPUT_DIR, exist_ok=True)
        chdir(PANGEASIM_OUTPUT_DIR)
        outfile = open('log.txt','w')
        try:
            call([GC.PangeaSim_Acute], stderr=STDOUT, stdout=outfile); outfile.close()
        except:
            outfile.close(); raise RuntimeError("PangeaSim crashed. See %s/log.txt for information" % PANGEASIM_OUTPUT_DIR)
        cn_list = []; GC.transmission_file = []; infected_by_acute = set()
        for f in glob('*.csv'):
            if f.startswith('phylogenetic_individualdata'): # individual attributes
                for l in open(f):
                    if l.startswith('Id') or len(l.strip()) == 0: # header line
                        continue
                    p = l.strip().split(',')
                    cn_list.append('NODE\t%s\t%s' % (p[0],','.join(p[1:])))
                remove(f)
            elif f.startswith('phylogenetic_transmission'): # transmission network
                for l in open(f):
                    if l.startswith('IdInfector') or len(l.strip()) == 0: # header line
                        continue
                    u,v,t,acute_infector = l.strip().split(',')
                    if u == '-1': # seed infection
                        u = None
                    GC.transmission_file.append((u,v,float(t)))
                    if acute_infector.strip() == '1':
                        infected_by_acute.add(v)
                remove(f)
            elif f.startswith('Annual'):
                tmp = gopen('../PangeaSim_annual_survey.csv.gz','wb',9)
                tmp.write(open(f).read().encode())
                tmp.close()
                remove(f)
        assert len(cn_list) != 0 and len(GC.transmission_file) != 0, "PangeaSim error. See %s/log.txt for information" % PANGEASIM_OUTPUT_DIR
        for u,v,t in GC.transmission_file:
            if u is not None:
                cn_list.append('EDGE\t%s\t%s\t%s\td' % (u,v,{True:'AcuteInfector',False:'NonAcuteInfector'}[v in infected_by_acute]))
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write(b'# Attributes: Id,Sex,DoB,DoD,HIV_pos,RiskGp,t_diagnosed,cd4_diagnosis,cd4atfirstART,t_1stARTstart,t_1stVLsupp_start,t_1stVLsupp_stop\n')
        f.write('\n'.join(cn_list).encode()); f.write(b'\n')
        f.close()
        remove('log.txt')
        chdir(orig_dir)
        rmdir(PANGEASIM_OUTPUT_DIR)
        return cn_list