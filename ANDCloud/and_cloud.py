import pycparser
import rustworkx as rx
from rustworkx.visualization import graphviz_draw  #  Import Graphviz rendering
import re
import graphviz
from pycparser import c_ast
import sys
import os
from pycparser import parse_file
sys.path.append(os.path.join(os.path.dirname(__file__), 'MaskedHLS_LP', 'src'))

from MaskedHLS_LP.src.Inliner.DiGraph import DiGraph
from MaskedHLS_LP.src.Inliner.Visitors import FunctionVisitor
from MaskedHLS_LP.src.RegBalancer.src.modules.utils import save_graph
from tabulate import tabulate


import heapq

def preprocess_c_code(code):
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'^\s*#.*', '', code, flags=re.MULTILINE)
    return code
#  Function to visualize the AST



def generate_ast_graph(node, graph, parent=None, counter=[0]):
    """
    Recursively traverses the AST and adds nodes to Graphviz.

    Args:
        node (c_ast.Node): The current AST node being processed.
        graph (graphviz.Digraph): The Graphviz graph for visualization.
        parent (str): The parent node label for connecting edges.
        counter (list): A mutable counter to ensure unique node IDs.
    """
    node_id = f"node{counter[0]}"  # Unique ID for Graphviz
    counter[0] += 1

    #  Get the token or type for annotation
    label = node.__class__.__name__

    if isinstance(node, c_ast.ID):  #  Variable name
        label += f"\\nID: {node.name}"
    elif isinstance(node, c_ast.Constant):  #  Constant value
        label += f"\\nConst: {node.value}"
    elif isinstance(node, c_ast.BinaryOp):  #  Operator
        label += f"\\nOp: {node.op}"

    #  Add node to Graphviz with a rounded rectangle
    graph.node(node_id, label, shape="ellipse", style="filled", fillcolor="lightblue")

    if parent:
        graph.edge(parent, node_id)  #  Connect to parent

    #  Recursively add child nodes
    for child_name, child in node.children():
        generate_ast_graph(child, graph, node_id, counter)

def visualize_c_ast(code, output_file="ast_tree.png"):
    """
    Parses C code into an AST and visualizes it with token annotations.

    Args:
        code (str): The C code to parse.
        output_file (str): The output image filename.
    """
    parser = pycparser.CParser()
    ast = parser.parse(code)

    #  Create a Graphviz Digraph
    graph = graphviz.Digraph(format="png", comment="C AST Visualization")
    generate_ast_graph(ast, graph)

    #  Save and render the graph
    output_path = graph.render(filename=output_file, cleanup=True)
    print(f"AST visualization saved as: {output_path}")



