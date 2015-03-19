# fips-jni

A small **fips** library to streamline the use of **jnigen** to generate and compile JNI code.

fips build system: https://github.com/floooh/fips

jnigen: https://github.com/libgdx/libgdx/wiki/jnigen

## Setup

In addition to the fips requirements, Maven and javah must be available in the path or through their respective environment variables (```${M2_HOME}```, ```${JAVA_HOME}```).

To check for the required dependencies:

```
./fips jni diag
```

To setup the code generator (uses Maven to compile a small Java application which calls the the jnigen code generator):

```
./fips jni setup
```

## How to use

To learn about how to inline C++ code inside your Java classes, please read the [jnigen documentation](https://github.com/libgdx/libgdx/wiki/jnigen).

A small example:

```
/*JNI
	#include "Remotery.h"
*/

private static native void rtmSetCurrentThreadName(long pointer); /*
	rmt_SetCurrentThreadName((const char*) pointer);
*/
```

To add JNI code generation to a fips module, simply add something like this to your CMakeLists.txt:

```
# searches and adds jni.h and jni_md.h to the include path
fips_setup_jni()

# the JNI code generator reads the configuration from Remotery.yml, calls
# jnigen, then writes #includes of all source files listed to Remotery.cc 
fips_generate(FROM Remotery.yml TYPE JNICodeGenerator SOURCE Remotery.cc)
```

An example configuration YAML looks like this:

```
source-path  : "../../remotery-bindings/src/main/java"
class-path   : "../../remotery-bindings/target/classes"

source-files :
    - com.codedisaster.remotery.Remotery
```

Paths are relative to the directory where this configuration is located. 'source-files' is a list of fully qualified Java class names.

That's it! During ```./fips build``` the *jnigen code generator* will be invoked. All source files listed in the config will be included into the .cc file created by the *fips JNICodeGenerator* script.