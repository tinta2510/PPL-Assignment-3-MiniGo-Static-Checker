import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_400(self):
        input = """var a int; var b int; var a int; """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_401(self):
        input = """var Abc = 1; 
var Abc = 2;"""
        expect = "Redeclared Variable: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_402(self):
        input = """var Abc = 1; 
const Abc = 2;"""
        expect = "Redeclared Constant: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_403(self):
        input = """const Abc = 1; 
var Abc = 2;"""
        expect = "Redeclared Variable: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_404(self):
        input = """const Abc = 1; 
func Abc () {return;};"""
        expect = "Redeclared Function: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_405(self):
        input = """func Abc () {return;}
var Abc = 1;"""
        expect = "Redeclared Variable: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_406(self):
        input = """var getInt = 1;"""
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_407(self):
        input = """
type  Animal struct {
    Animal int;
}
type PERSON struct {
    Animal string;
    PERSON int;
    PERSON float;
}
"""
        expect = "Redeclared Field: PERSON\n"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_408(self):
        input = """
func (v PERSON) putIntLn () {return;}
func (v PERSON) getInt () {return;}
func (v PERSON) getInt () {return;}
type PERSON struct {
    Animal int;
}
"""
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_409(self):
        input = """
type Abc interface {
    Abc ();
    Abc (a int);
}
"""
        expect = "Redeclared Prototype: Abc\n"
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_410(self):
        input = """func Animal (a, a int) {return;}
        """
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_411(self):
        input = """
func Animal (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
};"""
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_412(self):
        input = """
func Animal (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
        var b = 1;
        const b = 1;
    }
}
"""
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_413(self):
        input = """
var a = 1;
var b = a;
var c = d;"""
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_414(self):
        input = """
func Animal () int {return 1;}

func foo () {
    var b = Animal();
    foo_A();
    return;
};"""
        expect = "Undeclared Function: foo_A\n"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_415(self):
        input = """
type PERSON struct {
    Animal int;
}

func (v PERSON) getInt () {
    const c = v.Animal;
    var d = v.age;
}
"""
        expect = "Undeclared Field: age\n"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_416(self):
        input = """
type PERSON struct {
    Animal int;
}

func (v PERSON) getInt () {
    v.getInt ();
    v.putInt ();
}
"""
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_417(self):
        input = """
type PERSON struct {Animal int;}
type PERSON struct {v int;};"""
        expect = "Redeclared Type: PERSON\n"
        self.assertTrue(TestChecker.test(input, expect, 417))
        
    def test_418(self):
        input = """
type Person struct {
    name string;
    age int;
}

func (p Person) getAge (p string) int {
    return p.age;
}
"""
        expect = "Type Mismatch: FieldAccess(Id(p),age)\n"
        self.assertTrue(TestChecker.test(input, expect, 418))
        
    def test_419(self):
        input = """
func main () {
    arr := [1][3]int{1, 2, 3};
    var idx int = 1;
    var val int
    for idx, val := range arr {
        continue;
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(idx),Id(val),Id(arr),Block([Continue()]))\n"
        self.assertTrue(TestChecker.test(input, expect, 419))
        
    def test_420(self):
        input = """
    const a = 2;
    func foo () {
        const a = 1;
        for var b = 1; b < 1; b += 2 {
            const b = 1;
        }
    }
    """
        expect = "Redeclared Constant: b\n"
        self.assertTrue(TestChecker.test(input, expect, 420))
        
    def test_421(self):
        input = """
    func foo () {
        const a = 1;
        for a, b := range [3]int {1, 2, 3} {
            continue;
        }
    }
    """
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input, expect, 421))
    
    def test_422(self):
        input =  """
type S1 struct {name int;}
type I1 interface {name();}
var a I1;
var c I1 = nil;
var d S1 = nil;
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 422))
        
    def test_423(self):
        input = """
    func putIntLn() {return;}
    """
        expect = "Redeclared Function: putIntLn\n"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_424(self):
        input = """
type Person struct {
    name string;
    age int;
}

func main () {
    var p int;
    p.getAge();
}
"""
        expect = "Type Mismatch: MethodCall(Id(p),getAge,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 424))
        
    def test_425(self):
        input = """
func main() {
    var a int;
    var b = a + "Tin";
}
"""
        expect = """Type Mismatch: BinaryOp(Id(a),+,StringLiteral("Tin"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_426(self):
        input = """
