import os, sys, subprocess

#-------------------------------------------------------------------------------
def get_mvn_path() :
    try :
        subprocess.check_output(['mvn', '--version'], stderr=subprocess.STDOUT)
        return 'mvn'
    except (OSError, subprocess.CalledProcessError) :
        m2_home = os.environ.get('M2_HOME')
        if m2_home is 'None' :
            return None
        m2_path = '{}{}bin{}mvn'.format(m2_home, os.path.sep, os.path.sep)
        if sys.platform.startswith('win') :
            if os.path.exists(m2_path + '.cmd') :
                m2_path += '.cmd'
            else :
                m2_path += '.bat'
        return m2_path

#-------------------------------------------------------------------------------
def run(args) :
    try :
        mvn_path = get_mvn_path()
        if mvn_path is None :
            return False
        subprocess.check_call([mvn_path] + args, stderr=subprocess.STDOUT)
        return True
    except (OSError, subprocess.CalledProcessError) :
        return False

#-------------------------------------------------------------------------------
def check() :
    try :
        mvn_path = get_mvn_path()
        if mvn_path is None :
            return False
        subprocess.check_output([mvn_path, '--version'], stderr=subprocess.STDOUT)
        return True
    except (OSError, subprocess.CalledProcessError) :
        return False
