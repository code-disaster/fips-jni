import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/mod')

import subprocess
from mod import log, util
from tools import javah, maven

#-------------------------------------------------------------------------------
def jni_generator_path() :
    self_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = '{}{}fips-generators'.format(self_path, os.path.sep)
    return path

#-------------------------------------------------------------------------------
def compile_jni_generator() :
    return maven.run(['-f', '{}{}pom.xml'.format(jni_generator_path(), os.path.sep), 'package'])

#-------------------------------------------------------------------------------
def run(fips_dir, proj_dir, args) :

    noun = 'none'
    ok = False
    if len(args) > 0 :
        noun = args[0]
    if noun in ['diag'] :
        if maven.check() :
            log.ok('maven', 'found')
        else :
            log.failed('maven', 'NOT FOUND (M2_HOME environment variable must be set)')
        if javah.check() :
            log.ok('javah', 'found')
        else :
            log.failed('javah', 'NOT FOUND (JAVA_HOME environment variable must be set, and point to a JDK)')
        ok = True
    if noun in ['setup'] :
        if not compile_jni_generator() :
            log.failed('maven', 'COMPILE OF JNI CODE GENERATOR FAILED')
        ok = True
    if not ok :
        log.error("invalid noun '{}'".format(noun))

#-------------------------------------------------------------------------------
def help() :
    log.info(log.YELLOW + "fips jni diag\n" + log.DEF +
             "    run diagnostics and check for errors\n" +
             log.YELLOW + "fips jni setup\n" + log.DEF +
             "    fetches Java dependencies and compiles the code generator")