func main() {
    var a int;
    var b = a + 1.2;
    var c = a % b;
}
"""
        expect = """Type Mismatch: BinaryOp(Id(a),%,Id(b))\n"""
        self.assertTrue(TestChecker.test(input, expect, 426))
        
    def test_427(self):
        """Test Return type match"""
        input = """
func foo() int {
    return;
}
"""
        expect = "Type Mismatch: Return()\n"
        self.assertTrue(TestChecker.test(input, expect, 427))
        
    def test_428(self):
        """Test Return type match"""
        input = """
func main() {
    return 10;
}
"""
        expect = "Type Mismatch: Return(IntLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 428))
        
    def test_429(self):
        """Test return type of call statement"""
        input = """
func foo() int {
    return 1;
}
func main() {
    foo();
}
"""
        expect = "Type Mismatch: FuncCall(foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 429))
        
        
    def test_430(self):
        """Invalid func_call"""
        input = """
func f(a int, b float) int {
    return 10;
}

func main() {
    f(1, 2);
}
"""
        expect = "Type Mismatch: FuncCall(f,[IntLiteral(1),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 430))
        
    def test_431(self):
        """Invalid method call"""
        input = """
type Person struct {
    name string;
    age int;
}

func (p Person) getAge () int {
    return p.age;
}

func main() {
    var p Person;
    p.getAge(1);
}
"""
        expect = "Type Mismatch: MethodCall(Id(p),getAge,[IntLiteral(1)])\n"
        self.assertTrue(TestChecker.test(input, expect, 431))
        
    def test_432(self):
        """Invalid builtins function call"""
        input = """
func main() {
    var a = getInt(1);
}
"""
        expect = "Type Mismatch: FuncCall(getInt,[IntLiteral(1)])\n"
        self.assertTrue(TestChecker.test(input, expect, 432))
        
    def test_433(self):
        """Invalid function call"""
        input = """
type Person struct {
    name string;
    age int;
}

type Animal struct {}

func printInfo(p Person) {
    return;
}
func main() {
    var a Animal;
    printInfo(a);
}
"""     
        expect = "Type Mismatch: FuncCall(printInfo,[Id(a)])\n"
        self.assertTrue(TestChecker.test(input, expect, 433))
        
    def test_434(self):
        """Invalid method call"""
        input = """
type Person struct {
    name string;
    age int;
}

func (p Person) compareAge (p2 Person) boolean {
    return p.age > p2.age;
}

type Animal struct {
    age int;
    name string;
}

func main() {
    var a Animal;
    var b Person;
    b.compareAge(a);
}
"""
        expect = "Type Mismatch: MethodCall(Id(b),compareAge,[Id(a)])\n"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_435(self):
        """ A call statement must invoke a function/method with a return type of VoidType"""
        input = """
func foo() int {
    return 1;
}
func main() {
    foo();
}
"""
        expect = "Type Mismatch: FuncCall(foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 435))
        
    def test_436(self):
        """The number of arguments in the call must match the number of parameters in
 the function/method definition"""
        input = """
func foo(a int, b float) int {
    return 10;
}

func main() {
    foo(1, 2, 3);
}
"""
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])\n"
        self.assertTrue(TestChecker.test(input, expect, 436))
        
    def test_437(self):
        """Each argument must have the exact same type as its
 corresponding parameter. """
        input = """
func foo(a int, b string) {
    return;
}
func main() {
    foo(1, 2.0);
}
"""
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1),FloatLiteral(2.0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 437))
        
    def test_438(self):
        """"Each argument must have the exact same type as its
 corresponding parameter. """
        input = """
type Person struct {
    name string;
    age int;
}

type Animal struct {
    species string;
    age int;
}

func printInfo(p Person) {
    return;
}

func main() {
    var a Animal;
    var b Person;
    printInfo(b);
    printInfo(a);
}
"""
        expect = "Type Mismatch: FuncCall(printInfo,[Id(a)])\n"
        self.assertTrue(TestChecker.test(input, expect, 438))
        
    def test_439(self):
        """Initialized an undeclared scalar by assignment"""
        input = """
