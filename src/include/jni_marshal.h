#ifndef _jni_marshal_h
#define _jni_marshal_h

#define marshal_jstring(name) \
	char* _##name = (char*) env->GetStringUTFChars(name, 0)

#define cleanup_jstring(name) \
	env->ReleaseStringUTFChars(name, _##name)

#define return_jlong(result) \
	(jlong) (result)

#endif
