import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_400(self):
        input = """var a int; var b int; var a int; """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_401(self):
        input = """var VoTien = 1; 
var VoTien = 2;"""
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_402(self):
        input = """var VoTien = 1; 
const VoTien = 2;"""
        expect = "Redeclared Constant: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_403(self):
        input = """const VoTien = 1; 
var VoTien = 2;"""
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_404(self):
        input = """const VoTien = 1; 
func VoTien () {return;};"""
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_405(self):
        input = """func VoTien () {return;}
var VoTien = 1;"""
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_406(self):
        input = """var getInt = 1;"""
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_407(self):
        input = """
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
"""
        expect = "Redeclared Field: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_408(self):
        input = """
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
"""
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_409(self):
        input = """
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
"""
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_410(self):
        input = """func Votien (a, a int) {return;}
        """
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_411(self):
        input = """
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
};"""
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_412(self):
        input = """
func Votien (b int) {
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
func Votien () int {return 1;}

func foo () {
    var b = Votien();
    foo_votine();
    return;
};"""
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_415(self):
        input = """
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
"""
        expect = "Undeclared Field: tien\n"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_416(self):
        input = """
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
"""
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_417(self):
        input = """
type TIEN struct {Votien int;}
type TIEN struct {v int;};"""
        expect = "Redeclared Type: TIEN\n"
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
        expect = "Redeclared Parameter: p\n"
        self.assertTrue(TestChecker.test(input, expect, 418))
        
    def test_419(self):
        input = """
func main () {
    arr := [1]int{1, 2, 3};
    for idx, val := range arr {
        var idx = 1;
        var val = 2;
    }
}
"""
        expect = "Redeclared Variable: idx\n"
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
            var b = 1;
        }
    }
    """
        expect = "Redeclared Variable: b\n"
        self.assertTrue(TestChecker.test(input, expect, 421))
        
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
    a := [2][3]int{143, 213, 3}
    a := [1][2]float{{1.0, 2.0}, {3.0, 4.0}};
    a := [1][2]string{{3, 2}, {3, 4}};
}
"""
        expect = "Type Mismatch: Assign(Id(a),ArrayLiteral([IntLiteral(1),IntLiteral(2)],StringType,[[IntLiteral(3),IntLiteral(2)],[IntLiteral(3),IntLiteral(4)]]))\n"
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