class AndCloudGenerator(c_ast.NodeVisitor):
    def __init__(self):
        self.graph = rx.PyDiGraph()
        self.and_count = 0
        self.var_to_gate = {}
        self.node_map = {}
        self.level_nodes = {} # store node corresponding to a particular level
        self.max_level = 0 # keep track of node level

    def get_level_node(self):
        # return the 
        return self.level_nodes
    
    
    def construct_min_heap(self):
        node_level = self.get_level_node()
        
        min_heap = []

        for level, nodes in node_level.items():
            gate_count = len(nodes) # number of gate at this level
            heapq.heappush(min_heap, (gate_count, level, nodes))

        return min_heap


    def process_and_operation(self, var_name, rhs_node, and_operands):
        """Processes an AND operation and tracks dependencies correctly."""
        # and_operands = self.extract_and_operands(rhs_node)
        # print(f"extracted and operation : {and_operands}")

        # (2 <= len(and_operands) <= 3): is unnecessary as tac will contain atmost 3 input and
        # if and_operands and all(isinstance(op, str) for op in and_operands) and (2 <= len(and_operands) <= 3):
        expression_str = " & ".join(and_operands)
        expression_str = f"{var_name} = " + expression_str
        # gate_name = f"g{self.and_count} ({expression_str})"
        gate_name = f"{expression_str}"
        self.and_count += 1

        # print(f"Creating {gate_name} for AND operation: {and_operands}")

        gate_index = self.graph.add_node(gate_name)
        self.node_map[gate_name] = gate_index

        #  Track dependencies using only `var_to_gate`
        
        added_edges = set()
        max_parent_level = 0 # max level among the input operands
        for operand in and_operands:
            # print(f"added_edges : {added_edges}")
            operand = operand.lstrip("~*-+")
            if operand in self.var_to_gate:
                prev_gates = self.var_to_gate[operand] 
                # print(f"\tprevious gates : {prev_gates}")

                # print(f"\tnode map : {self.node_map}")
                # print(f"\tadded_edges : {added_edges}")
                for prev_gate in prev_gates:  # 
                    assert prev_gate in self.node_map, f"Error: {prev_gate} not found in node_map"
                    if prev_gate not in added_edges:
                        # print(f"\t adding edge from {prev_gate} to {gate_name}")
                        self.graph.add_edge(self.node_map[prev_gate], gate_index, None)
                        added_edges.add(prev_gate)
                        max_parent_level = max(max_parent_level, self.get_node_level(prev_gate))
                    
        # assign level to new gate 
        node_level = max_parent_level + 1
        self.max_level = max(self.max_level, node_level) # update tree level


        if node_level not in self.level_nodes:
            self.level_nodes[node_level] = []
        self.level_nodes[node_level].append(gate_name)

        #  Store direct gadget dependency for future operations
        self.var_to_gate[var_name] = [gate_name]
        # print(f"\tvar to gate : {var_name} :{self.var_to_gate[var_name]}")

    def visit_Decl(self, node):
        if node.init:
        # Create a fake Assignment node
            assignment_node = c_ast.Assignment(op="=", lvalue=c_ast.ID(node.name), rvalue=node.init)

        # Manually call visit_Assignment() to processs dependencies
            self.visit_Assignment(assignment_node)

        self.generic_visit(node)
        

    def get_node_level(self, node):
        """find the level of a given node in the AND tree"""
        for level, nodes in self.level_nodes.items():
            if node in nodes:
                return level
        return 0 
    

    def visit_Assignment(self, node):
        """Tracks assignments and propagates dependencies correctly."""
        # print(f"processing assignment node : \n {node}")
        if isinstance(node.lvalue, c_ast.ID):
            lhs = node.lvalue.name  # Normal variable assignment
        elif isinstance(node.lvalue, c_ast.UnaryOp) and node.lvalue.op == '*':
            lhs = "*"+node.lvalue.expr.name  # pointer dereference
        
        rhs = node.rvalue

         #  Case 1: If rhs is an AND operation (2 or 3 operands), process it
        and_operands = self.extract_and_operands(rhs)
        # print(f"extracted and operands : {and_operands}")
        # if and_operands and all(isinstance(op, str) for op in and_operands) and (2 <= len(and_operands) <= 3):
        CONST_PATTERN = re.compile(r"^(?:0x[0-9a-fA-F]+|0b[01]+|\d+)$")

        # if (and_operands and (2 <= len(and_operands) <= 3) and all(not CONST_PATTERN.match(op) for op in and_operands) ):
        if (and_operands and (2 <= len(and_operands) <= 3) and all(not op.startswith("dec_") for op in and_operands)):
            self.process_and_operation(lhs, rhs, and_operands)

        else:
            #  Case 2: Track dependencies if rhs is a variable or complex expression
            dependencies = set()

            if isinstance(rhs, c_ast.ID) and rhs.name in self.var_to_gate:
                stored_dependency = self.var_to_gate[rhs.name]
                if not isinstance(stored_dependency, list):
                    stored_dependency = [stored_dependency]  #  Convert single dependency to list
                dependencies.update(stored_dependency)

            elif isinstance(rhs, c_ast.BinaryOp):
                for var in self.get_used_variables(rhs):
                    if var in self.var_to_gate:
                        stored_dependency = self.var_to_gate[var]
                        if not isinstance(stored_dependency, list):
                            stored_dependency = [stored_dependency]  #  Convert single dependency to list
                        dependencies.update(stored_dependency)

            #  Store dependencies in `var_to_gate`
            if dependencies:
                if lhs in self.var_to_gate:
                    if not isinstance(self.var_to_gate[lhs], list):
                        self.var_to_gate[lhs] = [self.var_to_gate[lhs]]  #  Convert to list if needed
                    self.var_to_gate[lhs] = list(set(self.var_to_gate[lhs]) | dependencies)  # Enure unique entries
                else:
                    self.var_to_gate[lhs] = list(dependencies)

        self.generic_visit(node)
    
    def get_tree_level(self):
        """return the level of the ando cloud tree"""
        return self.max_level + 1
    
    def get_used_variables(self, node):
        """Extracts all variables used in an expression."""
        variables = set()
        if isinstance(node, c_ast.ID):
            variables.add(node.name)
        elif isinstance(node, c_ast.BinaryOp):
            variables |= self.get_used_variables(node.left)
            variables |= self.get_used_variables(node.right)
        return variables

    def extract_and_operands(self, node):
        if isinstance(node, c_ast.BinaryOp) and node.op == '&':
            operands = []

            left_operands = self.extract_and_operands(node.left) if isinstance(node.left, c_ast.BinaryOp) else [self.get_var_name(node.left)]
            # print(f"left operand : {left_operands}")
            right_operands = self.extract_and_operands(node.right) if isinstance(node.right, c_ast.BinaryOp) else [self.get_var_name(node.right)]
            # print(f"right operand : {right_operands}")
            if left_operands and right_operands:
                operands = left_operands + right_operands  

            if 2 <= len(operands) <= 3 and all(isinstance(op, str) for op in operands):
                return operands
        return None

    def get_var_name(self, node):
        if isinstance(node, c_ast.ID):
            return node.name
        elif isinstance(node, c_ast.UnaryOp):
            return f"{node.op}{self.get_var_name(node.expr)}"
        return None

    def visit_FuncDef(self, node):
        # print("\n=== Processing Function ===")
        self.visit(node.body)

    def print_data(self):
        for var, gates in self.var_to_gate.items():
            print(f"{var} -> {gates}")

        if isinstance(self.node_map, dict):
            print("[NODE MAP]")
            table_data = [(key, value) for key, value in self.node_map.items()]
            print(tabulate(table_data, headers=["Key", "Value"], tablefmt="grid"))
        # print(f"Node map {self.node_map}")

        # print(f"ode level : {self.level_nodes}")
        if isinstance(self.level_nodes, dict):
            print("[NODE IN EACH LEVEL {LEVEL MAP}]")
            table_data = [(key, value) for key, value in self.level_nodes.items()]
            print(tabulate(table_data, headers=["Key", "Value"], tablefmt="grid"))


        # heap =self.construct_max_heap()
        # while (heap):
        #     print(heapq.heappop(heap))

    def save_and_tree(self, filename):
        output_folder = r".\ANDCloud\AND_tree"
        sys.path.append(output_folder)
        
        image_path = os.path.join(output_folder, f"and_cloud.png")
        
        save_graph(self.graph, image_path)

