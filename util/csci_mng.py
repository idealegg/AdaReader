import os
import re


class CsciMng:
    MAKEFILE = "Makefile"
    SUBDIRS = "SUBDIRS"
    SOURCES = "AMG_SOURCES"
    def __init__(self, root_path, csci=None, stop_dir=None):
        self.csci = csci
        self.root_path = root_path
        self.stop_dir = stop_dir
        self.specs = []
        self.check_vars = [CsciMng.SUBDIRS, CsciMng.SOURCES]
        self.stopped = False

    def get_makefile_vars(self, mk, vars):
        out = {}
        pattern = []
        try:
            with open(mk) as fd:
                for var in vars:
                    pattern.append("".join([r'(?:^\s*(\b', var, r'\b)\s*=)']))
                pattern = re.compile('|'.join(pattern))
                for line in fd:
                    res = re.search(pattern, line)
                    if res:
                        var = next(filter(lambda x:x, res.groups()))
                        out[var] = ""
                        val = line[len(res.group())+1:]
                        while val.endswith('\\\n'):
                            out[var] = ' '.join([out[var], val[:-2].strip()])
                            val = next(fd)
                        out[var] = ' '.join([out[var], val.strip()]).strip()
        except Exception as exc:
            #print(exc)
            out = {}
        return out

    def get_spce_list(self, check_dirs, depth=0):
        depth += 1
        #print('[%s][%s][%s]' % (depth, self.stopped, check_dirs))
        if not self.stopped:
            for dir in check_dirs:
                vars = self.get_makefile_vars(os.path.join(dir, CsciMng.MAKEFILE), self.check_vars)
                if CsciMng.SUBDIRS in vars and vars[CsciMng.SUBDIRS]:
                    dirs = re.split('\s+', vars[CsciMng.SUBDIRS])
                    dirs = list(map(lambda x: os.path.join(dir, x), dirs))
                    #print(dirs)
                    if self.stop_dir != dir:
                        for t_dir in dirs:
                            if self.stop_dir and self.stop_dir.startswith("".join([t_dir, os.path.sep])):
                                dirs = dirs[:dirs.index(t_dir)+1]
                                break
                        self.get_spce_list(dirs, depth)

                files = []
                if CsciMng.SOURCES in vars and vars[CsciMng.SOURCES]:
                    files = re.split('\s+', vars[CsciMng.SOURCES])
                else:
                    if os.path.isdir(dir):
                        files = os.listdir(dir)
                if files:
                    files = list(filter(
                        lambda x: (x.endswith('.a') or x.endswith('.ads')) and not x.endswith('_b.a'), files))
                    #print("[%s]%s" %(depth, files))
                    self.specs.extend(list(map(lambda x: os.path.join(dir, x), files)))

                #if self.stop_dir and self.stop_dir.startswith("".join([dir, os.path.sep])):
                #    self.stopped = True
                #    break

    def get_all_spec(self):
        self.get_spce_list([self.root_path])
        return self.specs


if __name__ == "__main__":
    #cn = CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\common', 'common', r'D:\sourceCode\1_eurocat\btma_ada\common\cdc\cdc')
    #cn = CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\kinematics\Ada', 'kinematics', r'D:\sourceCode\1_eurocat\btma_ada\kinematics\Ada')
    cn = CsciMng(r'D:\sourceCode\1_eurocat\btma_ada\ubss_src',  'ubss')
    #print(cn.get_makefile_vars(r'C:\works\btma_code\common\cdc\cdc\Makefile', ['SUBDIRS', 'AMG_SOURCES']))
    #print(cn.get_makefile_vars(r'C:\works\btma_code\common\cdc\Makefile', ['SUBDIRS', 'AMG_SOURCES']))
    #cn.get_spce_list([r'C:\works\btma_code\common'])
    cn.get_all_spec()
    print("\n".join(cn.specs))