var b int = 1;
func main() {
    a := 10;
    const a = 20;
}
"""
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 439))
        
    def test_440(self):
        """ if the LHS has an interface type, the RHS may have a struct type, provided that the struct type implements all prototypes declared in the interface."""
        input = """
type Foo interface {
    foo();
}
type Bar struct {}

func main() {
    var a Foo = Bar{};
}
"""
        expect = "Type Mismatch: VarDecl(a,Id(Foo),StructLiteral(Bar,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 440))
    
    def test_441(self):
        """Array Literal"""
        input = """
var a = [1][2]float{{1, 2, 3}, {4, 5, 6}};
func main() {
    a := [1][2]float{{1.0, 2.0}, {3.0, 4.0}};
    a := [2][3]int{143, 213, 3}
}
"""
        expect = "Type Mismatch: Assign(Id(a),ArrayLiteral([IntLiteral(2),IntLiteral(3)],IntType,[IntLiteral(143),IntLiteral(213),IntLiteral(3)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_442(self):
        """ if the LHS has an interface type, the RHS may have a struct type, provided that the struct type implements all prototypes declared in the interface."""
        input = """
type Foo interface {
    foo();
}
type Bar struct {
    a int;
}

func (b Bar) foo() {
    return;
}

func main() {
    var a Foo = Bar{};
}
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 442))
        
    def test_443(self):
        input = """
func main () {
    arr := 10;
    for idx, val := range arr {
        var idx = 1;
        var val = 2;
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(idx),Id(val),Id(arr),Block([VarDecl(idx,IntLiteral(1)),VarDecl(val,IntLiteral(2))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 443))
        
    def test_444(self):
        input = """
var A int;
func (a A) b(x int) {
    return;
}
type A struct{
    attr int;
}
"""
        expect = "Redeclared Type: A\n"
        self.assertTrue(TestChecker.test(input, expect, 444))
    
    def test_445(self):
        input = """
const a = 2; 
const b = 1 + a;
var c [b]int = [2]int {1,2};
"""
        expect = "Type Mismatch: VarDecl(c,ArrayType(IntType,[Id(b)]),ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 445))
        
    def test_446(self):
        input = """
const a = 2; 
const b = 1 + a;
var c [b]int = [3]int {1,2};
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 446))
    
    def test_447(self):
        input =  """
const v = 3;
const a = v + v;
const f = a * 2 + a;
var b [f]int;
var c [18]int = b;
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 447)) 
        
    def test_448(self):
        input =  """
const v = 3;
const a = v + v;
const f = a * 2 + a + 10;
var b [f]int;
var c [18]int = b;
"""
        expect = "Type Mismatch: VarDecl(c,ArrayType(IntType,[IntLiteral(18)]),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 448)) 
    
    def test_449(self):
        input =  """
func foo(a [2]float) {
    foo([2]float{1.0,2.0})
    foo([2]int{1,2})
}
        """
        expect = """Type Mismatch: FuncCall(foo,[ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)])])\n"""
        self.assertTrue(TestChecker.test(input, expect, 449)) 
        
    def test_450(self):
        input =  """
    type A interface {foo();}
    const A = 2;
        """
        expect = "Redeclared Constant: A\n"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_451(self):
        input =  """
  
var v PERSON;      
type PERSON struct {
    a int;
} 
type TIN interface {
    foo() int;
}

func (v PERSON) foo() int {return 1;}
func (b PERSON) koo() {b.koo();}
func foo() {
    var x TIN;  
    const b = x.foo(); 
    x.koo(); 
}
"""
        expect = "Undeclared Method: koo\n" #???
        self.assertTrue(TestChecker.test(input, expect, 451))
        
    def test_452(self):
        input =  """
type S1 struct {v int; t int;}

var a = S1 {v : 1, t: 2}
var b S1 = a;
var c int = b;
"""
        expect = "Type Mismatch: VarDecl(c,IntType,Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 452))
        
    def test_453(self):
        input =  """
var a [2][3] int;
var b = a[1];
var c [3] int = b;
var d [3] string = b;
"""
        expect = "Type Mismatch: VarDecl(d,ArrayType(StringType,[IntLiteral(3)]),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 453))
        
    def test_454(self):
        input =  """
type S1 struct {v int; x S1;}
var b S1;
var c = b.x.v;
var d = c.x;
"""
        expect = "Type Mismatch: FieldAccess(Id(c),x)\n"
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_455(self):
        input =  """
