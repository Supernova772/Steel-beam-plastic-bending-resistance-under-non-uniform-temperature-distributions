def y_neutral_stre(y_neutral,stre_dist):
    for i in range(len(stre_dist)-1):
        if stre_dist[i][1]<=y_neutral and stre_dist[i+1][1]>y_neutral:
            y_neutral_stre=(y_neutral-stre_dist[i][1])*(stre_dist[i+1][0]-stre_dist[i][0])/(stre_dist[i+1][1]-stre_dist[i][1])+stre_dist[i][0]
    return y_neutral_stre
def interpolation(a,stre_dist):
    for i in  range(len(stre_dist)-1):
        if stre_dist[i][1] <= a and stre_dist[i+1][1] > a:
            y_inter = (a-stre_dist[i][1])*(stre_dist[i+1][0]-stre_dist[i][0])/(stre_dist[i+1][1]-stre_dist[i][1])+stre_dist[i][0]
    return y_inter
def stre_red(temp):
    coefficient=[[20,1],[100,1],[200,1],[300,1],[400,1],[500,0.78],[600,0.47],[700,0.23],[800,0.11],[900,0.06],[1000,0.04],[1100,0.02],[1200,0]]
    for i in range(len(coefficient)-1):
        if temp >= coefficient[i][0] and temp < coefficient[i+1][0]:
            co_of_red = (temp-coefficient[i][0])/(coefficient[i+1][0]-coefficient[i][0])*(coefficient[i+1][1]-coefficient[i][1])+coefficient[i][1]
    return co_of_red
def intemp(a,b,c):
    d_temp=(a-b[0])*(b[1]-c[1])/(b[0]-c[0])+b[1]
    return d_temp
def Sort(sub_li):
    sub_li.sort(key = lambda x: x[1])
    return sub_li
