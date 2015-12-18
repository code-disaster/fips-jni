package com.codedisaster.jnigen;

import com.badlogic.gdx.jnigen.NativeCodeGenerator;
import com.github.javaparser.ParseException;

import java.util.ArrayList;
import java.util.List;

public class JNICodeGenerator {

	public static void main(String[] arguments) {

		try {

			List<String> includes = new ArrayList<String>();
			List<String> excludes = new ArrayList<String>();

			int index = 3;
			while (index < arguments.length) {
				if (arguments[index].equalsIgnoreCase("--includes")) {
					++index;
					while (index < arguments.length) {
						if (arguments[index].startsWith("--")) {
							break;
						}
						includes.add(arguments[index]);
						++index;
					}
				} else if (arguments[index].equalsIgnoreCase("--excludes")) {
					++index;
					while (index < arguments.length) {
						if (arguments[index].startsWith("--")) {
							break;
						}
						excludes.add(arguments[index]);
						++index;
					}
				} else {
					++index;
				}
			}

			if (includes.isEmpty()) {
				includes.add("**/*.java");
			}

			String[] includesArray = new String[includes.size()];
			includes.toArray(includesArray);

			String[] excludesArray = null;
			if (!excludes.isEmpty()) {
				excludesArray = new String[excludes.size()];
				excludes.toArray(excludesArray);
			}

			new NativeCodeGenerator().generate(
					arguments[0], // input folder
					arguments[1], // classes folder
					arguments[2], // output folder
					includesArray,
					excludesArray);

		} catch (ParseException e) {
			System.err.println("japa.parser.ParseException: " + e.getMessage());
			System.exit(-1);
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(-1);
		}

	}

}
