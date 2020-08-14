import importlib
from pathlib import Path

CNS_DIRECTORY = '/home/rajroy/cns/cns_solve_1.3/'
MODEL_COUNT = 50

prog_dir = Path(__file__).parent.absolute()

pdb_libraries = importlib.util.spec_from_file_location("pdb_reader", str(prog_dir)+"/libs/pdb_reader.py")
pdb_config = importlib.util.module_from_spec(pdb_libraries)
pdb_libraries.loader.exec_module(pdb_config)

restrain_libraries = importlib.util.spec_from_file_location("restrain_file", str(prog_dir)+"/libs/restrain_file.py")
restrain_config = importlib.util.module_from_spec(restrain_libraries)
restrain_libraries.loader.exec_module(restrain_config)

util_libraries = importlib.util.spec_from_file_location("utils_file", str(prog_dir)+"/libs/utils.py")
util_config = importlib.util.module_from_spec(util_libraries)
util_libraries.loader.exec_module(util_config)

file_handler_libraries = importlib.util.spec_from_file_location("utils_file", str(prog_dir)+"/libs/file_handler.py")
file_handler_config = importlib.util.module_from_spec(file_handler_libraries)
file_handler_libraries.loader.exec_module(file_handler_config)