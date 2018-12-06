import os, sys, subprocess

#-------------------------------------------------------------------------------
def get_javah_path() :
    try :
        subprocess.check_output(['javah', '-version'], stderr=subprocess.STDOUT)
        return 'javah'
    except (OSError, subprocess.CalledProcessError) :
        jdk_home = os.environ.get('JAVA_HOME')
        if jdk_home is 'None' :
            return None
        javah_path = '{}{}bin{}javah'.format(jdk_home, os.path.sep, os.path.sep)
        try :
            subprocess.check_output([javah_path, '-version'], stderr=subprocess.STDOUT)
            return javah_path
        except (OSError, subprocess.CalledProcessError) :
            return None

#-------------------------------------------------------------------------------
def check() :
    javah_path = get_javah_path()
    if javah_path is None :
        return False
    return True