type S1 struct {v int; x S1;}

func (s S1) getX() S1 {
    return s.x;
}

var b S1;
var c = b.getX().v;
var d = c.x;
"""
        expect = "Type Mismatch: FieldAccess(Id(c),x)\n"
        self.assertTrue(TestChecker.test(input, expect, 455))
        
    def test_456(self):
        input =  """
type S1 struct {name int;}
type I1 interface {name();}
var a I1;
var c I1 = nil;
var d S1 = nil;
func foo(){
    c := a;
    a := nil;
}

var e int = nil;
"""
        expect = "Type Mismatch: VarDecl(e,IntType,Nil)\n"
        self.assertTrue(TestChecker.test(input, expect, 456))
        
    def test_457(self):
        input =  """
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
"""
        expect= "Type Mismatch: BinaryOp(IntLiteral(1),>,FloatLiteral(2.0))\n"
        self.assertTrue(TestChecker.test(input, expect, 457))
        
    def test_458(self):
        input =  """
func foo(){
    for var i int = 1; a < 10; i := 1.0 {
        var a = 1;
    }
}
"""
        expect = "Undeclared Identifier: a\n" # ???
        self.assertTrue(TestChecker.test(input, expect, 458))
        
    def test_459(self):
        input =  """
func foo() int {
    return [2]int{1, 2}[a]
}

var a = foo;
"""
        expect = "Undeclared Identifier: a\n"
        self.assertTrue(TestChecker.test(input, expect, 459))
        
    def test_460(self):
        input =  """

func foo(){
    for var i int = 3; i; i := 1.0 {
        var a = 1;
    }
}
"""
        expect = "Type Mismatch: For(VarDecl(i,IntType,IntLiteral(3)),Id(i),Assign(Id(i),FloatLiteral(1.0)),Block([VarDecl(a,IntLiteral(1))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 460))
        
    def test_461(self):
        input =  """

type S1 struct {age int;}
func (s S1) put() {return ;}
func (s S1) name() {
s.name();
var a = s.put();
}
"""     
        expect = "Type Mismatch: MethodCall(Id(s),put,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 461))
    
    def test_462(self):
        input =  """var a [2] int = [2][2] int {{1,2}, {2,2}};"""
        expect = "Type Mismatch: VarDecl(a,ArrayType(IntType,[IntLiteral(2)]),ArrayLiteral([IntLiteral(2),IntLiteral(2)],IntType,[[IntLiteral(1),IntLiteral(2)],[IntLiteral(2),IntLiteral(2)]]))\n"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_463(self):
        input =  """

type A interface {foo();}

func foo() {
    return A;
}
"""
        expect = "Undeclared Identifier: A\n"
        self.assertTrue(TestChecker.test(input, expect, 463))
    
    def test_464(self):
        input =  """

type S1 struct {age int;}
type I1 interface {name();}

func (s S1) name() {return;}

var b [2] S1;
var a [2] I1 = b;
"""
        expect = "Type Mismatch: VarDecl(a,ArrayType(Id(I1),[IntLiteral(2)]),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 464))
        
    def test_465(self):
        input =  """
var a = [2] int {1, 2}
var c [2] float = a
""" 
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 465))
        
    def test_466(self):
        input =  """
type K struct {a int;}
func (k K) koo(a [1 + 2] int) {return;}
type H interface {koo(a [1 + 2] int);}

const c = 4;
func foo() {
    var k H;
    k.koo([c - 1] int {1,2,3})
} 
"""
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([Return(None)]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],VoidType())]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],VoidType(),Block([VarDecl("k",Id("H"), None),MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 466)) #??? #!!!
        
    def test_467(self):
        input =  """
