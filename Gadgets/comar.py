from Gadgets import Gadget
class COMAR(Gadget):
    def __init__(self):
        super().__init__(d=1, random_required=6, latency=2, function_name="Comar")


    def generate_multiply_function(self, * var_names, var_c = None):
        """
        input:  [a0, a1]
                [b0, b1]
        output: [c0, c1]

        """

        if not var_names:
            var_names = ('a', 'b')
        if not var_c:
            var_c = 'c'
        params_list = []
        d = self.d
        n = len(var_names)
        for var in var_names:
            params_list.extend([f"int {var}{i}" for i in range(d + 1)])
        params = ", ".join(params_list)
        param_c = ", ".join([f"int* {var_c}{i}" for i in range(d + 1)])
        param_rand = ", ".join([f"int r{i}" for i in range(n)])
        param_prand = ", ".join([f"int r_{i}" for i in range(2 ** n)])

        param_str = f"{params}, {param_c}, {param_rand}, {param_prand}" # function parameter list 
        # # random number 

        function_signature = f"void Comar({param_str})"
        # store the functions body
        body_lines = []

        # input sharing refresh
        for j, var in enumerate(var_names):
            for i in range(d+1):
                body_lines.append(f"\tint {var}_{i};\n")
                body_lines.append(f"\t{var}_{i}= reg({var}{i} ^ r{j});\n")
        
        # declaring temporary variables for intermidiate calculation
        temp_var_counter = 0  # Start from t1
        temp_vars = []  # Store temp variable names

        #  Allocate 2 * (2 ** len(var_names)) temp variables
        if n > 2:
            total_temps = (2 ** n) * (n-2);
        else:    
            total_temps = (2 ** n)
        for _ in range(total_temps):
            temp_vars.append(f"t{temp_var_counter}")
            temp_var_counter += 1
        body_lines.append("\n")
        body_lines.append("\tint " + ", ".join(temp_vars) + ";\n")
        body_lines.append("\n")
        counter = 0
        
        # declare c_{i}
        body_lines.append("\tint "+", ".join([f"c_{i}" for i in range(2 ** n)])+";\n")
        

        # a0 & a1
        for i in range(2 ** n):
            bit0 = (i >> 0) & 1
            bit1 = (i >> 1) & 1 # jth bit of i
            
            body_lines.append(f"\tt{counter} = {var_names[0]}_{bit0} & {var_names[1]}_{bit1};\n")
            counter += 1
            for j, var in enumerate(var_names):
                if j > 2:
                    bit = (i >> j) & 1
                    body_lines.append(f"\tt{counter} = t{counter-1} & {var_names[j]}_{bit};\n")
                    counter += 1
        #         if j > 0:
        #             body_lines.append(f"\tt{j} = t{j-1} & temp;\n")            
            body_lines.append(f"\tc_{i} = reg(t{counter-1} ^ r_{i});\n")
        
        # # output:
          # Start from t1
        temp_vars = []  # Store temp variable names

        # #  Allocate (d + 1) * (d + 1) temp variables
        total_temps = 2 ** n -2
        for _ in range(total_temps):
            temp_vars.append(f"t{temp_var_counter}")
            temp_var_counter += 1

        body_lines.append("\tint " + ", ".join(temp_vars) + ";\n")

        # temp_index = 0  # Track temp variable usage
        body_lines.append(f"\t{temp_vars[0]} = c_{0} ^ c_{1};\n")

        for i in  range(2, 2 ** n-1):
            body_lines.append(f"\tt{counter+1} = t{counter} ^ c_{i};\n")
            counter += 1
        body_lines.append(f"\t*{var_c}0 = t{counter} ^ c_{2 ** n - 1};\n")
        counter += 1
        temp_vars = []  # Store temp variable names

        # #  Allocate (d + 1) * (d + 1) temp variables
        total_temps = 2 ** n - 2
        for _ in range(total_temps):
            temp_vars.append(f"t{temp_var_counter}")
            temp_var_counter += 1
        body_lines.append("\n")
        body_lines.append("\tint " + ", ".join(temp_vars) + ";\n")
        body_lines.append("\n")
        # temp_index = 0  # Track temp variable usage
        body_lines.append(f"\t{temp_vars[0]} = r_{0} ^ r_{1};\n")

        for i in  range(2,2 ** n-1):
            body_lines.append(f"\tt{counter+1} = t{counter} ^ r_{i};\n")
            counter += 1
        body_lines.append(f"\t*{var_c}1 = reg(t{counter} ^ r_{2 ** n - 1});\n")
        # temp_index = 0  # Track temp variable usage
        # body_lines.append(f"\t{temp_vars[temp_index]} = 0;\n")
        # for i in  range(2 ** n -1):
        #     body_lines.append(f"\t{temp_vars[temp_index + 1]} = {temp_vars[temp_index]} ^ r_{i};\n")
        #     temp_index += 1
        # body_lines.append(f"\t*{var_c}1 = {temp_vars[temp_index]} ^ r_{2 ** n - 1};")


        body_lines.append("}")
        function_body = "".join(body_lines)
        return function_signature+ "{\n" + function_body
