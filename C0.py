"""
Created on Sat Jun  9 16:58:14 2018

@author: Ana Parać i Sara Pužar

Kratki opis - 
    Omogućile smo definiranje funkcija s int, void ili bool povratnom
    vrijednosti. Implementirale smo  for i  while petlje te if , else 
    i return naredbe.Također implementirani su sljedeći aritmetički
    i logički operatori: 
        +, -, *, /, +=, -=, *=, /=, =, ==, !=, <, <=, >, >=, %.
"""



from pj import * 

# ------------------ TOKENI ------------------  #

class C0(enum.Enum):
    # ključne riječi, operatori, ... 
    FOR = 'for'
    INT = 'int'
    BOOL = 'bool'
    STRING = 'string'
    WHILE = 'while'
    CHAR = 'char'
    VOID = 'void'
    IF  = 'if'
    ELSE = 'else'
    RETURN = 'return'
    NULL = 'NULL'
    OOTV, OZATV, VOTV, VZATV, ZAREZ = '(){},'
    PLUS, MINUS, PUTA, DIV = '+-*/'
    MANJE, VEĆE, JEDNAKO, TOČKAZ, MOD, NE = '<>=;%!'
    PLUSP = '++'
    MINUSM = '--'
    PLUSJ = '+='
    MINUSJ = '-='
    MJEDNAKO = '<='
    JJEDNAKO = '=='
    DIVJ = '/='
    PUTAJ = '*='
    NJEDNAKO = '!='   
    VJEDNAKO = '>='

    class IMEV(Token):
        def vrijednost(self, mem):
            return mem[self]
        
    class IMEF(Token):
        def vrijednost(self, mem):
            return mem[self]
    
    class BROJ(Token):
        def vrijednost(self, mem):
            return int(self.sadržaj)
    
    class LKONST(Token):
        def vrijednost(self, mem):
            return self.sadržaj == 'true'
           
# ------------------ LEXER ------------------  #
      
def c0_lex(source):
    lex = Tokenizer( source )
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak == '+':
            sljedeći = lex.čitaj()
            if sljedeći == '+': yield lex.token(C0.PLUSP)
            elif sljedeći == '=': yield lex.token(C0.PLUSJ)
            else: 
                lex.vrati()
                yield lex.token(C0.PLUS)
        elif znak == '<':
            if lex.čitaj() == '=': yield lex.token(C0.MJEDNAKO)
            else:
                lex.vrati()
                yield lex.token(C0.MANJE)
        elif znak == '=':
            if lex.čitaj() == '=': yield lex.token(C0.JJEDNAKO)
            else:
                lex.vrati()
                yield lex.token(C0.JEDNAKO)
        elif znak == '-':
            sljedeći = lex.čitaj()
            if sljedeći == '-': yield lex.token(C0.MINUSM)
            elif sljedeći == '=': yield lex.token(C0.MINUSJ)
            else: 
                lex.vrati()
                yield lex.token(C0.MINUS)
        elif znak == '/':
            sljedeći = lex.čitaj()
            if sljedeći == '=': yield lex.token(C0.DIVJ)
            else: 
                lex.vrati()
                yield lex.token(C0.DIV)
        elif znak == '*':
            sljedeći = lex.čitaj()
            if sljedeći == '=': yield lex.token(C0.PUTAJ)
            else: 
                lex.vrati()
                yield lex.token(C0.PUTA)
        elif znak == '!':
            sljedeći = lex.čitaj()
            if sljedeći == '=': yield lex.token(C0.NJEDNAKO)
            else:
                lex.vrati()
                yield lex.token(C0.NE)
        elif znak == '>': 
            sljedeći = lex.čitaj()
            if sljedeći == '=' : yield lex.token(C0.VJEDNAKO)
            else: 
                lex.vrati()
                yield lex.token(C0.VEĆE)
        elif znak.isdigit():
            lex.zvijezda(str.isdigit)
            if lex.sadržaj == '0' or lex.sadržaj[0] != '0':
                yield lex.token(C0.BROJ)
            else: lex.greška('druge baze nisu podržane')
        elif znak.isalpha():
            lex.zvijezda(str.isalnum) # jer imena mogu sadrzavati i brojeve
            ime = lex.sadržaj
            if lex.sadržaj in {'true', 'false'}: yield lex.token(C0.LKONST)
            elif lex.sadržaj in {'return'}: yield lex.token(C0.RETURN) 
            else:
                if lex.pogledaj() == '(':
                    yield lex.token(ključna_riječ(C0, ime) or C0.IMEF)
                
                else:
                    yield lex.token(ključna_riječ(C0, ime) or C0.IMEV)
        else:
            yield lex.token(operator(C0, znak) or lex.greška())
    
    
    
