#ifndef _jni_marshal_h
#define _jni_marshal_h

// jlong

#define marshal_jlong(name) \
	int64_t _##name = name

#define cleanup_jlong(name)

// jstring

#define marshal_jstring(name) \
	char* _##name = (char*) env->GetStringUTFChars(name, 0)

#define cleanup_jstring(name) \
	env->ReleaseStringUTFChars(name, _##name)

// return values

#define return_jlong(result) \
	(jlong) (result)

#endif
