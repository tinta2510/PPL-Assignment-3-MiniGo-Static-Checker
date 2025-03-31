import unittest
from TestUtils import TestChecker
from AST import *
import inspect

class CheckSuite(unittest.TestCase):
    def test_001(self):
        """
var VoTien = 1; 
var VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", inspect.stack()[0].function))
    
    def test_002(self):
        """
var VoTien = 1; 
const VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),ConstDecl("VoTien",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: VoTien\n", inspect.stack()[0].function))
        
    def test_003(self):
        """
const VoTien = 1; 
var VoTien = 2;
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", inspect.stack()[0].function))
    
    def test_004(self):
        """
const VoTien = 1; 
func VoTien () {return;}
        
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),FuncDecl("VoTien",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: VoTien\n", inspect.stack()[0].function))
    
    def test_005(self):
        """
func VoTien () {return;}
var VoTien = 1;
        
        """
        input = Program([FuncDecl("VoTien",[],VoidType(),Block([Return(None)])),VarDecl("VoTien", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", inspect.stack()[0].function))

    def test_006(self):
        """
var getInt = 1;
        
        """
        input = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt\n", inspect.stack()[0].function))

    def test_007(self):
        """
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
        
        """
        input = Program([StructType("Votien",[("Votien",IntType())],[]),StructType("TIEN",[("Votien",StringType()),("TIEN",IntType()),("TIEN",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: TIEN\n", inspect.stack()[0].function))

    def test_008(self):
        """
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
        
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt\n", inspect.stack()[0].function))
        
    def test_009(self):
        """
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
        
        """
        input = Program([InterfaceType("VoTien",[Prototype("VoTien",[],VoidType()),Prototype("VoTien",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: VoTien\n", inspect.stack()[0].function))
        
    def test_010(self):
        """
func Votien (a, a int) {return;}
        
        """
        input = Program([FuncDecl("Votien",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n", inspect.stack()[0].function))
        
    def test_011(self):
        """
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n", inspect.stack()[0].function))
    
    def test_012(self):
        """
func Votien (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n", inspect.stack()[0].function))
    
    def test_013(self):
        """
var a = 1;
var b = a;
var c = d;
        
        """
        input = Program([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,Id("a")),VarDecl("c", None,Id("d"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: d\n", inspect.stack()[0].function))
        
    def test_014(self):
        """
func Votien () int {return 1;}

func foo () {
    var b = Votien();
    foo_votine();
    return;
}
        
        """
        input = Program([FuncDecl("Votien",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Votien",[])),FuncCall("foo_votine",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_votine\n", inspect.stack()[0].function))
        
    def test_015(self):
        """
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Votien")),VarDecl("d", None,FieldAccess(Id("v"),"tien"))])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: tien\n", inspect.stack()[0].function))
        
    def test_016(self):
        """
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
        
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt\n", inspect.stack()[0].function))
        
    def test_017(self):
        """
type TIEN struct {Votien int;}
type TIEN struct {v int;}
        
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),StructType("TIEN",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN\n", inspect.stack()[0].function))
    
    def test_018(self):
        input = """
var v TIEN;
const b = v.foo();        
type TIEN struct {
    a int;
} 
func (v TIEN) foo() int {return 1;}
func (v TIEN) koo() int {return 1;}
const c = v.koo();  
const d = v.zoo();
        """
        # input = Program([VarDecl("v",Id("TIEN"), None),ConstDecl("b",None,MethCall(Id("v"),"foo",[])),StructType("TIEN",[("a",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),MethodDecl("v",Id("TIEN"),FuncDecl("koo",[],IntType(),Block([Return(IntLiteral(1))]))),ConstDecl("c",None,MethCall(Id("v"),"koo",[])),ConstDecl("d",None,MethCall(Id("v"),"zoo",[]))])
        expect = "Undeclared Method: zoo\n"
        self.assertTrue(TestChecker.test(input, expect, inspect.stack()[0].function))

    def test_019(self):
        input = """
type S1 struct {name int;}
func (s S1) votien() int {
s.votien();
return 1;
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),votien,[])\n"
        self.assertTrue(TestChecker.test(input, expect, inspect.stack()[0].function))
        
    def test_020(self):
        input = """
var a = 1 + 2.0;
var b = 1 + 1;
func foo() int {
    return b;
    return a;
}
"""
        expect = "Type Mismatch: Return(Id(a))\n"
        self.assertTrue(TestChecker.test(input, expect, inspect.stack()[0].function))

    def test_021(self):
        input = """
  
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien();}
type I2 interface {votien();}

func (s S1) votien() {return;}

var a S1;
var b S2;
var c I1 = a;
var d I2 = b;
"""
        expect = "Type Mismatch: VarDecl(d,Id(I2),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, inspect.stack()[0].function))  

    def test_022(self):
        input =  """
func foo() {
    var a [5][6] int;
    var b [2] float;
    b[2] := a[2][3]
    a[2][3] := b[2] + 1;
}
        """
        self.assertTrue(TestChecker.test(input, """Type Mismatch: Assign(ArrayCell(Id(a),[IntLiteral(2),IntLiteral(3)]),BinaryOp(ArrayCell(Id(b),[IntLiteral(2)]),+,IntLiteral(1)))\n""", inspect.stack()[0].function)) 


    def test_023(self):
        input =  """
type S1 struct {name int;}
type I1 interface {votien();}

func (s S1) votien() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(a,ArrayType(Id(I1),[IntLiteral(2)]),Id(b))\n""", inspect.stack()[0].function)) 

    def test_024(self):
        """
var a [1 + 9] int;
var b [10] int = a;
        """
        input = Program([VarDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function)) 

    def test_025(self):
        input =  """
var A = 1;
type A struct {a int;}
        """
        self.assertTrue(TestChecker.test(input, """Redeclared Type: A\n""", inspect.stack()[0].function)) 

    def test_026(self):
        input =  """
var a TIEN;
func foo() TIEN {
    return a;
    return TIEN;
}

type TIEN struct {tien int;}
        """
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: TIEN\n""", inspect.stack()[0].function))
        
    def test_027(self):
        input =  """
type Person struct {
	name string
}

func main() {
	a := Person{name: "Tin", age: 30}
}
"""
        expect = "Undeclared Field: age\n"
        self.assertTrue(TestChecker.test(input, expect, inspect.stack()[0].function))