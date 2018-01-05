from PyOrgMode import OrgDataStructure, OrgNode, OrgKeyword, OrgSrcBlock

base = OrgDataStructure()

synopsis = OrgNode.Element()
synopsis.heading = "Synopsis"
synopsis.level = 1
base.root.append_clean(synopsis)

todo = OrgNode.Element()
todo.heading = "Describe the campaign"
todo.level = 2
todo.todo = "TODO"
synopsis.append_clean(todo)

# Add support for links

internals = OrgNode.Element()
internals.heading = "Internal Parameters and Exclusions"
internals.level = 1
base.root.append_clean(internals)

todo1 = OrgNode.Element()
todo1.heading = "Add an internal parameter for the batch queue name"
todo1.level = 2
todo1.todo = "TODO"
internals.append_clean(todo1)

key = OrgKeyword.Element()
key.keyword = "NAME"
key.name = "campaign"
base.root.append_clean(key)

src = OrgSrcBlock.Element()
src.language = "shell"
src.parameters = ":exports code :results silent"
src.value = "cat exclude/CAMPAIGN"
base.root.append_clean(src)

key1 = OrgKeyword.Element()
key1.keyword = "NAME"
key1.name = "group"
base.root.append_clean(key1)

src1 = OrgSrcBlock.Element()
src1.language = "shell"
src1.parameters = ":exports code :results silent"
src1.value = "cat exclude/GROUP"
base.root.append_clean(src1)

key2 = OrgKeyword.Element()
key2.keyword = "NAME"
key2.name = "upcase-group"
base.root.append_clean(key2)

key3 = OrgKeyword.Element()
key3.keyword = "HEADERS"
key3.value = ":var g=group"
base.root.append_clean(key3)

src2 = OrgSrcBlock.Element()
src2.language = "emacs-lisp"
src2.parameters = ":exports none :results silent"
src2.value = "(upcase g)"
base.root.append_clean(src2)

build_n_run = OrgNode.Element()
build_n_run.heading = "Build and Run"
build_n_run.level = 1
base.root.append_clean(build_n_run)

key4 = OrgKeyword.Element()
key4.keyword = "HEADERS"
key4.value = ":var c=campaign"
base.root.append_clean(key4)

base.root.append_clean(key3)

key5 = OrgKeyword.Element()
key5.keyword = "HEADERS"
key5.value = ":var ug=upcase-group"
base.root.append_clean(key5)

src3 = OrgSrcBlock.Element()
src3.language = "shell"
src3.parameters = ":exports code :results silent"
src3.value = """
    module swap PrgEnv-pgi/5.2.82 PrgEnv-gnu
    module load adios/1.13.0
    module load python/3.5.1
    PROJ_HOME=$PROJWORK/$g/$USER/$c
    mkdir -p $PROJ_HOME
    CODAR=$PROJ_HOME/CODAR
    HEAT_XFER=$CODAR/Example-Heat_Transfer
    mkdir -p $HEAT_XFER
    git clone https://github.com/CODARcode/Example-Heat_Transfer.git $HEAT_XFER
    cd $HEAT_XFER
    make adios2
    cd -
    CHEETAH_HOME=$CODAR/cheetah
    git clone https://github.com/CODARcode/cheetah.git $CHEETAH_HOME
    cp ./heat_transfer_simple.py $CHEETAH_HOME/examples
    sed -i -e "s/CSCNNN/$ug/" $CHEETAH_HOME/examples/heat_transfer_simple.py
    cd $CHEETAH_HOME
    OUTPUT_DIR=$PROJ_HOME/campaign_out
    ./cheetah.py -e examples/heat_transfer_simple.py \
       -m titan -a "$HEAT_XFER/" -o $OUTPUT_DIR
    cd $OUTPUT_DIR && ./run-all.sh
"""
base.root.append_clean(src3)

env = OrgNode.Element()
env.heading = "The Environment"
env.level = 1

emacs = OrgNode.Element()
emacs.heading = "Emacs Version"
emacs.level = 2
env.append_clean(emacs)

src4 = OrgSrcBlock.Element()
src4.language = "emacs-lisp"
src4.parameters = ":exports both"
src4.value = "emacs-version"
env.append_clean(src4)

org = OrgNode.Element()
org.heading = "Org Version"
org.level = 2
env.append_clean(org)

src5 = OrgSrcBlock.Element()
src5.language = "emacs-lisp"
src5.parameters = ":exports both"
src5.value = "org-version"
env.append_clean(src5)

system = OrgNode.Element()
system.heading = "System Info"
system.level = 2
env.append_clean(system)

src6 = OrgSrcBlock.Element()
src6.language = "shell"
src6.parameters = ":exports both"
src6.value = "uname -a"
env.append_clean(src6)

codar = OrgNode.Element()
codar.heading = "Codar Application Hash"
codar.level = 2
env.append_clean(codar)

key6 = OrgKeyword.Element()
key6.keyword = "NAME"
key6.name = "heat-xfer-hash"
env.append_clean(key6)
env.append_clean(key4)
env.append_clean(key3)

src7 = OrgSrcBlock.Element()
src7.language = "shell"
src7.parameters = ":exports results :results output"
src7.value = """
    SRC_DIR=$PROJWORK/$g/$USER/$c/CODAR/Example-Heat_Transfer
    git -C $SRC_DIR rev-parse --short HEAD
"""
env.append_clean(src7)

cheetah = OrgNode.Element()
cheetah.heading = "Cheetah Application Hash"
cheetah.level = 2
env.append_clean(cheetah)

key7 = OrgKeyword.Element()
key7.keyword = "NAME"
key7.name = "cheetah-hash"
env.append_clean(key7)
env.append_clean(key4)
env.append_clean(key3)

src8 = OrgSrcBlock.Element()
src8.language = "shell"
src8.parameters = ":exports results :results output"
src8.value = """
    SRC_DIR=$PROJWORK/$g/$USER/$c/CODAR/cheetah
    git -C $SRC_DIR rev-parse --short HEAD
"""
env.append_clean(src8)

base.root.append_clean(env)

findings = OrgNode.Element()
findings.heading = "Key Findings"
findings.level = 1

size = OrgNode.Element()
size.heading = "Size of =heat.bp="
size.level = 2
findings.append_clean(size)

findings.append_clean(key4)
findings.append_clean(key3)
src9 = OrgSrcBlock.Element()
src9.language = "shell"
src9.parameters = ":exports both :results output"
src9.value = """
  PROJ_HOME=$PROJWORK/$g/$USER/$c/campaign_out
  stat -c %s "$PROJ_HOME/small_scale/run-000/heat.bp"
"""
findings.append_clean(src9)

summary = OrgNode.Element()
summary.heading = "Summary from =bpls="
summary.level = 2
findings.append_clean(summary)

findings.append_clean(key4)
findings.append_clean(key3)
src10 = OrgSrcBlock.Element()
src10.language = "shell"
src10.parameters = ":exports both :results output"
src10.value = """
  module swap PrgEnv-pgi/5.2.82 PrgEnv-gnu
  module load adios/1.13.0
  PROJ_HOME=$PROJWORK/$g/$USER/$c/campaign_out
  bpls -al $PROJ_HOME/small_scale/run-000/heat.bp | grep -v timer | sort
"""
findings.append_clean(src10)

base.root.append_clean(findings)


base.save_to_file("example2.org")
