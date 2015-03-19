package com.codedisaster.jnigen;

import com.badlogic.gdx.jnigen.NativeCodeGenerator;

public class JNICodeGenerator {

	public static void main(String[] arguments) {

		try {

			new NativeCodeGenerator().generate(
					arguments[0], // input folder
					arguments[1], // classes folder
					arguments[2], // output folder
					new String[] { "**/*.java" },
					null);

		} catch (Exception e) {
			e.printStackTrace();
			System.exit(-1);
		}

	}

}
