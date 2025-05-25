from Gadgets import Gadget

class Domand(Gadget):
    def __init__(self, d):
        super().__init__(d=d, random_required=0, latency=2, function_name=f"Domand")
    
    
    def generate_multiply_function(self, var_a = "a", var_b = "b", var_c = "c"):
        d = self.d
        
        param_a = ", ".join([f"int {var_a}{i}" for i in range(d + 1)])
        param_b = ", ".join([f"int {var_b}{i}" for i in range(d + 1)])
        param_c = ", ".join([f"int * {var_c}{i}" for i in range(d + 1)])
        # param_rand = ", ".join([f"int r{i}" for i in range(d+1)])
        param_rand = []
        # The upper limit for i and j is d. So range(d + 1) gives 0, 1, ..., d
        # The outer loop for i
        for i in range(d + 1):  # i goes from 0 to d
            # The inner loop for j, starting from i+1 to ensure i < j
            for j in range(i + 1, d + 1): # j goes from i+1 to d
                param_rand.append(f"int r{i}{j}")
        param_rand = ", ".join(param_rand)  # Convert list to string
        param_str = f"{param_a}, {param_b}, {param_c}, {param_rand}" # function parameter list 
        self.random_required = len(param_rand)
        function_signature = f"void Domand({param_str})"

        body_lines = []
        temp_counter = 0
        i_counter = 0
        rand_counter = 0
        # declare temp varibales used 

        body_lines.append(f"\t\tint {', '.join([f't{i}' for i in range((d + 1) * (d + 1))])};\n") 
        body_lines.append(f"\t\tint {', '.join([f'i{i}' for i in range((d + 1) * (d + 1) - (d + 1))])};\n\n") 
        
        for i in range(d + 1):
            rand_counter = 0
            for j in range(d + 1):
                body_lines.append(f"\t\tt{temp_counter} = {var_a}{i} & {var_b}{j};\n")
                temp_counter += 1
                if i != j:
                    body_lines.append(f"\t\ti{i_counter} = t{temp_counter-1} ^ r{min(i, j)}{max(i,j)};\n")
                    i_counter += 1
                    rand_counter += 1
            body_lines.append("\n")


        # number of shares = d + 1
      
        i_counter = 0

        if d == 1:
            body_lines.append(f"\t\t*{var_c}{0} = reg(i0) ^ t{(d+1)*i + i};\n")
            body_lines.append(f"\t\t*{var_c}{1} = reg(i1) ^ t{(d+1)*i + i};\n")
            return [function_signature]+ ["{\n"] + body_lines
        
        for i in range(d+1):
            body_lines.append(f"\t\tint t{temp_counter} = 0;\n")
            body_lines.append(f"\t\tt{temp_counter} = reg(i{i_counter}) ^ reg(i{i_counter+1});\n ")
            i_counter += 2
            temp_counter += 1

            for j in range(d-2):

                body_lines.append(f"\t\tint t{temp_counter} = 0;\n")
                body_lines.append(f"\t\tt{temp_counter} = t{temp_counter-1} ^ reg(i{i_counter});\n ")
                i_counter += 1
            body_lines.append(f"\t\t*{var_c}{i} = t{temp_counter-1} ^ t{(d+1)*i + i};\n\n ")

        body_lines.append("}")
        return [function_signature]+ ["{\n"] + body_lines