from Gadgets import Gadget

class HPC2(Gadget):
    def __init__(self, d):
        super().__init__(d=d, random_required=0, latency=2, function_name=f"HPC2")

    
    def generate_multiply_function(self, var_a = "a", var_b = "b", var_c = "c"):
        """
        input:  [a0, a1, ..., ad]
                [b0, b1, ..., bd]
        output: [c0, c1, ..., cd]

        """
        d = self.d
        param_a = ", ".join([f"int {var_a}{i}" for i in range(d + 1)])
        param_b = ", ".join([f"int {var_b}{i}" for i in range(d + 1)])
        param_c = ", ".join([f"int * {var_c}{i}" for i in range(d + 1)])

        param_rand_list = []
        for i in range(d):
            for j in range(i + 1, d + 1):
                param_rand_list.append(f"int r{i}{j}")
                self.random_required += 1  # Increment the counter

        param_rand = ", ".join(param_rand_list)  # Convert list to string
        # print(f"random required HPC2 : {self.random_required}")
        # param_rand = ", ".join([f"int r{i}{j}" for i in range(d) for j in range(i + 1, d + 1)])

        param_str = f"{param_a}, {param_b}, {param_c}, {param_rand}" # function parameter list 
        # random number 

        # latency = 2 for HPC2
        self.latency = 2  # Set the latency for the HPC2 gadget
        helper_func = f"""
void hpc2_same_shares_{d}_order(int a_share, int b_share, int * u_share) {{
    int b_share_reg;
	b_share_reg = reg(b_share);
	* u_share  = reg(a_share & b_share_reg);
}}

void hpc2_v_{d}_order(int a_share, int b_share, int * v_share, int rand){{
    int temp; 
    temp = reg(b_share ^ rand);
    *v_share = reg(temp & a_share);
}}

void hpc2_w_{d}_order(int a_share, int rand, int *  w_share){{
    int rand_reg;
	rand_reg = reg(rand);
	int a_neg;
    a_neg = ~(a_share);
    *w_share = reg(a_neg & rand_reg);
}}

void hpc2_xor_vw_{d}_order(int v_share, int w_share, int * u_share){{
    *u_share = v_share ^ w_share;
}}

"""
        # void multiply_different(int a_share, int b_share, int & u_share, int rand, int prand){{
        #     int v_share, w_share;
        #     hpc3_v(a_share, b_share, &v_share, rand);
        #     hpc3_w(a_share, rand, prand, &w_share);
        #     *u_share = v_share ^ w_share;
        # }}
        function_signature = f"void HPC2({param_str})"
        # store the functions body
        body_lines = []

        # generating decalarations for u_ij
        body_lines.append(f"\tint {', '.join([f'u{i}{j}' for i in range(d + 1) for j in range(d+1)])};\n") 
        body_lines.append(f"\tint {', '.join([f'v{i}{j}' for i in range(d + 1) for j in range(d+1) if i != j])};\n\n")
        body_lines.append(f"\tint {', '.join([f'w{i}{j}' for i in range(d + 1) for j in range(d+1) if i != j])};\n\n")
        for i in range(d + 1):
            for j in range(d+1):
                if i == j:
                    body_lines.append(f"\thpc2_same_shares_{d}_order({var_a}{i}, {var_b}{i}, &u{i}{i});\n")
                if i != j:
                    r_param = f"r{min(i, j)}{max(i, j)}"
                    body_lines.append(f"\thpc2_v_{d}_order({var_a}{i}, {var_b}{j}, &v{i}{j} , {r_param});\n")

                    body_lines.append(f"\thpc2_w_{d}_order({var_a}{i}, {r_param}, &w{i}{j});\n")

                    body_lines.append(f"\thpc2_xor_vw_{d}_order(v{i}{j}, w{i}{j}, &u{i}{j});\n\n")

        temp_var_counter = 1  # Start from t1
        temp_vars = []  # Store temp variable names

        #  Allocate (d + 1) * (d + 1) temp variables
        if d > 1:
            total_temps = (d - 1) * (d + 1)
            for _ in range(total_temps):
                temp_vars.append(f"t{temp_var_counter}")
                temp_var_counter += 1

            # Declare all temp variables at once
            body_lines.append("\tint " + ", ".join(temp_vars) + ";\n\n")

        temp_index = 0  # Track temp variable usage

        for i in range(d + 1):
            # Initialize the first temp variable
            if d == 1:
                body_lines.append(f"\t*{var_c}{i} = u{i}{0} ^ u{i}{1};\n")
            else:
                body_lines.append(f"\t{temp_vars[temp_index]} = u{i}{0} ^ u{i}{1};\n")

                for j in range(2,d):
                    body_lines.append(f"\t{temp_vars[temp_index + 1]} = {temp_vars[temp_index]} ^ u{i}{j};\n")
                    temp_index += 1  # Move to next temp variable

                # Final XOR step directly assigns to *c{i}
                body_lines.append(f"\t*{var_c}{i} = {temp_vars[temp_index]} ^ u{i}{d};\n\n")
                temp_index += 1  # Move to next temp variable for the next iteration

        # for i in range(d + 1):
        #     body_lines.append(f"\t\t*{var_c}{i} = 0;\n")
        #     for j in range(d + 1):
        #         body_lines.append(f"\t\t*{var_c}{i} = *{var_c}{i} ^ u{i}{j};\n ")

        body_lines.append("}")
        function_body = "{\n" + "".join(body_lines)
        return helper_func + function_signature + function_body

