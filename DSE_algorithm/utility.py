# test mlrc class
import os, sys, time
from pycparser import parse_file
from PIL import Image # type: ignore
from IPython.display import display # type: ignore
from ANDCloud import AndCloudGenerator
from mlrc import MLRC
from mrlc import MRLC
import json
import subprocess

def run_inliner(input_file, output_file, top_module, script_path="./MaskedHLS_LP/src/Inliner/inliner.py"):
    """
    Writes systemArgs.json and runs the inliner script.
    
    Parameters:
    - input_file: path to the input C file
    - output_file: path where inlined C code will be saved
    - top_module: the top-level function to inline
    - script_path: the Python script that runs mainInline (default: 'inliner.py')
    """
    args = {
        "inputFile": input_file,
        "inlinerOutput": output_file,
        "topModule": top_module
    }

    # Write systemArgs.json
    with open(".\mtp_tetris\MaskedHLS_LP\src\systemArgs.json.json", "w") as f:
        json.dump(args, f, indent=4)

    print(f"[INFO] systemArgs.json written:")
    print(json.dumps(args, indent=4))

    # Run the inliner script
    try:
        result = subprocess.run(
            ["python", script_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("[INFO] Inliner Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("[ERROR] Inliner script failed:\n", e.stderr)
  
def create_and_cloud(filename):
    input_C_dir = r".\mtp_tetris\TestFiles"
    # inlined output of the c file 
    sys.path.append(input_C_dir)
    input_C = os.path.join(input_C_dir, f"{filename}.c")
    # inlined c code file
    ast = parse_file(input_C, use_cpp = True)
    
    and_cloud = AndCloudGenerator()
    and_cloud.visit(ast)
    and_cloud.print_data()
    print(f"Number of node in the tree :{and_cloud.graph.num_nodes()}")
    and_cloud.save_and_tree(filename=filename)

    # create folder if does not exist 

    output_folder = r".\mtp_tetris\and_tree_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # system path append output folder 
    sys.path.append(output_folder)
    # save the and_could image 
    image_path = os.path.join(output_folder, f"and_cloud.png")
    # Load and display image
    image = Image.open(image_path)  # Change to your image path
    display(image)
    return and_cloud

def run_mrlc_test(latency_target, d, and_cloud):
    run_mrlc = MRLC(d=d, and_tree=and_cloud)

    start_time = time.perf_counter()
    run_mrlc.mrlc_algo(latency_target)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    gadget_mapping = run_mrlc.get_gadget_definition()
    gadget_def = run_mrlc.get_unique_gadgets_definition()

    run_mrlc.print_gadget_definition()

    print(f"MRLC execution time : {end_time - start_time:.6f} seconds")

    design_latency = run_mrlc.get_total_latency()
    design_randomness, design_area = run_mrlc.get_total_randomness_and_area()

    gate_map = {}  # e.g., {0: 'HPC3', 1: 'HPC3', ...}
    for expr, gadget_info in run_mrlc.gadget_definition.items():
        gadget_type = gadget_info.get("gadget_name", "")
        node_no = run_mrlc.and_tree.node_map.get(expr, None)
        if node_no is not None:
            gate_map[node_no] = gadget_type


    return {
        "target_latency": latency_target,
        "gate_map": gate_map,
        "total_randomness": design_randomness,
        "total_latency": design_latency,
        "total_area": design_area,  # example area formula
        "execution_time": execution_time
    }, gadget_mapping, gadget_def
    # return design_latency, design_randomness, design_area


def run_mlrc_test(randomness_target, d, and_cloud):
    run_mlrc = MLRC(d=d, and_tree=and_cloud)
    
    start_time = time.perf_counter()  
    run_mlrc.mlrc_algo(randomness_target)
    end_time = time.perf_counter()
    gadget_mapping = run_mlrc.get_gadget_definition()
    # print(f"gadget_info\n{gadget_mapping}")
    gadget_def = run_mlrc.get_unique_gadgets_definition()
    # print(f"gadget_def\n{gadget_def}")

    # transformer = CFunctionTransformer(gadget_info, gadget_def)


    execution_time = end_time - start_time
    
    # run_mlrc.get_gadget_definition()

    # run_mlrc.print_gadget_definition()

    # run_mlrc.print_unique_gadgets_definition()

    # run_mlrc.print_level_latency()
    design_latency = sum(run_mlrc.level_latency.values())
    # print(f"Design Latency: {design_latency}")
    # design_randomness = sum(gadget_info.get("radom_numbers", 0) for gadget_info in run_mlrc.gadget_definition.values())
    design_randomness, design_area = run_mlrc.get_total_randomness_and_area()
    
    # comar_counted = False

    # for gadget_info in run_mlrc.gadget_definition.values():
    #     print(f"gadget_info: {gadget_info}")
    #     gadget_type = gadget_info.get("gadget_name", "")
    #     print(f"gadget_Type : {gadget_type}")
        
    #     rand = gadget_info.get("radom_numbers", 0)
    #     print(f"random used : {rand}")
    #     if gadget_type == "Comar":
    #         if not comar_counted:
    #             design_randomness += rand
    #             comar_counted = True  # Only once!
    #     else:
    #         design_randomness += rand


    # print(f"Design randomness: {design_randomness}")
    
    # Build gate_no to gadget_type map using node_map
    # creating a new map to store gate no and its corresponding gadget that has been assigned
    gate_map = {}  # e.g., {0: 'HPC3', 1: 'HPC3', ...}
    for expr, gadget_info in run_mlrc.gadget_definition.items():
        gadget_type = gadget_info.get("gadget_name", "")
        node_no = run_mlrc.and_tree.node_map.get(expr, None)
        if node_no is not None:
            gate_map[node_no] = gadget_type
    
    run_mlrc.print_gadget_definition()

    return {
        "target_randomness": randomness_target,
        "gate_map": gate_map,
        "total_randomness": design_randomness,
        "total_latency": design_latency,
        "total_area": design_area,
        "execution_time": execution_time
    }, gadget_mapping, gadget_def


def run_mlrc_test_ru(randomness_target, d, and_cloud):
    run_mlrc = MLRC(d=d, and_tree=and_cloud)
    
    start_time = time.perf_counter()  
    run_mlrc.mlrc_algo_ru(randomness_target)
    end_time = time.perf_counter()
    gadget_mapping = run_mlrc.get_gadget_definition()

    gadget_def = run_mlrc.get_unique_gadgets_definition()

    execution_time = end_time - start_time

    design_latency = sum(run_mlrc.level_latency.values())

    design_randomness, design_area = run_mlrc.get_total_randomness_and_area()
    
    gate_map = {}  # e.g., {0: 'HPC3', 1: 'HPC3', ...}
    for expr, gadget_info in run_mlrc.gadget_definition.items():
        gadget_type = gadget_info.get("gadget_name", "")
        node_no = run_mlrc.and_tree.node_map.get(expr, None)
        if node_no is not None:
            gate_map[node_no] = gadget_type
    
    run_mlrc.print_gadget_definition()

    return {
        "target_randomness": randomness_target,
        "gate_map": gate_map,
        "total_randomness": design_randomness,
        "total_latency": design_latency,
        "total_area": design_area,
        "execution_time": execution_time
    }, gadget_mapping, gadget_def


# def write_to_csv(result_file_mlrc,result_file_mlrc_ru,result_file_mrlc, d, filename):
#     # input directory where test file are present that we use to generate "and tree"
#     input_C_dir = r".\mtp_tetris\test_files"
#     sys.path.append(input_C_dir)
#     input_C = os.path.join(input_C_dir, f"{filename}.c")

#     # output directory where we will save our c file masked with optimised gadget placement
#     base_mlrc_dir = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\mlrc\masked_C_code\MLRC"
#     base_mrlc_dir = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\mlrc\masked_C_code\MRLC"


#     output_c_mlrc_dir = os.path.join(base_mlrc_dir, f"test_{filename}")
#     output_c_mlrc_dir_ru = os.path.join(base_mlrc_dir, f"test_{filename}_ru")
#     output_c_mrlc_dir = os.path.join(base_mrlc_dir, f"test_{filename}")

    

#     os.makedirs(output_c_mlrc_dir, exist_ok=True)
#     os.makedirs(output_c_mrlc_dir, exist_ok=True)
#     os.makedirs(output_c_mlrc_dir_ru, exist_ok=True)

#     # output_c_dir = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\mlrc\masked_C_code"
    
#     # verilog_output_path = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\mlrc\verilog_output"
    
#     # creat the ast for test c file 
#     ast = parse_file(input_C, use_cpp = True)

#     # generate the and tree form c file
#     and_cloud = AndCloudGenerator()
#     and_cloud.visit(ast)
#     and_cloud.print_data()
#     print(f"Number of node in the tree :{and_cloud.graph.num_nodes()}")
#     and_cloud.save_and_tree(filename=filename)


#     # Load and display image of the generated and tree
#     output_folder = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\and_tree_images"
#     sys.path.append(output_folder)
            
#     image_path = os.path.join(output_folder, f"and_cloud_{filename}.png")
#     image = Image.open(image_path)  # Change to your image path
#     display(image)


#     total_gates = len(and_cloud.graph.nodes())
#     test = 2 * total_gates
#     levels = len(and_cloud.get_level_node())
#     total_levels = 2 * levels

#     import csv
#     with open(result_file_mlrc, mode='w', newline='') as file, open(result_file_mrlc, mode='w', newline='') as file1, open(result_file_mlrc_ru, mode='w', newline='') as file2:
#         writer = csv.writer(file)
#         mrlc_writer = csv.writer(file1)
#         writer_ru = csv.writer(file2)

#         header = ['target_randomness'] + [f'g{i}' for i in range(total_gates)] + ['total_randomness', 'total_latency', 'total_area', 'execution_time']
#         header_mrlc = ['target_latency'] + [f'g{i}' for i in range(total_gates)] + ['total_randomness', 'total_latency', 'total_area', 'execution_time']
#         writer.writerow(header)
#         mrlc_writer.writerow(header_mrlc)

#         for randomness_target in range(6, test+1):
#             result, gadget_info, gadget_def = run_mlrc_test(randomness_target, d, and_cloud)
#             output_C = os.path.join(output_c_mlrc_dir, f"output_{filename}_{randomness_target}.c")
#             print(f"Gadget info {gadget_info}")
#             print(f"gadget definition :\n{gadget_def}")
#             transformer = CFunctionTransformer(gadget_info, gadget_def)

#             # run script.py  with output.c to get verilog and from that the area
#             # create a row for the CSV file
            
#             row = [result["target_randomness"]] + [result["gate_map"].get(i, "") for i in range(total_gates)] + [result["total_randomness"], result["total_latency"], result["total_area"], result["execution_time"]
#             ]
#             writer.writerow(row)
#             transformer.transform_c_file(input_C, output_C)

#         for randomness_target in range(6, test+1):
#             result, gadget_info, gadget_def = run_mlrc_test_ru(randomness_target, d, and_cloud)
#             output_C = os.path.join(output_c_mlrc_dir_ru, f"output_{filename}_ru_{randomness_target}.c")
#             print(f"Gadget info {gadget_info}")
#             print(f"gadget definition :\n{gadget_def}")
#             transformer = CFunctionTransformer(gadget_info, gadget_def)

#             # run script.py  with output.c to get verilog and from that the area
#             # create a row for the CSV file
            
#             row = [result["target_randomness"]] + [result["gate_map"].get(i, "") for i in range(total_gates)] + [result["total_randomness"], result["total_latency"], result["total_area"], result["execution_time"]
#             ]
#             writer_ru.writerow(row)
#             transformer.transform_c_file(input_C, output_C)



#         for latency_target in range(levels,total_levels+1):
#             result, gadget_info, gadget_def = run_mrlc_test(latency_target, d, and_cloud)
#             output_C = os.path.join(output_c_mrlc_dir, f"output_{filename}_{latency_target}.c")
#             # print(f"Gadget info {gadget_info}")
#             # print(f"gadget definition :\n{gadget_def}")
#             # run_mlrc_test.print_gadget_definition()
#             transformer = CFunctionTransformer(gadget_info, gadget_def)

#             # run script.py  with output.c to get verilog and from that the area
#             # create a row for the CSV file
            
#             row = [result["target_latency"]] + [result["gate_map"].get(i, "") for i in range(total_gates)] + [result["total_randomness"], result["total_latency"], result["total_area"], result["execution_time"]
#             ]
#             mrlc_writer.writerow(row)
#             transformer.transform_c_file(input_C, output_C)
#             # verilog_output = os.path.join(verilog_output_path, f"verilog_{randomness_target}.v")
#             # script_path = r"C:\Users\nupur\Desktop\mtp_phase2\MaskedHLS_LP\src\script.py"
#             # cmd = f"python {script_path} --topModule=fun --inputFile={output_C} --rtlfile={verilog_output} --bitWidth=1"
#             # print(f"running: {cmd}")
#             # os.system(cmd)
#             # modify the c file with the new gadget definition
#             # run script.py to get verilog and from that the area
#             # verilog_out = f"verilog_out_{randomness_target}.v" 
#             # !python script.py --topModule=fun --inputFile={output_C} --rtlfile={verilog_out} --bitWidth=1
#         for latency_target in range(levels,total_levels+1):
#             result, gadget_info, gadget_def = run_mrlc_test(latency_target, d, and_cloud)
#             output_C = os.path.join(output_c_mrlc_dir, f"output_{filename}_{latency_target}.c")
#             # print(f"Gadget info {gadget_info}")
#             # print(f"gadget definition :\n{gadget_def}")
#             # run_mlrc_test.print_gadget_definition()
#             transformer = CFunctionTransformer(gadget_info, gadget_def)

#             # run script.py  with output.c to get verilog and from that the area
#             # create a row for the CSV file
            
#             row = [result["target_latency"]] + [result["gate_map"].get(i, "") for i in range(total_gates)] + [result["total_randomness"], result["total_latency"], result["total_area"], result["execution_time"]
#             ]
#             mrlc_writer.writerow(row)
#             transformer.transform_c_file(input_C, output_C)
    
#     # import pandas as pd
#     # df = pd.read_csv("mlrc_results.csv")
#     # print(df)   

#      # test mlrc class
# from pycparser import parse_file
# from PIL import Image # type: ignore
# from IPython.display import display # type: ignore


# and_cloud= create_and_cloud(filename="ex2")
