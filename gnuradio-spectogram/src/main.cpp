// #include <gnuradio/blocks/file_source.h>

#include <gnuradio/constants.h>

#include <string>
#include <iostream>  

#include <gnuradio/top_block.h>
#include <gnuradio/blocks/file_source.h>

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

    // Create the top block of the flowgraph
    gr::top_block_sptr topBlock = gr::make_top_block("default");

    gr::blocks::file_source::sptr fileSource = gr::blocks::file_source::make(sizeof(float), file);

    topBlock->connect(fileSource);

    topBlock->run();

    return 0;
}
