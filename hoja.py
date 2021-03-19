## Autores:
##Estefanía Elvira 20725
##Walter Cruz
## hoja de algoritmos numero 5

import simpy
import random
import statistics


## FUNCION

def proceso(env, tiempoproceso, nomb, ram, cantiRam, ninstrucciones, velocidad, cpu, colaespera):
    
    global temp ## varibles que almacenaran el tiempo que toma  cada proceso 
    global tiempo
    
    
    # El proceso entra al sistema pero tiene que esperar a que este le asigne memoria ram para empezar.
    yield env.timeout(tiempoproceso)
    print('%s. Solicita %d de RAM (Nuevo Proceso)' % (nomb, cantiRam))
    # Se guarda el tiempo en el que llego
    tiempoLlegada = env.now

    # Se solicita la  memoria RAM para la iniciacion del proceso.
    yield ram.get(cantiRam)
    print('%s. Solicitud aceptada por %d de RAM (Proceso Admitido)' % (nomb, cantiRam))
 
    # Variable que almacena las instrucciones 
    insf = 0
    
    while insf < ninstrucciones:
        with cpu.request() as req:
            yield req
            # muestra la instruccion que se va a realizar 
            if (ninstrucciones - insf) >= velocidad:
                ejecutadas = velocidad
            else:
                ejecutadas = (ninstrucciones - insf)
 
            print('%s. CPU ejecutara %d instrucciones. (Proceso Listo)' % (nomb, ejecutadas))

            #El tiempo que se ejecuta 
            yield env.timeout(ejecutadas/velocidad)   
 
            # La cantidad de instrucciones realizadas 
            insf += ejecutadas
            print('%s. CPU (%d/%d) instrucciones completadas. (Proceso Corriendo)' % (nomb, insf, ninstrucciones))
 
        # Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)
 
        if desicion == 1 and insf < ninstrucciones:
            #Etapa de espera en la cola.
            with colaespera.request() as cola:
                yield cola
                yield env.timeout(1);              
                print('%s. Realizadas operaciones de entrada/salida. (Proceso Esperando)' % (nomb))

    #Etapa finalizada
    yield ram.put(cantiRam)#Se devuelve la memoria Ram
    print('%s. Retorna %d de RAM. (Proceso terminado)' % (nomb, cantiRam))
    #Total de tiempo que llevo el proceso
    temp+= (env.now - tiempoLlegada)
    #Se guarda tiempo en el Array para luego hacer uso de este y hacer los diferentes calculos.
    tiempo.append(env.now - tiempoLlegada) 


vel = 4   #Velocidad que llevará el procesadir 
cantiram = 100 #Memoria Ram asignada 
numeroprocesos = 25  # La cantidad de los procesos que se va a realizar 
temp = 0.0       #Varialble que almacena el tiempo 
tiempo=[]      # Lista que guarda los timepos de cada proceso que nos servirá para el calculo de la desviacion estandaer 
 

#Se crea el ambiente de simulacion.
env = simpy.Environment()

# Cola de tipo Resource para el CPU 
cpu = simpy.Resource (env, capacity=2)

# Cola de tipo Container para la RAM
ram = simpy.Container(env, cantiram, cantiram)

# Cola de tipo Resource Wait para las operaciones I/O
colaespera = simpy.Resource (env, capacity=2) 

# Numero de intervalos
numerointervalos = 5

# Semilla del random
random.seed(10000)

# Creacion de un for para poder crear el numero de procesos requeridos por la simulacion.
for i in range(numeroprocesos):
    tiemproceso = random.expovariate(1.0 / numerointervalos)
    #Se genera un numero de instrucciones aleatorio
    ninstrucciones = random.randint(1,10)
    #Se genera una cantidad de memoria RAM aleatoria
    cantiRam = random.randint(1,10) 
    env.process(proceso(env, tiemproceso, 'Proceso %d' % i, ram, cantiRam, ninstrucciones, vel, cpu, colaespera))
 
#Se inicial la simulacion 
env.run()
print

# Calculo del tiempo promedio transcurrido
prom = (temp/numeroprocesos)

print("\nSe realizaron %d procesos con la cantidad de intervalos de %d" % (numeroprocesos, numerointervalos))
print ("El tiempo promedio de los procesos es: ",prom," segundos")
#Calculo de la desviacion estandar de la simulacion con la ayuda del modulo de statistics
print("La desviacion estandar es: ",statistics.pstdev(tiempo))

    
    