import os
from abc import ABC, abstractmethod
class Gadget(ABC):
    def __init__(self, d, random_required, latency, function_name):
        self.d = d
        self.random_required = random_required
        self.latency = latency
        self.function_name = function_name

    def get_random_count(self):
        return self.random_required

    def get_latency(self):
        return self.latency

    def get_function_name(self):
        return self.function_name
    
    @abstractmethod
    def generate_multiply_function(self):
        pass
    
    @staticmethod
    def generate_and_write_function(gadget_instance, filename_prefix, output_folder="gadget_output"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, output_folder)
        os.makedirs(output_path, exist_ok=True)
  
        function_def = gadget_instance.generate_multiply_function()
        
        c_filename = os.path.join(output_path, f"{filename_prefix}_generated.c")

        with open(c_filename, "w") as f:
            f.write(f"/* {filename_prefix.upper()} Function Definition */\n")
            f.write("".join(function_def))

        # print("-" * 56)
        # print(f"| Printing [{filename_prefix.upper()} DEFINITION] for {d} order security... ")
        # print("-" * 56)
        # print("".join(function_def))
        # print("-" * 56)
        # print(f"C file '{c_filename}' created successfully.\n")

