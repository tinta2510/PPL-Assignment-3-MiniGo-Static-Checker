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


        
        