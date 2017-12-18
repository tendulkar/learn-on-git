package com.yugandhar.learn.git.benchmarks.javabench.core.methods.services;

/**
 * @author Yugandhar
 */
public class Coder1 implements Coder {
    @Override
    public int work(byte[] data) {
        return data.length;
    }
}
