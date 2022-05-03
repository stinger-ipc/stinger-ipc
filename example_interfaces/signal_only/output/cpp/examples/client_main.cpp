
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = DefaultConnection('localhost', 1883);
    auto client = SignalOnlyClient(conn);
    client.registerAnotherSignalCallback([](double one, bool two, const std::string& three) {
        std::cout << "one=" << one << " | " << "two=" << two << " | " << "three=" << three <<  std::endl;
    });

    pause();

    return 0;
}