#  Function to Extract Graph and Save It
def extract_and_draw_graph(filename, output_file="and_cloud.png"):
    # Parse the C file into an AST
    ast = parse_file(filename, use_cpp=True)

    # Visualize AST (optional)
    # print("\n=== Parsed AST ===")
    # ast.show()
    
    extractor = AndCloudGenerator()
    extractor.visit(ast)
    extractor.print_data()

    # print("\n=== Extracted Graph Data ===")
    # print("Nodes:", [extractor.graph[i] for i in range(len(extractor.graph.nodes()))])
    # print("Edges:", extractor.graph.edge_list())
    if len(extractor.graph.nodes()) == 0:
        print("No valid AND operations found in the given C code.")
        return

    #  Save the Graph as an Image
    save_graph(extractor.graph, output_file)

# #  Sample C Code Input
# c_code = """
# void f2(int a, int d, int *z)
# {
#   int a_inp;
#   int d_inp;
#   a_inp = a;
#   d_inp = d;
#   int y;
#   int x;
#   int p;
#   y = a_inp & d_inp;
#   p = y & d_inp;
#   *z = (y & p) & a_inp;
# }

# """



# test_file_dir = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\test_files"
# filename = "ex2.c"
# output_folder = r"C:\Users\nupur\Desktop\mtp_phase2\MTP\LatencyRandomnessMaskedHLS\and_tree_images"
# sys.path.append(test_file_dir)
# sys.path.append(output_folder)


# # if len(sys.argv) < 2:
# #     print("Usage: python script.py <filename>")
# #     sys.exit(1)

# # filename = sys.argv[1]  # Take filename from the command line
# # print(f"Processing file: {filename}")

# test_file_path = os.path.join(test_file_dir, filename)
# image_path = os.path.join(output_folder, f"and_cloud_{filename}.png")

# extract_and_draw_graph(test_file_path, image_path)
