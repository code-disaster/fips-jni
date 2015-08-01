
import os

import yaml

from mod import log
from pycparser import c_parser, c_ast, parse_file

Version = 1
HeaderNote = '/* Machine generated by fips-jni (version {}). Do not edit! */\n\n'.format(Version)

#-------------------------------------------------------------------------------
def jni_type(type_name, is_ptr) :
	
	if is_ptr :
		if type_name == 'char' :
			return 'jstring'

	return '?'

#-------------------------------------------------------------------------------
def decl_type(decl, is_jni) :
	
	# pointer

	is_ptr = type(decl) == c_ast.PtrDecl

	if is_ptr :
		decl = decl.type

	result = ''

	if is_jni :
		return jni_type(decl.type.names[0], is_ptr)
	else :
		for qual in decl.quals :
			result += '{} '.format(qual)
		
		result += decl.type.names[0]

		if is_ptr :
			result += '*'

	return result

#-------------------------------------------------------------------------------
def parse_function_arguments(args, out, is_decl) :

	first_arg = not is_decl

	for arg in args :

		if not first_arg :
			out.write(', ')
		else :
			first_arg = False

		if is_decl :
			out.write('{} '.format(decl_type(arg.type, is_decl)))

		if is_decl :
			out.write(arg.name)
		else :
			out.write('_{}'.format(arg.name))

#-------------------------------------------------------------------------------
def marshal_function_arguments(args, out) :

	for arg in args :

		out.write('\tmarshal_{}({});\n'.format(decl_type(arg.type, True), arg.name))

#-------------------------------------------------------------------------------
def cleanup_function_arguments(args, out) :

	for arg in reversed(args) :

		out.write('\tcleanup_{}({});\n'.format(decl_type(arg.type, True), arg.name))

#-------------------------------------------------------------------------------
def parse_function_declaration(func_name, func_decl, src, hdr, class_prefix) :

	# return type

	return_type = func_decl.type.type.names[0]

	if return_type == 'void' :
		has_return_type = False
	else:
		has_return_type = True

	# write function implementation

	src.write('JNIEXPORT {} JNICALL Java_{}_{}(\n\t'.format(return_type, class_prefix, func_name))
	src.write('JNIEnv* env, jclass clazz')

	parse_function_arguments(func_decl.args.params, src, True)

	src.write(')\n{\n')

	marshal_function_arguments(func_decl.args.params, src)

	src.write('\t')

	if has_return_type :
		src.write('{} _result = '.format(return_type))

	src.write('{}('.format(func_name))

	parse_function_arguments(func_decl.args.params, src, False)

	src.write(');\n')

	cleanup_function_arguments(func_decl.args.params, src)

	if has_return_type :
		src.write('\treturn jni_return_{}(_result);\n'.format(return_type))

	src.write('}\n\n')

	# write function declaration

	hdr.write('JNIEXPORT {} JNICALL Java_{}_{}(\n\t'.format(return_type, class_prefix, func_name))
	hdr.write('JNIEnv* env, jclass clazz')

	parse_function_arguments(func_decl.args.params, hdr, True)

	hdr.write(');\n\n')

#-------------------------------------------------------------------------------
def generate_source(input_path, jni_class_name, header_file) :
	src = open(input_path + '/' + jni_class_name + '.cc', 'w')
	src.write(HeaderNote)
	src.write('#include \"{}.h\"\n\n'.format(jni_class_name))
	src.write('#include \"{}\"\n'.format(os.path.basename(header_file)))
	src.write('#include <jni_marshal.h>\n\n'.format(os.path.basename(header_file)))
	return src

#-------------------------------------------------------------------------------
def generate_header(input_path, jni_class_name, class_prefix) :
	hdr = open(input_path + '/' + jni_class_name + '.h', 'w')
	hdr.write(HeaderNote)
	hdr.write('#ifndef _{}_h\n'.format(class_prefix))
	hdr.write('#define _{}_h\n\n'.format(class_prefix))
	hdr.write('#include <jni.h>\n\n')
	hdr.write('#ifdef __cplusplus\nextern "C"\n{\n#endif\n\n')
	return hdr

#-------------------------------------------------------------------------------
def complete_header(hdr) :
	hdr.write('#ifdef __cplusplus\n}\n#endif\n\n#endif\n')

#-------------------------------------------------------------------------------
def generate(input, out_src, out_hdr) :

	input_path = os.path.dirname(input)

	with open(input, 'r') as f :
		desc = yaml.load(f)

	header_file = input_path + '/' + desc['header']
	jni_class_name = desc['class']
	jni_class_prefix = jni_class_name.replace('.', '_')

	print('header: {}'.format(header_file))
	print('class: {} ({})'.format(jni_class_name, jni_class_prefix))

	src = generate_source(input_path, jni_class_name, header_file)
	hdr = generate_header(input_path, jni_class_name, jni_class_prefix)

	ast = parse_file(header_file, use_cpp=True, cpp_path='cl', cpp_args=['/EP'])

	ast.show()

	for ext in ast.ext :
		decl_type = type(ext.type)

		if decl_type == c_ast.FuncDecl :
			parse_function_declaration(ext.name, ext.type, src, hdr, jni_class_prefix)

	complete_header(hdr)

	# write generator source file

	with open(out_src, 'w') as out :
		out.write(HeaderNote)
		out.write('#include "{}.cc"'.format(jni_class_name))