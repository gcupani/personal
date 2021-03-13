from copy import deepcopy as dc
from datetime import date, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta as rd
from IPython.display import HTML, Javascript, display
import sys

def initialize():
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
    points = 0
    days, months, exc, years = 0, 0, 0, 0
    #name, surname = sys.argv[1:3]
    dt = timedelta(0)
    #s = date.fromisoformat(sys.argv[3].split(',')[0])
    #s = date.fromisoformat(periods[0].split('-')[0].replace('/','-'))
    s = parser.parse(periods[0].split('-')[0])#, '%y/%m/%d')
    #print(s)

    #for i,a in enumerate(sys.argv[3:]):
        #t1, t2 = date.fromisoformat(a.split(',')[0]),\
        #         date.fromisoformat(a.split(',')[1])
    for j, p in enumerate(periods):
        #t1, t2 =  date.fromisoformat(p.split('-')[0].replace('/','-')),date.fromisoformat(p.split('-')[1].replace('/','-'))
        ps = p.split('-')
        t1, t2 = parser.parse(ps[0]), parser.parse(ps[1])
        if t2<t1:
            print("Le date %s non sono ordinate correttamente. Controllare." % p)
            return
        if t2.year-t1.year>1 or (t2.month>8 and t1.month<9):
            print("Le date %s non appartengono allo stesso anno scolastico. Controllare." % p)
            return
        ey = s.year if s.month < 9 else s.year+1
        if t1.year > ey or (t1.year == ey and t1.month > 8):
            dtm, dte = dt.days//30, dt.days%30
            add = min(dtm*2 + (dte>=16)*2, 12)
            points += add
            days += dt.days
            if add >= 12:
                years += 1
            else:
                months += dtm
                exc += dte
            #if i<len(sys.argv[3:])-1:
            if j<len(p)-1:
                dt = timedelta(0)
                s = t1
        dt += t2-t1+timedelta(days=1)

    dtm, dte = dt.days//30, dt.days%30
    add = min(dtm*2 + (dte>=16)*2, 12)
    points += add

    days += dt.days
    if add >= 12:
        years += 1
    else:
        months += dtm
        exc += dte



    print('%s ha guadagnato %i punti!' % (name, points))
    print('\nGiorni di servizio:     %3i' % days)
    if years > 0:
        print('Anni a punteggio pieno:  %2i  × 12 =%3i +' % (years, 12*years))
        print('Mesi aggiuntivi:         %2i  ×  2 = %2i +' % (months, 2*months))
        print('Giorni aggiuntivi:       %2i %s 16 → %2i =' % (exc, ' <' if exc<16 else '>=', 0 if exc<16 else 2))
    else:
        print('Mesi:                    %2i  ×  2 = %2i +' % (months, 2*months))
        print('Giorni aggiuntivi:       %2i %s 16 → %2i =' % (exc, ' <' if exc<16 else '>=', 0 if exc<16 else 2))
    print('                                   ----')
    print('Totale:                             %2i' % points)




    return
