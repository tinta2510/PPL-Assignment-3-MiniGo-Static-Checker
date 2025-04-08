import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_400(self):
        input = """
var x int
var x int
"""
        expect = "Redeclared Variable: x\n"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_401(self):
        input = """
const c = 5
const c = 10
"""
        expect = "Redeclared Constant: c\n"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_402(self):
        input = """
var a = 1
func a() {return;}
"""
        expect = "Redeclared Function: a\n"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_403(self):
        input = """
func test() { 
    var x = 1
    var x = 2
}
"""
        expect = "Redeclared Variable: x\n"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_404(self):
        input = """
var y = x
"""
        expect = "Undeclared Identifier: x\n"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_405(self):
        input = """
func main() { 
    unknown()
}
"""
        expect = "Undeclared Function: unknown\n"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_406(self):
        input = """
var a int = "hello"
"""
        expect = """Type Mismatch: VarDecl(a,IntType,StringLiteral("hello"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_407(self):
        input = """
func foo() int { 
    return "text"
}
"""
        expect = """Type Mismatch: Return(StringLiteral("text"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_408(self):
        input = """
type T struct { 
    x int
    x string
}
"""
        expect = "Redeclared Field: x\n"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_409(self):
        input = """
func main() { 
    var a = 1 + "two"
}
"""
        expect = """Type Mismatch: BinaryOp(IntLiteral(1),+,StringLiteral("two"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_410(self):
        input = """
var a = 1
func main() {
    a := "string"
    b := a + 2
}
"""
        expect = """Type Mismatch: Assign(Id(a),StringLiteral("string"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_411(self):
        input = """
type S struct {
    x int
}
var s = S{}
var y = s.y
"""
        expect = "Undeclared Field: y\n"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_412(self):
        input = """
func foo(x int) {
    x := "redeclared"
}
"""
        expect = """Type Mismatch: Assign(Id(x),StringLiteral("redeclared"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_413(self):
        input = """
type I interface {
    get()
}
type S struct {
    val int
}
var i = S{name: "Tin"}
"""
        expect = "Undeclared Field: name\n"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_414(self):
        input = """
func main() {
    arr := [2]int{1, 2}
    var x string
    x := arr[2]
}
"""
        expect = "Type Mismatch: Assign(Id(x),ArrayCell(Id(arr),[IntLiteral(2)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_415(self):
        input = """
type S struct {
    x int
}
func (s S) x() {
    return
}
"""
        expect = "Redeclared Method: x\n"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_416(self):
        input = """
func main() {
    a := 0
    for a := 1; a < 5; a += "step" {
        putLn()
    }
}
"""
        expect = """Type Mismatch: BinaryOp(Id(a),+,StringLiteral("step"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_417(self):
        input = """
const a = 1
func a() {
    const a = 2
    a := 3
}
"""
        expect = "Redeclared Function: a\n"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_418(self):
        input = """
type S struct {
    field int
}
func (s S) get() int {
    return s.field
}
func main() {
    s := S{}
    s.get(1)
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),get,[IntLiteral(1)])\n"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_419(self):
        input = """
var arr = [2]int{}
var x = arr[1] + arr
"""
        expect = "Type Mismatch: BinaryOp(ArrayCell(Id(arr),[IntLiteral(1)]),+,Id(arr))\n"
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_420(self):
        input = """
type A interface {
    foo()
}
type A struct {
    x int
}
"""
        expect = "Redeclared Type: A\n"
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_421(self):
        input = """
func foo() int {
    return
}
func main() {
    foo()
}
"""
        expect = "Type Mismatch: Return()\n"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_422(self):
        input = """
type S struct {
    x int
}
func (s S) set(x int) {
    s.x := x
}
func main() {
    s := S{}
    s.set("wrong")
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),set,[StringLiteral(\"wrong\")])\n"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_423(self):
        input = """
func main() {
    for i, v := range 5 {
        i := 1
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(i),Id(v),IntLiteral(5),Block([Assign(Id(i),IntLiteral(1))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_424(self):
        input = """
type I interface {
    get() int
}
func main() {
    var i I
    i.get("param")
}
"""
        expect = "Type Mismatch: MethodCall(Id(i),get,[StringLiteral(\"param\")])\n"
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_425(self):
        input = """
var a = [2]int{1, 2}
var b = a
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_426(self):
        input = """
type S struct {
    x int
}
func main() {
    s := 5
    s.x := 5
}
"""
        expect = "Type Mismatch: FieldAccess(Id(s),x)\n"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_427(self):
        input = """
func foo(a int, b float) {
    foo(1)
}
"""
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1)])\n"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_428(self):
        input = """
type S struct {
    val int
}
func (s S) get() S {
    return s
}
func main() {
    s := S{}
    x := s.get().val + s.get()
}
"""
        expect = "Type Mismatch: BinaryOp(FieldAccess(MethodCall(Id(s),get,[]),val),+,MethodCall(Id(s),get,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_429(self):
        input = """
const n = 2
var a = [n]int{1, 2}
var b = [3]int{1, 2, 3}
"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_430(self):
        input = """
func main() {
    x := 1
    x := "reassign"
}
"""
        expect = """Type Mismatch: Assign(Id(x),StringLiteral("reassign"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_431(self):
        input = """
type S struct {
    a int
    b string
}
var s = S{a: 1, c: "test"}
"""
        expect = "Undeclared Field: c\n"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_432(self):
        input = """
func foo() {
    return
}
func foo(x int) {
    return
}
"""
        expect = "Redeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_433(self):
        input = """
type I interface {
    get() int
}
type S struct {
    val int
}
func (s S) get() string {
    return "wrong"
}
var i I = S{}
"""
        expect = "Type Mismatch: VarDecl(i,Id(I),StructLiteral(S,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_434(self):
        input = """
func main() {
    arr := [2][3]int{{1, 2, 3}, {4, 5, 6}}
    var x [3][2]int
    x := arr
}
"""
        expect = "Type Mismatch: Assign(Id(x),Id(arr))\n"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_435(self):
        input = """
type S struct {
    x int
}
func main() {
    s := S{}
    s.y := 5
}
"""
        expect = "Undeclared Field: y\n"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_436(self):
        input = """
func main() {
    a := [2]int{1, 2}
    for i := 0; i < "end"; i += 1 {
        putLn()
    }
}
"""
        expect = """Type Mismatch: BinaryOp(Id(i),<,StringLiteral("end"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_437(self):
        input = """
var x = 1
func main() {
    const x = 2
    for x := 3; x + 5; x += 1 {
        putLn()
    }
}
"""
        expect = """Type Mismatch: For(Assign(Id(x),IntLiteral(3)),BinaryOp(Id(x),+,IntLiteral(5)),Assign(Id(x),BinaryOp(Id(x),+,IntLiteral(1))),Block([FuncCall(putLn,[])]))\n"""
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_438(self):
        input = """
type S struct {
    val int
}
func (s S) set(v int) int {
    return v
}
func main() {
    s := S{}
    s.set()
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),set,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_439(self):
        input = """
var a = 10.0
var b int = a
"""
        expect = "Type Mismatch: VarDecl(b,IntType,Id(a))\n"
        self.assertTrue(TestChecker.test(input, expect, 439))

    def test_440(self):
        input = """
type S struct {
    x int
}
type S struct {
    y string
}
var s = S{x: 1}
"""
        expect = "Redeclared Type: S\n"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_441(self):
        input = """
func foo() string {
    return 42
}
"""
        expect = """Type Mismatch: Return(IntLiteral(42))\n"""
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_442(self):
        input = """
type I interface {
    set(x int)
}
func main() {
    var i I
    i.set(1, 2)
}
"""
        expect = "Type Mismatch: MethodCall(Id(i),set,[IntLiteral(1),IntLiteral(2)])\n"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_443(self):
        input = """
func main() {
    arr := [2]int{1, 2}
    for i, v := range arr {
        v := "redeclared"
    }
}
"""
        expect = """Type Mismatch: Assign(Id(v),StringLiteral("redeclared"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_444(self):
        input = """
type S struct {
    x int
}
func (s S) get() int {
    return s.x
}
func main() {
    s := 5
    s.get()
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),get,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_445(self):
        input = """
const size = 2
const size_2 = size + 1
var a = [size]int{1, 2}
var b = [size_2]int{1, 2, 3}
func main() {
    a := b
}
"""
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_446(self):
        input = """
type S struct {
    x int
}
func (s S) x() int {
    return s.x
}
func (s S) x(y int) {
    return
}
"""
        expect = "Redeclared Method: x\n"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_447(self):
        input = """
func main() {
    x := 1
    y := x > "compare"
}
"""
        expect = """Type Mismatch: BinaryOp(Id(x),>,StringLiteral("compare"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_448(self):
        input = """
type I interface {
    foo()
}
type S struct {
    x int
}
func (s S) foo() {
    return
}
var i I = S{}
var x = i + 1
"""
        expect = "Type Mismatch: BinaryOp(Id(i),+,IntLiteral(1))\n"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_449(self):
        input = """
func main() {
    arr := [2][2]int{{1, 2}, {3, 4}}
    x := arr[1]
    y := x[0] + x
}
"""
        expect = "Type Mismatch: BinaryOp(ArrayCell(Id(x),[IntLiteral(0)]),+,Id(x))\n"
        self.assertTrue(TestChecker.test(input, expect, 449))
        
    def test_450(self):
        input = """
func main() {
    x := 1
    y := x()
}
"""
        expect = "Undeclared Function: x\n"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_451(self):
        input = """
type S struct {
    x int
}
var s = S{}
func main() {
    s.x := "wrong"
}
"""
        expect = """Type Mismatch: Assign(FieldAccess(Id(s),x),StringLiteral("wrong"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_452(self):
        input = """
type Inner struct {
    val int
}
type Outer struct {
    inner Inner
    inner string
}
"""
        expect = "Redeclared Field: inner\n"
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_453(self):
        input = """
type I interface {
    get() int
}
type S struct {
    x int
}
func (s S) get() int {
    return s.x
}
var i I = S{}
var x = i.get().val
"""
        expect = "Type Mismatch: FieldAccess(MethodCall(Id(i),get,[]),val)\n"
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_454(self):
        input = """
func main() {
    arr := [2]int{1, 2}
    arr[0] := "invalid"
}
"""
        expect = """Type Mismatch: Assign(ArrayCell(Id(arr),[IntLiteral(0)]),StringLiteral("invalid"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_455(self):
        input = """
type S struct {
    name string
}
func (s S) name() string {
    return s.name
}
func (s S) name(x int) {
    return
}
"""
        expect = "Redeclared Method: name\n"
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_456(self):
        input = """
func main() {
    x := 1
    if (x) {
        putLn()
    }
}
"""
        expect = """Type Mismatch: If(Id(x),Block([FuncCall(putLn,[])]))\n"""
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_457(self):
        input = """
const c = 1
func main() {
    c := "shadow"
}
"""
        expect = """Type Mismatch: Assign(Id(c),StringLiteral("shadow"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_458(self):
        input = """
type S struct {
    x int
}
func (s S) set() {
    return
}
func main() {
    s := S{}
    x := s.set()
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),set,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_459(self):
        input = """
var a = [2]int{1, 2}
var b = [2]string{"a", "b"}
func main() {
    a := b
}
"""
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_460(self):
        input = """
type I interface {
    foo()
}
type J interface {
    fun()
}
type S struct {}
func (s S) foo() {
    return
}
var i I = S{}
var j J = S{}
"""
        expect = "Type Mismatch: VarDecl(j,Id(J),StructLiteral(S,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_461(self):
        input = """
func foo() int {
    return "wrong"
}
func main() {
    x := foo() + foo
}
"""
        expect = """Type Mismatch: Return(StringLiteral("wrong"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_462(self):
        input = """
type S struct {
    x int
}
func main() {
    s := S{}
    s := "reassign"
}
"""
        expect = """Type Mismatch: Assign(Id(s),StringLiteral("reassign"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_463(self):
        input = """
func main() {
    arr := [2][3]int{{1, 2, 3}, {4, 5, 6}}
    for i, row := range arr {
        row := i
    }
}
"""
        expect = "Type Mismatch: Assign(Id(row),Id(i))\n"
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_464(self):
        input = """
type S struct {
    val int
}
func (s S) get() int {
    return s.val
}
func main() {
    s := S{}
    s.get := 5
}
"""
        expect = "Undeclared Field: get\n"
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_465(self):
        input = """
const n = 3
var a = [n]int{1, 2, 3}
func main() {
    a[0] := a
}
"""
        expect = "Type Mismatch: Assign(ArrayCell(Id(a),[IntLiteral(0)]),Id(a))\n"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_466(self):
        input = """
type I interface {
    get(x int) int
}
func main() {
    var i I
    x := i.get()
}
"""
        expect = "Type Mismatch: MethodCall(Id(i),get,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_467(self):
        input = """
func main() {
    x := 1
    y := x % "mod"
}
"""
        expect = """Type Mismatch: BinaryOp(Id(x),%,StringLiteral("mod"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 467))

    def test_468(self):
        input = """
type S struct {
    x int
}
type T struct {
    s S
}
var t = T{s: S{x: 1}}
var x = t.s.y
"""
        expect = "Undeclared Field: y\n"
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_469(self):
        input = """
func foo(x int, y int) int {
    return x + y
}
func main() {
    x := foo(1, 2, 3)
}
"""
        expect = "Type Mismatch: FuncCall(foo,[IntLiteral(1),IntLiteral(2),IntLiteral(3)])\n"
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_470(self):
        input = """
func main() {
    x := 1
    y := x[0]
}
"""
        expect = "Type Mismatch: ArrayCell(Id(x),[IntLiteral(0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_471(self):
        input = """
type S struct {
    x int
}
func (s S) get() int {
    return s.x
}
func main() {
    s := S{}
    x := s.get().x
}
"""
        expect = "Type Mismatch: FieldAccess(MethodCall(Id(s),get,[]),x)\n"
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_472(self):
        input = """
func foo(x int) int {
    return x
}
func foo() {
    return
}
"""
        expect = "Redeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 472))

    def test_473(self):
        input = """
type I interface {
    set(x string)
}
type S struct {
    val string
}
func (s S) set(x string) {
    s.val := x
}
var i I = S{}
func main() {
    i.set(42)
}
"""
        expect = "Type Mismatch: MethodCall(Id(i),set,[IntLiteral(42)])\n"
        self.assertTrue(TestChecker.test(input, expect, 473))

    def test_474(self):
        input = """
const n = 2
var a = [n]int{1, 2}
func main() {
    for i, v := range a {
        i := v + "text"
    }
}
"""
        expect = """Type Mismatch: BinaryOp(Id(v),+,StringLiteral("text"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_475(self):
        input = """
type S struct {
    x int
    x string
}
var s = S{x: 1}
"""
        expect = "Redeclared Field: x\n"
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_476(self):
        input = """
func main() {
    x := 1
    var y boolean 
    y := x + 1
}
"""
        expect = "Type Mismatch: Assign(Id(y),BinaryOp(Id(x),+,IntLiteral(1)))\n"
        self.assertTrue(TestChecker.test(input, expect, 476))

    def test_477(self):
        input = """
type S struct {
    val int
    t T
}
type T interface {
    get() S
}
func main() {
    s := S{}
    s.t := S{}
}
"""
        expect = "Type Mismatch: Assign(FieldAccess(Id(s),t),StructLiteral(S,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 477))

    def test_478(self):
        input = """
func foo() int {
    return 1
}
func main() {
    x := foo
    y := x()
}
"""
        expect = "Undeclared Identifier: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_479(self):
        input = """
type T struct {
    x int
}
var t = T{x: 1}
func main() {
    t.x := t
}
"""
        expect = "Type Mismatch: Assign(FieldAccess(Id(t),x),Id(t))\n"
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
func (v ABC) print () {return ;}
func (v ABC) Hi () {return ;}
type ABC struct {
    TrungTin int;
    Hi int;
}
        """
        self.assertTrue(TestChecker.test(input, """Redeclared Method: Hi\n""", 491))

    def test_492(self):
        input = """
type S struct {
    x int
}
func main() {
    s := S{}
    s := s.x
}
"""
        expect = "Type Mismatch: Assign(Id(s),FieldAccess(Id(s),x))\n"
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_493(self):
        input = """
func main() {
    arr := [2][2]int{{1, 2}, {3, 4}}
    arr[1] := "row"
}
"""
        expect = """Type Mismatch: Assign(ArrayCell(Id(arr),[IntLiteral(1)]),StringLiteral("row"))\n"""
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_494(self):
        input = """
type I interface {
    print() 
}
type S struct {
    val S
}
func (s S) print() {
    return
}
func (s S) get() S {
    return s.val
}
var i I 
var a S = S{}
func main() {
    i := a.get()
    var a int = a.get()
}
"""
        expect = "Type Mismatch: VarDecl(a,IntType,MethodCall(Id(a),get,[]))\n"
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_495(self):
        input = """
func foo(x int) int {
    return x
}
func main() {
    x := foo(foo)
}
"""
        expect = "Undeclared Identifier: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_496(self):
        input = """
const n = 2
var a = [n]int{1, 2}
func main() {
    for i := 0; i < a; i += 1 {
        putLn()
    }
}
"""
        expect = "Type Mismatch: BinaryOp(Id(i),<,Id(a))\n"
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test_497(self):
        input = """
type S struct {
    x int
}
func (s S) set(x int) {
    s.x := x
}
func main() {
    s := S{}
    s.set(s)
}
"""
        expect = "Type Mismatch: MethodCall(Id(s),set,[Id(s)])\n"
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_498(self):
        input = """
type T struct {
    val int
}
var t = T{val: 1}
var x = t.val[0]
"""
        expect = "Type Mismatch: ArrayCell(FieldAccess(Id(t),val),[IntLiteral(0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_499(self):
        input = """
func main() {
    x := 1
    y := x
    for x, y := range y {
        putLn()
    }
}
"""
        expect = "Type Mismatch: ForEach(Id(x),Id(y),Id(y),Block([FuncCall(putLn,[])]))\n"
        self.assertTrue(TestChecker.test(input, expect, 499))