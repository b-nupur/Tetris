from tabulate import tabulate
from ANDCloud.and_cloud import AndCloudGenerator

class DSE:

    GADGET_PARAM_MAP = {}

    """Design space Exploration class"""
    def __init__(self, d, and_tree: AndCloudGenerator):
        self.gadget_definition = {}  # store AND expression mapped to {gadget name mapped to gadget function call}
        self.and_tree = and_tree
        self.nodes_by_level = and_tree.get_level_node() #sore nodes by the level 
        self.d = d
        self.unique_gadgets_definition = {}
        self.level_latency = {}

    @classmethod
    def set_param_map(cls, param_map):
        if not cls.GADGET_PARAM_MAP:
            cls.GADGET_PARAM_MAP = param_map
            print("[INFO] GADGET_PARAM_MAP initialized.")
        else:
            print("[INFO] GADGET_PARAM_MAP already set. Skipping.")

    @classmethod
    def get_params_for(cls, gadget_name):
        return cls.GADGET_PARAM_MAP.get(gadget_name)
    def get_unique_gadgets_definition(self):
        return self.unique_gadgets_definition

    def get_gadget_definition(self):
        return self.gadget_definition
    
    def get_total_latency(self):
        """
            return the sum of latency of each level in the and tree
        """
        return sum(self.level_latency.values())
    
    def get_total_randomness_and_area(self):
        
        """
        Logic: 

            - For randomness we need to add the randomness of each node in the and_tree if node is hpc3 or hpc2 
            - but if it is commar then we can resue the randomness so we will just add 6 if commar is present in 
            - the design
        
        """
        
        design_randomness = 0
        design_area = 0

        comar_counted = False

        for gadget_info in self.gadget_definition.values():
            # print(f"gadget_info: {gadget_info}")
            gadget_type = gadget_info.get("gadget_name", "")
            # print(f"gadget_Type : {gadget_type}")
            rand = gadget_info.get("radom_numbers", 0)
            # print(f"random used : {rand}")
            if gadget_type == "COMAR":
                if not comar_counted:
                    design_randomness += rand
                    comar_counted = True # counting only once for comar
            else:
                design_randomness += rand
            design_area += self.GADGET_AREA_MAP[gadget_type]

        # print(f"Design randomness: {design_randomness}")
        # print(f"Design area: {design_area}")
        
        return design_randomness, design_area

    def print_gadget_definition(self):
        if isinstance(self.gadget_definition, dict):
            table_data = []
            for expr, gadget_call in self.gadget_definition.items():
                node_no = self.and_tree.node_map.get(expr, "N/A")  # Use "N/A" if expr not in node_map
                table_data.append((node_no, expr, gadget_call))
            print(tabulate(table_data, headers=["Gate No", "Expression", "Gadget Call"], tablefmt="grid"))
