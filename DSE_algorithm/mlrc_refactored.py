from DSE_algorithm import DSE
from tabulate import tabulate # type: ignore
import json
from collections import defaultdict
import heapq
import Gadgets as secure_gadget

class MLRC(DSE):
    """Minimise Latency Under Randomness Constraint (MLRC)""" 
    def __init__(self, d, and_tree):
        super().__init__(d, and_tree)

    def print_unique_gadgets_definition(self):
        if isinstance(self.unique_gadgets_definition, dict):
            print(json.dumps(self.unique_gadgets_definition, indent=4))

    def construct_min_heap(self):
        # node_level = self.and_tree.get_level_node()
        
        min_heap = []

        for level, nodes in self.nodes_by_level.items():
            gate_count = len(nodes) # number of gate at this level
            # intialising level_latency of each levek in the and_tree
            # assuming initially all gate are hpc2 or comar with latency of 2 
            self.level_latency[level] = 2
            heapq.heappush(min_heap, (gate_count, -level, nodes))
            
        return min_heap
    
    def find_min_gate_level(self, min_heap):
        """
        Extract the level with the minimum number of nodes
        @param min_heap: The min heap storing (gate_count, level, nodes)
        @return: the level with least gate.
        """
        if not min_heap:
            return None
        
        _, level, _ = heapq.heappop(min_heap)
        return abs(level) 
        
    def replace_gadget(self,gadget_name, node, randomness_used, current_gadget_randomness, prev_gadet_randomness):
            """
                @param gadget_name: The name of the gadget to replace the AND nodes
                @param node: The AND node to be replaced with the gadget
                @param randomness_used: to keep track of the randomness used 
                                        while replaceing a node (allows us to keep total randomness used in the repalcement processs)
                @param current_gadget_randomness: randomness used by the current gadget
                @param prev_gadet_randomness: randomness used by the replaced gadget

                Logic:
                    - retrive the gadget class.
                    - create object of the gadget class 
                    - generate the definition of the gadget
                    - get the gadget name of the function name of gadget
                    - get the number of random variable use by the gadget
                    - get the latency of the gadget

            """
            if gadget_name not in self.print_unique_gadgets_definition:

                gadget_class = getattr(secure_gadget, gadget_name) # retrive gadget class
                gadget = gadget_class(self.d)

                # generate the function definition for this And Gadget
                gadget_def = gadget.generate_multiply_function()
                func_name = gadget.get_function_name()

                num_random_vars = gadget.get_random_count()
                latency = gadget.get_latency()

                if func_name not in self.unique_gadgets_definition:
                    self.unique_gadgets_definition[gadget_name] = {
                        "func_name": func_name,
                        "gadget_def" : gadget_def,
                        "random_number": num_random_vars,
                        "latency": latency
                    }
            
            # if self.gadget_definition.get(gate) is None: # not replaced yet 
            self.gadget_definition[node] = gadget_name
            randomness_used += prev_gadet_randomness - current_gadget_randomness
            return randomness_used

    def mlrc_algo(self, target_randomness): 
        """
            Logic:
                target_randomness < number of nodes in and Tree
                    - If target randomness is less than number of nodes we need to replace with comar
                    - As comar always uses less 6 randomness compared to HPC2 which uses 1 randomness 
                target_randomness >= number of nodes in and tree.
                    - we replace with hpc2 as area of hpc2 is less than that of comar
                
        """
        if target_randomness < self.and_tree.graph.num_nodes() and target_randomness >= 6:

            self.mlrc_comar(target_randomness)
            # if gadget definition not present for any gadget with comar
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "COMAR"
                    # initially all the gadget should be comar.
                    _ = self.replace_gadget(gadget_name, node=node, randomness_used=0, current_gadget_randomness=0, prev_gadet_randomness=0)
        else:
            self.mlrc_without_comar(target_randomness)
            # if gadget definition not present for any gadget the replace it with hpc2 
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "HPC2"
                    # initially all the gadgets should hpc2
                    _ = self.replace_gadget(gadget_name, node, randomness_used=0, current_gadget_randomness=0, prev_gadet_randomness=0)
            
    def mlrc_comar(self, randomness_target):
        """
            - calculate the leastpossible randomness = 6 as comar uses 6 randomness
            - figure out the bonus (extra randomness) we have.
            - construct min heap of 
        """
        randomness_leastpossible = 6
        randomness_bonus = randomness_target - randomness_leastpossible
        # construct the min heap of node levels
        min_heap = self.construct_min_heap()
        # print(f"Intial randomness_bonus: {randomness_bonus}")
        if randomness_bonus > 0:
            while(randomness_bonus > 0):
                # get the level with least gate count 

                min_gate_level = self.find_min_gate_level(min_heap) 
                # self.level_latency[min_gate_level] = 2

                if min_gate_level == None:
                    break # no further optimisation possible
 
                randomness_used = self.replace_gates_With_optimisied_gadgets_comar(min_gate_level, randomness_bonus)
                randomness_bonus = randomness_bonus - randomness_used # it should be randomness used

        
        elif randomness_bonus < 0:
            print(f"Target randomness cannot be met")
        
    def replace_gates_With_optimisied_gadgets_comar(self, min_gate_level, randomness_bonous):
        """
        Replaces gates at a given level with optimized gadgets based on available randomness.

        Logic:
        - If the number of gates (`gate_count`) at `min_gate_level` is less than or equal to `randomness_bonus`,
        all gates in that level are replaced with optimized gadgets.
        - If `gate_count` exceeds `randomness_bonus`, replacing the gadgets will not reduce latency
        and will only increase randomness unnecessarily. but comar has more area so we will replace some comar with hpc2 

        Args:
            min_gate_level (int): The level with the minimum number of gates.
            randomness_bonus (int): The available randomness budget for gadget replacement.
        
        Returns:
            randomness_used : randomness used while replacing the gadgets
        """
        # initially all gates are comar and comar reuses the randomness.
        # and if we have bonus randomness then we can replace some comar
        # this function will only be called if we have bonus randomness
        # we need fresh randomness for replacing comar with hpc2, hpc3
        # we have two possibilities :
        #   randomness_reuired <= randomness bonus -> replace all the gates in the level with hpc3 (reduces the overall latency)
        #   randomness_required > randomness bonus -> replace some gates in the level with hpc2 (reduces the overall area )
        #   randomness_required to replace gates with less latency gadget HPC3 will be twice the number of gates in a
        #   level.
        
        gate_count = len(self.nodes_by_level[min_gate_level] ) 
        # print(f"2 * number of gate at level {min_gate_level} : {gate_count * 2}")
        # print(f"{gate_count * 2} (replacable randomness) <= {randomness_bonous} (randomness bonus)")
        
        # replaceable_randomness is the randomess that is needed to replace all the gates in that level 
        # for example if nodes in the level are 3 then we need 6 randomness to replace 3 gates with HPC3 
        # as it requires 2 randomn

        hpc3_randomness = 2
        replaceable_randomness = gate_count * hpc3_randomness
        randomness_used = 0
        if replaceable_randomness <= randomness_bonous:
            # replace all the gates in that level with optimised gadget
            for gate in self.nodes_by_level[min_gate_level]: 
                gadget_name = "HPC3"
                randomness_hpc3 = 2
                randomness_Comar = 0 # becuase comar can resuse randomness 
                randomness_used = self.replace_gadget(gadget_name, gate, randomness_used, randomness_Comar, randomness_hpc3)
            latency_hpc3 = 1 
            self.level_latency[min_gate_level] = 1
        else:
            # replacing comar with hpc2 because we have some randomness bonus and we can use that bonous
            # to reduce the area as hpc2 have less area and randomness required by hpc2 is 1.
            
            for node in self.nodes_by_level[min_gate_level]:
                # print(f"randomness bonus {randomness_bonous}")
                if randomness_used < randomness_bonous:
                    gadget_name = "HPC2"
                    randomness_Comar = 0
                    randomness_hpc2 = 1
                    randomness_used = self.replace_gadget(gadget_name, node, randomness_used, randomness_Comar, randomness_hpc2)  
                # replacing with hpc2 won't change latency
        return randomness_used
    
    def replace_gates_with_optimisied_gadgets(self,min_gate_level, randomness_bonous, latency_reduction_gadget, area_reduction_gadget):

        """
        Replaces gates at a given level with optimized gadgets based on available randomness.

        Logic:
        - If the number of gates (`gate_count`) at `min_gate_level` is less than or equal to `randomness_bonus`,
        all gates in that level are replaced with optimized gadgets.
        - If `gate_count` exceeds `randomness_bonus`, replacing the gadgets will not reduce latency
        and will only increase randomness unnecessarily.

        Args:
            min_gate_level (int): The level with the minimum number of gates.
            randomness_bonus (int): The available randomness budget for gadget replacement.
        
        Returns:
            None
        """

        
        # node_level = self.and_tree.get_level_node()
        
        gate_count = len(self.nodes_by_level[min_gate_level] )
        randomness_used = 0
        
        # as initally all the gates are hpc2 (randomness = 1) 
        # and we are replacing the gates with hpc3 (randomness = 2) so the required randomess is (2-1) * number of gate = `gate_count`
        # therefore gate_count <= randomness to replace gates in a level with hpc3 having latency 1
        if gate_count <= randomness_bonous:
            # replace all the gates in that level with optimised gadget
            for gate in self.nodes_by_level[min_gate_level]:
                # print(f"gate: {gate} replacing with {latency_reduction_gadget}")
                randomness_hpc2 = 1
                randomness_hpc3 = 2 
                randomness_used = self.replace_gadget("HPC3", gate,randomness_used, randomness_hpc2, randomness_hpc3)
            latency_hpc3 = 1
            self.level_latency[min_gate_level] = latency_hpc3 # every gadget in that level is replaced by hpc3 with latency of 1
      
        return randomness_used
    
    def print_level_latency(self):
        table_data = [(key, value) for key, value in self.level_latency.items()]
        print(tabulate(table_data, headers=["Level", "Latency"], tablefmt="grid"))
        