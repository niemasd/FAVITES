#! /usr/bin/env python3
'''
Niema Moshiri 2019

"ContactNetworkGenerator" module, where the epidemic is simulated using EpiModel
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser
from os import chdir,getcwd,makedirs
from subprocess import call
EPIDEMIC_TYPES = {'SI', 'SIS', 'SIR'}
EPIMODEL_OUTDIR = 'EpiModel_output'
EPIMODEL_R_SCRIPT = 'FAVITES_EPIMODEL_COMMAND.R'
EPIMODEL_OUTPUT_INDIVIDUALS = 'output_individuals.tsv'
EPIMODEL_OUTPUT_CONTACTS = 'output_contact_network.tsv'
EPIMODEL_OUTPUT_TRANSMISSIONS = 'output_transmission_network.tsv'
EPIMODEL_LOG_STDOUT = 'EpiModel_stdout.log'
EPIMODEL_LOG_STDERR = 'EpiModel_stderr.log'
EPIMODEL_R_SESSION_FILE = 'output_session.RData'

class ContactNetworkGenerator_EpiModel(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_EPIMODEL

    def init():
        assert "EndCriteria_EpiModel" in str(MF.modules['EndCriteria']), "Must use EndCriteria_EpiModel module"
        assert "SeedSelection_EpiModel" in str(MF.modules['SeedSelection']), "Must use SeedSelection_EpiModel module"
        assert "TransmissionNodeSample_EpiModel" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_EpiModel module"
        assert "TransmissionTimeSample_EpiModel" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_EpiModel module"
        assert isinstance(GC.Rscript_path, str), "Rscript_path must be a str"
        if isinstance(GC.epimodel_save_session, str):
            assert GC.epimodel_save_session.lower() in {'true','false'}, "GC.epimodel_save_session must be True or False"
            GC.epimodel_save_session = bool(GC.epimodel_save_session.capitalize())
        else:
            assert isinstance(GC.epimodel_save_session, bool), "GC.epimodel_save_session must be True or False"
        assert isinstance(GC.epimodel_type, str), "epimodel_type must be a str"
        GC.epimodel_type = GC.epimodel_type.strip()
        assert GC.epimodel_type in EPIDEMIC_TYPES, "Invalid epimodel_type: %s (valid options: %s)" % (GC.epimodel_type, ', '.join(sorted(EPIDEMIC_TYPES)))
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.epimodel_attributes, list), "epimodel_attributes must be a list of (name, num_categories) tuples"
        for e in GC.epimodel_attributes:
            assert isinstance(e, tuple) and len(e) == 2 and isinstance(e[0], str) and isinstance(e[1], int), "epimodel_attributes must be a list of (name, num_categories) tuples"
            assert e[1] > 0, "Encountered a non-positive number of categories in epimodel_attributes"
        GC.epimodel_nsteps = int(GC.epimodel_nsteps)
        assert GC.epimodel_nsteps > 0, "epimodel_nsteps must be a positive integer"
        GC.num_init_infected = int(GC.num_init_infected)
        assert GC.num_init_infected >= 1, "num_init_infected must be a positive integer"
        GC.num_init_recovered = int(GC.num_init_recovered)
        GC.recovery_rate = float(GC.recovery_rate)
        if GC.epimodel_type == 'SIR':
            assert GC.num_init_recovered >= 0, "num_init_recovered must be a non-negative integer when using the SIR model"
            assert GC.recovery_rate >= 0, "recovery_rate must be non-negative when using the SIR model"
        elif GC.num_init_recovered != 0:
            assert GC.num_init_recovered == 0, "num_init_recovered must be 0 when not using the SIR model"
            assert GC.recovery_rate == 0, "recovery_rate must be 0 when not using the SIR model"
        GC.transmission_probability = float(GC.transmission_probability)
        assert GC.transmission_probability >= 0, "transmission_probability must be non-negative"
        GC.act_rate = float(GC.act_rate)
        assert GC.act_rate >= 0, "act_rate must be non-negative"
        GC.average_edge_duration = float(GC.average_edge_duration)
        assert GC.average_edge_duration >= 0, "average_edge_duration must be non-negative"
        assert isinstance(GC.epimodel_formation_line, str), "epimodel_formation_line must be a str"
        GC.epimodel_formation_line = GC.epimodel_formation_line.strip()
        assert GC.epimodel_formation_line.replace(' ','').replace('\t','').startswith("formation<-"), "Invalid EpiModel 'formation' object line"
        GC.epimodel_target_stats_line = GC.epimodel_target_stats_line.strip()
        assert GC.epimodel_target_stats_line.replace(' ','').replace('\t','').startswith("target.stats<-"), "Invalid EpiModel 'target.stats' object line"

    def get_edge_list():
        # create folders/files to prep for running EpiModel
        orig_dir = getcwd()
        makedirs(EPIMODEL_OUTDIR, exist_ok=True)
        chdir(EPIMODEL_OUTDIR)
        f = open(EPIMODEL_R_SCRIPT,'w')
        f.write("### Load Packages ###\nlibrary('EpiModel')\nlibrary('ergm')\nlibrary('tergm')\n\n")
        f.write("### Estimate TERGM ###\n")
        f.write("# build empty network with attributes\n")
        f.write("sim.net <- network.initialize(n = %d, directed = FALSE)\n" % GC.num_cn_nodes)
        for attr_name,num_cats in GC.epimodel_attributes:
            f.write('sim.net <- set.vertex.attribute(sim.net, "%s", rep(0:%d, each = %d))\n' % (attr_name, num_cats-1, int(GC.num_cn_nodes/num_cats)))
        f.write("# specify how edges are added\n")
        f.write(GC.epimodel_formation_line.strip()); f.write('\n')
        f.write(GC.epimodel_target_stats_line.strip()); f.write('\n')
        f.write("# specify how edges are deleted\n")
        f.write("coef.diss <- EpiModel::dissolution_coefs(dissolution = ~offset(edges), duration = %f)\n" % GC.average_edge_duration)
        f.write("# estimate dynamic network parameters\n")
        f.write("dyn_net.est <- EpiModel::netest(sim.net, formation, target.stats, coef.diss, edapprox = TRUE)\n\n")
        f.write("### Simulate Epidemic ###\n")
        f.write("# specify epidemic characteristics\n")
        f.write("param <- EpiModel::param.net(inf.prob = %f, act.rate = %f" % (GC.transmission_probability, GC.act_rate))
        if GC.epimodel_type == 'SIR':
            f.write(", rec.rate = %f" % GC.recovery_rate)
        f.write(")\n")
        f.write("init <- EpiModel::init.net(i.num = %d" % GC.num_init_infected)
        if GC.epimodel_type == 'SIR':
            f.write(", r.num = %d" % GC.num_init_recovered)
        f.write(")\n")
        f.write('control <- EpiModel::control.net(type = "%s", nsteps = %d, nsims = 1)\n' % (GC.epimodel_type, GC.epimodel_nsteps))
        f.write("# run epidemic simulation\n")
        f.write("epi.sim <- EpiModel::netsim(dyn_net.est, param, init, control)\n\n")
        f.write("### Extract Information\n")
        f.write("dyn.net <- EpiModel::get_network(epi.sim, sim = 1)\n")
        f.write("write.table(data.frame(get.vertex.pid(dyn.net)")
        for attr_name,num_cats in GC.epimodel_attributes:
            f.write(', get.vertex.attribute(dyn.net,"%s")' % attr_name)
        f.write("), file = '%s', quote = FALSE, sep = '\\t', col.names = NA)\n" % EPIMODEL_OUTPUT_INDIVIDUALS)
        f.write("write.table(as.data.frame(dyn.net), file = '%s', quote = FALSE, sep = '\\t', col.names = NA)\n" % EPIMODEL_OUTPUT_CONTACTS)
        f.write("write.table(as.data.frame(EpiModel::get_transmat(epi.sim, sim = 1)), file = '%s', quote = FALSE, sep = '\\t', col.names = NA)\n" % EPIMODEL_OUTPUT_TRANSMISSIONS)
        if GC.epimodel_save_session:
            f.write("save.image('%s')" % EPIMODEL_R_SESSION_FILE)
        f.close()

        # run EpiModel and parse output
        f1 = open(EPIMODEL_LOG_STDOUT,'w'); f2 = open(EPIMODEL_LOG_STDERR,'w')
        call([GC.Rscript_path, EPIMODEL_R_SCRIPT], stdout=f1, stderr=f2); f1.close(); f2.close()
        people = [[v.strip() for v in l.strip().split('\t')] for l in open(EPIMODEL_OUTPUT_INDIVIDUALS) if l[0] != '\t']
        num_to_name = {p[0]:p[1] for p in people}

        # build contact network edge list
        lines = ["# Node Attributes: %s" % ','.join(e[0] for e in GC.epimodel_attributes), "# Edge Attributes: start,end"]
        for p in people:
            lines.append("NODE\t%s\t%s" % (p[1], ','.join(p[2:])))
        for l in open(EPIMODEL_OUTPUT_CONTACTS):
            if l[0] == '\t':
                continue
            s,e,u,v = [x.strip() for x in l.split('\t')[1:5]]
            lines.append("EDGE\t%s\t%s\t%s,%s\tu" % (num_to_name[u],num_to_name[v],s,e))

        # build transmission network list
        GC.transmission_file = list()
        for l in open(EPIMODEL_OUTPUT_TRANSMISSIONS):
            if l[0] == '\t':
                continue
            t,v,u = [x.strip() for x in l.split('\t')[1:4]]
            GC.transmission_file.append((u,v,float(t)))

        # find seed nodes
        seeds = list(); infected = set()
        for u,v,t in GC.transmission_file:
            if u not in infected:
                seeds.append(u); infected.add(u)
            infected.add(v)
        GC.transmission_file = [(None,u,0.) for u in seeds] + GC.transmission_file

        # clean up and return contact network edge list
        chdir(orig_dir)
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(lines).encode()); f.write(b'\n')
        f.close()
        return lines
