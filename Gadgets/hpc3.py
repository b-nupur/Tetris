from Gadgets import Gadget

class HPC3(Gadget):
    def __init__(self, d):
        super().__init__(d=d, random_required=0, latency=1, function_name=f"HPC3")


    def generate_multiply_function(self, var_a= "a", var_b= "b", var_c= "c"):
        """
        input:  [a0, a1, ..., ad]
                [b0, b1, ..., bd]
        output: [c0, c1, ..., cd]


        we need to multiply a and b and output is c

        """
        d = self.d
        param_a = ", ".join([f"int {var_a}{i}" for i in range(d + 1)])
        param_b = ", ".join([f"int {var_b}{i}" for i in range(d + 1)])
        param_c = ", ".join([f"int* {var_c}{i}" for i in range(d + 1)])
        # param_rand = ", ".join([f"int r{i}{j}" for i in range(d) for j in range(i + 1, d + 1)]) 
        # param_prand = ", ".join([f"int p{i}{j}" for i in range(d) for j in range(i + 1, d + 1)]) 
        param_rand_list = []
        param_prand_list = []

        # Generate param_rand and param_prand in a single loop
        for i in range(d):
            for j in range(i + 1, d + 1):
                param_rand_list.append(f"int r{i}{j}")
                param_prand_list.append(f"int p{i}{j}")

        # Convert lists to comma-separated strings
        param_rand = ", ".join(param_rand_list)
        param_prand = ", ".join(param_prand_list)

        # Assign total random variables count
        self.random_required = len(param_rand_list) + len(param_prand_list)
        
        # print(f"random required : {self.random_required}") 
        param_str = f"{param_a}, {param_b}, {param_c}, {param_rand}, {param_prand}" # function parameter list 
        # print(f"param str : {param_str}")
        
        
        helper_func = f"""
void hpc3_same_shares_{self.d}_order(int a_share, int b_share, int * u_share) {{
    * u_share  = reg(a_share & b_share);
}}

void hpc3_v_{self.d}_order(int a_share, int b_share, int * v_share, int rand){{
    int temp;
    temp = reg(b_share ^ rand);
    int a_share_reg;
	a_share_reg = reg(a_share);
    *v_share = temp & a_share_reg;
}}

void hpc3_w_{self.d}_order(int a_share, int rand, int prand, int * w_share){{
    int temp;
    int a_share_neg;
    a_share_neg = ~(a_share);
    temp = a_share_neg & rand;
    *w_share = reg(temp ^ prand);
}}

void hpc3_xor_vw_{self.d}_order(int v_share, int w_share, int * u_share){{
    *u_share = v_share ^ w_share;
}}


"""
        # void multiply_different(int a_share, int b_share, int & u_share, int rand, int prand){{
        #     int v_share, w_share;
        #     hpc3_v(a_share, b_share, &v_share, rand);
        #     hpc3_w(a_share, rand, prand, &w_share);
        #     *u_share = v_share ^ w_share;
        # }}
        function_signature = f"void HPC3({param_str})"
        
        
        # store the functions body
        body_lines = []

        # generating decalarations for u_ij
        body_lines.append(f"\tint {', '.join([f'u{i}{j}' for i in range(d + 1) for j in range(d+1)])};\n") 
        body_lines.append(f"\tint {', '.join([f'v{i}{j}' for i in range(d + 1) for j in range(d+1) if i != j])};\n")
        body_lines.append(f"\tint {', '.join([f'w{i}{j}' for i in range(d + 1) for j in range(d+1) if i != j])};\n\n")
        for i in range(d + 1):
            for j in range(d+1):
                if i == j:
                    body_lines.append(f"\thpc3_same_shares_{d}_order({var_a}{i}, {var_b}{i}, &u{i}{i});\n\n")
                if i != j:

                    p_param = f"p{min(i, j)}{max(i, j)}"
                    r_param = f"r{min(i, j)}{max(i, j)}"
        
                    body_lines.append(f"\thpc3_v_{self.d}_order({var_a}{i}, {var_b}{j}, &v{i}{j} , {r_param});\n")

                    body_lines.append(f"\thpc3_w_{self.d}_order({var_a}{i}, {r_param}, {p_param}, &w{i}{j});\n")

                    body_lines.append(f"\thpc3_xor_vw_{self.d}_order(v{i}{j}, w{i}{j}, &u{i}{j});\n\n")
        
        
        # for i in range(d + 1):
        #     body_lines.append(f"\t*{var_c}{i} = 0;\n")
        #     for j in range(d + 1):
        #         body_lines.append(f"\t*{var_c}{i} = *{var_c}{i} ^ u{i}{j};\n ")

        temp_var_counter = 1  # Start from t1
        temp_vars = []  # Store temp variable names

        #  Allocate (d + 1) * (d + 1) temp variables
        if d > 1:
            total_temps = (d - 1) * (d + 1)
            for _ in range(total_temps):
                temp_vars.append(f"t{temp_var_counter}")
                temp_var_counter += 1

            # Declare all temp variables at once
            body_lines.append("\tint " + ", ".join(temp_vars) + ";\n")

        temp_index = 0  # Track temp variable usage

        for i in range(d + 1):
            # Initialize the first temp variable
            if d == 1:
                body_lines.append(f"\t*{var_c}{i} = u{i}{0} ^ u{i}{1};\n")
            else:
                body_lines.append(f"\t{temp_vars[temp_index]} = u{i}{0} ^ u{i}{1};\n")

                for j in range(2, d):
                    body_lines.append(f"\t{temp_vars[temp_index + 1]} = {temp_vars[temp_index]} ^ u{i}{j};\n")
                    temp_index += 1  # Move to next temp variable

                # Final XOR step directly assigns to *c{i}
                body_lines.append(f"\t*{var_c}{i} = {temp_vars[temp_index]} ^ u{i}{d};\n\n")
                temp_index += 1  # Move to next temp variable for the next iteration


                                
        body_lines.append("}")
        function_body = "{\n" + "".join(body_lines)
        return helper_func +function_signature+ function_body