# ------------------GRAMATIKA ------------------  #    

## Komentar !! 
            """Ovo je gramatika s kojom smo započele izradu rada na temelju C0 dokumentacije.
            Prilikom implementacije smo izmjenile neke implementacijske detalje, međutim
            držale smo se generalne ideje."""
        
#   Start     -> funkcija | funckija funckije
#   funkcije  -> funkcije funkcija  | ε 
#   funkcija  -> tip IMEF OOTV  tip IMEV ( ZAREZ tip IMEV)*  OZATV VOTV tijelo VZATV

#   tijelo    -> IF OOTV vrijednost ZOTV tijelo [ ELSE tijelo ]   
#   tijelo    -> WHILE OOTV vrijednost OZAT tijelo
#   tijelo    -> FOR OOTV [ izraz ] TOČKAZ vrijednost TOČKAZ [ izraz ] OZAT tijelo
#   tijelo    -> return [ vrijednost ] TOČKAZ           
#   tijelo    -> VOTV ( tijelo )* VZAT
#   tijelo    -> izraz
            
#   izraz     -> IMEV PLUSP | IMEV MINUSM
#   izraz     -> tip IMEV [ JENDAKO vrijednost ]
#   izraz     -> IMEV JEDNAKO vrijednost | IMEV PLUSJ vrijednost | IMEV MINUSJ vrijednost
#   izraz     -> IMEV PUTAJ vrijednost | IMEV DIVJ vrijednost
#   izraz     -> vrijednost 

#   vrijednost -> OOTV vrijednost OZAT
#   vrijednost -> BROJ | TRUE | FALSE | NULL | IMEV 
#   vrijednost -> vrijednost operator vrijednost           

#   operator   -> PUTA | DIV | PLUS | MINUS | JJEDNAKO | NJEDNAKO | MJEDNAKO | VJEDNAKO | MANJE | VEĆE | MOD
        
#   tip -> INT | BOOL | VOID
            
# ------------------ PARSER ------------------  #    
  