func foo() {
    var arr [2][3]int
    var a string
    var  b [3] int
    for a, b := range arr {
        var c int = a
        var d [3]float = b
        var e [2]string = a
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(a),Id(b),Id(arr),Block([VarDecl(c,IntType,Id(a)),VarDecl(d,ArrayType(FloatType,[IntLiteral(3)]),Id(b)),VarDecl(e,ArrayType(StringType,[IntLiteral(2)]),Id(a))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 467))
        
    def test_468(self):
        input = """
  
type S1 struct {abcd int;}
type S2 struct {abcd int;}
type I1 interface {abcd();}
type I2 interface {abcd();}

func (s S1) abcd() {return;}

var a S1;
var b S2;
var c I1 = a;
"""
        expect = "Redeclared Method: abcd\n"
        self.assertTrue(TestChecker.test(input, expect, 468))     
        
    def test_469(self):
        input = """
  
type S1 struct {name int;}
type S2 struct {name int;}
type I1 interface {abcd();}
type I2 interface {abcd();}

func (s S1) abcd() {return;}

var a S1;
var b S2;
var c I1 = a;
var d I2 = b;
"""
        expect = "Type Mismatch: VarDecl(d,Id(I2),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 469))  
        
    def test_470(self):
        input = """
func main() {
    for i := 0; i < 10; c += 1 {
        var c = 5
        i += 1 
    }
}
"""
        expect = "Undeclared Identifier: c\n"
        self.assertTrue(TestChecker.test(input, expect, 470))
        
    def test_471(self):
        input = """
type Person struct {
    name string
}        

func (p Person) getName(a int) {}

func main() {
    var p Person;
    p.getName(10.0)
}
"""
        expect = "Type Mismatch: MethodCall(Id(p),getName,[FloatLiteral(10.0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 471))
        
    def test_472(self):
        input = """
var b [3]int = [3]int{1, 2, 3}
var a [3]float = b
var c [3]float = [3]string{1.0, 2.0, 3.0}
"""
        expect = "Type Mismatch: VarDecl(c,ArrayType(FloatType,[IntLiteral(3)]),ArrayLiteral([IntLiteral(3)],StringType,[FloatLiteral(1.0),FloatLiteral(2.0),FloatLiteral(3.0)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 472))
    
    def test_473(self):
        input = """
type EFG struct {
    Abc int;
}
func (v EFG) foo (v int) {return;}
func foo () {return;}
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 473))
    
    def test_474(self):
        input ="""
func foo() {
    a := 1;
    var a = 1;
}
"""
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_475(self):
        input = """
func Abc (b int) {
    for var a = 1; c < 1; a += c {
        const c = 2;
    }
}
        """
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c\n""", 475)) 
        
    def test_476(self):
        input = """
var v EFG;
func (v EFG) foo (v int) int {
    return v;
}

type EFG struct {
    Abc int;
}
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 476))
        
    def test_477(self):
        input = """
func foo(){
    for var i int = 1; a < 10; i := 1.0 {
        var a = 1;
    }
}
"""
        expect = "Undeclared Identifier: a\n"
        self.assertTrue(TestChecker.test(input, expect, 477))
        
    def test_478(self):
        input = """
type putLn struct {
    name int;
}
"""
        expect = "Redeclared Type: putLn\n"
        self.assertTrue(TestChecker.test(input, expect, 478))
        
    def test_479(self):
        input = """
var a int; 
type b struct {c int;}; 
func (x b) a() {
    putLn();
}; 
func (x b) c() {
    return;
};
"""
        expect = "Redeclared Method: c\n"
        self.assertTrue(TestChecker.test(input, expect, 479))
        
    def test_480(self):
        input = """
var a int; 
func main() {
    a := a + "str";
}
"""
        expect = "Type Mismatch: BinaryOp(Id(a),+,StringLiteral(\"str\"))\n"
        self.assertTrue(TestChecker.test(input, expect, 480))
        
    def test_481(self):
        input = """
var a int; 
var b int; 
var c int; 
func main() {
    for a,b := range c {
        putLn();
    }    
}
"""
        expect = "Type Mismatch: ForEach(Id(a),Id(b),Id(c),Block([FuncCall(putLn,[])]))\n"
        self.assertTrue(TestChecker.test(input, expect, 481))

    def test_482(self):
        input = """
func (v TIEN) VO () {return ;}
func (v TIEN) Tien () {return ;}
type TIEN struct {
    Votien int;
    Tien int;
}
"""     
        expect = """Redeclared Method: Tien\n"""
        self.assertTrue(TestChecker.test(input, expect, 482))
        
    def test_483(self):
        input = """
