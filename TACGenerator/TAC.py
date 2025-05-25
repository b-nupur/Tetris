from pycparser import c_ast
import copy
from pycparser import c_parser, c_generator
class TempVarGen:
    def __init__(self):
        self.count = 0
    
    def reset(self):
        self.count = 0

    def new_temp(self):
        name = f"temp_var_{self.count}"
        self.count += 1
        return name

class TACStyleASTBuilder:
   # no need to refactor 
    def __init__(self):
        self.temp_gen = TempVarGen()
        self.func_return_types = {}
        self.var_datatypes = {}
        self.func_parameter_type = {}
        self.scope_stack = [{}]  # stack of variable -> versioned name per scope
        self.suppress_scope = False
        self.for_loop_var = {}

    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        self.scope_stack.pop()

    def get_latest_name(self, var):
        for scope in reversed(self.scope_stack):
            if var in scope:
                return scope[var]
        return var

    # _1_version_x
    def transform_ID(self, node):
        curr_name = node.name
        if curr_name in self.for_loop_var:
            curr_name = self.for_loop_var[curr_name]
        node.name = self.get_previous_name(self.get_latest_name(curr_name), curr_name)
        return node

    def get_previous_name(Self, latest_name, original_Var):
        # we will only call this function when latest_name is not equal to the original name
        # so var will always have the form var = _{i}_version_{original var name}
        # return previous will be _{i-1}_version_{orginal var name} 
        # but if latest is _1_version_{original var name} then we need to return original_var_name
        if latest_name == original_Var:
            return original_Var
        # parse the version index: _{i}_version_{var}
        try:
            parts = latest_name.split('_', 3)  # ['','1','version_x']
            version = int(parts[1])
            base_name = parts[3]
            

            if version == 1:
                return base_name
            else:
                return f"_{version - 1}_version_{base_name}"
        except Exception as e:
            raise ValueError(f"Invalid version format in variable name: {latest_name}")
               
    def get_new_name(self, var):
        latest = self.get_latest_name(var)
        if latest == var:
            version = 1
        else:
            try:
                version = int(latest.split('_')[1]) + 1
            except:
                version = 1

        new_name = f"_{version}_version_{var}"
        self.scope_stack[-1][var] = new_name
        return new_name

    def get_return_type(self, func_name):
        return self.func_return_types.get(func_name, 'int')
    
    def transform(self, node):
        method = f"transform_{type(node).__name__}"
        return getattr(self, method, self.generic_transform)(node)
    
    def get_expr_type(self, expr):
        if isinstance(expr, c_ast.ID):
            return self.var_datatypes.get(expr.name, 'int')
        elif isinstance(expr, c_ast.Constant):
            # constant ka type field check karo, jaise 'int', 'float', 'char', 'bool'
            if expr.type == 'float':
                return 'float'
            elif expr.type == 'int':
                return 'int'
            elif expr.type == 'char':
                return 'char'
            elif expr.type == '_Bool':
                return '_Bool'
            elif expr.type == 'long':
                return 'long'
            elif expr.type == 'short':
                return 'short'
            elif expr.type == 'double':
                return 'double'
            elif expr.type == 'long double':
                return 'long double'
            else:
                return 'int'  # default fallback
        elif isinstance(expr, c_ast.FuncCall):
            return self.get_return_type(expr.name.name)
        else:
            return 'int'  # default fallback

    def promote_types(self, type1, type2):
        type_priority = {
            '_Bool': 0,
            'char': 1,
            'short': 1,
            'int': 1,
            'long': 1,
            'long long': 1,
            'float': 2,
            'double': 3,
            'long double': 4
        }

        priority1 = type_priority.get(type1, 1)  # default to int if unknown
        priority2 = type_priority.get(type2, 1)

        if priority1 > priority2:
            return type1
        else:
            return type2

    def transform_Compound(self, node):

        # self.push_scope()

        new_items = []
        for stmt in node.block_items or []:
            result = self.transform(stmt)
            if isinstance(result, list):
                new_items.extend(result)
            elif result:
                new_items.append(result)

        # print(f"poping scope : {self.scope_stack[-1]}")
        # if self.suppress_scope == False:
        #     self.pop_scope()
        # self.pop_scope()
        return c_ast.Compound(block_items=new_items)

    def transform_Return(self, node):
        expr = node.expr

        if isinstance(expr, c_ast.BinaryOp):
            stmts, final_expr = self.flatten_binary_expr(expr, top_level=True)
        elif isinstance(expr, c_ast.FuncCall):
            stmts, final_expr = self.handle_func_call_in_binary(expr)
        elif isinstance(expr, c_ast.ID):
            stmts = []

            final_expr = self.transform_ID(expr)
        else:
            stmts, final_expr = [], expr

        assign = c_ast.Assignment(
            op='=',
            lvalue=c_ast.UnaryOp(op='*', expr=c_ast.ID(name='__return_value')),
            rvalue=final_expr
        )
        return stmts + [assign]
  
    
    def transform_FuncCall(self, node):
        """
        Transform function calls to TAC style.
        Returns: 
        - If top-level call: returns the transformed call
        - If nested call: returns (statements, temp_var_reference)
        """
        # print(f"transforming function call:\n{node}")
        new_stmts = []
        new_args = []
        
        # Transform all arguments
        if node.args and node.args.exprs:

            for arg in node.args.exprs:
                if isinstance(arg, c_ast.BinaryOp):
                    result, var = self.flatten_binary_expr(arg, top_level=False)
                    # print(result)
                    # print(var)
                    new_stmts.extend(result)
                    new_args.append(var)

                elif isinstance(arg, c_ast.FuncCall):
                    # Handle nested function call
                    nested_stmts, temp_var = self.process_nested_func_call(arg)
                    new_stmts.extend(nested_stmts)
                    new_args.append(temp_var)
                else:
                    transformed = self.transform(arg)
                    if isinstance(transformed, list):
                        new_stmts.extend(transformed[:-1])
                        new_args.append(transformed[-1])
                    else:
                        new_args.append(transformed)

        # Create the transformed call
        # print(f"new_args: {new_args}/n ------------")

        new_call = c_ast.FuncCall(
            name=node.name,
            args=c_ast.ExprList(exprs=new_args) if new_args else None
        )
        # For top-level calls, just return the call
        if not new_stmts:

            # print(f"returning new call : {new_call}")
            # print(f"new_stmts : {new_stmts}")
            return new_call
            
        # For nested calls, return statements + call
        return new_stmts, new_call
    
    class IndexReplacer:
        def __init__(self, var_name, const_value, rename_all_vars=True):
            self.var_name = var_name
            self.const_value = const_value
            self.rename_all_vars = rename_all_vars
            self.generated_vars = set() 

        def visit(self, node):
            if node is None:
                return None

            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)


        def visit_ArrayRef(self, node):
            # Process array index (subscript)
            new_index = self.visit(node.subscript)

            return c_ast.ArrayRef(
                name=node.name,            # keep array base (e.g., c) unchanged
                subscript=new_index        # replace index like i → 0, 1, etc.
            )

        
        def visit_ID(self, node):
            if node.name == self.var_name:
                return c_ast.Constant(type='int', value=str(self.const_value))
            elif self.rename_all_vars:
                rename = name=f"_{self.const_value}_{node.name}"
                self.generated_vars.add(rename)
                return c_ast.ID(rename)
            return node


        # import copy

        def generic_visit(self, node):
            new_node = copy.deepcopy(node)  # create new copy to avoid in-place modification

            for attr in node.__slots__:
                val = getattr(new_node, attr)

                if isinstance(val, c_ast.Node):
                    setattr(new_node, attr, self.visit(val))

                elif isinstance(val, list):
                    new_list = []
                    for item in val:
                        if isinstance(item, c_ast.Node):
                            new_list.append(self.visit(item))
                        else:
                            new_list.append(item)
                    setattr(new_node, attr, new_list)

            return new_node
    
    def generic_transform(self, node):
        return node
 
    def create_temp_variable(self, type):
        temp_name = self.temp_gen.new_temp()
        # type = self.get_return_type(func_node.name.name)

        # Update datatype map
        self.var_datatypes[temp_name] = type

        temp_decl = c_ast.Decl(
            name=temp_name,
            quals=[], storage=[], funcspec=[], align=None,
            type=c_ast.TypeDecl(
                declname=temp_name, quals=[], align=None,
                type=c_ast.IdentifierType([type])
            ),
            init=None, bitsize=None
        )
        return temp_name, temp_decl

    def transform_Decl(self, node):
            # add the variable and its data type in map
            type_name = node.type.type.names[0]
            self.var_datatypes[node.name] = node.type.type.names[0]

            # store the variable in scope stack to check if it is reassigned or not
            
            if node.init is None:
                self.scope_stack[-1][node.name] = node.name 
            else:
                new_name = self.get_new_name(node.name)
                

            # process the initialisation of decl node
            if isinstance(node.init, c_ast.BinaryOp):
                # process the binary expression and transform it into tac
                # ex:  int a = b + c * d;
                # int a;
                # int t0;
                # t0 = c * d;
                # a = b + t0;
    
                
                stmts, final_expr = self.flatten_binary_expr(node.init, top_level=True)
                new_decl = c_ast.Decl(
                    name=node.name,
                    quals=[],
                    storage=[],
                    funcspec=[],
                    align=None,
                    type=c_ast.TypeDecl(
                        declname=node.name,
                        quals=[],
                        align=None,
                        type=copy.deepcopy(node.type.type)                ),
                    init=None,
                    bitsize=None
                )
                assign = c_ast.Assignment(
                    op='=',
                    lvalue=c_ast.ID(name=node.name),
                    rvalue=final_expr
                )
                return stmts + [new_decl, assign]
            
            elif isinstance(node.init, c_ast.FuncCall):
                
                result = self.transform_FuncCall(node.init)
                if isinstance(result, tuple):
                    func_stmts, new_func_call = result
                else:
                    func_stmts = []
                    new_func_call = result

                temp_name = node.name  # jaise int x = foo(...);

            
                new_decl = c_ast.Decl(
                    name=temp_name,
                    quals=[], storage=[], funcspec=[], align=None,
                    type=c_ast.TypeDecl(
                        declname=temp_name, quals=[], align=None,
                        type=copy.deepcopy(node.type.type),
                    ),
                    init=None,
                    bitsize=None
                )

                
                new_func_call.args.exprs.append(
                    c_ast.UnaryOp(op='&', expr=c_ast.ID(name=temp_name))
                )

                return func_stmts + [new_decl, new_func_call]
            elif isinstance(node.init, c_ast.ID):
                new_decl = c_ast.Decl(
                    name=node.name,
                    quals=[],
                    storage=[],
                    funcspec=[],
                    align=None,
                    type=c_ast.TypeDecl(
                        declname=node.name,
                        quals=[],
                        align=None,
                        type=copy.deepcopy(node.type.type)                ),
                    init=None,
                    bitsize=None
                )
                assign = c_ast.Assignment(
                    op='=',
                    lvalue=c_ast.ID(name=node.name),
                    rvalue=node.init
                )
                return [new_decl, assign]
            elif isinstance(node.init, c_ast.Constant):
                new_decl = c_ast.Decl(
                    name=node.name,
                    quals=[],
                    storage=[],
                    funcspec=[],
                    align=None,
                    type=c_ast.TypeDecl(
                        declname=node.name,
                        quals=[],
                        align=None,
                        type=copy.deepcopy(node.type.type)                ),
                    init=None,
                    bitsize=None
                )
                assign = c_ast.Assignment(
                    op='=',
                    lvalue=c_ast.ID(name=node.name),
                    rvalue=node.init
                )
                return [new_decl, assign]
            else:
                result = self.transform(node.init)

            return node


    def transform_FuncDef(self, node):
            # reset for each function
            self.push_scope()
            self.temp_gen.reset()
            # for var in self.var_datatypes:
            #     print(f"var name : {var} type : {self.var_datatypes[var]}")
            # print(f"function name : {node.decl.name}")
            # print("======================================")
            self.var_datatypes = {}

            func_name = node.decl.name
            return_type = node.decl.type.type.type
            

            # print(f"visiting function  {node.decl.name} return type : {return_type}")

            if isinstance(return_type, c_ast.IdentifierType) and return_type.names != ['void']:
                # Add int *__return_value parameter
                
                self.func_return_types[func_name] = return_type.names[0]
                # print(f"return type is not void")
                node.decl.type.type.type = c_ast.IdentifierType(names=['void'])

                return_ptr_param = c_ast.Decl(
                    name='__return_value',
                    quals=[], storage=[], funcspec=[], align=None,
                    type=c_ast.PtrDecl(
                        quals=[],
                        type=c_ast.TypeDecl(
                            declname='__return_value', quals=[], align=None,
                            type=return_type
                        )
                    ),
                    init=None, bitsize=None
                )

                # Append new param
                if node.decl.type.args:
                    node.decl.type.args.params.append(return_ptr_param)
                else:
                    node.decl.type.args = c_ast.ParamList(params=[return_ptr_param])
                    
            # adding parameter types to the var_datatypes map
            if node.decl.type.args:
                for param in node.decl.type.args.params:
                    if isinstance(param.type, c_ast.PtrDecl):
                        self.var_datatypes[param.name] = param.type.type.type.names[0]+'*'
                        
                        # print(f"param name : {param.name} type : {self.var_datatypes[param.name]}")
                    elif isinstance(param.type, c_ast.TypeDecl):
                        self.var_datatypes[param.name] = param.type.type.names[0]
                        self.scope_stack[-1][param.name] = param.name 
                        
                        # print(f"param name : {param.name} type : {self.var_datatypes[param.name]}")
                # Replace any `return expr;` with `*__return_value = expr;`
            # body = self.transform_return_rewrite(node.body)
            result_ = c_ast.FuncDef(decl=node.decl, param_decls=node.param_decls, body=self.transform(node.body))
            self.pop_scope()
            return result_

    def decl_if_reassigned(self, lhs_name, latest_name):
        """
            return a Decl node if varible is reassigned
            Note: varaible will be reassigned inside a assignemnet node only
            so it is suffice to declare and add it to var_datatype only here  
        """
        if lhs_name == latest_name:
            return None
        
        var_type = self.get_expr_type(lhs_name)
        self.var_datatypes[latest_name] = var_type
        return c_ast.Decl(
            name=latest_name,
            quals=[], storage=[], funcspec=[], align=None,
            type=c_ast.TypeDecl(
                declname=latest_name,
                quals=[], align=None,
                type=c_ast.IdentifierType([var_type])
            ),
            init=None,
            bitsize=None
        )

    def transform_Assignment(self, node):

        # Expand compound assignments
        compound_ops = {
            '+=': '+',
            '-=': '-',
            '*=': '*',
            '/=': '/',
            '%=': '%',
            '<<=': '<<',
            '>>=': '>>',
            '&=': '&',
            '|=': '|',
            '^=': '^'
        }

        if node.op in compound_ops:
            # convert a += b * c  -> a = a + b * c
            # print("processing compound node")
            stmts, final_expr = self.flatten_binary_expr(node.rvalue, top_level=False)

            latest_name = self.get_latest_name(node.lvalue.name)
            

            # instead of this add it to the latest_name wala node
            temp_assign = c_ast.Assignment(
                op = '=',
                lvalue = c_ast.ID(name=latest_name),
                rvalue=c_ast.BinaryOp(
                    op=compound_ops[node.op],
                    left=c_ast.ID(self.get_previous_name(latest_name,node.lvalue.name)),
                    right=final_expr
                )
            )
            decl = self.decl_if_reassigned(node.lvalue.name, latest_name)
            if decl:
                self.get_new_name(node.lvalue.name)
                return stmts + [decl, temp_assign]

            self.get_new_name(node.lvalue.name)

            return stmts + [temp_assign]
            
       
        
        if isinstance(node.rvalue, c_ast.BinaryOp):
            stmts, final_expr = self.flatten_binary_expr(node.rvalue, top_level=True)
            # print(node.lvalue)
            if isinstance(node.lvalue, c_ast.UnaryOp):
                assign = c_ast.Assignment(
                    op = node.op,
                    lvalue=node.lvalue,
                    rvalue = final_expr
                )
                
                return stmts + [assign]
            
            latest_name = self.get_latest_name(node.lvalue.name)

            
            assign = c_ast.Assignment(
                op=node.op,
                lvalue=c_ast.ID(name=latest_name),
                rvalue=final_expr
            )

            decl = self.decl_if_reassigned(node.lvalue.name, latest_name)
            if decl:
                self.get_new_name(node.lvalue.name)
                return stmts +[decl, assign]

            self.get_new_name(node.lvalue.name)
            return stmts + [assign]
        elif isinstance(node.rvalue, c_ast.FuncCall):

            result = self.transform_FuncCall(node.rvalue)
            if isinstance(result, tuple):
                func_stmts, new_func_call = result
            else:
                func_stmts = []
                new_func_call = result
            # print(f"transforming node : {node.rvalue} to {new_func_call}")
            latest_name = self.get_latest_name(node.lvalue.name)  # jaise x = foo(...);
            decl = self.decl_if_reassigned(node.lvalue.name, latest_name)
            new_func_call.args.exprs.append(
                c_ast.UnaryOp(op='&', expr=c_ast.ID(name=latest_name))
            )
            if decl:
                self.get_new_name(node.lvalue.name)
                return func_stmts + [decl, new_func_call]
            # Last add &x

            self.get_new_name(node.lvalue.name)
            return func_stmts + [new_func_call]
        else:
            latest_name = self.get_latest_name(node.lvalue.name)
            decl = self.decl_if_reassigned(node.lvalue.name, latest_name)
            if decl:
                self.get_new_name(node.lvalue.name)
                return stmts +[decl, assign]

            self.get_new_name(node.lvalue.name)
            
        return node
    
    def handle_func_call_in_binary(self, func_node):
        result = self.transform_FuncCall(func_node)
        if isinstance(result, tuple):
            func_stmts, func_call = result
        else:
            func_stmts = []
            func_call = result

        return_type = self.get_return_type(func_node.name.name)

        temp_name, temp_decl = self.create_temp_variable(return_type)
        # Add &temp_name as argument
        func_call.args.exprs.append(
            c_ast.UnaryOp(op='&', expr=c_ast.ID(name=temp_name))
        )

        return func_stmts + [temp_decl, func_call], c_ast.ID(name=temp_name)
    
    def flatten_binary_expr(self, expr, top_level=True):
        # print(f"falttening binary expression \\n {expr}")
        new_stmts = []
        if not isinstance(expr, c_ast.BinaryOp):
            return [], expr
        # Process Left side
        if isinstance(expr.left, c_ast.BinaryOp):
            left_stmts, left_expr = self.flatten_binary_expr(expr.left, top_level=False)
            new_stmts.extend(left_stmts)
        elif isinstance(expr.left, c_ast.FuncCall):
            stmts, left_expr = self.handle_func_call_in_binary(expr.left)
            new_stmts.extend(stmts)
        else:
            if isinstance(expr.left, c_ast.ID):
                var_name = expr.left.name
                latest_name = self.get_latest_name(var_name)
                # print(f" latest_name : {latest_name}")
                # it must have been declarred before we need to use the latest value so we figure it out using 
                # get_previous_name 
                prev_version = self.get_previous_name(latest_name, var_name)
                # print(f"prev_version {prev_version}")
                left_expr = c_ast.ID(name=prev_version)
            else:
                left_expr = expr.left

        # Process Right side
        if isinstance(expr.right, c_ast.BinaryOp):
            right_stmts, right_expr = self.flatten_binary_expr(expr.right, top_level=False)
            new_stmts.extend(right_stmts)
        elif isinstance(expr.right, c_ast.FuncCall):
            stmts, right_expr = self.handle_func_call_in_binary(expr.right)
            new_stmts.extend(stmts)
        else:
            if isinstance(expr.right, c_ast.ID):
                var_name = expr.right.name
                latest_name = self.get_latest_name(var_name)
                # print(f" latest_name : {latest_name}")
                prev_version = self.get_previous_name(latest_name, var_name)
                # print(f"prev_version {prev_version}")
                right_expr = c_ast.ID(name=prev_version)
            else:
                right_expr = expr.right
            # right_expr = expr.right
        gen = c_generator.CGenerator()
            # print(gen.visit(right_expr))
        # Final Expression
        if top_level:
            final_expr = c_ast.BinaryOp(op=expr.op, left=left_expr, right=right_expr)
            # print(gen.visit(final_expr))
            return new_stmts, final_expr
        else:

            left_type = self.get_expr_type(left_expr) # figure out the datatype of left expr
            right_type = self.get_expr_type(right_expr) # datatype of right expr
            temp_type = self.promote_types(left_type, right_type) 
            temp_name, decl = self.create_temp_variable(temp_type)

            assign = c_ast.Assignment(
                op='=',
                lvalue=c_ast.ID(name=temp_name),
                rvalue=c_ast.BinaryOp(op=expr.op, left=left_expr, right=right_expr)
            )
            # print(gen.visit(assign))
            new_stmts.append(decl)
            new_stmts.append(assign)

            return new_stmts, c_ast.ID(name=temp_name)

    def transform(self, node):
        method = f"transform_{type(node).__name__}"
        return getattr(self, method, self.generic_transform)(node)

    def process_nested_func_call(self, node):
        """Process nested function calls and create temp variables"""
        # print("processing nested function call ------")
        func_name = node.name.name
        return_type = self.get_return_type(func_name)
        temp_name, temp_decl = self.create_temp_variable(return_type)

        result = self.transform_FuncCall(node)
        if isinstance(result, tuple):
            nested_stmts, processed_call = result
        else:
            nested_stmts = []
            processed_call = result
        # print(f"nested stmt: {nested_stmts}")
        # print(f"processed call : {processed_call}")
        # Ensure we have an args ExprList
        if not processed_call.args:
            processed_call.args = c_ast.ExprList(exprs=[])
        
        # Add pointer to temp as last argument
        processed_call.args.exprs.append(
            c_ast.UnaryOp(op='&', expr=c_ast.ID(name=temp_name)))
        
        # print(f"processed call : {processed_call}")
        # print(f"temp decl : {temp_decl}")
        # print(f"nested stmts : {nested_stmts}")
        
        return [temp_decl] + nested_stmts+[processed_call], c_ast.ID(name=temp_name)
    
    def transform_stmt_with_guard(self, stmt, cond_temp, neg_cond_temp):
            if isinstance(stmt, c_ast.Assignment):
                # same guarded assignment logic you already wrote above
                lhs = stmt.lvalue
                # print(f"lhs : {lhs}")
                flatten_stmts = self.transform_Assignment(stmt)
                gen = c_generator.CGenerator()

                if isinstance(stmt.rvalue, c_ast.FuncCall):
                    func_call = flatten_stmts[-1]
                    type = self.get_expr_type(lhs)

                    # temp_name = self.temp_gen.new_temp()
                    # self.var_datatypes[temp_name] = self.get_expr_type(lhs)
                    # decl = c_ast.Decl(
                    #     name=temp_name,
                    #     quals=[], storage=[], funcspec=[], align=None,
                    #     type=c_ast.TypeDecl(
                    #         declname=temp_name, quals=[], align=None,
                    #         type=c_ast.IdentifierType([self.get_expr_type(lhs)])
                    #     ),
                    #     init=None,
                    #     bitsize=None
                    # )
                    temp_name, decl = self.create_temp_variable(type)
                    func_call.args.exprs[-1] = c_ast.UnaryOp(op='&', expr=c_ast.ID(name=temp_name))
                    final_rhs = c_ast.ID(name=temp_name)

                    stmts = flatten_stmts[:-1] + [decl, func_call]
                else:
                    final_rhs = flatten_stmts[-1].rvalue
                    stmts = flatten_stmts[:-1]

            
                guarded_rhs = c_ast.BinaryOp(
                    op='+',
                    left=c_ast.BinaryOp(op='*', left=final_rhs, right=c_ast.ID(name=cond_temp)),
                    right=c_ast.BinaryOp(op='*', left=lhs, right=c_ast.ID(name=neg_cond_temp))
                )
                
                guarded_assign = c_ast.Assignment(op='=', lvalue=lhs, rvalue=guarded_rhs)
                # print(self.scope_stack)
                # print(f"gaurded assign : {gen.visit(guarded_assign)}")
                # transform guarded assignment
                stmts = [
                    s for s in stmts
                    if not (isinstance(s, c_ast.Decl) and s.name == self.get_previous_name( self.get_latest_name(lhs.name), lhs.name))
                ]
                 # remove the declartion with lhs.name latest version if present
                self.scope_stack[-1][lhs.name] = self.get_previous_name(self.get_latest_name(lhs.name), lhs.name)
                final = self.transform(guarded_assign)
                # print("gauraded assigment after transformation")
                # print(final)
                # print(f"{final}")
                if isinstance(final, list):
                    return stmts + final
                else:
                    return stmts + [final]

            elif isinstance(stmt, c_ast.Decl):
                # print(f"decl stmt : {stmt}")
                return [stmt]
                # For non-assignment, just recurse normally
            else:
                raise Exception(f"Error: Statement of type `{type(stmt).__name__}` is not supported inside maskedHLS if-condition.")

    def transform_If(self, node):
            # Step 1: Generate condition temp variables
            cond_temp = f"_if_cond_{self.temp_gen.count}"
            neg_cond_temp = f"_if_neg_cond_{self.temp_gen.count}"
            self.temp_gen.count += 1

            # Step 2: Flatten the condition expression
            if isinstance(node.cond, c_ast.BinaryOp):
                cond_stmts, cond_expr = self.flatten_binary_expr(node.cond, top_level=True)
            elif isinstance(node.cond, c_ast.FuncCall):
                result = self.transform_FuncCall(node.cond)
                if isinstance(result, tuple):
                    func_stmts, func_call = result
                else:
                    func_stmts = []
                    func_call = result
                return_type = self.get_return_type(node.cond.name.name)
                temp_name, temp_decl = self.create_temp_variable(return_type)

                func_call.args.exprs.append(
                    c_ast.UnaryOp(op='&', expr=c_ast.ID(name=temp_name))
                )

                cond_stmts = func_stmts + [temp_decl, func_call]
                cond_expr = c_ast.ID(name=temp_name)
            else:
                cond_stmts = []
                cond_expr = node.cond

            cond_decl = c_ast.Decl(
                name=cond_temp,
                quals=[], storage=[], funcspec=[], align=None,
                type=c_ast.TypeDecl(
                    declname=cond_temp, quals=[], align=None,
                    type=c_ast.IdentifierType(['int'])
                ),
                init=None, bitsize=None
            )

            cond_assign = c_ast.Assignment(
                op='=',
                lvalue=c_ast.ID(name=cond_temp),
                rvalue=cond_expr
            )

            neg_decl = c_ast.Decl(
                name=neg_cond_temp,
                quals=[], storage=[], funcspec=[], align=None,
                type=c_ast.TypeDecl(
                    declname=neg_cond_temp, quals=[], align=None,
                    type=c_ast.IdentifierType(['int'])
                ),
                init=None, bitsize=None
            )

            neg_assign = c_ast.Assignment(
                op='=',
                lvalue=c_ast.ID(name=neg_cond_temp),
                rvalue=c_ast.UnaryOp(op='!', expr=c_ast.ID(name=cond_temp))
            )
            # Step 4: Transform the if body
            result = cond_stmts + [cond_decl, cond_assign, neg_decl, neg_assign]
            if isinstance(node.iftrue, c_ast.Compound):
                iftrue_stmts = node.iftrue.block_items or []
            else:
                iftrue_stmts = [node.iftrue]
                
            for stmt in iftrue_stmts:
                if isinstance(stmt, c_ast.Assignment):
                    result.extend(self.transform_stmt_with_guard(stmt, cond_temp, neg_cond_temp))
        
                elif isinstance(stmt, c_ast.Decl):
                    flatten_stmts = self.transform_Decl(stmt) 
                    for curr_stmt in flatten_stmts: 
                        result.extend(self.transform_stmt_with_guard(curr_stmt, cond_temp, neg_cond_temp))
                    
                    return result

                else:
                    flatten_stmts = self.transform(stmt)

                    for curr_stmt in flatten_stmts:
                        result.extend(self.transform_stmt_with_guard(curr_stmt, cond_temp, neg_cond_temp))  # handle nested structures

            return result

    def transform_For(self, node):

        decl_stmt = None
        # self.suppress_scope = True
        # print(f"printing scope stack \\n {self.scope_stack}")
        # Step 1: Parse loop initialization
        if isinstance(node.init, c_ast.DeclList):
            decl = node.init.decls[0]
            if not isinstance(decl.init, c_ast.Constant):
                raise NotImplementedError("Loop init must be a constant.")
            iter_var = decl.name
            start = int(decl.init.value)
            decl_stmt = decl
        elif isinstance(node.init, c_ast.Decl):
            decl = node.init
            if not isinstance(decl.init, c_ast.Constant):
                raise NotImplementedError("Loop init must be a constant.")
            iter_var = decl.name
            start = int(decl.init.value)
            decl_stmt = decl
        elif isinstance(node.init, c_ast.Assignment):
            if not isinstance(node.init.rvalue, c_ast.Constant):
                raise NotImplementedError("Loop init must be a constant.")
            iter_var = node.init.lvalue.name
            start = int(node.init.rvalue.value)
        else:
            raise NotImplementedError("Unsupported loop init type.")

        # Step 2: Parse loop condition
        if not isinstance(node.cond, c_ast.BinaryOp):
            raise NotImplementedError("Unsupported loop condition type.")
        cond_op = node.cond.op
        if not isinstance(node.cond.right, c_ast.Constant):
            raise NotImplementedError("Loop bound must be a constant.")
        end = int(node.cond.right.value)

        # Step 3: Parse loop step
        if isinstance(node.next, c_ast.UnaryOp):
            if node.next.op in ['p++', '++']:
                step = 1
            elif node.next.op in ['p--', '--']:
                step = -1
            else:
                raise NotImplementedError("Unsupported unary loop step.")
        elif isinstance(node.next, c_ast.Assignment):
            if isinstance(node.next.rvalue, c_ast.BinaryOp):
                binop = node.next.rvalue
                if (isinstance(binop.left, c_ast.ID) and binop.left.name == iter_var and
                    isinstance(binop.right, c_ast.Constant) and binop.op in ['+', '-']):
                    step = int(binop.right.value) if binop.op == '+' else -int(binop.right.value)
                else:
                    raise NotImplementedError("Unsupported binary loop step.")
            else:
                raise NotImplementedError("Unsupported assignment step.")
        else:
            raise NotImplementedError("Unsupported loop step format.")

        # Step 4: Convert condition
        if cond_op == '<':
            condition = lambda i: i < end
        elif cond_op == '<=':
            condition = lambda i: i <= end
        elif cond_op == '>':
            condition = lambda i: i > end
        elif cond_op == '>=':
            condition = lambda i: i >= end
        else:
            raise NotImplementedError(f"Unsupported loop condition operator: {cond_op}")

        # Step 5: Unroll loop
        new_stmts = []
        # if decl_stmt:
        #     new_stmts.append(decl_stmt)

        i = start
        while condition(i):
            # print(f"Unrolling for i={i}")
            replacer = self.IndexReplacer(iter_var, i)
            # print(f"rpelacer : {node.stmt}")
            unrolled_body = replacer.visit(node.stmt)
            # print('unrolled_body')
            # print(unrolled_body)

            for var in replacer.generated_vars:
                if var.startswith(f"_{i}_"):
                    original_var = var[len(f"_{i}_"):]
                    prev_var = f"_{i - step}_{original_var}" if i != start else original_var


                    decl = c_ast.Decl(
                        name=var,
                        quals=[],
                        storage=[],
                        funcspec=[],
                        align=None,
                        type=c_ast.TypeDecl(
                            declname=var,
                            quals=[],
                            align=None,
                            type=c_ast.IdentifierType(['int'])
                        ),
                        init =None,
                        bitsize=None
                    )
                    assign = c_ast.Assignment(
                        op='=',
                        lvalue=c_ast.ID(name=var),
                        rvalue=c_ast.ID(self.get_previous_name(self.get_latest_name(prev_var), prev_var))
                    )
                    
                    new_stmts.append(decl)
                    new_stmts.append(assign)

                    # print(f"Current assigned name for {prev_var}: {self.get_previous_name(self.get_latest_name(prev_var), prev_var)}")
                    # print(f"current assigned name for {var} : {self.get_previous_name(self.get_latest_name(var), var)}")
                    # print(f"latest name {var} : {self.get_latest_name(var)}")
                    new_name = self.get_new_name(var)
                    # print(f"latest name {var} : {self.get_latest_name(var)}")

                
            transformed_body = self.transform(unrolled_body)
            # print(f"transformed body : {transformed_body}")
            # if isinstance(transformed_body, list):
            #     new_stmts.extend(transformed_body)
            # else:
            #     new_stmts.append(transformed_body)

            if isinstance(transformed_body, list):
                for stmt in transformed_body:
                    if isinstance(stmt, c_ast.Compound):
                        new_stmts.extend(stmt.block_items or [])
                    else:
                        new_stmts.append(stmt)
            elif isinstance(transformed_body, c_ast.Compound):
                new_stmts.extend(transformed_body.block_items or [])
            else:
                new_stmts.append(transformed_body)

            def extract_final_assignments(stmts, i):

                for stmt in stmts:
                    if isinstance(stmt, c_ast.Assignment):
                        lhs = stmt.lvalue
                        if isinstance(lhs, c_ast.ID):
                            original_var = lhs.name
                            renamed_var = f"_{i}_{original_var}"
                            self.for_loop_var[original_var] = renamed_var

                    elif isinstance(stmt, c_ast.If):
                        inner_stmts = []
                        if isinstance(stmt.iftrue, c_ast.Compound):
                            inner_stmts.extend(stmt.iftrue.block_items or [])
                        elif isinstance(stmt.iftrue, c_ast.Assignment):
                            inner_stmts.append(stmt.iftrue)

                        extract_final_assignments(inner_stmts, i)



            if not condition(i + step):
                if isinstance(node.stmt, c_ast.Compound):
                    body_stmts = node.stmt.block_items or []
                else:
                    body_stmts = [node.stmt]

                extract_final_assignments(body_stmts, i)
                # print(self.for_loop_var)

                       
            i += step

        # print(F"new_stmt after transformation: {new_stmts}")
        # Final pass: transform every unrolled statement
        # final_stmts = []
        # for stmt in new_stmts:
        #     # print(f"tranforming {stmt}")
        #     transformed = self.transform(stmt)
        #     if isinstance(transformed, list):
        #         final_stmts.extend(transformed)
        #     else:
        #         final_stmts.append(transformed)

        # self.suppress_scope = False
        # print(f"Stack scope of after for loop {self.scope_stack}")
        # return final_stmts


        return new_stmts
    
   