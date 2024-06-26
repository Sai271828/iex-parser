import os

def compile():
    """
    This function compiles the C++ code for the IEX parser.
    
    Parameters:
        None
    
    Returns:
        None
    """
    CPP_DIR = os.path.join(os.path.dirname(__file__), "cpp")
    BIN_DIR = os.path.join(os.path.dirname(__file__), "bin")

    # Compile iex_parser_threaded.cpp
    command1 = f"g++ -O2 {CPP_DIR}/logger.cpp {CPP_DIR}/decode_messages.cpp {CPP_DIR}/iex_parser_threaded.cpp -o {BIN_DIR}/iex_parser_threaded.out -pthread"
    os.system(command1)

    # Compile iex_parser_all_threaded.cpp
    command2 = f"g++ -O2 {CPP_DIR}/logger.cpp {CPP_DIR}/decode_messages.cpp {CPP_DIR}/iex_parser_all_threaded.cpp -o {BIN_DIR}/iex_parser_all_threaded.out -pthread"
    os.system(command2)

    # Compile iex_parser_split.cpp
    command3 = f"g++ -O2 {CPP_DIR}/logger.cpp {CPP_DIR}/decode_messages.cpp {CPP_DIR}/iex_parser_split.cpp -o {BIN_DIR}/iex_parser_split.out"
    os.system(command3)

    # Compile iex_parser.cpp
    command4 = f"g++ -O2 {CPP_DIR}/logger.cpp {CPP_DIR}/decode_messages.cpp {CPP_DIR}/iex_parser.cpp -o {BIN_DIR}/iex_parser.out"
    os.system(command4)


if __name__ == "__main__":
    compile()