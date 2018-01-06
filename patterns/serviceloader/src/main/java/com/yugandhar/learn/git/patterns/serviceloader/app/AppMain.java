package com.yugandhar.learn.git.patterns.serviceloader.app;

import com.sun.tools.javac.util.ServiceLoader;
import com.yugandhar.learn.git.patterns.serviceloader.spi.IService;

/**
 * @author Yugandhar
 */
public class AppMain {
    public static void main(String[] args) {
        ServiceLoader<IService> serviceLoader = ServiceLoader.load(IService.class);
        for (IService service : serviceLoader) {
            service.show();
        }
    }
}
