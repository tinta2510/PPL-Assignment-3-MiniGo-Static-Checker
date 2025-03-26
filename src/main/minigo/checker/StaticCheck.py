"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"
    
    def __repr__(self):
        return self.__str__()

class StaticChecker(BaseVisitor,Utils):
    def __init__(self,ast):
        self.ast = ast
        self.builtin_funcs = [
            Symbol("getInt",MType([],IntType())),
            Symbol("putInt",MType([IntType()],VoidType())),
            Symbol("putIntLn",MType([IntType()],VoidType())),
            Symbol("getFloat",MType([],FloatType())),
            Symbol("putFloat",MType([FloatType()],VoidType())),
            Symbol("putFloatLn",MType([FloatType()],VoidType())),
            Symbol("getBool",MType([],BoolType())),
            Symbol("putBool",MType([BoolType()],VoidType())),
            Symbol("putBoolLn",MType([BoolType()],VoidType())),
            Symbol("getString",MType([],StringType())),
            Symbol("putString",MType([StringType()],VoidType())),
            Symbol("putStringLn",MType([StringType()],VoidType())),
            Symbol("putLn",MType([],VoidType()))
        ]
        self.structs = [] # list[StructType]
        self.interfaces = [] # list[InterfaceType]
        self.functions = [] # list[FuncDecl]
        self.current_func = None # FuncDecl
        self.current_struct = None # StructType
    
    def check(self):
        return self.visit(self.ast,[])

    def visitProgram(self, ast , c):
        """
        :param ast: Program
        :param c: list[list[Symbol]]"""
        # Global scope
        ## Get StructType list
        self.structs = reduce(
            lambda acc, ele: acc + [self.visit(ele, acc)], 
            filter(lambda x: isinstance(x, StructType), ast.decl), 
            []
        )
        ## Get InterfaceType list
        self.interfaces = reduce(
            lambda acc, ele: acc + [self.visit(ele, acc)],
            filter(lambda x: isinstance(x, InterfaceType), ast.decl),
            []
        )
        
        ## Get FuncDecl list (Get all functions, but not check redecalred) (Predefined Functions)
        self.functions = self.builtin_funcs + list(filter(lambda x: isinstance(x, FuncDecl), ast.decl)) 
                        
        ## Predefined Methods
        def preVisitMethodDecl(methodDecl):
            """
            :param methodDecl: MethodDecl
            """
            # Undeclared Receiver
            structType = self.lookup(methodDecl.recType.name, self.structs, lambda x: x.name)
            if structType is None:
                raise Undeclared(Type(), methodDecl.recType.name) #??? Not check this case
            # Redeclared Method
            if self.lookup(methodDecl.fun.name, structType.methods, lambda y: y.fun.name) is not None:
                raise Redeclared(Method(), methodDecl.fun.name)
            # Add Names of Methods to StructType
            structType.methods = structType.methods + [methodDecl]
        list(map(
            lambda x: preVisitMethodDecl(x), 
            filter(lambda x: isinstance(x, MethodDecl), ast.decl)
        ))
        
        
        # Loop through FuncDecl, VarDecl, ConstDecl, MethodDecl
        c = reduce(
            lambda acc, ele: (acc[:-1] + [acc[-1] + [result]] )
                if (result := self.visit(ele, acc)) is not None 
                else acc,
            filter(lambda x: isinstance(x, Decl), ast.decl),
            [self.builtin_funcs]
        )
        return c
    
    def visitParamDecl(self, ast , c):
        """
        :param ast: ParamDecl
        :param c: list[Symbol]
        :return: Symbol
        """
        # Redeclared ParamDecl
        if self.lookup(ast.parName, c[-1], lambda x: x.name) is not None:
            raise Redeclared(Parameter(), ast.parName)
        return Symbol(ast.parName, ast.parType, None)

    def visitVarDecl(self, ast, c):
        """
        :param ast: VarDecl
        :param c: list[list[Symbol]]
        :return: Symbol
        """
        # Redeclared Variable
        if self.lookup(ast.varName, c[-1], lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName) 
        return Symbol(
            ast.varName, 
            ast.varType, 
            self.visit(ast.varInit, c) if ast.varInit is not None else None
        )

    def visitConstDecl(self, ast, c):
        """
        :param ast: ConstDecl
        :param c: list[list[Symbol]]
        :return: Symbol
        """
        # Redeclared Constant
        if self.lookup(ast.conName, c[-1], lambda x: x.name) is not None:
            raise Redeclared(Constant(), ast.conName)
        return Symbol(
            ast.conName, 
            ast.conType, 
            self.visit(ast.iniExpr, c) if ast.iniExpr is not None else None
        )
   
    def visitFuncDecl(self, ast, c):
        """
        :param ast: FuncDecl
        :param c: list[list[Symbol]]
        :return: Symbol
        """
        # Redeclared Function
        if self.lookup(ast.name, c[-1], lambda x: x.name) is not None:
            raise Redeclared(Function(), ast.name)
        # Redeclared ParamDecl
        reduce(lambda acc, ele: acc[:-1] + [acc[-1] + [self.visit(ele, acc)]], ast.params, c + [[]])
        # Redeclared in Block
        self.visit(ast.body, c)
        return Symbol(ast.name, MType([param.parType for param in ast.params], ast.retType), None)

    def visitStructType(self, ast, c):
        """
        :param ast: StructType
        :param c: list[StructType]
        :return StructType
        """
        # Redeclared Struct
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Type(), ast.name)
        
        # Redeclared Field
        def visitElement(element_name, c):
            """
            :param element_name: str
            :param c: list[str]
            """
            if self.lookup(element_name, c, lambda x: x) is not None:
                raise Redeclared(Field(), element_name)
            return element_name
        reduce(lambda acc, ele: acc + [visitElement(ele, acc)], [e[0] for e in ast.elements], [])
        return ast

    def visitMethodDecl(self, ast, c):
        """
        :param ast: MethodDecl
        :param c: 
        :return MethodDecl
        """
        # Undeclard Receiver (Already checked in Program)
        # Redeclared Method (Already checked in Program)

        # Redeclared ParamDecl
        c = reduce(
            lambda acc, ele: acc[:-1] + [acc[-1] + [self.visit(ele, acc)]], 
            ast.fun.params, 
            c + [[Symbol(ast.receiver, ast.recType, None)]]
        )
        # Redeclared in Block
        self.visit(ast.fun.body, c)
        
    def visitPrototype(self, ast, c):
        """
        :param ast: Prototype
        :param c: list[Prototype]
        :return Prototype
        """
        # Redeclared Prototype
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Prototype(), ast.name)
        return ast

    def visitInterfaceType(self, ast, c):
        """
        :param ast: InterfaceType
        :param c: list[InterfaceType]
        :return InterfaceType
        """
        # Redeclared Interface
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Type(), ast.name)
        # Redeclared Prototype
        reduce(lambda acc, ele: acc + [self.visit(ele, acc)], ast.methods, [])
        return ast

    def visitForBasic(self, ast, c): 
        """
        :param ast: ForBasic
        :param c: list[list[Symbol]]
        """
        self.visit(ast.loop, c)

    def visitForStep(self, ast, c): 
        """
        :param ast: ForStep
        :param c: list[list[Symbol]]
        """
        # Redeclared Variable
        block = Block([ast.init] + ast.loop.member + [ast.upda])
        self.visit(block, c)
        
    def visitForEach(self, ast, c):
        """
        :param ast: ForEach
        :param c: list[list[Symbol]]
        """
        block = Block(
            [
                VarDecl(ast.idx.name, IntType(), None), 
                VarDecl(ast.value.name, None, None)
            ] + 
            ast.loop.member
        )
        self.visit(block, c)

    def visitBlock(self, ast, c) -> None:
        """
        :param ast: Block
        :param c: list[list[Symbol]]
        """
        reduce(
            lambda acc,ele: (
                result := self.visit(ele, acc), 
                acc[:-1] + [acc[-1] + [result]] if isinstance(result, Symbol) else acc
            )[1],
            ast.member, 
            c + [[]]
        )

    def visitIf(self, ast, c): return None
    def visitIntType(self, ast, c): return None
    def visitFloatType(self, ast, c): return None
    def visitBoolType(self, ast, c): return None
    def visitStringType(self, ast, c): return None
    def visitVoidType(self, ast, c): return None
    def visitArrayType(self, ast, c): return None
    def visitAssign(self, ast, c): return None
    def visitContinue(self, ast, c): return None
    def visitBreak(self, ast, c): return None
    def visitReturn(self, ast, c): return None
    def visitBinaryOp(self, ast, c): return None
    def visitUnaryOp(self, ast, c): return None
    def visitFuncCall(self, ast, c): 
        """
        :param ast: FuncCall
        :param c: list[list[Symbol]]
        """
        # Undeclared Function
        # func_symbol: FuncDecl
        func_decl = self.lookup(ast.funName, self.functions, lambda x: x.name) 
        if func_decl is None:
            raise Undeclared(Function(), ast.funName)
        return func_decl.retType
    
    def visitMethCall(self, ast, c): 
        """
        :param ast: MethCall
        :param c: list[list[Symbol]]
        """
        
        receiver = self.visit(ast.receiver, c) # receiver: Type
        if not isinstance(receiver, (StructType, InterfaceType)):
            raise TypeMismatch(ast) #??? Future
        #??? Undeclared StrucType receiver
        
        # Undeclared Method
        method = self.lookup(ast.metName, receiver.methods, lambda x: x.fun.name)
        if method is None:
            raise Undeclared(Method(), ast.metName)
        return method.fun.retType
    
    def visitId(self, ast, c): 
        """
        :param ast: Id
        :param c: list[list[Symbol]]
        """
        # Undeclared Identifier
        all_symbols = reduce(lambda acc, ele: ele + acc, c, [])
        id_symbol = self.lookup(ast.name, all_symbols, lambda x: x.name)
        if id_symbol is None or isinstance(id_symbol.mtype, MType):
            raise Undeclared(Identifier(), ast.name)
        # StructType and InterfaceType are represented by Id
        if isinstance(id_symbol.mtype, Id):
            user_defined_type = self.lookup(id_symbol.mtype.name, self.structs + self.interfaces, lambda x: x.name)
            if user_defined_type is None:
                raise Undeclared(Type(), id_symbol.mtype.name) #??? Not check this case
            return user_defined_type
        return id_symbol.mtype
    
    def visitArrayCell(self, ast, c): return None
    def visitFieldAccess(self, ast, c): 
        """
        :param ast: FieldAccess
        :param c: list[list[Symbol]]
        """
        receiver = self.visit(ast.receiver, c) # receiver: Type
        if not isinstance(receiver, StructType):
            raise TypeMismatch(ast) #??? Future
        #??? Undeclared StrucType receiver
        
        # Undeclared Field
        field = self.lookup(ast.field, receiver.elements, lambda x: x[0])
        if field is None:
            raise Undeclared(Field(), ast.field)
        return field[1]

    def visitIntLiteral(self, ast: IntLiteral, c): return None
    def visitFloatLiteral(self, ast: FloatLiteral, c): return None
    def visitBooleanLiteral(self, ast: BooleanLiteral, c): return None
    def visitStringLiteral(self, ast: StringLiteral, c): return None
    def visitArrayLiteral(self, ast: ArrayLiteral, c): return None
    def visitStructLiteral(self, ast: StructLiteral, c):  return None
    def visitNilLiteral(self, ast: NilLiteral, c): return None