def plastic_bending_moment(d,w,tf,tw,tempdist,fpl,E,Iz,Iw,It,Wpl,G):
    add=[]
    for i in range(len(tempdist)-1):
        num=int(abs(tempdist[i+1][0]-tempdist[i][0])//100)
        if num >1:
            if tempdist[i+1][0]>tempdist[i][0]:
                for j in range(1,num):
                    temp=tempdist[i][0]+j*100
                    pos=intemp(temp,tempdist[i],tempdist[i+1])
                    add.append([temp,pos])
            if tempdist[i+1][0]<tempdist[i][0]:
                for j in range(1,num):
                    temp=tempdist[i][0]-j*100
                    pos=intemp(temp,tempdist[i],tempdist[i+1])
                    add.append([temp,pos])    
    tempdist=tempdist+add
    tempdist=Sort(tempdist)
    print('<<<<<<  Plastic Bending Moment Calculation  >>>>>>')
    print('\n<<<<<<  Section Geometry  >>>>>>')
    print('Depth  d = '+str(d)+' mm')
    print('Width  w = '+str(w)+' mm')
    print('Flange thickness  tf = '+str(tf)+' mm')
    print('Web thickness  tw = '+str(tw)+' mm')
    print('\n<<<<<<  Section Properties  >>>>>>')
    print('Second moment of inertia of weak axis Iz = '+str(round(Iz*1e-4,2))+' cm^4')
    print('Warping constant Iw = '+str(round(Iw*1e-6,2))+' cm^6')
    print('Torsional constant It = '+str(round(It*1e-4,2))+' cm^4')
    print('Plastic section modulus Wpl = '+str(round(Wpl*1e-3,2))+' cm^3')
    print('\n<<<<<<  Material properties  >>>>>>')
    print('Yielding strength f_y = '+str(fpl)+' N/mm^2')
    print('Elastic modulus E = '+str(E)+' N/mm^2')
    print('Shear modulus G = '+str(G)+' N/mm^2')

    print('\n<<<<<<  Temperature Distribution  >>>>>>')
    print('Temp.distribution = [[Temperature,Position (x/d, x is the distance from top of the beam)],...]')
    disp_tempdist=[]
    for i in tempdist:
        disp_tempdist.append([i[0],round(i[1],2)])
    print('Temp.distribution =',disp_tempdist)
    stre_dist=[]
    i=0
    for i in range(len(tempdist)):
        stre_dist.append(tempdist[i].copy())
    i=0
    # Strength Reduction according to EC3
    i=0
    for stre_pt in stre_dist:
        co_of_red=stre_red(stre_pt[0])
        stre_dist[i][0]=co_of_red
        i=i+1
    a_s=tf/d
    b_s=(d-tf)/d
    uf_lower_stre=interpolation(a_s,stre_dist)
    lf_upper_stre=interpolation(b_s,stre_dist)
    stre_dist.append([uf_lower_stre,a_s])
    stre_dist.append([lf_upper_stre,b_s])
    stre_dist=Sort(stre_dist)
    counter_half=0
    area1=0
    area2=0
    area3=0
    area4=0
    y_neu=[]
    y_neutral=0
    for i in range(len(stre_dist)-1):
        if stre_dist[i+1][1]==0.5:
            break
        else:
            counter_half=counter_half+1
    i=0
    disp_stre_dist=[]
    for i in stre_dist:
        disp_stre_dist.append([round(i[0],2),round(i[1],2)])
    
    for i in range(len(stre_dist)): 
        area1=0
        area2=0
        area3=0
        area4=0     
        for j in range(i):
            if stre_dist[j+1][1]<=tf/d or stre_dist[j][1]>=(d-tf)/d and stre_dist[j+1][1]<=1:
                area1=area1+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*w
            elif stre_dist[j][1]>=tf/d and stre_dist[j+1][1]<=(d-tf)/d:
                area1=area1+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*tw
        #if i==len(stre_dist)-1:
        #    if stre_dist[i+1][1]<=tf/d or stre_dist[i][1]>=(d-tf)/d and stre_dist[i+1][1]<=1:
        #        area2=area2+(stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*w
        #    elif stre_dist[i][1]>=tf/d and stre_dist[i+1][1]<=(d-tf)/d:
        #        area2=area2+(stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*tw
        #else:    
        for k in range(i,len(stre_dist)-1):
            if stre_dist[k+1][1]<=tf/d or stre_dist[k][1]>=(d-tf)/d and stre_dist[k+1][1]<=1:
                area2=area2+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*w
            elif stre_dist[k][1]>=tf/d and stre_dist[k+1][1]<=(d-tf)/d:
                area2=area2+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*tw
        for j in range(i-1):
            if stre_dist[j+1][1]<=tf/d or stre_dist[j][1]>=(d-tf)/d and stre_dist[j+1][1]<=1:
                area3=area3+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*w
            elif stre_dist[j][1]>=tf/d and stre_dist[j+1][1]<=(d-tf)/d:
                area3=area3+(stre_dist[j][0]+stre_dist[j+1][0])*(stre_dist[j+1][1]-stre_dist[j][1])/2*tw
        for k in range(i-1,len(stre_dist)-1):
            if stre_dist[k+1][1]<=tf/d or stre_dist[k][1]>=(d-tf)/d and stre_dist[k+1][1]<=1:
                area4=area4+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*w
            elif stre_dist[k][1]>=tf/d and stre_dist[k+1][1]<=(d-tf)/d:
                area4=area4+(stre_dist[k][0]+stre_dist[k+1][0])*(stre_dist[k+1][1]-stre_dist[k][1])/2*tw     
        if area1>=area2 and area3<=area4:
            x = symbols('x')
            f_y_inter = (x-stre_dist[i-1][1])*(stre_dist[i][0]-stre_dist[i-1][0])/(stre_dist[i][1]-stre_dist[i-1][1])+stre_dist[i-1][0]
            if stre_dist[i][1]<=tf/d or stre_dist[i-1][1]>=(d-tf)/d and stre_dist[i][1]<=1:
                expr = area3+ w*(x-stre_dist[i-1][1])*(f_y_inter+stre_dist[i-1][0])/2-(area2+w*(stre_dist[i][1]-x)*(f_y_inter+stre_dist[i][0])/2)
            elif stre_dist[i-1][1]>=tf/d and stre_dist[i][1]<=(d-tf)/d:
                expr = area3+ tw*(x-stre_dist[i-1][1])*(f_y_inter+stre_dist[i-1][0])/2-(area2+tw*(stre_dist[i][1]-x)*(f_y_inter+stre_dist[i][0])/2)
            print('Equation of neutral axis',expr)
            y_neu=solve(expr)
            for sol in y_neu:
                if sol>=0:
                    y_neutral=sol
                    break
    y_neutral=round(y_neutral,2)
    print('\n<<<<<<  Non_dimensional_plastic_neutral_axis_position  >>>>>>')
    print('Equation of neutral axis = ',expr)
    print('plastic_neutral_axis_position='+str(y_neutral))    
    y_neutral_stre1=y_neutral_stre(y_neutral,stre_dist)
    if y_neutral != 0.5:
        stre_dist.append([y_neutral_stre1,y_neutral])
    stre_dist=Sort(stre_dist)
    i=0

    print('\n<<<<<<  Strength Distribution  >>>>>>')
    print('Strength distribution = [[Strength reduction factor,Position (x/d, x is the distance from top of the beam)],...]')
    print('Strength distribution =',disp_stre_dist)
    m=0
    print('\n<<<<<<  Calculate the plastic bending moment of each part  >>>>>>')
    print('x is the distance from top of the beam')



    for i in range(len(stre_dist)-1):
        print('\nPosition of calculation point (x/d)=',round(stre_dist[i][1],2))
        if i==0:
            if stre_dist[i][0]>=stre_dist[i+1][0]:
                print('Current strength reduction factor >= the next strength reduction factor')
                if stre_dist[i][1] < tf/d:
                    print('the next calculation point is in the upper flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                    print('the next calculation point is in the web')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                    print( 'Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                    print('the next calculation point is in the lower flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')      
            elif stre_dist[i][0]<stre_dist[i+1][0]:
                print('Current strength reduction factor < the next strength reduction factor')
                if stre_dist[i][1] < tf/d:
                    print('the next calculation point is in the upper flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                    print('the next calculation point is in the web')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                    print('the next calculation point is in the lower flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*min('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+')+max('+str(round(stre_dist[i+1][0],2))+','+str(round(stre_dist[i][0],2))+'))/(('+str(round(stre_dist[i+1][0],2))+')+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
        elif i>0:
            if stre_dist[i][0]>=stre_dist[i+1][0]:
                print('Current strength reduction factor >= the next strength reduction factor')
                if stre_dist[i][1] < tf/d:
                    print('the next calculation point is in the upper flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(d)+'^2*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                    print('the next calculation point is in the web')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*tw*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(tw)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                    print('the next calculation point is in the lower flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3+stre_dist[i][1]))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
            elif stre_dist[i][0]<stre_dist[i+1][0]:
                print('Current strength reduction factor < the next strength reduction factor')
                if stre_dist[i][1] < tf/d:
                    print('the next calculation point is in the upper flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= tf/d and stre_dist[i][1] < (d-tf)/d:
                    print('the next calculation point is in the web')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*tw*d*d)*fpl+m
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(tw)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
                elif stre_dist[i][1] >= (d-tf)/d and stre_dist[i][1] < 1:
                    print('the next calculation point is in the lower flange')
                    m=((stre_dist[i][0]+stre_dist[i+1][0])*(stre_dist[i+1][1]-stre_dist[i][1])/2*abs(y_neutral-stre_dist[i+1][1]+((2*min(stre_dist[i+1][0],stre_dist[i][0])+max(stre_dist[i+1][0],stre_dist[i][0]))/(stre_dist[i+1][0]+stre_dist[i][0])*(stre_dist[i+1][1]-stre_dist[i][1])/3))*w*d*d)*fpl+m
                    
                    print('Sum of plastic bending moment ='+'('+str(round(stre_dist[i][0],2))+'+'+str(round(stre_dist[i+1][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/2*abs('+str(y_neutral)+'-'+str(round(stre_dist[i+1][1],2))+'+((2*'+str(min(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+'+'+str(max(round(stre_dist[i+1][0],2),round(stre_dist[i][0],2)))+')/('+str(round(stre_dist[i+1][0],2))+'+'+str(round(stre_dist[i][0],2))+')*('+str(round(stre_dist[i+1][1],2))+'-'+str(round(stre_dist[i][1],2))+')/3))*'+str(w)+'*'+str(d)+'*'+str(d)+'*'+str(fpl)+'='+str(round(m*1e-6,2))+'kN*m')
    print('Overall plastic bending moment = '+str(round(m*1e-6,2))+'kN*m\n')
    print('<<<<<<<<<  Calculation finnished  >>>>>>>>>\n        **************************')

    return m
