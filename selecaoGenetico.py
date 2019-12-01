import subprocess
import random
import statistics
import sys
import getopt

def usage():
    print("Utilizacao: parte2.py [opcoes]")
    print("Opcoes:")
    print("\t-h, --help\t\t\t\t\t\t\tMostra esta mensagem de ajuda")
    print("\t-n <int>, --numiteracoes=<int>\t\tDefine numero de iteracoes que o algoritmo executara (Padrao = 10)")
    print("\t-t <int>, --tampopulacao=<int>\t\tDefine o tamanho da populacao do algoritmo genetico (Padrao = 10)")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'n:t:h', ['numiteracoes=', 'tampopulacao=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

subprocess.call("[ ! -d 'geneticoResults' ] && mkdir -p geneticoResults/{1..10}", shell=True)


crossoverProb= 0.9
mutationProb= 0.05
tamanhoPop= 10
numIteracoes= 10


for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-n', '--numiteracoes'):
        numIteracoes = int(arg)
    elif opt in ('-t', '--tampopulacao'):
        tamanhoPop = int(arg)
    else:
        print("Opcao nao encontrada: "+opt)
        usage()
        sys.exit(2)

O3= [" -tti", " -verify", " -ee-instrument", " -targetlibinfo", " -assumption-cache-tracker", " -profile-summary-info", " -forceattrs", " -basiccg", " -barrier", " -targetlibinfo", " -tti", " -tbaa", " -scoped-noalias", " -assumption-cache-tracker", " -profile-summary-info", " -forceattrs", " -inferattrs", " -ipsccp", " -called-value-propagation", " -globalopt", " -domtree", " -mem2reg", " -deadargelim", " -basicaa", " -aa", " -loops", " -lazy-branch-prob", " -lazy-block-freq", " -opt-remark-emitter", " -instcombine", " -simplifycfg", " -basiccg", " -globals-aa", " -prune-eh", " -always-inline", " -functionattrs", " -sroa", " -memoryssa", " -early-cse-memssa", " -speculative-execution", " -lazy-value-info", " -jump-threading", " -correlated-propagation", " -libcalls-shrinkwrap", " -branch-prob", " -block-freq", " -pgo-memop-opt", " -tailcallelim", " -reassociate", " -loop-simplify", " -lcssa-verification", " -lcssa", " -scalar-evolution", " -loop-rotate", " -licm", " -loop-unswitch", " -indvars", " -loop-idiom", " -loop-deletion", " -loop-unroll", " -memdep", " -memcpyopt", " -sccp", " -demanded-bits", " -bdce", " -dse", " -postdomtree", " -adce", " -barrier", " -rpo-functionattrs", " -globaldce", " -float2int", " -loop-accesses", " -loop-distribute", " -loop-vectorize", " -loop-load-elim", " -alignment-from-assumptions", " -strip-dead-prototypes", " -loop-sink", " -instsimplify", " -div-rem-pairs", " -verify", " -ee-instrument", " -early-cse", " -lower-expect", " -inline", " -mldst-motion", " -gvn", " -elim-avail-extern", " -slp-vectorizer", " -constmerge", " -callsite-splitting", " -argpromotion"]
otimizacoes= [' -tti', ' -verify', ' -ee-instrument', ' -targetlibinfo', ' -assumption-cache-tracker', ' -profile-summary-info', ' -forceattrs', ' -basiccg', ' -barrier', ' -tbaa', ' -scoped-noalias', ' -inferattrs', ' -ipsccp', ' -called-value-propagation', ' -globalopt', ' -domtree', ' -mem2reg', ' -deadargelim', ' -basicaa', ' -aa', ' -loops', ' -lazy-branch-prob', ' -lazy-block-freq', ' -opt-remark-emitter', ' -instcombine', ' -simplifycfg', ' -globals-aa', ' -prune-eh', ' -always-inline', ' -functionattrs', ' -sroa', ' -memoryssa', ' -early-cse-memssa', ' -speculative-execution', ' -lazy-value-info', ' -jump-threading', ' -correlated-propagation', ' -libcalls-shrinkwrap', ' -branch-prob', ' -block-freq', ' -pgo-memop-opt', ' -tailcallelim', ' -reassociate', ' -loop-simplify', ' -lcssa-verification', ' -lcssa', ' -scalar-evolution', ' -loop-rotate', ' -licm', ' -loop-unswitch', ' -indvars', ' -loop-idiom', ' -loop-deletion', ' -loop-unroll', ' -memdep', ' -memcpyopt', ' -sccp', ' -demanded-bits', ' -bdce', ' -dse', ' -postdomtree', ' -adce', ' -rpo-functionattrs', ' -globaldce', ' -float2int', ' -loop-accesses', ' -loop-distribute', ' -loop-vectorize', ' -loop-load-elim', ' -alignment-from-assumptions', ' -strip-dead-prototypes', ' -loop-sink', ' -instsimplify', ' -div-rem-pairs', ' -early-cse', ' -lower-expect', ' -inline', ' -mldst-motion', ' -gvn', ' -elim-avail-extern', ' -slp-vectorizer', ' -constmerge', ' -callsite-splitting', ' -argpromotion']

opt= ""


def fitness(tempo):
    return 100/tempo

def mutacao(individuo):
    tamanhoIndividuo= len(individuo)
    pos= 0
    while pos < tamanhoIndividuo:
        tipo= random.randint(1,3)
        if tipo == 1:       #Insercao de gene
            nova= random.randint(0,len(otimizacoes) - 1)
            if pos > 0 and pos < len(individuo)-1:
                contador= 0
                while otimizacoes[nova] in individuo[pos-1:pos+1] and contador < 30:
                    nova= random.randint(0,len(otimizacoes) - 1)
                    contador+= 1
                if contador > 29:
                    continue
            elif pos > 0:
                contador= 0
                while otimizacoes[nova] != individuo[pos-1] and contador < 30:
                    nova= random.randint(0,len(otimizacoes) - 1)
                    contador+= 1
                if contador > 29:
                    continue
            else:
                contador= 0
                while otimizacoes[nova] != individuo[pos] and contador < 30:
                    nova= random.randint(0,len(otimizacoes) - 1)
                    contador+= 1
                if contador > 29:
                    continue
            individuo.insert(pos, otimizacoes[nova])
        elif tipo == 2:     #Remocao de gene
            if pos > 0 and pos < len(individuo)-1:
                if individuo[pos-1] == individuo[pos+1]:
                    individuo.pop(pos+1)
            individuo.pop(pos)
        else:               #Troca de posicao de genes
            pos2= pos
            contador= 0
            while pos2 == pos  and contador < 30:
                pos2= random.randint(0, len(individuo) - 1)
                contador+= 1
            if contador > 29:
                continue
            individuo[pos], individuo[pos2]= individuo[pos2], individuo[pos]
        tamanhoIndividuo= len(individuo)
        pos+= 1

def crossover(pai1, pai2):
    meio1= []
    meio2= []
    pos1= random.randint(1, len(pai1) - 1)
    pos2= random.randint(1, len(pai2) - 1)
    contador= 0
    while pai1[pos1 - 1] == pai2[pos2] or pai1[pos1] == pai2[pos2 - 1]:
        pos1= random.randint(1, len(pai1) - 1)
        pos2= random.randint(1, len(pai2) - 1)
        contador+= 1
        if contador > 29:
            break
    meio1= pai1[:pos1].copy()
    meio1.extend(pai2[pos2:].copy())
    meio2= pai2[:pos2].copy()
    meio2.extend(pai1[pos1:].copy())
    return (meio1, meio2)

def escolhePais(temposPop, listaRep):
    cumulativo= 0
    limites= []
    for individuo in range(tamanhoPop):
        if individuo in listaRep:
            #listaRep.append(individuo)
            atual= fitness(temposPop[individuo])
            limites.append(cumulativo+atual)
            cumulativo+= atual
    escolhido1= -1
    numeroGerado1= random.uniform(0, cumulativo)
    #print("Limites:")
    #print(limites)
    #print("Rand:")
    #print(numeroGerado1)
    for limite in limites:
        if numeroGerado1 <= limite:
            escolhido1= limites.index(limite)
            break
    #print("Escolhido:")
    #print(escolhido1)
    #print("Rep")
    #print(listaRep)
    #listaRep.pop(escolhido1)
    #jaReproduziu.append(listaRep[escolhido1])
    return (escolhido1, listaRep)


for bench in range(1, 11):
    iteracao= 1
    estagnou= 0
    populacao= []
    tempos= []
    melhoresTempos= []
    opt= ""
    melhor= []
    for i in range(tamanhoPop):
        individuo= []
        tamanhoIndividuo= random.randint(1, 2*len(otimizacoes))
        anterior= -1
        for j in range(tamanhoIndividuo):
            indice= random.randint(0, len(otimizacoes) - 1)
            while indice == anterior:
                indice= random.randint(0, len(otimizacoes) - 1)
            individuo.append(otimizacoes[indice])
            anterior= indice
        populacao.append(individuo.copy())
    temposPop= []
    parada= False
    execucoes= []
    large= ""
    if bench != 4:
        large= "LARGE_PROBLEM_SIZE=1 "
    subprocess.call("COMPILE=1 EXEC=0 BENCH="+ str(bench) + " "+ large + " OPT='-O3' ./run.sh", shell=True)
    for i in range(3):
        subprocess.call("COMPILE=0 EXEC=1 BENCH="+ str(bench) + " "+ large + " OPT='-O3' ./run.sh", shell=True)
        subprocess.call("mv run.log ../geneticoResults/"+str(bench)+"/BaseO3-v"+str(i+1)+".log", shell=True)
    subprocess.call("COMPILE=1 EXEC=0 BENCH="+ str(bench) + " "+ large + " ./run.sh", shell=True)
    for i in range(3):
        subprocess.call("COMPILE=0 EXEC=1 BENCH="+ str(bench) + " "+ large + " ./run.sh", shell=True)
        subprocess.call("mv run.log ../geneticoResults/"+str(bench)+"/Base-v"+str(i+1)+".log", shell=True)
    while(not parada):
        ind= 1
        while ind <= tamanhoPop:
            #numInd= 1
            opt= ''
            individuo= populacao[ind-1]
            for otimizacao in individuo:
                opt= ''.join([opt, otimizacao])
            opt= "'"+opt[1:]+"'"
            with open("opts"+str(bench)+"-"+str(iteracao)+".txt", "a") as logOpts:
                print(opt, file=logOpts)
            subprocess.call("mv opts"+str(bench)+"-"+str(iteracao)+".txt ../geneticoResults/"+str(bench)+"/"+ str(iteracao) +"-"+ str(ind) +"opt.txt", shell=True)
            execucoesDaBench= []
            subprocess.call("COMPILE=1 EXEC=0 BENCH="+ str(bench) + " " + large +" OPT=" + opt + " ./run.sh", shell=True)
            for i in range(3):
                subprocess.call("COMPILE=0 EXEC=1 BENCH="+ str(bench) + " " + large +" OPT=" + opt + " ./run.sh", shell=True)
                subprocess.call("mv run.log ../geneticoResults/"+str(bench)+"/"+ str(iteracao) +"-"+ str(ind+1) +"v"+str(i+1)+".log", shell=True)
                #with open("../geneticoResults/"+str(bench)+"/"+str(iteracao)+"-"+str(ind)+"v"+str(i+1)+".log", "a") as logOpt:
                    #print(opt, file= logOpt)
                with open("../geneticoResults/"+str(bench)+"/"+ str(iteracao)+"-"+ str(ind) +"v"+str(i+1)+".log", 'r') as log:
                    primeira= True
                    for linha in log:
                        if primeira:
                            primeira= False
                            continue
                        execucoesDaBench.append(float(linha.split()[3]))
            tempo= statistics.mean(execucoesDaBench)
            temposPop.append(tempo)
            execucoes.append(execucoesDaBench.copy())
            ind+= 1
        gerados= []
        jaReproduziu= []
        maiorFit= 0
        #print(len(populacao))
        #print(len(temposPop))
        for individuo in range(tamanhoPop):
            fit= fitness(temposPop[individuo])
            if fit > maiorFit:
                maiorFit= fit
                melhor= populacao[individuo].copy()
        listaRep= []
        for indice in range(tamanhoPop):
            listaRep.append(indice)
        numGerados= 0            
        for i in range(int(tamanhoPop/2)):
            #print("Pop:")
            #print(len(populacao))
            (escolhido1, listaRep)= escolhePais(temposPop, listaRep)
            pai1= populacao[listaRep.pop(escolhido1)]
            #print(len(populacao))
            (escolhido2, listaRep)= escolhePais(temposPop, listaRep)
            pai2= populacao[listaRep.pop(escolhido2)]
            gerado1= []
            gerado2= []
            if random.random() > crossoverProb or len(pai1) < 2 or len(pai2) < 2:
                gerado1= pai1
                numGerados+= 1
                if i == int(tamanhoPop/2)-1:
                    gerado2= melhor.copy()
                    numGerados+= 1
                else:
                    gerado2= pai2
                    numGerados+= 1
            else:
                (gerado1, gerado2)= crossover(pai1, pai2)
                numGerados+= 2
                if i == int(tamanhoPop/2)-1:
                    gerado2= melhor.copy()
            mutacao(gerado1)
            mutacao(gerado2)
            gerados.append(gerado1.copy())
            gerados.append(gerado2.copy())
        #print("Num gerados:")
        #print(numGerados)
        #print("Len(gerados)")
        #print(len(gerados))
        tempos.append(temposPop)
        melhoresTempos.append(min(temposPop))
        
        #Parada
        #if len(melhoresTempos > 5):
        #   melhora= min(melhoresTempos[:-1]) - melhoresTempos[-1]
        #   if  melhora < 0:
        #       estagnou= 0
        #   else:
        #       estagnou+= 1
        iteracao+= 1
        if iteracao > numIteracoes:
            parada= True
        #Nova população

        
        #subprocess.call("mv melhoresOpts"+str(bench)+".txt ../geneticoResults/"+str(bench)+"/melhoresOpts.txt", shell=True)
        with open("tempos"+str(bench)+".txt", "a") as log:
            count= 1
            for rodada in tempos:
                print("Geracao "+str(count)+":\n", file= log)
                for tempo in rodada:
                    print(tempo, file=log)
                print("\n\n", file=log)
                count+= 1
        subprocess.call("mv tempos"+str(bench)+".txt ../geneticoResults/"+str(bench)+"/tempos"+str(iteracao)+".txt", shell=True)
        with open("melhores"+str(bench)+".txt", "a") as log:
            for tempo in melhoresTempos:
                print(tempo, file=log)
        subprocess.call("mv melhores"+str(bench)+".txt ../geneticoResults/"+str(bench)+"/melhores.txt", shell=True)
        
        populacao= gerados.copy()