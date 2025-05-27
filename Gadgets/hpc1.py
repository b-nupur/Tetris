from Gadgets import Gadget

class HPC1(Gadget):

    """
        Implemention form Alogrithm1 : https://tches.iacr.org/index.php/TCHES/article/view/11942/11802
    """
    def __init__(self, d):
        """
        Initialise HPC1 with security order d (number of shares = d + 1)
        """
        super().__init__(d=d, random_required=0, latency=2, function_name=f"HPC1")

    
    def generate_multiply_function(self, var_a = "a", var_b = "b", var_c = "c"):
        """
        input:  [a0, a1, ..., ad]
                [b0, b1, ..., bd]
        output: [c0, c1, ..., cd]

        """
        d = self.d
        param_a = ", ".join([f"int {var_a}{i}" for i in range(d + 1)])
        param_b = ", ".join([f"int {var_b}{i}" for i in range(d + 1)])
        param_c = ", ".join([f"int* {var_c}{i}" for i in range(d + 1)])


        param_rand_list = [f"int r{i}" for i in range(d)]
        param_prand_list = [f"int p{i}{j}" for i in range(d) for j in range(i + 1, d + 1)]

        # Convert to string format
        param_rand = ", ".join(param_rand_list)
        param_prand = ", ".join(param_prand_list)

        # Count total random variables
        num_rand_vars = len(param_rand_list)
        num_prand_vars = len(param_prand_list)
        
        self.random = num_rand_vars + num_prand_vars
        self.latency = 2  # Set the latency for the HPC1 gadget

        param_str = f"{param_a}, {param_b}, {param_c}, {param_rand}, {param_prand}" # function parameter list 
        # # random number 
        helper_func = f"""

// {d} order secure hpc1 code 
// same domain term e.g. (bi = bi & ai)
void hpc1_same_shares_{d}_order(int a_share, int b_share, int rand, int * v_share) {{
    int b_share_;
    b_share_ = reg(b_share ^ rand);
    *v_share  = a_share & b_share_;
}}

// cross domain terms ( e.g., vij = ai & bj )
void hpc1_cross_domain_{d}_order(int a_share, int b_share, int * v_share, int rand, int prand){{

    //refresh sharing of b_share
    int b_share_;
    b_share_ = reg(b_share ^ rand);

    int a_and_b;
    a_and_b = a_share & b_share_;
    *v_share = a_and_b ^ prand;
}}

        """            # print(f"printing function signature for hpc1:\n {helper_func}")

        function_signature = f"void HPC1({param_str})"
        # print(f"printing function signature for hpc1:\n {function_signature}")
        # store the functions body
        body_lines = []

        # generating decalarations for u_ij
        body_lines.append(f"\t\tint {', '.join([f'v{i}{j}' for i in range(d + 1) for j in range(d+1)])};\n") 
        # body_lines.append(f"\t\tint {', '.join([f'v{i}{j}' for i in range(d + 1) for j in range(d+1) if i != j])};\n")
        body_lines.append(f"\t\tint r{d};\n")
        body_lines.append(f"\t\tr{d} = {' ^ '. join([f'r{i}' for i in range(d)])};\n")
        
        for i in range(d + 1):
            for j in range(d+1):
                if i == j:
                    body_lines.append(f"\t\thpc1_same_shares_{d}_order({var_a}{i}, {var_b}{i}, r{i}, &v{i}{i});\n")
                if i != j:
                    p_param = f"p{min(i, j)}{max(i, j)}"
                    body_lines.append(f"\t\thpc1_cross_domain_{d}_order({var_a}{i}, {var_b}{j}, &v{i}{j} , r{j}, {p_param});\n")

    
        temp_var_counter = 1  # Start from t1
        temp_vars = []  # Store temp variable names

        #  Allocate (d + 1) * (d + 1) temp variables
        if d > 1:
            total_temps = (d - 1) * (d + 1)
            for _ in range(total_temps):
                temp_vars.append(f"t{temp_var_counter}")
                temp_var_counter += 1

            # Declare all temp variables at once
            body_lines.append("\n\t\tint " + ", ".join(temp_vars) + ";\n\n")

        temp_index = 0  # Track temp variable usage

        for i in range(d + 1):
            # Initialize the first temp variable
            if d == 1:
                body_lines.append(f"\t\t*{var_c}{i} = reg(v{i}{0} ^ v{i}{1});\n")
            else:
                body_lines.append(f"\t\t{temp_vars[temp_index]} = v{i}{0} ^ v{i}{1};\n")

                for j in range(2, d):
                    body_lines.append(f"\t\t{temp_vars[temp_index + 1]} = {temp_vars[temp_index]} ^ v{i}{j};\n")
                    temp_index += 1  # Move to next temp variable

                # Final XOR step directly assigns to *c{i}
                body_lines.append(f"\t\t*{var_c}{i} = reg({temp_vars[temp_index]} ^ v{i}{d});\n\n")
                temp_index += 1  # Move to next temp variable for the next iteration

        
        # for i in range(d + 1):
        #     body_lines.append(f"\t\t*{var_c}{i} = 0;\n")
        #     for j in range(d + 1):
        #         body_lines.append(f"\t\t*{var_c}{i} = *{var_c}{i} ^ v{i}{j};\n ")
                                
        body_lines.append("}")
        return [helper_func] +["\n"]+[function_signature]+ ["{\n"] + body_lines
