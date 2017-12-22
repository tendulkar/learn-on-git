package com.yugandhar.learn.git.buildtools.javabazel.stage1.cmdline;

import com.yugandhar.learn.git.buildtools.javabazel.stage1.Greeter;

public class CMDRunner {

    public static void main(String [] args) {
        Greeter greeter = new Greeter();
        System.out.println("This is CMD Runner to show case multiple projects capability of Java bazel");
        greeter.greet();
    }
}

