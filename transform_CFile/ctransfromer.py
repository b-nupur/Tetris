from pycparser import c_ast, c_generator, c_parser
from copy import deepcopy

class ShareTransformer:
    def __init__(self, num_shares, gadget_expr_map, unique_gadget_def):
        self.num_shares = num_shares
        self.gadget_expr_map = gadget_expr_map  # rvalue string -> gadget spec
        self.generator = c_generator.CGenerator()
        self.injected_random_decls = set() # declarations to add once
        self.rand_counter = 0 
        self.comar_rand_added = False
        self.unique_gadget_def = unique_gadget_def


    def transform(self, node):
        method = f"transform_{type(node).__name__}"
        return getattr(self, method)(node)

    def transform_FileAST(self, node):
        assert len(node.ext) == 1 and isinstance(node.ext[0], c_ast.FuncDef), "Expected single function"
        
        transformed_top_level = self.transform(node.ext[0])
        gadget_funcdefs = []

        parser = c_parser.CParser()
        
        # adding all the function unique definition of unique definition 
        
        for gadget_name, func_str in self.unique_gadget_def.items():
            try:
                parsed = parser.parse(func_str)
                for ext_node in parsed.ext:
                    if isinstance(ext_node, c_ast.FuncDef):
                        gadget_funcdefs.append(ext_node)
            except Exception as e:
                print(f"[ERROR] : Failed to parse a definition of Function in unique definition {gadget_name}")
        node.ext = gadget_funcdefs + [transformed_top_level]
        return node

    def transform_FuncDef(self, node):
        # Transform function body first
        node.body = self.transform(node.body)

        # Ensure function has a ParamList
        if not node.decl.type.args:
            node.decl.type.args = c_ast.ParamList(params=[])

        original_params = node.decl.type.args.params
        new_params = []

        # split Share-wise 
        for param in original_params:
            if param.name.startswith("dec_"):
                new_params.append(param)  # leave dec_ untouched
            else:
                for i in range(self.num_shares):
                    new_param = deepcopy(param)
                    new_param.name = f"{param.name}_{i}"

                    # Rename inside TypeDecl or inside PtrDecl
                    typ = new_param.type
                    if isinstance(typ, c_ast.TypeDecl):
                        typ.declname = new_param.name
                    elif isinstance(typ, c_ast.PtrDecl) and isinstance(typ.type, c_ast.TypeDecl):
                        typ.type.declname = new_param.name

                    new_params.append(new_param)

        # Add rndomness parameters added as is
        print(f"adding random variables to the top module : {self.injected_random_decls}")
        for rand_id in self.injected_random_decls:
            param_decl = c_ast.Decl(
                name=rand_id.name,
                quals=[], storage=[], funcspec=[], align=None,
                type=c_ast.TypeDecl(
                    declname=rand_id.name,
                    quals=[], align=None,
                    type=c_ast.IdentifierType(['int'])
                ),
                init=None,
                bitsize=None
            )
            new_params.append(param_decl)

        # Final updated parameter list
        node.decl.type.args.params = new_params
        return node


    def transform_Compound(self, node):
        new_items = []

        # add gadget randomness declarations
        new_items.extend(self.injected_random_decls)
        self.injected_random_decls.clear()

        for stmt in node.block_items or []:
            result = self.transform(stmt)
            if isinstance(result, list):
                new_items.extend(result)
            elif result:
                new_items.append(result)

        return c_ast.Compound(block_items=new_items)

    def transform_Decl(self, node):
        if node.name.startswith("dec_"):
            return node

        decls = []
        for i in range(self.num_shares):
            new_decl = deepcopy(node)
            new_decl.name = f"{node.name}_{i}"
            if isinstance(new_decl.type, c_ast.TypeDecl):
                new_decl.type.declname = new_decl.name
            decls.append(new_decl)
        return decls

    def transform_Assignment(self, node):
        assign_str = self.generator.visit(node)

        # If this assignment node is in gadget_expr_map we replace it with function call
        if assign_str in self.gadget_expr_map:
            gadget = self.gadget_expr_map[assign_str]
            gadget_name = gadget["gadget_name"].lower()  # e.g., comar
            func_name = gadget["function_name"]          # e.g., Comar
            rand_count = gadget["random_numbers"]

            # Collecting operands for all shares
            binop = node.rvalue
            a_all = [self.rename_ids(deepcopy(binop.left), i) for i in range(self.num_shares)]
            b_all = [self.rename_ids(deepcopy(binop.right), i) for i in range(self.num_shares)]
            
            
            # append the rand args into the top level function
        
            print(f"Gadget name : {gadget_name}")
            if gadget_name == 'comar':
                rand_args = [c_ast.ID(f"{gadget_name}_r{j+1}") for j in range(rand_count)]
                # comar_rand_arg = rand_arg
                if self.comar_rand_added == False:
                    for rand_arg in rand_args:
                        self.injected_random_decls.add(rand_arg)
                    self.comar_rand_added = True
            else:
                rand_args = [c_ast.ID(f"rand_{j+1}") for j in range(self.rand_counter, self.rand_counter+rand_count)]
                self.rand_counter += rand_count

                for rand_arg in rand_args:
                    self.injected_random_decls.add(rand_arg)
                    
            print(f"comar rand added = {self.comar_rand_added}")


        

            if isinstance(node.lvalue, c_ast.ID):
                out_all = [
                    c_ast.UnaryOp(op='&', expr=c_ast.ID(f"{node.lvalue.name}_{i}"))
                    for i in range(self.num_shares)
                ]
                args = a_all + b_all + out_all + rand_args
            else:
                args = a_all + b_all + rand_args

            call = c_ast.FuncCall(
                name=c_ast.ID(func_name),
                args=c_ast.ExprList(args)
            )

            
            return call

        if isinstance(node.lvalue, c_ast.ID) and node.lvalue.name.startswith("dec_"):
            return node
        # Otherwise: share-wise transformation
        results = []

        for i in range(self.num_shares):
            new_assign = deepcopy(node)

            
            if isinstance(new_assign.lvalue, c_ast.ID):
                new_assign.lvalue.name = f"{new_assign.lvalue.name}_{i}"
            elif isinstance(new_assign.lvalue, c_ast.UnaryOp) and new_assign.lvalue.op == '*':
                inner = new_assign.lvalue.expr
                if isinstance(inner, c_ast.ID):
                    inner.name = f"{inner.name}_{i}"

            # RHS: rename with dec_ check
            new_assign.rvalue = self.rename_ids(new_assign.rvalue, i)

            results.append(new_assign)
        return results

    def rename_ids(self, node, i):
        if node is None:
            return None
        elif isinstance(node, c_ast.ID):
            if node.name.startswith("dec_"):
                return node
            node.name = f"{node.name}_{i}"
            return node
        else:
            for attr_name, child in node.children():
                if isinstance(child, c_ast.ID):
                    self.rename_ids(child, i)
                elif isinstance(child, c_ast.Node):
                    self.rename_ids(child, i)
                elif isinstance(child, list):
                    for elem in child:
                        if isinstance(elem, c_ast.Node):
                            self.rename_ids(elem, i)
            return node

