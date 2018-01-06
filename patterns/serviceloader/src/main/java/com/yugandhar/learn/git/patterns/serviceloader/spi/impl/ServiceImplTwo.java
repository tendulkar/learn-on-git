package com.yugandhar.learn.git.patterns.serviceloader.spi.impl;

import com.yugandhar.learn.git.patterns.serviceloader.spi.IService;

/**
 * @author Yugandhar
 */
public class ServiceImplTwo implements IService {
    public void show() {
        System.out.println("ServiceImplTwo is used!");
    }
}
