import sqlite3 as lite
import sys

con = lite.connect("bayes.db")

T = 'U' # do not set this
L = 'U' # do not set this
B = 'U' # do not set this

## set each of the following features to either 'U', 'Y', or 'N':
## 'U' (no evidence),
## 'Y' (sympton is present)
## 'N' (sympton is not present)
## Then run program. Output is the probability of T (tuberculosis), L (lung cancer), B (bronchitis)

Smoke = 'U'
Asia = 'U'
e = 'U'
X = 'U'
D = 'U'


with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS PeNorm")

    # create prior Smoke
    cur.execute("DROP TABLE IF EXISTS Smoke")
    cur.execute("CREATE TABLE Smoke(Id int, S text, PS real)")
    cur.execute("INSERT INTO Smoke VALUES(1, 'Y', .5)")
    cur.execute("INSERT INTO Smoke VALUES(2, 'N', .5)")

    #create prior Asia
    cur.execute("DROP TABLE IF EXISTS Asia")
    cur.execute("CREATE TABLE Asia(Id int, A text, PA real)")
    cur.execute("INSERT INTO Asia VALUES(1, 'Y', .01)")
    cur.execute("INSERT INTO Asia VALUES(2, 'N', .99)")

    # create Tub table
    cur.execute("DROP TABLE IF EXISTS Tub")
    cur.execute("CREATE TABLE Tub(Id int, T text, A text, PT real)")
    cur.execute("INSERT INTO Tub VALUES(1, 'Y', 'Y', .05)")
    cur.execute("INSERT INTO Tub VALUES(2, 'Y', 'N', .01)")
    cur.execute("INSERT INTO Tub VALUES(3, 'N', 'N', .99)")
    cur.execute("INSERT INTO Tub VALUES(4, 'N', 'Y', .95)")

    # create Lung table
    cur.execute("DROP TABLE IF EXISTS Lung")
    cur.execute("CREATE TABLE Lung(Id int, L text, S text, PL real)")
    cur.execute("INSERT INTO Lung VALUES(1, 'Y', 'Y', .10)")
    cur.execute("INSERT INTO Lung VALUES(2, 'Y', 'N', .01)")
    cur.execute("INSERT INTO Lung VALUES(3, 'N', 'N', .99)")
    cur.execute("INSERT INTO Lung VALUES(4, 'N', 'Y', .90)")
    
    # create Bron table
    cur.execute("DROP TABLE IF EXISTS Bron")
    cur.execute("CREATE TABLE Bron(Id int, B text, S text, PB real)")
    cur.execute("INSERT INTO Bron VALUES(1, 'Y', 'Y', .60)")
    cur.execute("INSERT INTO Bron VALUES(2, 'Y', 'N', .30)")
    cur.execute("INSERT INTO Bron VALUES(3, 'N', 'N', .70)")
    cur.execute("INSERT INTO Bron VALUES(4, 'N', 'Y', .40)")

    # create Xray table
    cur.execute("DROP TABLE IF EXISTS Xray")
    cur.execute("CREATE TABLE Xray(Id int, X text, e text, PX real)")
    cur.execute("INSERT INTO Xray VALUES(1, 'Y', 'Y', .98)")
    cur.execute("INSERT INTO Xray VALUES(2, 'Y', 'N', .05)")
    cur.execute("INSERT INTO Xray VALUES(3, 'N', 'N', .95)")
    cur.execute("INSERT INTO Xray VALUES(4, 'N', 'Y', .02)")

    # create Dyson table
    cur.execute("DROP TABLE IF EXISTS Dyson")
    cur.execute("CREATE TABLE Dyson(Id int, D text, e text, B text, PD real)")
    cur.execute("INSERT INTO Dyson VALUES(1, 'Y', 'Y', 'Y', .90)")
    cur.execute("INSERT INTO Dyson VALUES(2, 'Y', 'Y', 'N', .70)")
    cur.execute("INSERT INTO Dyson VALUES(3, 'Y', 'N', 'Y', .80)")
    cur.execute("INSERT INTO Dyson VALUES(4, 'Y', 'N', 'N', .10)")
    cur.execute("INSERT INTO Dyson VALUES(5, 'N', 'N', 'N', .90)")
    cur.execute("INSERT INTO Dyson VALUES(6, 'N', 'N', 'Y', .20)")
    cur.execute("INSERT INTO Dyson VALUES(7, 'N', 'Y', 'N', .30)")
    cur.execute("INSERT INTO Dyson VALUES(8, 'N', 'Y', 'Y', .10)")
    
    # create Either table
    cur.execute("DROP TABLE IF EXISTS Either")
    cur.execute("CREATE TABLE Either(Id int, e text, T text, L text, PE real)")
    cur.execute("INSERT INTO Either VALUES(1, 'Y', 'Y', 'Y', 1.)")
    cur.execute("INSERT INTO Either VALUES(2, 'Y', 'Y', 'N', 1.)")
    cur.execute("INSERT INTO Either VALUES(3, 'Y', 'N', 'Y', 1.)")
    cur.execute("INSERT INTO Either VALUES(4, 'Y', 'N', 'N', 0.)")
    cur.execute("INSERT INTO Either VALUES(5, 'N', 'N', 'N', 1.)")
    cur.execute("INSERT INTO Either VALUES(6, 'N', 'N', 'Y', 0.)")
    cur.execute("INSERT INTO Either VALUES(7, 'N', 'Y', 'N', 0.)")
    cur.execute("INSERT INTO Either VALUES(8, 'N', 'Y', 'Y', 0.)")

    # update prior Asia table
    if (Asia == 'Y'):
        cur.execute("DROP TABLE IF EXISTS Asia")
        cur.execute("CREATE TABLE Asia(Id int, A text, PA real)")
        cur.execute("INSERT INTO Asia VALUES(1, 'Y', 1.0)")
        cur.execute("INSERT INTO Asia VALUES(2, 'N', 0.0)")
    if (Asia == 'N'):
        cur.execute("DROP TABLE IF EXISTS Asia")
        cur.execute("CREATE TABLE Asia(Id int, A text, PA real)")
        cur.execute("INSERT INTO Asia VALUES(1, 'Y', 0.0)")
        cur.execute("INSERT INTO Asia VALUES(2, 'N', 1.0)")

    # update prior Smoke table
    if (Smoke == 'Y'):
        cur.execute("DROP TABLE IF EXISTS Smoke")
        cur.execute("CREATE TABLE Smoke(Id int, S text, PS real)")
        cur.execute("INSERT INTO Smoke VALUES(1, 'Y', 1.0)")
        cur.execute("INSERT INTO Smoke VALUES(2, 'N', 0.0)")
    if (Smoke == 'N'):
        cur.execute("DROP TABLE IF EXISTS Smoke")
        cur.execute("CREATE TABLE Smoke(Id int, S text, PS real)")
        cur.execute("INSERT INTO Smoke VALUES(1, 'Y', 0.0)")
        cur.execute("INSERT INTO Smoke VALUES(2, 'N', 1.0)")

    # create TubV view
    cur.execute("DROP VIEW IF EXISTS TubV")
    cur.execute("create view TubV as\
                select Tub.T, sum(Tub.PT * Asia.PA) as PT \
                from Tub, Asia \
                where Asia.A = Tub.A \
                group by Tub.T")
    cur.execute("select * from TubV")
    data = cur.fetchall()
    print "prior p(T) , Asia = ", Asia
    for row in data:
        print row

    # create LungV view
    cur.execute("DROP VIEW IF EXISTS LungV")
    cur.execute("create view LungV as \
                select Lung.L as L, sum(Lung.PL * Smoke.PS) as PL \
                from Lung, Smoke \
                where Smoke.S = Lung.S \
                group by Lung.L")
    cur.execute("select * from LungV")
    data = cur.fetchall()
    print "prior P(L), Smoking = ", Smoke
    for row in data:
        print row
    
    # create BronV view
    cur.execute("DROP VIEW IF EXISTS BronV")
    cur.execute("create view BronV as \
                select Bron.B as B, sum(Bron.PB * Smoke.PS) as PB \
                from Bron, Smoke \
                where Smoke.S = Bron.S \
                group by Bron.B")
    cur.execute("select * from BronV")
    data = cur.fetchall()
    print "prior p(B) , Smoking = ", Smoke
    for row in data:
        print row

    # calculate p(e); p(e=Y) and p(e=N)       
        cur.execute("select Either.e, sum(PE * PT * PL) as PE \
                    from Either, TubV, LungV \
                    group by Either.e")
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS EitherNorm")
        cur.execute("CREATE TABLE EitherNorm(Id int, e text, PE real)")
        cur.execute("INSERT INTO EitherNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO EitherNorm VALUES(2, ?, ? )", (data10, data1))
    cur.execute("SELECT * from EitherNorm")
    print "prior p(e)"
    rows = cur.fetchall()
    for row in rows:
        print row

    # check for evidence of e
    if (e != 'U'):
        cur.execute("DROP TABLE IF EXISTS PeNorm")
        cur.execute("CREATE TABLE PeNorm(Id int, e text, PE real)")
        if (e == 'Y'):
            cur.execute("INSERT INTO PeNorm VALUES(1, 'Y', 1.0)")
            cur.execute("INSERT INTO PeNorm VALUES(2, 'N', 0.0)")
        else:
            cur.execute("INSERT INTO PeNorm VALUES(1, 'Y', 0.0)")
            cur.execute("INSERT INTO PeNorm VALUES(2, 'N', 1.0)")
        cur.execute("SELECT * from PeNorm")
        data = cur.fetchall()
        print "posterior p(e)"
        for row in data:
            print row
        
    # p(e B | x D) = sig * p(x|e) * p(D|eB) * p(e) * p(B); sum out B; p(e|XD)
    if (e == 'U' and B == 'U' and D != 'U' and X != 'U'):
        cur.execute("select Xray.e, sum(Xray.PX * Dyson.PD * EitherNorm.PE * BronV.PB) \
                    from Xray, Dyson, EitherNorm, BronV \
                    where Xray.e = Dyson.e and Xray.e = EitherNorm.e and Dyson.B = BronV.B \
                    and Xray.X = ? and Dyson.D = ? \
                    group by Xray.e", (X, D))
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS PeNorm")
        cur.execute("CREATE TABLE PeNorm(Id int, e text, PE real)")
        cur.execute("INSERT INTO PeNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO PeNorm VALUES(2, ?, ?)", (data10, data1))
        cur.execute("SELECT * from PeNorm")
        data = cur.fetchall()
        print "posterior p(e) with X = ", X, " and D = ", D
        for row in data:
            print row
    
    # p(e|X) = sig * p(x|e)p(e)
    if (e == 'U' and X != 'U' and D == 'U'):
        cur.execute("select Xray.e, sum(PX * PE) \
                    from Xray, EitherNorm \
                    where Xray.e = EitherNorm.e and Xray.X = ? \
                    group by Xray.e", X)
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS PeNorm")
        cur.execute("CREATE TABLE PeNorm(Id int, e text, PE real)")
        cur.execute("INSERT INTO PeNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO PeNorm VALUES(2, ?, ?)", (data10, data1))
        cur.execute("SELECT * from PeNorm")
        data = cur.fetchall()
        print "posterior p(e) with X = ", X
        for row in data:
            print row

    # p(B, e | D) = sig * p(D | eB) * p(e) * p(B); sum out e; p(B|D)
    if (D != 'U' and e == 'U'):
        cur.execute("select Dyson.B, sum(Dyson.PD * EitherNorm.PE * BronV.PB) \
                 from Dyson, EitherNorm, BronV \
                 where Dyson.e = EitherNorm.e and Dyson.B = BronV.B and Dyson.D = ? \
                 group by Dyson.B", D)
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS BPbNorm")
        cur.execute("CREATE TABLE BPbNorm(Id int, B text, PB real)")
        cur.execute("INSERT INTO BPbNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO BPbNorm VALUES(1, ?, ?)", (data10, data1))
        cur.execute("SELECT * from BPbNorm")
        data = cur.fetchall()
        print "posterior p(B) with Dyson =", D
        for row in data:
            print row

    # p(B | eD) = sig * p(eD | B) * p(e) * p(B); p(B|D)
    if (D != 'U' and e != 'U'):
        cur.execute("select Dyson.B, sum(Dyson.PD * EitherNorm.PE * BronV.PB) \
                 from Dyson, EitherNorm, BronV \
                 where Dyson.e = ? and EitherNorm.e= ? and Dyson.B = BronV.B and Dyson.D = ? \
                 group by Dyson.B", (e, e, D))
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS BPbNorm")
        cur.execute("CREATE TABLE BPbNorm(Id int, B text, PB real)")
        cur.execute("INSERT INTO BPbNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO BPbNorm VALUES(1, ?, ?)", (data10, data1))
        cur.execute("SELECT * from BPbNorm")
        data = cur.fetchall()
        print "posterior p(B) with Dyson =", D
        for row in data:
            print row

    # p(e, B | D) = sig * p(D | eB) * p(e) * p(B); sum out B; p(e|D)
    if (e == 'U' and D != 'U' and B == 'U' and X == 'U'):
        cur.execute("select Dyson.e, sum(Dyson.PD * EitherNorm.PE * BronV.PB) \
                 from Dyson, EitherNorm, BronV \
                 where Dyson.e = EitherNorm.e and Dyson.B = BronV.B and Dyson.D = ? \
                 group by Dyson.e", D)
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS PeNorm")
        cur.execute("CREATE TABLE PeNorm(Id int, e text, PE real)")
        cur.execute("INSERT INTO PeNorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO PeNorm VALUES(1, ?, ?)", (data10, data1))
        cur.execute("SELECT * from PeNorm")
        data = cur.fetchall()
        print "posterior p(e) with Dyson =", D
        for row in data:
            print row

    # p(T, L | e = ?) = sig * p(e|TL) * p(T) * p(L); sum out L; p(T|e=?)
    if (e != 'U' and L == 'U'):
        cur.execute("DROP VIEW IF EXISTS TGivenE")
        cur.execute("select Either.T, sum(PE * PL * PT) as PT \
                from Either, LungV, TubV \
                where Either.L = LungV.L and Either.T = TubV.T and Either.e = ? \
                group by Either.T", e)
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS TGivenENorm")
        cur.execute("CREATE TABLE TGivenENorm(Id int, T text, PT real)")
        cur.execute("INSERT INTO TGivenENorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO TGivenENorm VALUES(2, ?, ?)", (data10, data1))
        cur.execute("SELECT * from TGivenENorm")
        data = cur.fetchall()
        print "p(T); sum out L"
        for row in data:
            print row    
    
    # p(L, T | e = ?) = sig * p(e|LT) * p(L) * p(T); sum out T; p(L|e=?)
    if (e != 'U' and T == 'U'):
        cur.execute("select Either.L, sum(PE * PL * PT) as PL \
                from Either, LungV, TubV \
                where Either.L = LungV.L and Either.T = TubV.T and Either.e = ? \
                group by Either.L", e)
        data = cur.fetchall()
        totalprob = data[0][1] + data[1][1]
        data00 = data[0][0]
        data10 = data[1][0]
        data0 = data[0][1]/totalprob
        data1 = data[1][1]/totalprob
        cur.execute("DROP TABLE IF EXISTS LGivenENorm")
        cur.execute("CREATE TABLE LGivenENorm(Id int, L text, PL real)")
        cur.execute("INSERT INTO LGivenENorm VALUES(1, ?, ?)", (data00, data0))
        cur.execute("INSERT INTO LGivenENorm VALUES(2, ?, ?)", (data10, data1))
        cur.execute("SELECT * from LGivenENorm")
        data = cur.fetchall()
        print "p(L); sum out T"
        for row in data:
            print row

    # Now use p(T|e) and p(L|e) and aposterior p(e) (PeNorm) to update p(T), p(L)
    # if PeNorm exists

    # check whether there is any need to update p(T) and p(L) (only if evidence)   
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PeNorm'")
    data = cur.fetchall()
    if data:    
        if (e == 'U' and L == 'U'):
            cur.execute("select Either.T, sum(Either.PE * LungV.PL * TubV.PT * PeNorm.PE) as PT \
                    from Either, LungV, TubV, PeNorm \
                    where Either.L = LungV.L and Either.T = TubV.T \
                    and PeNorm.e = Either.e \
                    group by Either.T")
            data = cur.fetchall()
            totalprob = data[0][1] + data[1][1]
            data00 = data[0][0]
            data10 = data[1][0]
            data0 = data[0][1]/totalprob
            data1 = data[1][1]/totalprob
            cur.execute("DROP TABLE IF EXISTS TGivenENorm")
            cur.execute("CREATE TABLE TGivenENorm(Id int, T text, PT real)")
            cur.execute("INSERT INTO TGivenENorm VALUES(1, ?, ?)", (data00, data0))
            cur.execute("INSERT INTO TGivenENorm VALUES(2, ?, ?)", (data10, data1))
            cur.execute("SELECT * from TGivenENorm")
            data = cur.fetchall()
            print "p(T), sum out L"
            for row in data:
                print row

        if (e == 'U' and T == 'U'):
            cur.execute("select Either.L, sum(Either.PE * LungV.PL * TubV.PT * PeNorm.PE) as PT \
                    from Either, LungV, TubV, PeNorm \
                    where Either.L = LungV.L and Either.T = TubV.T \
                    and PeNorm.e = Either.e \
                    group by Either.L")
            data = cur.fetchall()
            totalprob = data[0][1] + data[1][1]
            data00 = data[0][0]
            data10 = data[1][0]
            data0 = data[0][1]/totalprob
            data1 = data[1][1]/totalprob
            cur.execute("DROP TABLE IF EXISTS LGivenENorm")
            cur.execute("CREATE TABLE LGivenENorm(Id int, T text, PT real)")
            cur.execute("INSERT INTO LGivenENorm VALUES(1, ?, ?)", (data00, data0))
            cur.execute("INSERT INTO LGivenENorm VALUES(2, ?, ?)", (data10, data1))
            cur.execute("SELECT * from LGivenENorm")
            data = cur.fetchall()
            print "p(L); sum out T"
            for row in data:
                print row
            
