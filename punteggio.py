"""
© Guido Cupani, 2021 – guido.cupani(at)gmail.com
DISCLAIMER: Il software è offerto senza alcuna garanzia riguardo all'affidabilità e all'accuratezza dei risultati.
Lo sviluppatore declina qualsiasi responsabilità derivante dal suo utilizzo da parte di terzi.
"""

from copy import deepcopy as dc
from datetime import date, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta as rd
from IPython.display import HTML, Javascript, display
from pandas import read_excel
import sys
    

def initialize():
    # From https://stackoverflow.com/questions/54886701/how-to-code-restart-kernel-and-run-all-in-button-for-python-jupyter-notebook
    display(HTML(
        '''
            <script>
                code_show = false;
                function restart_run_all(){
                    IPython.notebook.kernel.restart();
                    setTimeout(function(){
                        IPython.notebook.execute_all_cells();
                    }, 10000)
                }
            </script>
            <button onclick="restart_run_all()">Calcola</button>
        '''
    ))
initialize()

def calcola(name, classes, periods, path=None):
    
    if path is not None:
        print("I periodi sono importati dal file %s." % path)
        df = read_excel(path)
        t1, t2, c = df['Unnamed: 2'], df['Unnamed: 3'], df['Table 1']
        periods = []
        for i in range(1,len(df)):
            periods.append("%2i/%02i/%2i-%2i/%02i/%2i,%s" \
                           % (t1[i].day, t1[i].month, t1[i].year, t2[i].day, t2[i].month, t2[i].year, c[i]))
        
    
    # Accumula intervalli secondo l'anno scolastico
    years = {}
    periods_new = []
    for j, p in enumerate(periods):
        ps = p.split(',')[0].split('-')
        try:
            c = p.split(',')[1].strip()
            if c not in classes:
                print("Le date %s sono assegnate a una classe non in lista. Controllare." % p.split(',')[0])
                return
        except:
            if len(classes)==1:
                c = classes[0]
            else:
                print("Le date %s non sono assegnate a una classe. Controllare." % p)
                return
        t1, t2 = parser.parse(ps[0], dayfirst=True), parser.parse(ps[1], dayfirst=True)
        #print(t1, t2)
        if t2<t1:
            print("Le date %s non sono ordinate correttamente. Controllare." % p)
            return
        if t2.year-t1.year>1 or (t2.month>8 and t1.month<9):
            print("Le date %s non appartengono allo stesso anno scolastico. Controllare." % p)
            return
        #ey = s.year if s.month > 9 else s.year-1
        
        y = t1.year if t1.month >= 9 else t1.year-1
        if y not in years:
            years[y] = [(t1, t2, c)]
        else:
            years[y].append((t1, t2, c))
            
        periods_new.append((y, t1, p.split(',')[0], t2-t1+timedelta(days=1), c))
    years = dict(sorted(years.items(), key=lambda item: item[1]))    
    
    periods_new = sorted(periods_new)
    len_p = max([len(p[2]) for p in periods_new])
    len_c = max(max([len(p[4]) for p in periods_new]), 6)

    
    print('┌'+'─'*(len_p+2)+'┬'+'─'*8+'┬'+'─'*11+'┬'+'─'*(len_c+2)+'┐')
    print("│ Periodo "+" "*(len_p-8)+" │ Durata │ Anno      │ Classe "+" "*(len_c-6)+"│") 
    print('├'+'─'*(len_p+2)+'┼'+'─'*8+'┼'+'─'*11+'┼'+'─'*(len_c+2)+'┤')
    for y,_,p,d,c in periods_new:
        print("│ %s │ %3i gg │ %s-%s │ %s%s │" % (p, d.days, y, y+1, c, " "*(len_c-len(c)))) 
    print('└'+'─'*(len_p+2)+'┴'+'─'*8+'┴'+'─'*11+'┴'+'─'*(len_c+2)+'┘')
    
    
    # Calcola il punteggio per ciascun anno scolastico
    days = {c: 0 for c in classes}
    points = {c: 0 for c in classes}
    
    print('┌'+'─'*11+('┬'+'─'*15)*len(classes)+'┐')
    print("│ Anno     ", end=' │ ') 
    for c in classes:
        print("%s         " % c, end=' │ ')
    print('\n├'+'─'*11+('┼'+'─'*15)*len(classes)+'┤')        
        
    for y in years:
        #dt = timedelta(0)
        dt = {c: timedelta(days=0) for c in classes}
        p = {c: 0 for c in classes}
        for t1, t2, c in years[y]:
            dt[c] += t2-t1+timedelta(days=1)
        for c0 in classes:
            if dt[c0].days > 16:
                for c1 in classes: 
                    p[c1] = min(p[c1]+1+(dt[c0].days-16)//30, 12)
                    if c1 == c0:
                        p[c1] = min(p[c1]+1+(dt[c0].days-16)//30, 12)
        print("│ %i-%i" % (y, y+1), end=' │ ') 
        for c in classes:
            days[c] += dt[c].days
            points[c] += p[c]
            print("%3i gg, %2i pp" % (dt[c].days, p[c]), end=' │ ')
        print("")
    
    print('├'+'─'*11+('┼'+'─'*15)*len(classes)+'┤')         
    print("│ Totale   ", end=' │ ')
    for c in classes:
        print("%3i gg, %2i pp" % (days[c], points[c]), end=' │ ')
    print('\n└'+'─'*11+('┴'+'─'*15)*len(classes)+'┘')        



    #print('%s ha guadagnato %i punti!' % (name, points))

    return
