
# 1. convert the c file into tac. remove reassignmnet of varaibles
# 2. run script to inline the c file. 
# 3. run and_cloud generator to get the and tree.

# 4. generate the gadget defintion for the d order security.

# 5. get the area and latency of each gadget.
# 6. generate the dict for each gadget area latnecy and randomness

# 7. run mlrc and mrlc to get the optimisation gadget placement
# 8. replace the and operation with the gadgets

# 9. pass this file to maskedHLS

# import sys
# import os
# import glob # For finding directories

# # Get the directory of the current script (MTP_Tetris/)
# project_root = os.path.dirname(os.path.abspath(__file__))

# # Path to the MaskedHLS_LP/src/ directory
# masked_hls_src_dir = os.path.join(project_root, 'MaskedHLS_LP', 'src')

# # 1. Add the MaskedHLS_LP/src/ directory itself to sys.path
# # This allows your script.py to do imports like:
# # from Inliner.Visitors import ...
# # from TACGenerator.TAC import ...
# if masked_hls_src_dir not in sys.path:
#     sys.path.insert(0, masked_hls_src_dir)
#     print(f"Added to sys.path: {masked_hls_src_dir}") # For debugging

# # 2. Add all immediate subdirectories of MaskedHLS_LP/src/ to sys.path
# # This helps resolve absolute imports of sibling modules within those subdirectories.
# # For example, if Inliner/Visitors.py does 'from DiGraph import DiGraph'
# # and DiGraph.py is also in Inliner/, this will help.

# if os.path.isdir(masked_hls_src_dir):
#     # List all entries in masked_hls_src_dir
#     for entry_name in os.listdir(masked_hls_src_dir):
#         potential_subdir_path = os.path.join(masked_hls_src_dir, entry_name)
#         # Check if it's a directory and not a hidden directory (like .git, __pycache__)
#         if os.path.isdir(potential_subdir_path) and not entry_name.startswith('.') and not entry_name == '__pycache__':
#             if potential_subdir_path not in sys.path:
#                 sys.path.insert(0, potential_subdir_path)
#                 print(f"Added to sys.path: {potential_subdir_path}") # For debugging
# else:
#     print(f"Warning: Directory not found - {masked_hls_src_dir}", file=sys.stderr)

# # 3. Add specific deeper paths known to cause issues
# # For the current error: MaskedHLS_LP/src/RegBalancer/src/
# regbalancer_specific_path = os.path.join(masked_hls_src_dir, 'RegBalancer', 'src')
# if os.path.isdir(regbalancer_specific_path): # Check if it actually exists
#     paths_to_add.append(regbalancer_specific_path)
# else:
#     print(f"Warning: Specific RegBalancer path not found - {regbalancer_specific_path}", file=sys.stderr)

# # Add all collected paths to sys.path (prepending for priority)
# for path_to_add in reversed(paths_to_add): # Reversed to maintain insert(0) effective order
#     if path_to_add not in sys.path:
#         sys.path.insert(0, path_to_add)
#         print(f"Added to sys.path: {path_to_add}") # For debugging

import sys
import os
import glob # For finding directories

# Get the directory of the current script (MTP_Tetris/)
project_root = os.path.dirname(os.path.abspath(__file__))

# Path to the MaskedHLS_LP/src/ directory
masked_hls_src_dir = os.path.join(project_root, 'MaskedHLS_LP', 'src')

# --- Paths to add to sys.path ---
paths_to_add = []

# 1. Add the MaskedHLS_LP/src/ directory itself
paths_to_add.append(masked_hls_src_dir)

# 2. Add all immediate subdirectories of MaskedHLS_LP/src/
if os.path.isdir(masked_hls_src_dir):
    for entry_name in os.listdir(masked_hls_src_dir):
        potential_subdir_path = os.path.join(masked_hls_src_dir, entry_name)
        if os.path.isdir(potential_subdir_path) and not entry_name.startswith('.') and not entry_name == '__pycache__':
            paths_to_add.append(potential_subdir_path)
else:
    print(f"Warning: Directory not found - {masked_hls_src_dir}", file=sys.stderr)