class C0Parser(Parser):
    
    def start(self):
        self.funkcije = {}
        while not self >> E.KRAJ: 
            funkcija = self.funkcija()
            imef = funkcija.ime
            if imef in self.funkcije: raise SemantičkaGreška(
                    'Dvaput definirana funkcija ' + imef.sadržaj)
            self.funkcije[imef] = funkcija
        return self.funkcije   


    def funkcija(self):
        self.povratni_tip = self.pročitaj( C0.INT, C0.BOOL, C0.VOID )
        ime = self.pročitaj(C0.IMEF)
        self.pročitaj(C0.OOTV)
        tipovi = []
        argumenti = []
        tipovi.append( self.pročitaj(C0.INT, C0.BOOL) )
        argumenti.append( self.pročitaj(C0.IMEV) )      
        while not self >> C0.OZATV:
            self.pročitaj(C0.ZAREZ)
            tipovi.append( self.pročitaj(C0.INT, C0.BOOL) )
            argumenti.append( self.pročitaj(C0.IMEV) )
        return Funkcija( self.povratni_tip, ime, tipovi, argumenti, self.tijelo() )
    
    
    def tijelo(self):      
        if self >> C0.VOTV : 
            naredbe = []
            while not self >> C0.VZATV:
                naredbe.append( self.procitaj_naredbu() )
            return naredbe
        else:
            return [self.procitaj_naredbu()]


    def procitaj_naredbu(self):
        if self >> C0.IF: return self.grananje()
        elif self >> C0.FOR: return self.for_petlja()
        elif self >> C0.WHILE: return self.while_petlja()
        elif self >> C0.RETURN: 
            if self.povratni_tip ** {C0.BOOL}:
                log = self.log()
                self >> C0.TOČKAZ
                return Return(log )
            elif self.povratni_tip ** {C0.INT}:
                ari = self.aritm()
                self >> C0.TOČKAZ
                return Return(ari )
            elif self.povratni_tip ** {C0.VOID}:
                self >> C0.TOČKAZ   
                return Return("void")
        else: 
            izraz_ = self.izraz()
            self >> C0.TOČKAZ
            return( izraz_ )
          
            
    def while_petlja(self):
        self.pročitaj(C0.OOTV)
        uvjet_zaustavljanja = self.log()
        self.pročitaj( C0.OZATV)
        while_tijelo = self.tijelo()
        return While_petlja(uvjet_zaustavljanja, while_tijelo)
        
        
    def for_petlja(self):
        self.pročitaj(C0.OOTV)
        if self >> C0.TOČKAZ:
            start_ = "None"
        else :
            start_ = self.izraz()    
            self.pročitaj(C0.TOČKAZ)       
        uvjet_zaustavljanja = self.log()
        self.pročitaj(C0.TOČKAZ)        
        if self >> C0.OZATV:
            korak_ = "None"
        else :
            korak_ = self.izraz()
            self.pročitaj(C0.OZATV)           
        for_tijelo = self.tijelo()        
        return For_petlja( start_, uvjet_zaustavljanja, korak_, for_tijelo )       
        
        
    def izraz(self):       
        if self >> { C0.INT}:
                tip = self.zadnji
                ime = self.pročitaj(C0.IMEV)
                if self >> C0.JEDNAKO:
                    desna_v = self.aritm()
                    return Deklaracija(tip, ime, desna_v)               
                return Deklaracija(tip, ime, 0)
        elif self >> { C0.BOOL}:
                tip = self.zadnji
                ime = self.pročitaj(C0.IMEV)
                if self >> C0.JEDNAKO:
                    desna_v = self.log()
                    return Deklaracija(tip, ime, desna_v)               
                return Deklaracija(tip, ime, False)
        elif self >> C0.IMEV:
            lijeva_vrijednost = self.zadnji
            if self >> C0.PLUSP:
                return Postkrement(lijeva_vrijednost, self.zadnji)
            elif self >> C0.MINUSM:
                return Postkrement(lijeva_vrijednost, self.zadnji)
            elif self >> {C0.JEDNAKO, C0.PLUSJ, C0.MINUSJ, C0.PUTAJ, C0.DIVJ}:
                op_pridruživanja = self.zadnji
                desna_vrijednost = self.vrijednost() 
                return Pridruživanje(lijeva_vrijednost, op_pridruživanja, desna_vrijednost)
            else:
                if self.pogledaj() ==  C0.TOČKAZ :
                    return lijeva_vrijednost
        else:
            vrijednost_ = self.vrijednost()
            return vrijednost_  
        
        
    def vrijednost(self):
        if self >> C0.BROJ: return self.zadnji
        elif self >> C0.LKONST: return self.zadnji 
        elif self >> C0.NULL: return self.zadnji 
        elif self >> C0.IMEV: return self.zadnji
        elif self >> C0.OOTV:
            vrijednost_ = self.vrijednost()
            self >> C0.ZATV
            return vrijednost_
        else:
            l_vrijednost = self.vrijednost()
            if self >> { C0.PLUS, C0.MINUS, C0.DIV, C0.PUTA, C0.MOD }:
                aritmeticki = self.zadnji
                d_vrijednost = self.vrijednost()
                return Aritmeticki(l_vrijednost, aritmeticki, d_vrijednost)
            if self >> { C0.MANJE, C0.MJEDNAKO, C0.VJEDNAKO, C0.VEĆE, C0.JJEDNAKO, C0.NJEDNAKO }:
                logicki = self.zadnji
                d_vrijednost = self.vrijednost()
                return Logicki(l_vrijednost, logicki, d_vrijednost)    
        return
          
    
    def log(self):
        log_element = self.log_element(); 
        return log_element
    
    
    def log_element(self):
        if self >> C0.LKONST: return self.zadnji
        elif self >> { C0.IMEV, C0.BROJ }:
            self.vrati()
            lijevi = self.aritm()
            if self >> {C0.JJEDNAKO, C0.MANJE, C0.MJEDNAKO, C0.VEĆE, C0.VJEDNAKO, C0.NJEDNAKO}:
                Op_usporedbe = self.zadnji
                desni = self.aritm()  
                return Usporedba( Op_usporedbe, lijevi, desni )
            return lijevi
        
        
    def aritm(self):
        članovi = [self.član()]
        while self >> {C0.PLUS, C0.MINUS}:
            operator = self.zadnji
            dalje = self.član()
            članovi.append( dalje if operator ** C0.PLUS else Suprotan(dalje))
        return članovi[0] if len(članovi) == 1 else Zbroj(članovi)


    def član(self):
        if self >> C0.MINUS: return Suprotan(self.faktor())
        faktori = [self.faktor()]
        if self >> C0.MOD :
            faktori.append(self.faktor())
            while self >>  C0.MOD: 
                faktori.append(self.faktor())
            return faktori[0] if len(faktori) == 1 else Modulo(faktori)
        elif self >> C0.DIV :
            faktori.append(self.faktor())
            while self >>  C0.DIV: 
                faktori.append(self.faktor())
            return faktori[0] if len(faktori) == 1 else Div(faktori)
        elif self >> C0.PUTA :
            faktori.append(self.faktor())
            while self >>  C0.PUTA: 
                faktori.append(self.faktor())
            return faktori[0] if len(faktori) == 1 else Umnožak(faktori)
        return faktori[0]
    
    
    def faktor(self):
        if self >> C0.BROJ: return self.zadnji
        elif self >> C0.IMEV: return self.zadnji        
                
    
    def grananje(self):
        self.pročitaj(C0.OOTV)
        uvjet = self.log()    
        self.pročitaj(C0.OZATV)
        naredbe = self.tijelo();
        else_naredbe = []
        if self >> C0.ELSE:
            else_naredbe = self.tijelo()
        return Grananje(uvjet, naredbe, else_naredbe)

    
