# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 13:46:38 2015

@author: Binoy
"""


from wageningen import *
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.interpolate import interp1d

pds = np.arange(0.6, 1.4, 0.2)                  # pitch ratio values
str_pds = [ str(i) for i in pds]                # pd as strings
jx = np.arange(0.01,1.5,.05)                    # for plotting purposes
js =[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]   # J values
f, ax = plt.subplots()                          # Plot handle
rho = 1.025                                     # t/m3
ax.grid(1)

def kt_j_optim(T, va, aea0, z, **kwargs):
    """Find optimum propeller for Required Thrust, advanced velocity, BAR,
    n or D

    T : Thrust
    va : Advance velocity
    aea0: Blade area ratio
    z : Number of blades

    kwargs can be revolution of propeller or Diameter
    """
    tabkt = ktpds(jx, pds, aea0, z)     # kt table for plot / curve fit
    pltTab(ax, tabkt)
    for key, value in kwargs.iteritems():
        print "%s = %s" % (key, value)
    if 'D' in kwargs:
        D = kwargs['D']
        kt_j2_const = (T / (rho * va **2 * D**2))
        kt_j2 = kt_j2_const* jx**2 # Eliminating n from the equation
        ax.plot(jx, kt_j2, linestyle= '--')
        optivals = np.zeros((len(pds)), \
        dtype = [('pd','f8'),('j', 'f8'), \
        ('kt','f8'), ('kq', 'f8'),('eta', 'f8')]) #Optimum value array

        row = 0
        for pdi in str_pds:
            curint = getIntersect(jx, tabkt[pdi], jx, kt_j2, 3, 2)
            valans = filter(lambda x : x > 0 and x <  max(jx), onlyreal(curint))
            if len(valans) > 1: print "more than one intersection found"
            cj = valans[0]
            ckt = kt(cj ,float(pdi), aea0, z)
            ckq = kq(cj ,float(pdi), aea0, z)
            eta0 = (cj * ckt)/ (ckq *2 * 3.14)
            optivals[row] = np.array([float(pdi), cj, ckt , ckq,eta0])
            plotInter(ax,  cj, kt(cj,float(pdi),aea0,z))
            row +=1

        print "Intersections of kt_j^2 curve with kt vals:"
        print print_structarray(optivals)

        # Finding optimum efficiency
        optietafit = np.polyfit(optivals['j'], optivals['eta'],3)
        j4eta = np.linspace(min(optivals['j']),max(optivals['j']),50)
        eta_fiteval = np.polyval(optietafit, j4eta)
        dereta = np.polyder(optietafit)
        ax.plot(j4eta,eta_fiteval)
        ax.plot(optivals['j'], optivals['eta'], 'o', color ='b')
        optipt = np.roots(dereta)
        opti_rps = va/(optipt*D)

        print "Optimum J vals :", optipt
        print "Optimum n vals:", opti_rps
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]
        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))
        print "Selected n val:", va/(sel_j*D)
        _max_eta = np.polyval(optietafit, sel_j)
        print "Maximum Efficiency:", _max_eta
        f2 = interp1d(optivals['j'], optivals['pd'], kind='linear')
        sel_pd = f2(sel_j)
        print "P/D for maximum efficiency:", sel_pd
        f2,a2 = plt.subplots()
        a2.plot(optivals['pd'], optivals['eta'],'o')
        a2.plot(sel_pd, _max_eta,'+')
        a2.set_xlabel('P/D')
        a2.set_ylabel('$\eta$')
        sel_kt = kt(sel_j,sel_pd, aea0, z)
        sel_kq = kq(sel_j, sel_pd, aea0,z)

        outl = [['Optimised j', sel_j], ['Optimised pd', sel_pd],\
        ['Optimised kt', sel_kt], ['Optimised kq', sel_kq],\
        ['Optimised efficiency', _max_eta], ['D optimised',D],\
        ['Optimised n', va/(sel_j*D) ]]
        print tabulate(outl)

    if 'n' in kwargs:
        n = kwargs['n']
        kt_j4_const = ((T*n**2) / (rho * va **4 ))
        kt_j4 = kt_j4_const* jx**4 # Eliminating n from the equation
        ax.plot(jx, kt_j4, linestyle= '--')
        optivals = np.zeros((len(pds)), \
        dtype = [('pd','f8'),('j', 'f8'), \
        ('kt','f8'), ('kq', 'f8'),('eta', 'f8')]) #Optimum value array

        row = 0
        for pdi in str_pds:
            curint = getIntersect(jx, tabkt[pdi], jx, kt_j4, 3, 4)
            valans = filter(lambda x : x > 0 and x <  max(jx), onlyreal(curint))
            if len(valans) > 1: print "more than one intersection found"
            cj = valans[0]
            ckt = kt(cj ,float(pdi), aea0, z)
            ckq = kq(cj ,float(pdi), aea0, z)
            eta0 = (cj * ckt)/ (ckq *2 * 3.14)
            optivals[row] = np.array([float(pdi), cj, ckt , ckq,eta0])
            plotInter(ax,  cj, kt(cj,float(pdi),aea0,z))
            row +=1

        print "Intersections of kt_j^4 curve with kt vals:"
        print print_structarray(optivals)

        # Finding optimum efficiency
        optietafit = np.polyfit(optivals['j'], optivals['eta'],3)
        j4eta = np.linspace(min(optivals['j']),max(optivals['j']),50)
        eta_fiteval = np.polyval(optietafit, j4eta)
        dereta = np.polyder(optietafit)
        ax.plot(j4eta,eta_fiteval)
        ax.plot(optivals['j'], optivals['eta'], 'o', color ='b')
        optipt = np.roots(dereta)
        opti_D = va/(optipt*n)
        print optipt
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]
        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))

        print "Optimum J vals :", optipt
        print "Optimum D vals:", opti_D
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]
        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))
        print "Selected D val:", va/(sel_j*n)

        _max_eta = np.polyval(optietafit, sel_j)
        print "Maximum Efficiency:", _max_eta
        f2 = interp1d(optivals['j'], optivals['pd'], kind='linear')
        sel_pd = f2(sel_j)
        print "P/D for maximum efficiency:", sel_pd
        f2,a2 = plt.subplots()
        a2.plot(optivals['pd'], optivals['eta'],'o')
        a2.plot(sel_pd, _max_eta,'+')
        a2.set_xlabel('P/D')
        a2.set_ylabel('$\eta$')
        sel_kt = kt(sel_j,sel_pd, aea0, z)
        sel_kq = kq(sel_j, sel_pd, aea0,z)
        _sel_D = va/(sel_j*n)
        outl = [['Optimised j', sel_j], ['Optimised pd', sel_pd],\
        ['Optimised kt', sel_kt], ['Optimised kq', sel_kq],\
        ['Optimised efficiency', _max_eta], ['n optimised',n],\
        ['Optimised D', _sel_D], ["Thrust Developed", sel_kt*rho*n**2*_sel_D**4]]
        print tabulate(outl)



def kq_j_optim(Q, va, aea0, z, **kwargs):
    """Find optimum propeller for Required Torque, advanced velocity, BAR,
    n or D


    Q: Torque
    va : Advance velocity
    aea0: Blade area ratio
    z : Number of blades

    kwargs can be revolution of propeller or Diameter


    """

    ax.set_title(r'$K_Q$')
    tabkq = kqpds(jx, pds, aea0, z)     # kt table for plot / curve fit
    pltTab(ax, tabkq)



    if 'D' in kwargs:
        print "Given Power delivered and Diameter"
        D = kwargs['D']
        kq_j3_const = (Q / (2* np.pi*rho * va **3 * D**2))
        kq_j3 = kq_j3_const* jx**3 # Eliminating n from the equation

        ax.plot(jx, kq_j3, linestyle= '--')
        optivals = np.zeros((len(pds)), \
        dtype = [('pd','f8'),('j', 'f8'), \
        ('kt','f8'), ('kq', 'f8'),('eta', 'f8')]) #Optimum value array

        row = 0
        for pdi in str_pds:
            curint = getIntersect(jx, tabkq[pdi], jx, kq_j3, 3, 3)
            valans = filter(lambda x : x > 0 and x <  max(jx), onlyreal(curint))
            if len(valans) > 1: print "more than one intersection found"
            cj = valans[0]
            ckt = kt(cj ,float(pdi), aea0, z)
            ckq = kq(cj ,float(pdi), aea0, z)
            eta0 = (cj * ckt)/ (ckq *2 * 3.14)
            optivals[row] = np.array([float(pdi), cj, ckt , ckq,eta0])
            plotInter(ax,  cj, kq(cj,float(pdi),aea0,z))
            row +=1

        print "Intersections of kq_j^3 curve with kt vals:"
        print print_structarray(optivals)

        # Finding optimum efficiency
        optietafit = np.polyfit(optivals['j'], optivals['eta'],3)
        j4eta = np.linspace(min(optivals['j']),max(optivals['j']),50)
        eta_fiteval = np.polyval(optietafit, j4eta)
        dereta = np.polyder(optietafit)
        ax.plot(j4eta,eta_fiteval)
        ax.plot(optivals['j'], optivals['eta'], 'o', color ='b')
        optipt = np.roots(dereta)
        opti_rps = va/(optipt*D)

        print "Optimum J vals :", optipt
        print "Optimum n vals:", opti_rps
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]
        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))
        print "Selected n val:", va/(sel_j*D)

        _max_eta = np.polyval(optietafit, sel_j)
        print "Maximum Efficiency:", _max_eta
        f2 = interp1d(optivals['j'], optivals['pd'], kind='linear')
        sel_pd = f2(sel_j)
        print "P/D for maximum efficiency:", sel_pd
        f2,a2 = plt.subplots()
        a2.plot(optivals['pd'], optivals['eta'],'o')
        a2.plot(sel_pd, _max_eta,'+')
        a2.set_xlabel('P/D')
        a2.set_ylabel('$\eta$')

        sel_kt = kt(sel_j,sel_pd, aea0, z)
        sel_kq = kq(sel_j, sel_pd, aea0,z)
        outl = [['Optimised j', sel_j], ['Optimised pd', sel_pd],\
        ['Optimised kt', sel_kt], ['Optimised kq', sel_kq],\
        ['Optimised efficiency', _max_eta], ['n optimised',va/(sel_j*D)],\
        ['Optimised D', D ], ['Torque Generated',sel_kq*rho*(va/(sel_j*D))**2*D**5],\
        ['P developed',sel_kq*rho*(va/(sel_j*D))**2*D**5 * 2 *np.pi*(va/(sel_j*D))]]
        print tabulate(outl)

    if 'n' in kwargs:
        n = kwargs['n']
        kq_j5_const = ((Q*n**3) / (rho * va **5 ))
        kq_j5 = kq_j5_const* jx**5 # Eliminating n from the equation
        ax.plot(jx, kq_j5, linestyle= '--')
        optivals = np.zeros((len(pds)), \
        dtype = [('pd','f8'),('j', 'f8'), \
        ('kt','f8'), ('kq', 'f8'),('eta', 'f8')]) #Optimum value array

        row = 0
        for pdi in str_pds:
            curint = getIntersect(jx, tabkq[pdi], jx, kq_j5, 3, 5)
            valans = filter(lambda x : x > 0 and x <  max(jx), onlyreal(curint))
            if len(valans) > 1: print "more than one intersection found"
            cj = valans[0]
            ckt = kt(cj ,float(pdi), aea0, z)
            ckq = kq(cj ,float(pdi), aea0, z)
            eta0 = (cj * ckt)/ (ckq *2 * 3.14)
            optivals[row] = np.array([float(pdi), cj, ckt , ckq,eta0])
            plotInter(ax,  cj, kq(cj,float(pdi),aea0,z))
            row +=1

        print "Intersections of kq_j^5 curve with kt vals:"
        print print_structarray(optivals)

        # Finding optimum efficiency
        optietafit = np.polyfit(optivals['j'], optivals['eta'],3)
        j4eta = np.linspace(min(optivals['j']),max(optivals['j']),50)
        eta_fiteval = np.polyval(optietafit, j4eta)
        dereta = np.polyder(optietafit)
        ax.plot(j4eta,eta_fiteval)
        ax.plot(optivals['j'], optivals['eta'], 'o', color ='b')
        optipt = np.roots(dereta)
        opti_D = va/(optipt*n)



        print optipt
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]
        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))

        print "Optimum J vals :", optipt
        print "Optimum D vals:", opti_D
        sel_j = filter(lambda x : x > 0 and x <  max(optivals['j']), onlyreal(optipt))[0]


        _max_eta = np.polyval(optietafit, sel_j)
        print "Maximum Efficiency:", _max_eta
        f2 = interp1d(optivals['j'], optivals['pd'], kind='linear')
        sel_pd = f2(sel_j)
        print "P/D for maximum efficiency:", sel_pd

        f2,a2 = plt.subplots()
        a2.plot(optivals['pd'], optivals['eta'],'o')
        a2.plot(sel_pd, _max_eta,'+')
        a2.set_xlabel('P/D')
        a2.set_ylabel('$\eta$')
        print


        plotInter(ax, sel_j, np.polyval(optietafit,optipt[1]))
        print "Selected D val:", va/(sel_j*n)

        sel_kt = kt(sel_j,sel_pd, aea0, z)
        sel_kq = kq(sel_j, sel_pd, aea0,z)
        outl = [['Optimised j', sel_j], ['Optimised pd', sel_pd],\
        ['Optimised kt', sel_kt], ['Optimised kq', sel_kq],\
        ['Optimised efficiency', _max_eta], ['n optimised',n],\
        ['Optimised D', va/(sel_j*n) ],['Torque gen',sel_kq*rho*n**2*(va/(sel_j*n))**5]]
        print tabulate(outl)



if __name__ == "__main__":

    v_ship      = 16                    # velocity in knots
    aea0        =  0.55                 # BAR
    w           = 0.3                   # wake
    z           = 4                     # Number of Blades

    v_m         = v_ship * 0.5144       # velocity in m/s
    va          = v_m*(1-w)             # Velocity of advance


    Thrust      = 525
    D           = 5.2

    kt_j_optim(Thrust, va, aea0, z, D=D)

    Pd = 5250 #kW
    n = 120 /60 #rps
    Q = Pd /(2*3.14*n)

#    kq_j_optim(Q,va,aea0,z, n = n)
#