var a int = 10
var c int = "Tin"
    """
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl(c,IntType,StringLiteral("Tin"))\n""", 483)) 
    
    def test_484(self):
        input = """
func (p Person) printName() string{
    return p.name;
}
       
type Person struct {
    name string;
    age int;
}

func (p Person) printName() {
    return;
}
"""
        expect = "Redeclared Method: printName\n"
        self.assertTrue(TestChecker.test(input, expect, 484))
        
    def test_485(self):
        input = """
func (p Person) printName() string{
    return p.name;
}
       
type Person struct {
    name string;
    printName int;
}
"""
        expect = "Redeclared Method: printName\n"
        self.assertTrue(TestChecker.test(input, expect, 485))
    
    def test_486(self):
        input = """
type Person struct {
    name string;
    printName int;
}

func (p Person) printName() string{
    return p.name;
}
"""
        expect = "Redeclared Method: printName\n"
        self.assertTrue(TestChecker.test(input, expect, 486))
    
    def test_487(self):
        input = """
type Person struct {
    name string;
    age int;
    name Person;
}
func (p Person) name() string {
    return p.name;
}
"""
        expect = "Redeclared Field: name\n"
        self.assertTrue(TestChecker.test(input, expect, 487))
        
    def test_488(self):
        input = """
        type Person struct {
            name string
        }
        func (p Person) getName(p string) string {
            return p.name;
        }
        """
        expect = "Type Mismatch: FieldAccess(Id(p),name)\n"
        self.assertTrue(TestChecker.test(input, expect, 488))
        
    def test_489(self):
        input = """
func foo(a int) {

      foo(1);

      var foo = 1;

      foo(2); // error

 }
"""
        expect = "Undeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 489))
    
    def test_490(self):
        input = """
func foo() int {
    const foo = 1;
    return foo()
}
        """
        self.assertTrue(TestChecker.test(input, """Undeclared Function: foo\n""", 490))
        
    def test_491(self):
        input ="""
func (v TIEN) VO () {return ;}
func (v TIEN) Tien () {return ;}
type TIEN struct {
    Votien int;
    Tien int;
}
        """
        self.assertTrue(TestChecker.test(input, """Redeclared Method: Tien\n""", 491))
        
        
    def test_492(self):
        input = Program([StructType("C1",[("a",ArrayType([IntLiteral(2),IntLiteral(3),IntLiteral(4)],IntType()))],[]),
                StructType("C2",[("a",ArrayType([IntLiteral(2),IntLiteral(3),IntLiteral(4)],Id("C1")))],[]),
                VarDecl("o",Id("C2"),NilLiteral()), VarDecl("x",FloatType(),
                ArrayCell(FieldAccess(ArrayCell(FieldAccess(Id("o"),"a"), [IntLiteral(2),IntLiteral(3),IntLiteral(4)]), "a"),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        self.assertTrue(TestChecker.test(input, "", 492))
        
    def test_493(self):
        input = """
func foo() {
    var a = foo
}
        """
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: foo\n""", 493))
    
    def test_494(self):
        input = """
var arr = [2][3] int {1, 2, 3}
var val [3] int 
func main() {
    for idx, val := range arr {
        getIntLn()
    }
}

        """
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: idx\n""", 494))
    
    def test_495(self):
        input = """
var v TIEN;      
type TIEN struct {
    a int;
} 
type VO interface {
    fooA();
    fooB();
    fooC();
}

func (v TIEN) fooA() {return ;}
func (v TIEN) fooB() {return ;}
func (v TIEN) fooC(a int) {return ;}

func foo() {
    var x VO = TIEN{a:1};  
}
"""   
        expect = """Type Mismatch: VarDecl(x,Id(VO),StructLiteral(TIEN,[(a,IntLiteral(1))]))\n"""
        self.assertTrue(TestChecker.test(input, expect, 495))
        
    def test_496(self):
        input = """
func Votien (b int) {
    var array = [2] int {1,2}
    var index = 1.0;
    var value int;

    for index, value := range  array {
        return;
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(index),Id(value),Id(array),Block([Return()]))\n"
        self.assertTrue(TestChecker.test(input, expect, 496))
    
    def test_497(self):
        input = """
func Votien () {
    var array = [2] int {1,2}
    var index int;
    var value float;
    for index, value := range array {
        return;
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(index),Id(value),Id(array),Block([Return()]))\n"
        self.assertTrue(TestChecker.test(input, expect, 497))
        
    def test_498(self):
        input = """

func foo () {
    var a = 1;
    var b = 1;
    for a, b := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 498))