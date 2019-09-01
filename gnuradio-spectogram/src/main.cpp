// #include <gnuradio/blocks/file_source.h>

#include <gnuradio/constants.h>

#include <string>
#include <iostream>  

using namespace std;

int main(int argc, char const *argv[])
{
    string v = gr::version();
    cout << "Starting gnuradio-spectogram with gnuradio version: " << v << endl;

    string file;
    if (argc > 1) {
        file = argv[1];
        cout << "Reading from file: " << file << endl;
    } else {
        cout << "No filename provided. Exiting" << endl;
    }

    return 0;
}
