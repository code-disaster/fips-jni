#-------------------------------------------------------------------------------
#   fips_setup_jni()
#
#   Helper macro to find and add the JNI headers (jni.h, jni_md.h) to the
#   include path. Requires a JDK to be installed on the host system.
#
macro(fips_setup_jni)
    
    find_package(JNI)
    
    if (NOT JNI_FOUND)
        message (FATAL_ERROR "Unable to locate JNI headers")
    endif()

    fips_include_directories(${JAVA_INCLUDE_PATH} ${JAVA_INCLUDE_PATH2})

endmacro()