# ------------------ INTERPRETER ------------------  #


class UndefinedVariable(Exception):pass


class Funkcija(AST('povratni_tip ime tipovi parametri tijelo')): 
     def pozovi(self, argumenti):
        lokalni = dict(zip(self.parametri, argumenti))
        for naredba in self.tijelo:
            try: 
                naredba.izvrši(lokalni)
            except Povratak as exc: return exc.povratna_vrijednost


class Povratak(Exception):
    @property
    def povratna_vrijednost(self): return self.args[0]

   
class Return(AST('povratna_vrijednost')):
    def izvrši(self, mem): 
        if self.povratna_vrijednost != "void":
            raise Povratak(self.povratna_vrijednost.vrijednost(mem) )    


class Postkrement(AST('varijabla krement')): 
    def izvrši(self, mem):
        if self.krement ** {C0.PLUSP}:
            mem[self.varijabla] += 1
        elif self.krement ** {C0.MINUSM}:
            mem[self.varijabla] -= 1


class Pridruživanje(AST('lijeva_vrijednost op_pridruživanja desna_vrijednost')): 
    def izvrši(self, mem):
        assert( self.lijeva_vrijednost in mem) , "Undefined variable."  
        if self.op_pridruživanja ** {C0.JEDNAKO}:
            mem[self.lijeva_vrijednost] = self.desna_vrijednost.vrijednost(mem)
        elif self.op_pridruživanja ** {C0.PLUSJ}:
            mem[self.lijeva_vrijednost] += self.desna_vrijednost.vrijednost(mem)              
        elif self.op_pridruživanja ** {C0.PUTAJ}:
            mem[self.lijeva_vrijednost] *= self.desna_vrijednost.vrijednost(mem) 
        elif self.op_pridruživanja ** {C0.MINUSJ}:
            mem[self.lijeva_vrijednost] -= self.desna_vrijednost.vrijednost(mem) 
        elif self.op_pridruživanja ** {C0.DIVJ} and mem[self.lijeva_vrijednost] != 0:
            mem[self.lijeva_vrijednost] = int(mem[self.lijeva_vrijednost] / self.desna_vrijednost.vrijednost(mem) )                 

        
class Deklaracija(AST('tip ime desna_v')): 
    def izvrši(self, mem):
        if self.desna_v != 0:
            mem[self.ime] = self.desna_v.vrijednost(mem)
        else:
            mem[self.ime] = 0

class Aritmeticki(AST('l_vrijednost aritmeticki d_vrijednost')):pass


class Logicki(AST('l_vrijednost logicki d_vrijednost')):pass


class Zbroj(AST('pribrojnici')):
    def vrijednost(self, mem):
        return sum(pribroj.vrijednost(mem) for pribroj in self.pribrojnici)
    
    
class Suprotan(AST('od')):
    def vrijednost(self, mem): return -self.od.vrijednost(mem)
    
    
