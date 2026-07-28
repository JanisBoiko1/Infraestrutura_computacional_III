from multiprocessing import Pool
import time

## Função elaborada em colaboração com os estudantes Lúcio e Jorge
def pi_naive(start, end, step):
    
    #iniciamos a soma local em 0
    sum = 0.0

    #criamos um loop para cada retangulo, iniciando em x milhões e finalizando em y milhões
    for i in range(start, end):

        # marcamos onde calcularemos a altura do retangulo pelo paço (largura)
        x = (i+0.5) * step

        #calculamos a área do retangulo e atualizamos isso na soma local
        #fórmula da área: Área = altura (sum+4/1+x*x) *Base (step)
        #formula da altura vem da derivada da arctangente: 4/(1+x*x)
        sum = sum + (4.0/(1.0+x*x)) * step
        
    #retorna o valor de pi para esse step(chunk de retangulos)
    return sum

if __name__ == '__main__':
    
    #estabelecemos uma lista em branco de resultados
    resultados = []

    #criamos a variável num_steps, que recebe 100 milhões de retangulos, que serão nossos passos
    num_steps = 100_000_000 #100.000.000

    #criamos as variáveis num_process, que marca a quantidade de "trabalhadores" que utilizaremos
    #criamos os trabalhadores e iniciamos a contagem dos retangulos em 0
    num_processos = 4
    p = Pool(num_processos) 
    inicio = 0
    
    #calculamos o tamanho do processo
    #isto é: o número de passos dividido pelo número de processos, 25 milhões
    tamanho_processo = int(num_steps/num_processos)

    #calculamos o tamanho do passo, isto é 1/X milhões
    #o tamanho do passo que damos é a largura de um retangulo
    step = 1.0/num_steps

    #marcamos o tempo inicial
    tic = time.time()

    #iniciamos o loop dos processos, de 0 à 3
    for i in range(num_processos):
        
        #calculamos o inicio pelo passo * o tamanho do processo,
        #Ex 0*25 000 000 = 0; 1*25 000 000 = 25 000 000
        inicio = int( i * (tamanho_processo))

        #calculamos o fim pelo tamanho do processo * passo + 1
        #Ex (25 000 000 * 0+1) = 25 000 000 (tirei o "-1" para não ter uma sobra)
        fim = int((tamanho_processo * (i+1)))
        
        #chamamos o apply_async, passando a função e seus parametros como parametro do próprio apply
        #e anexamos tudo na lista resultados
        resultados.append(p.apply_async(pi_naive,(inicio, fim, step)))
    
    #o output é calculado pelo p.get() para cada resultado da lista
    output = [p.get() for p in resultados]

    #calculamos tempo final
    toc = time.time()

    #printamos o tempo
    print("Tempo Pi: %.8f s" %(toc-tic))

    #somamos os resultados pelos outputs
    somatoria = sum(output)

    #printamos a soma
    print(somatoria)