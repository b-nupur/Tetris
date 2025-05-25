from DSE_algorithm.dse import DSE
from tabulate import tabulate # type: ignore
import json
from collections import defaultdict
import heapq
import Gadgets as secure_gadget


"""
MINIMISE LATENCY UNDER RANDOMNESS CONSTRAINT.
latnecy = number of levels in and-tree * inital gadget placement assuming hpc2.
randomess = randomness used by each node in the and-tree.


[input] = target_randomness (it tell the maximum limit of randomness that can be used by the design)

[Motivation] : if the randomness is more than needed the we can use this extra randomness to replace the gadgets.

- if the security order (d) = 1
    - randomness used by HPC2 = 1.
    - Therefore, least possible randomness of the design = number of nodes in the and-tree.

        - If {target_randomness} < {number of node in the and-tree}: 
            * use Comar (as it uses only 6 randomness)
            * Initially all the gadgets are COMAR.
            * latency = Number of levels in the and-tree * latency of comar gadget (2)
            * run MLRC to replace gadgets at each level 
        - Else if {target_randomness} >= number of nodes in and-tree.
            * Initially all the gadgets are HPC2. 
            * latency = Number of levels in the and-tree * latency of comar gadget (2)
            * run MLRC to replace gadgets at each level 
            

- for security order > 1:

    - Initially assuming all the nodes are assigned hpc2 gadget.
    - total randomness = number of nodes in the and tree * randomness used per hpc2 gadget of nth order.
- 
"""
class MLRC(DSE):
    """Minimise Latency Under Randomness Constraint (MLRC)""" 
    def __init__(self, d, and_tree):
        super().__init__(d, and_tree)
        # self.level_randomness_used = defaultdict(set) # map containing the randomness correspoonding level 😭 no need
        # randomness_used -> level
        # 1 = {1, 2, 4} `randomness 1 is used in level 1, 2, 4`
        # 2 = {3,5,7} `randomness 2 is used in level 3, 5, 7`

    # def print_unique_gadgets_definition(self):
        # if isinstance(self.unique_gadgets_definition, dict):
        #     table_data = []
        #     for name, definition in self.unique_gadgets_definition.items():
        #         # Just preview the first line and number of lines
        #         preview = definition.strip().split('\n')[0]  # e.g., "void HPC3(...) {"
        #         num_lines = len(definition.strip().split('\n'))
        #         table_data.append((name, preview, num_lines))

        # print(tabulate(table_data, headers=["Gadget Name", "Preview", "Lines"], tablefmt="grid"))

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
        Extract the level with the highest number of nodes
        @param min_heap: The min heap storing (gate_count, level, nodes)
        @return: the level with least gate.
        """
        if not min_heap:
            return None
        
        _, level, _ = heapq.heappop(min_heap)
        return abs(level) 
    
    def mlrc_algo_ru(self, target_randomness): 
        """
            Logic:
                target_randomness < number of nodes in and Tree
                    - If target randomness is less than number of nodes we need to replace with comar
                    - As comar always uses less 6 randomness 
                target_randomness >= number of nodes in and tree.
                    - we replace with hpc2 as area of hpc2 is less than that of comar
                
        """
        # print(f"number of nodes : {self.and_tree.graph.num_nodes()}")
        # print(f"target randomness: {target_randomness}")

        if target_randomness < self.and_tree.graph.num_nodes() and target_randomness >= 6:

            # print(f"target randomness: {target_randomness}")
            self.mlrc_with_comar_ru(target_randomness)
            # if gadget definition not present for any gadget with comar
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "COMAR"
                    _ = self.replace_gadget(gadget_name, node, 0, 0, 1)
        else:
            self.mlrc_without_comar_ru(target_randomness)
            # if gadget definition not present for any gadget the replace it with hpc2 
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "HPC2"
                    _ = self.replace_gadget(gadget_name, node, 0, 0, 1)
    
    def mlrc_algo(self, target_randomness): 
        """
            Logic:
                target_randomness < number of nodes in and-Tree * randomness of hpc2(for that order) and security order is 1. then we can 
                use comar as comar only works for security order = 1. 
                    - If target randomness is less than number of nodes we need to replace with comar
                    - As comar always uses 6 randomness. 
                target_randomness >= number of nodes in and tree.
                    - we replace with hpc2 as area of hpc2 is less than that of comar
                
        """
        # print(f"number of nodes : {self.and_tree.graph.num_nodes()}")
        # print(f"target randomness: {target_randomness}")

        if target_randomness < self.and_tree.graph.num_nodes():

            # print(f"target randomness: {target_randomness}")
            self.mlrc_comar(target_randomness)
            # if gadget definition not present for any gadget with comar
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "COMAR"
                    _ = self.replace_gadget(gadget_name, node, 0, 0, 1)
        else:
            self.mlrc_without_comar(target_randomness)
            # if gadget definition not present for any gadget the replace it with hpc2 
            for node in self.and_tree.graph.nodes():
                if self.gadget_definition.get(node) is None:
                    gadget_name = "HPC2"
                    _ = self.replace_gadget(gadget_name, node, 0, 0, 1)
            
    def mlrc_comar(self, randomness_target):
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
 
                gate_replace_at_level = self.replace_gates_With_optimisied_gadgets_comar(min_gate_level, randomness_bonus)
                randomness_bonus = randomness_bonus - gate_replace_at_level # it should be randomness used

        
        elif randomness_bonus < 0:
            print(f"Target randomness cannot be met")


        # no need for this as it will never happen 

        #  target randomnes = t
        #  number of nodes = n
        #  if the following if condition is satified then alteast n-6 nodes needs to be replaced 
        #  which means the buffer randomness need will be 2 * (n-6).
        #  as we are using comar:
        #  buffer randomness = t - 6 = 2 * (n-6)
        #  t = 2 * (n-6) + 6 => t = 2n - 6 
        #  also, t < n as we are processing comar case
        #  solving the inequality:
        #  2n-6 < n
        #  n < 6
        #  but t (target randomness) < n (number of nodes)
        #  t < 6  but for comar we can never have randomness less than 6 so target randomness can't be met. 

        # if (self.and_tree.graph.num_nodes() - len(self.gadget_definition) <= 6):
        #     print("INSIDE MLRC COMAR ")
        #     print("IF condition satisfied node in the and tree - gadget definition len <= 6")
        #     node_level = self.and_tree.get_level_node()
        #     print("PRINTING NODE LEVEL")
        #     print(node_level)
        #     for level in node_level:
        #         max_latency = 0
        #         for gate in node_level[level]:
        #             if gate not in self.gadget_definition:
        #                 gadget_name = "HPC2"
        #                 _ = self.replace_gadget(gadget_name, gate, 0, 0, 1)

        #             max_latency = max(max_latency, self.level_latency.get(level, 2))
        #         self.level_latency[level] = max_latency

    def mlrc_without_comar(self, randomness_target):

        randomness_leastpossible = self.and_tree.graph.num_nodes()
        randomness_bonus = randomness_target - randomness_leastpossible
        # construct the min heap of node levels
        min_heap = self.construct_min_heap()
        if randomness_bonus == 0:
            return 
            self.replace_all_gadget_with_hpc2()

        elif randomness_bonus > 0:
            while(randomness_bonus > 0):
                # get the level with least gate count 
                min_gate_level = self.find_min_gate_level(min_heap) 
                # self.level_latency[min_gate_level] = 2 # initially all gates are hpc2
                if min_gate_level == None:
                    break # no further optimisation possible

                randomness_used = self.replace_gates_with_optimisied_gadgets(min_gate_level, randomness_bonus, "HPC3", "HPC3")
                randomness_bonus = randomness_bonus - randomness_used

        else:
            print(f"Target randomness cannot be met")

    def mlrc_with_comar_ru(self, randomness_target):
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

                randomness_used = self.replace_gates_With_optimisied_gadgets_comar_ru(min_gate_level, randomness_bonus)
                
                self.level_randomness_used[randomness_used].add(min_gate_level)
                randomness_bonus = randomness_bonus - randomness_used # it should be randomness used
                # print(f"randomness_bonus: {randomness_bonus}")  
            # remaining gadget should be replaced with comar
            # self.replace_all_gadget_with_comar()
        
        elif randomness_bonus < 0:
            print(f"Target randomness cannot be met")

        if (self.and_tree.graph.num_nodes() - len(self.gadget_definition) <= 6):
            node_level = self.and_tree.get_level_node()
            for level in node_level:
                max_latency = 0
                for gate in node_level[level]:
                    if gate not in self.gadget_definition:
                        gadget_name = "HPC2"
                        _ = self.replace_gadget(gadget_name, gate, 0, 0, 1)
                    # latency of the level will be the max latency of any gate in that level
                    # 2 as defualt latency because initally all the gadget are comar and comar have latency of 2
                    max_latency = max(max_latency, self.level_latency.get(level, 2))
                self.level_latency[level] = max_latency

    def mlrc_without_comar_ru(self, randomness_target):
        """
         
        """
        randomness_leastpossible = self.and_tree.graph.num_nodes()
        randomness_bonus = randomness_target - randomness_leastpossible
        # construct the min heap of node levels
        min_heap = self.construct_min_heap()
        if randomness_bonus == 0:
            return 
            self.replace_all_gadget_with_hpc2()

        elif randomness_bonus > 0:
            while(randomness_bonus > 0):
                # get the level with least gate count 
                min_gate_level = self.find_min_gate_level(min_heap) 
                # self.level_latency[min_gate_level] = 2 # initially all gates are hpc2
                if min_gate_level == None:
                    break # no further optimisation possible

                # using bonus randomness to replace the gates with optimised gadgets,
                # such that the latency of design is reduced as HPC3 have less latency than HPC2 
                # if all the gates can't be replace in the a level then we replace some gates in that
                # level with HPC3 as it will reduce the area as HPC3 have less area as compared to HPC2
                # becuse latency is less therefore area is also less. 
                randomness_used = self.replace_gates_with_optimisied_gadgets_ru(min_gate_level, randomness_bonus)
                # print(f"randomness used: {randomness_used}")
                self.level_randomness_used[randomness_used].add(min_gate_level)
                # print(f"print level random map : {self.level_randomness_used}")
                randomness_bonus = randomness_bonus - randomness_used

    def replace_gates_With_optimisied_gadgets_comar_ru(self, min_gate_level, randomness_bonus):
        gate_count = len(self.nodes_by_level[min_gate_level] ) 
        # print(f"2 * number of gate at level {min_gate_level} : {gate_count * 2}")
        # print(f"{gate_count * 2} (replacable randomness) <= {randomness_bonous} (randomness bonus)")
        
        # replaceable_randomness is the randomess that is needed to replace all the gates in that level 
        # for example if nodes in the level are 3 then we need 6 randomness to replace 3 gates with HPC3 
        # as it requires 2 randomn

        replaceable_randomness = gate_count * 2
        randomness_used = 0

        if replaceable_randomness <= randomness_bonus:
            # replace all the gates in that level with optimised gadget
            for gate in self.nodes_by_level[min_gate_level]: 
                gadget_name = "HPC3"
                randomness_used = self.replace_gadget(gadget_name, gate, randomness_used, 0, 2)
            self.level_latency[min_gate_level] = 1
        else:
            
            # calculate extra randomness needed for level replacement
            extra_randomness = replaceable_randomness - randomness_bonus

            print(f"{replaceable_randomness} - {randomness_bonus} = {extra_randomness}")
            print(f"processing level : {min_gate_level}")
            print(f"extra randomness: {extra_randomness}" )
            print(f"randomness map : {self.level_randomness_used}")
            # find the level with randomness_used >= extra_randomness
            key = self.find_least_key_ge(extra_randomness)

            if key is not None:
                replaceable_level = self.level_randomness_used[key].pop()
                for gate in self.nodes_by_level[replaceable_level]:
                    randomness_used = self.replace_gadget("COMAR",gate, randomness_used, 2, 0)
                for gate in self.nodes_by_level[min_gate_level]:
                    randomness_used = self.replace_gadget("HPC3",gate, randomness_used, 0, 2)
                # replace with the gates used in this level with the current level.
            else:
                
                # replacing comar with hpc2 because we have some randomness bonus and we can use that bonous
                # to reduce the area as hpc2 have less area and randomness required by hpc2 is 1.
                for node in self.nodes_by_level[min_gate_level]:
                    # print(f"randomness bonus {randomness_bonous}")
                    if randomness_used < randomness_bonus:
                        gadget_name = "HPC2"
                        randomness_used = self.replace_gadget(gadget_name, node, randomness_used, 0, 1)  
                            
        return randomness_used

    def replace_gates_with_optimisied_gadgets_ru(self, min_gate_level, randomness_bonus):
        gate_count = len(self.nodes_by_level[min_gate_level] )
        randomness_used = 0
        
        # as initally all the gates are hpc2 (randomness = 1) 
        # and we are replacing the gates with hpc3 (randomness = 2) so the required randomess is (2-1) * number of gate = `gate_count`
        # therefore gate_count <= randomness to replace gates in a level with hpc3 having latency 1
        if gate_count <= randomness_bonus:
            # replace all the gates in that level with optimised gadget
            for gate in self.nodes_by_level[min_gate_level]:
                # print(f"gate: {gate} replacing with {latency_reduction_gadget}")
                randomness_used = self.replace_gadget("HPC3", gate,randomness_used, 1, 2)

            self.level_latency[min_gate_level] = 1 # every gadget in that level is replaced by hpc3 with latency of 1
        elif randomness_bonus > 0: # yaha else bhi ho skata h
            # calculate extra randomness needed
            extra_randomness = gate_count - randomness_bonus
            key = self.find_least_key_ge(extra_randomness)
            # print(f"key : {key}")
            # find the level with randomness_used >= extra_randomness (number of gates in this level will always be <= current level)
            if key is not None and self.level_randomness_used[key]:
                replacable_level = self.level_randomness_used[key].pop() # ye ek set hoga 
                # replace with the gates used in this level with the current level.
                for gate in self.nodes_by_level[replacable_level]:
                    randomness_used = self.replace_gadget("HPC2",gate, randomness_used, 2, 1)
                for gate in self.nodes_by_level[min_gate_level]:
                    randomness_used = self.replace_gadget("HPC3",gate, randomness_used, 1, 2)

        return randomness_used
    
    def find_least_key_ge(self, extra_randomness):
        keys_ge = [key for key in self.level_randomness_used.keys() if key >= extra_randomness]
        return min(keys_ge) if keys_ge else None 
    
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
                randomness_used = self.replace_gadget("HPC3", gate,randomness_used, 1, 2)
            self.level_latency[min_gate_level] = 1 # every gadget in that level is replaced by hpc3 with latency of 1
      
        return randomness_used
        # pass

    def replace_gates_With_optimisied_gadgets_comar(self, min_gate_level, randomness_bonous):
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
        # initially all gates are comar and comar reuses the randomness.
        # and if we have bonus randomness then we can replace some comar
        # this function will only be called if we have bonus randomness
        # we need fresh randomness for replacing comar with hpc2, hpc3
        # we have two possibilities :
        #   randomness_reuired >= randomness bonus -> replace all the gates in the level with hpc3 (reduces the overall latency)
        #   randomness_required < randomness bonus -> replace some gates in the level with hpc2 (reduces the overall area )
        #   randomness_required to replace gates with less latency gadget HPC3 will be twice the number of gates in a
        #   level.
        
        gate_count = len(self.nodes_by_level[min_gate_level] ) 
        # print(f"2 * number of gate at level {min_gate_level} : {gate_count * 2}")
        # print(f"{gate_count * 2} (replacable randomness) <= {randomness_bonous} (randomness bonus)")
        
        # replaceable_randomness is the randomess that is needed to replace all the gates in that level 
        # for example if nodes in the level are 3 then we need 6 randomness to replace 3 gates with HPC3 
        # as it requires 2 randomn


        replaceable_randomness = gate_count * 2
        randomness_used = 0
        if replaceable_randomness <= randomness_bonous:
            # replace all the gates in that level with optimised gadget
            for gate in self.nodes_by_level[min_gate_level]: 
                gadget_name = "HPC3"
                randomness_used = self.replace_gadget(gadget_name, gate, randomness_used, 0, 2)
            self.level_latency[min_gate_level] = 1
        else:
            # replacing comar with hpc2 because we have some randomness bonus and we can use that bonous
            # to reduce the area as hpc2 have less area and randomness required by hpc2 is 1.
            
            for node in self.nodes_by_level[min_gate_level]:
                # print(f"randomness bonus {randomness_bonous}")
                if randomness_used < randomness_bonous:
                    gadget_name = "HPC2"
                    randomness_used = self.replace_gadget(gadget_name, node, randomness_used, 0, 1)  
                        
        return randomness_used

    def replace_gadget(self,gadget_name, gate, randomness_used, current_gadget_randomness, replaced_gadget_randomness):
        gadget_class = getattr(secure_gadget, gadget_name) # retrive gadget class
        gadget = gadget_class(self.d)

        # generate the function definition for this And Gadget
        gadget_def = gadget.generate_multiply_function()
        func_name = gadget.get_function_name()

        num_random_vars = gadget.get_random_count()
        latency = gadget.get_latency()

        if func_name not in self.unique_gadgets_definition:
            self.unique_gadgets_definition[func_name] = gadget_def

        
        # if self.gadget_definition.get(gate) is None: # not replaced yet 
        self.gadget_definition[gate] = {
            # "gadget_definition": gadget_def,
            "gadget_name": gadget_name,
            "function_name": func_name,
            "radom_numbers": num_random_vars,
            "gadget_latency": latency 
        }
        randomness_used += replaced_gadget_randomness - current_gadget_randomness
        return randomness_used

    def print_level_latency(self):
        table_data = [(key, value) for key, value in self.level_latency.items()]
        print(tabulate(table_data, headers=["Level", "Latency"], tablefmt="grid"))
        