class Umnožak(AST('faktori')):
    def vrijednost(self, mem):
        p = 1
        for faktor in self.faktori: p *= faktor.vrijednost(mem)
        return p


class Modulo(AST('faktori')):
    def vrijednost(self, mem):
        return self.faktori[0].vrijednost(mem) % self.faktori[1].vrijednost(mem)


class Div(AST('faktori')):
    def vrijednost(self, mem):
        return self.faktori[0].vrijednost(mem) / self.faktori[1].vrijednost(mem)


class Usporedba(AST('op_usporedbe lijevi desni')):
    def vrijednost(self, mem):
        if self.op_usporedbe ** {C0.JJEDNAKO}: 
            return self.lijevi.vrijednost(mem) == self.desni.vrijednost(mem)
        elif self.op_usporedbe ** {C0.MJEDNAKO}:
            return self.lijevi.vrijednost(mem) <= self.desni.vrijednost(mem)
        elif self.op_usporedbe ** {C0.MANJE}:
            return self.lijevi.vrijednost(mem) < self.desni.vrijednost(mem)
        elif self.op_usporedbe ** {C0.VEĆE}:
            return self.lijevi.vrijednost(mem) > self.desni.vrijednost(mem)
        elif self.op_usporedbe ** {C0.VEĆEJ}:
            return self.lijevi.vrijednost(mem) >= self.desni.vrijednost(mem)
        elif self.op_usporedbe ** {C0.NJEDNAKO}:
            return self.lijevi.vrijednost(mem) != self.desni.vrijednost(mem)
        

class For_petlja(AST('start_ uvjet_zaustavljanja korak_ for_tijelo')):
    def izvrši(self, mem):
        self.start_.izvrši(mem)
        while self.uvjet_zaustavljanja.vrijednost(mem):
            for naredba in self.for_tijelo: 
                naredba.izvrši(mem)
                self.korak_.izvrši(mem)


class While_petlja(AST('uvjet_zaustavljanja while_tijelo')): 
    def izvrši(self, mem):
        while self.uvjet_zaustavljanja.vrijednost(mem):
            for naredba in self.while_tijelo: 
                naredba.izvrši(mem)
                

class Grananje(AST('uvjet naredbe else_naredbe')): 
    def izvrši(self, mem):
        if ( self.uvjet.vrijednost(mem) ):
            for naredba in self.naredbe:
                naredba.izvrši(mem)
        else:
            for naredba in self.else_naredbe:
                naredba.izvrši(mem)

def izvrši(funkcije, funkcija,  *argv):
    program = Token(C0.IMEF, funkcija)
    if program in funkcije:
        izlazna_vrijednost = funkcije[program].pozovi(argv)
        print('Program je vratio: ', izlazna_vrijednost)
    else: raise SemantičkaGreška('Nema željenje funkcije', funkcija, '.')




# ------------------ TESTIRANJE ------------------  #

if __name__ == '__main__':    

    """
    U varijablu ulaz zapisati željenje funkcije. 
    U funkciju izvrši upisati ime funkcije za koju želite da se izvrši te argumente
    s kojima ju želite pokrenuti.
    """
    
    ulaz = '''
    int Fakt(int n)
    {
      int F = 1;
      while ( n > 0 ){
        F *= n;
        n--;
      }    
      return F;
    }
      
    bool isPrime(int n)
    {
      if (n < 2) return false;
      if (n == 2) return true;
      if (n % 2 == 0) return false;
      for (int factor = 3; factor <= n/factor; factor += 2) {
        if (n % factor == 0)
          return false;
      }
      return true;
    }  
      
     int Bigger( int a, int b)
     {
      if ( a - b > 0 ){
        return a;
      }
      else{
        return b;
      }
     } 
      
'''

 
# Provjera lexera 
    print("********LEXER********")
    tokeni = list(c0_lex(ulaz))
    print(*tokeni)    
    
# Provjera parsera 
    print("********PARSER********")
    c0 = C0Parser.parsiraj(c0_lex(ulaz) )
    print(c0)
    
# Provjera interpretera
    """
    Funkcije : Fakt - poziv s jednim argumentom n, vraća n!
                    - demonstracija while petlje
               Bigger - poziv s dva argumenta a, b, vraća većeg                       
                      - demonstracija if else 
               isPrime - defaultna funkcija
    """
    
    print("********IZVRŠAVANJE********")
    izvrši(c0, "isPrime", 311 )    
    