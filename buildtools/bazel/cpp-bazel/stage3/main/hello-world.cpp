#include "main/hello-greet.hpp"
#include "lib/hello-time.hpp"
#include <string>

int main(int argc, char **argv) {
    string in = "DefaultInput";
    if (argc > 1) {
        in = argv[1];
    }
    
    printHello(in);
    printLocalTime();
}