# 3. Add specific deeper paths known to cause issues
# For the current error: MaskedHLS_LP/src/RegBalancer/src/
regbalancer_specific_path = os.path.join(masked_hls_src_dir, 'RegBalancer', 'src')
if os.path.isdir(regbalancer_specific_path): # Check if it actually exists
    paths_to_add.append(regbalancer_specific_path)
else:
    print(f"Warning: Specific RegBalancer path not found - {regbalancer_specific_path}", file=sys.stderr)

# Add all collected paths to sys.path (prepending for priority)
for path_to_add in reversed(paths_to_add): # Reversed to maintain insert(0) effective order
    if path_to_add not in sys.path:
        sys.path.insert(0, path_to_add)
        # print(f"Added to sys.path: {path_to_add}") # For debugging


from pycparser import parse_file, c_ast, c_generator
from TACGenerator.TAC import TACStyleASTBuilder
from ANDCloud.and_cloud import AndCloudGenerator
from PIL import Image
from IPython.display import display
import subprocess
import json

from Gadgets import Gadget, HPC2, HPC1, HPC3, COMAR, Domand

# 1. Convert the file into TAC
def convert_to_TAC(CFile_path):
    """
    Parses C code and writes corresponding TAC.
    """
    print(f"[INFO] : Transforming input file to TAC ...")
    
    ast = parse_file(CFile_path, use_cpp=True)

    tac_gen = TACStyleASTBuilder()
    for i, ext in enumerate(ast.ext):
        if isinstance(ext, c_ast.FuncDef):
            ast.ext[i] = tac_gen.transform(ext)

    gen = c_generator.CGenerator()

    # output_path = r"./TestFiles/TAC_files"
    # output_path = os.path.join(output_path, "output.c")
    output_path = os.path.abspath(r"./TestFiles/TAC_files/output.c")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        code = gen.visit(ast)
        f.write(code)

    print(f"[INFO] : TAC output written to {output_path}\n")

# # 2. Inline C-file
def run_inliner(input_file, top_module, script_path="./MaskedHLS_LP/src"):

    """
    Writes systemArgs.json and runs the inliner script.
    
    Parameters:
    - input_file: path to the input C file
    - top_module: the top-level function to inline
    - script_path: the Python script that runs mainInline (default: 'inliner.py')
    """
    script_abs_path = os.path.abspath(script_path)
    # script_dir = os.path.dirname(script_abs_path) # 
    
    
    print(f"[INFO] : Inlining the TAC file ...")
    args = {
        "inputFile": input_file,
        "inlinerOutput": os.path.abspath(r".\TestFiles\inlined_output\output.c"),
        "topModule": top_module
    }

    # Write systemArgs.json
    with open(r".\MaskedHLS_LP\src\systemArgs.json", "w") as f:
        json.dump(args, f, indent=4)

    print(f"[INFO] : systemArgs.json written:")
    print(json.dumps(args, indent=4))
    print()

    # Run the inliner script
    print(f"[INFO] : Subprocess CWD will be: {script_abs_path}")
    try:
        result = subprocess.run(
            ["python", r"./Inliner/inliner.py"],
            check=True,
            # capture_output=True,
            text=True,
            cwd=script_abs_path
        )
        print(f"[INFO] : Inlined file written to {os.path.abspath(r".\TestFiles\inlined_output\output.c")}\n")
        # print("[INFO] Inliner Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("[ERROR] Inliner script failed:\n", e.stderr)

