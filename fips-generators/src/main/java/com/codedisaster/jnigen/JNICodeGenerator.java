package com.codedisaster.jnigen;

import com.badlogic.gdx.jnigen.NativeCodeGenerator;
import java.util.Arrays;

public class JNICodeGenerator {

	public static void main(String[] arguments) {

		try {

			String[] excludes = null;
			if (arguments.length > 3) {
				excludes = Arrays.copyOfRange(arguments, 3, arguments.length);
			}

			new NativeCodeGenerator().generate(
					arguments[0], // input folder
					arguments[1], // classes folder
					arguments[2], // output folder
					new String[] { "**/*.java" },
					excludes);

		} catch (Exception e) {
			e.printStackTrace();
			System.exit(-1);
		}

	}

}
