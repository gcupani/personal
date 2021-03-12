from datetime import date, timedelta
from dateutil.relativedelta import relativedelta as rd
from copy import deepcopy as dc
import sys


def calcola(name, surname, start, end):
    points = 0
    #name, surname = sys.argv[1:3]
    dt = timedelta(0)
    #s = date.fromisoformat(sys.argv[3].split(',')[0])
    s = date.fromisoformat(start[0])

    #for i,a in enumerate(sys.argv[3:]):
        #t1, t2 = date.fromisoformat(a.split(',')[0]),\
        #         date.fromisoformat(a.split(',')[1])
    for j, (S,E) in enumerate(zip(start, end)):
        t1, t2 =  date.fromisoformat(S),date.fromisoformat(E)
        ey = s.year if s.month < 9 else s.year+1
        if t1.year > ey or (t1.year == ey and t1.month > 8):
            dtm, dte = dt.days//30, dt.days%30
            points += min(dtm*2 + (dte>=16)*2, 12)
            #if i<len(sys.argv[3:])-1:
            if j<len(start)-1:
                dt = timedelta(0)
                s = t1
        dt += t2-t1+timedelta(days=1)

    dtm, dte = dt.days//30, dt.days%30
    points += min(dtm*2 + (dte>=16)*2, 12)

    print('%s %s ha guadagnato %i punti!' % (name, surname, points))