def run_maskedHLS(top_module, input_file, rtl_file, bit_width,script_path="./MaskedHLS_LP/src/script.py"):
    """
        @param top_module: top function of the file 
        @param input_file: input_file is the for which verilog need to be generated
        @param rltFile: name of the file where verilog need to be saved
        @param bit_width: sepicfy the bit width of the design 
    """
    script_abs_path = os.path.abspath(script_path)
    # resolve script path to absolute path
    script_dir = os.path.dirname(script_abs_path)
    # print(f"script path : {script_dir}")

    # input_file_abs = os.path.abspath(input_file)
    # print(f"input_file :{input_file}")


    rtl_file_abs = os.path.abspath(f"./Gadgets/gadget_verilog/{rtl_file}")
    # print(f"rtl_file : {rtl_file_abs}")

    command =[
        "python",
        "script.py",
        f"--topModule={top_module}",
        f"--inputFile={input_file}",
        f"--rtlFile={rtl_file_abs}",
        f"--bitWidth={bit_width}"
    ]

    # print("[INFO] : Running Commnad: ", " ".join(command))
    # print(f"[INFO] : Suprocess CWD will be : {script_dir}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=script_dir)
        print("[INFO] Script output:\n", result.stdout)

        # extracting the latency of the design 
        import re
        match = re.search(r"Max path weight\s*(\d+)", result.stdout)
        if match:
            latency = int(match.group(1))
            # print(f"[INFO] : Latency of the design: {latency}")
            
        else:
            print("[WARNING] : Latency not found in script output.")


    except subprocess.CalledProcessError as e:
        print("[ERROR] : Script failed:\n", e.stderr)
        print("[ERROR] : stdout (if any):\n", e.stdout) # Print stdout too, it might have clues
    except FileNotFoundError:
        print(f"[ERROR] : Python interpreter or script '{script_abs_path}' not found. Check paths.")

    return latency if latency else None
# 3. generate and_tree 
def generator_and_cloud(filename):
    print(f"[INFO] : Generating the AND tree ...")
    and_cloud = AndCloudGenerator()
    ast = parse_file(filename, use_cpp=True)
    and_cloud.visit(ast)
    # and_cloud.print_data()

    print(f"[INFO] : Number of node in the tree :{and_cloud.graph.num_nodes()}")
    and_cloud.save_and_tree(filename=filename)

    # Load and display image
    # output_folder = r".\ANDCloud\AND_tree"
    # sys.path.append(output_folder)
            
    # image_path = os.path.join(output_folder, f"and_cloud.png")
    # image = Image.open(image_path)  # Change to your image path
    # display(image)
    return and_cloud
# 4. generate the gadget definition for nth order security 

# 5. run mlrc & mrlc to get the optimal gadget placement 
import time
from DSE_algorithm.dse import DSE
from DSE_algorithm.mrlc import MRLC
from DSE_algorithm.mlrc import MLRC

def run_mrlc_test(latency_target, d, and_cloud):
    run_mrlc = MRLC(d=d, and_tree=and_cloud)
    
    start_time = time.perf_counter()
    run_mrlc.mrlc_algo(latency_target)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    gadget_mapping = run_mrlc.get_gadget_definition()
# 
    run_mrlc.print_gadget_definition()
    print(run_mrlc.get_unique_gadgets_definition())

    print(f"[INFO] : MRLC FINISH PROCESSING in {execution_time}s.")
    
    return run_mrlc.get_unique_gadgets_definition(), gadget_mapping



