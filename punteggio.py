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

def calcola(name, periods):
    
    # Accumula intervalli secondo l'anno scolastico
    years = {}
    for j, p in enumerate(periods):
        ps = p.split('-')
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
            years[y] = [(t1, t2)]
        else:
            years[y].append((t1, t2))    
    years = dict(sorted(years.items(), key=lambda item: item[1]))    
    
    # Calcola il punteggio per ciascun anno scolastico
    days, points = 0, 0
    for y in years:
        dt = timedelta(0)
        for t1, t2 in years[y]:
            dt += t2-t1+timedelta(days=1)

        if dt.days < 16:
            p = 0
        if dt.days > 16:
            p = min(2+2*(dt.days-16)/30, 12)
        days += dt.days
        points += p
        print("%i-%i: %3i giorni, %2i punti" % (y, y+1, dt.days, p))
            

    print('%s ha guadagnato %i punti!' % (name, points))

    return
