#include "hello-greet.hpp"
#include<string>
using namespace std;

int main(int argc, char **argv) {
    string in = "DefaultInput";
    if (argc > 1) {
        in = argv[1];
    }

    printHello(in);
    return 0;
}
