from multiprocessing import Process
import time

## feito por mim e pelo Lúcio. Espero que não seja um problema
def pi_naive(start, end, step):
    #marca o inicio
    print ("Start: ", str(start))
    #marca o fim
    print ("End: ", str(end))
    #inicia a soma em 0
    sum = 0.0
    #para cada retangulo
    for i in range(start, end):
        #marca onde calcularemos a altura do retangulo pelo paço -- que é também a largura
        x = (i+0.5) * step
        #calcula a área do retangulo e atualiza isso na soma
        #Área = altura (sum+4/1+x*x) *Base (step)
        #formula da altura vem da derivada da arctangente
        #4/(1+x*x)
        #por que 4? por que 1? por que x^2?
        sum = sum + (4.0/(1.0+x*x)) * step
        
    print ("Valor Pi: %.10f" %sum)
    return sum

if __name__ == '__main__':
    procs = []
    #haverão 100 milhões de passos, ou seja, 100 milhões de retangulos
    num_steps = 100_000_000 #100.000.000

    #variável do processo e do início em 4 e 0
    n_process = 4
    inicio = 0

    #loop dos processos, de 0 à 3
    for i in range(n_process):
        
        #tamanho do processo é o número de passos dividido pelo número de processos, ou seja, 25 milhões
        tamanho_processo = num_steps/n_process

        #inicio é o valor do processo * o tamanho do processo,
        #Ex 0*25 000 000 = 0; 1*25 000 000 = 25 000 000
        inicio = int( i * (tamanho_processo))

        #fim = tamanho do processo * passo + 1, -1
        #Ex (25 000 000 * 0+1) - 1 = 24 999 999
        fim = int((tamanho_processo * (i+1)) - 1)

        #paço atualizado = 1/X milhões
        step = 1.0/num_steps
        
        #tempo inicial
        tic = time.time()
        
        #chama o processo p e passa inicio, fim e step
        p = Process(target = pi_naive, args = (inicio, fim, step, ))

        #anexa o processo na lista de processos
        procs.append(p)
        #inicia
        procs[i].start()

        #tempo final
        toc = time.time()

        print("Tempo Pi: %.8f s" %(toc-tic))
    
    #loop de 'pagamento dos pedreiros'
    for i in range(n_process):
        procs[i].join()
   #falow valeu