# 6. replace the AND operation with gadget definition and save it into the file 
# 7. pass this file into maskedHLS
# from DSE_algorithm.mrlc import MRLC

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TAC conversion and inliner.")
    parser.add_argument("--input_file", help="Path to input C file")
    parser.add_argument("--top_module", help="Top-level function name for inliner")
    parser.add_argument("--security_order",type=int,  help="Security order of the design")
    parser.add_argument("--latency", type=int, help="Maximum possible latency of the design")
    parser.add_argument("--randomness", type=int, help="Maximum possible randomness of the design")

    args = parser.parse_args()

    convert_to_TAC(args.input_file)
    file = os.path.abspath(r"./TestFiles/TAC_files/output.c")

    
    # # inline the tac 
    run_inliner(file, args.top_module)
    # print(f"[INFO] Inlining TAC file")
    # print(f"[IN]")

    # # use the inlined file to generate and cloud
    file = os.path.abspath(r"./TestFiles/inlined_output/output.c")

    # # get the and tree this will be use to find the optimal gadget placement 
    and_tree = generator_and_cloud(file)
    print()
    # # generate Gadget definition 
    # # if the table does not have entry for dth order
    print(f"[INFO] : Generating the Gadgets definition ...")
    
    # declare the DSE
    d = args.security_order

    # use sql lite for the table
    import sqlite3
    # create db if does not exist
    print(f"[INFO] : Connecting Database ... ")
    conn = sqlite3.connect('gadget_info.db')
    conn.execute("PRAGMA forgien_keys = ON")

    # cursor to query the database
    cur = conn.cursor()

    """
        gadget
        +----------------+
        | security order |
        +----------------+

        HPC1
        +--+---------+-----------+------+
        |d | latency | randomness| area |
        +--+---------+-----------+------+

        HPC2
        +--+---------+-----------+------+
        |d | latency | randomness| area |
        +--+---------+-----------+------+

        HPC3
        +--+---------+-----------+------+
        |d | latency | randomness| area |
        +--+---------+-----------+------+

        Comar
        +--+---------+-----------+------+
        |d | latency | randomness| area |
        +--+---------+-----------+------+
        
    """
    # create central gadget tabel
    cur.execute('''
        CREATE TABLE IF NOT EXISTS gadget(
            d INTEGER PRIMARY KEY
                )
    ''')
    for table in ["hpc1", "hpc2", "hpc3", "comar", "domand"]:
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table}(
                d INTEGER PRIMARY KEY,
                latency INTEGER,
                randomness INTEGER,
                area INTEGER,
                FOREIGN KEY (d) REFERENCES gadget(d) ON DELETE CASCADE
            )
        ''')

    # cur.execute(f"DELETE FROM gadget WHERE d = ?",(1,))
    # cur.execute(f"SELECT * FROM gadget WHERE d = ?", (1,))
    # if cur.fetchone() is None:
        
    #     cur.execute("INSERT INTO gadget (d) VALUES (?)", (1,))
        
    #     cur.execute("INSERT INTO hpc1 (d, latency, randomness, area) VALUES (?, ?, ?, ?)", (1, 2, 2, 1))

    #     cur.execute("INSERT INTO hpc2 (d, latency, randomness, area) VALUES (?, ?, ?, ?)",(1, 2, 1, 2))

    #     cur.execute("INSERT INTO hpc3 (d, latency, randomness, area) VALUES (?, ?, ?, ?)",(1, 1, 2, 3))

    #     cur.execute("INSERT INTO comar (d, latency, randomness, area) VALUES (?, ?, ?, ?)",(1, 2, 6, 4))

    cur.execute(f"SELECT * FROM gadget WHERE d = {d}")
    row = cur.fetchone()


    # check the contents of the tabkes in the database
    print("[INFO] : Gadget Table Contents:")

    tables = ["gadget", "hpc1", "hpc2", "hpc3", "comar", "domand"]
    
    # for d in [1, 2, 3]:
    #     cur.execute(f"INSERT OR IGNORE INTO gadget (d) VALUES (?)", (d,))
    
    # data = {
    #     'hpc1' : [(1,2,2,),(2,2,5),(3,2,9)],
    #     'hpc2' :[(1,2,1,),(2,2,3),(3,2,6)],
    #     'hpc3' : [(1,1,2,),(2,1,6),(3,1,12)],
    #     'comar' : [(1,2,6,)],
    #     'domand' : [(1,2,1,),(2,1,3),(3,1,6)],
    # }

    # for table, entries in data.items():
    #     for entry in entries:
    #         cur.execute(f"INSERT OR IGNORE INTO {table} (d, latency, randomness, area) VALUES (?, ?, ?, ?)", (entry[0], entry[1], entry[2], entry[3]))

    for table in tables:
        print(f"\nTable: {table}")
        # cur.execute(f"DELETE FROM {table}")
        cur.execute(f"SELECT * FROM {table}")

        column_names = [description[0] for description in cur.description]
        print(" | ".join(column_names))
        print("-" * 50)
        rows = cur.fetchall()
        for r in rows:
            print(r)
    conn.commit()
    conn.close()
    
    # if row is not none fetch the values form table
    # if row is none call the gadget definition and populate the row of table

 
    if row is None:
        print("[INFO] : Generating gadget definition..")
        
        # generate gadget definition 
        HPC2_obj = HPC2(d=d)
        HPC2_obj.generate_and_write_function(HPC2_obj, filename_prefix="HPC2")
        # create object of HPC2 and get randomness.
        randomness_HPC2 = HPC2_obj.get_random_count()
        print(f"[INFO] : Randomness of HPC2: {randomness_HPC2}")
        
        HPC1_obj = HPC1(d=d)
        HPC1_obj.generate_and_write_function(HPC1_obj, filename_prefix="HPC1")
        randomness_HPC1 = HPC1_obj.get_random_count()

        print(f"[INFO] : Randomness of HPC1: {randomness_HPC1}")
        HPC3_obj = HPC3(d=d)
        HPC3_obj.generate_and_write_function(HPC3_obj, filename_prefix="HPC3")
        randomness_HPC3 = HPC3_obj.get_random_count()
        print(f"[INFO] : Randomness of HPC3: {randomness_HPC3}")

        COMAR_obj = COMAR()
        COMAR_obj.generate_and_write_function(COMAR_obj, filename_prefix="Comar")
        randomness_COMAR = COMAR_obj.get_random_count()
        print(f"[INFO] : Randomness of COMAR: {randomness_COMAR}")
        
        Domand_obj = Domand(d=d)
        Domand_obj.generate_and_write_function(Domand_obj, filename_prefix="Domand")
        randomness_Domand = Domand_obj.get_random_count()
        print(f"[INFO] : Randomness of Domand: {randomness_Domand}")

        print(f"[INFO] : Gadget Definition written to {os.path.abspath(r".\Gadgets\gadget_output")}\n")
        # # pass the generated c files into the masked HLS to get verilog 
        folder_path = os.path.abspath(r"./Gadgets/gadget_output")

        for filename in os.listdir(folder_path):
            print()
            print(f"[INFO] : filename : {filename}")
            top_module = filename.replace("_generated.c","") 

            rtl_file = filename.replace(".c", ".v")
            filename= os.path.abspath(f"./Gadgets/gadget_output/{filename}")
            #print(f"filename {filename}")
            latnecy = run_maskedHLS(top_module=top_module,input_file=filename, rtl_file=rtl_file,bit_width=8)
            if latnecy is not None:
                print(f"[INFO] : Latency of the design: {latnecy}")
            # call design compiler to get the area and latency of the design
            # latnecy and rnadomness is already with us just need area
            
    
    
    # # populate the dse map 
    
    # param_map = {}
    # for gadget in ["COMAR", "HPC1", "HPC2", "HPC3"]:
    #     table = gadget.lower()
    #     cur.execute(f"SELECT * FROM {table} WHERE d = ?", (d,))
    #     row = cur.fetchone()
    #     if row:
    #         param_map[gadget] = {
    #             "latency": row[1],
    #             "randomness": row[2],
    #             "area": row[3]
    #         }
    #     else:
    #         print(f"[WARN] No entry for {gadget} with d = {d}")

    # DSE.set_param_map(param_map)
    # print(f"DSE.GADGET_PARAM_MAP :\n {DSE.GADGET_PARAM_MAP}")
    # conn.commit()


    # # create table ..

    
    # # pass these verilog file to design compiler 
    # # get the area latency 
    # # get the randomness 
    # # store these values into the table

    # if args.latency is None and args.randomness is None:
    #     parser.error("[ERROR] : At least one of --latency or --randomness must be provided.")
    # from transform_CFile.ctransfromer import ShareTransformer

    # if args.latency is not None:
    #     # run mrlc
    
    #     print("[INFO] : Running MRLC for optimal gadget placement.")
    #     unique_def, gadget_mapping = run_mrlc_test(latency_target=args.latency, d=d, and_cloud=and_tree)
    #     print("[INFO] : printing the unique definitions")
    #     # print(unique_def)
        
    #     inlined_file = r"./TestFiles/inlined_output/output.c"
    #     ast = parse_file(inlined_file, use_cpp=True)

    #     shareTransformer = ShareTransformer(d+1, gadget_mapping, unique_def)
    #     transformed_ast = shareTransformer.transform(ast)

    #     gen = c_generator.CGenerator()

    #     # output_path = r"./TestFiles/TAC_files"
    #     # output_path = os.path.join(output_path, "output.c")
    #     output_path = os.path.abspath(r"./TestFiles/share_output/output.c")
        
    #     os.makedirs(os.path.dirname(output_path), exist_ok=True)

    #     with open(output_path, 'w') as f:
    #         code = gen.visit(ast)
    #         f.write(code)

    #     print(f"[INFO] : shared output written to {output_path}\n")



    # else:
    #     print("[INFO] : Running MLRC for optimal gadget placement.")

    # # use the unique definition to replace the expression with gadget definition 
    # # run maskedHLS on the design




