


def model(query,ans):
    import pandas as pd
    import numpy as np
    import json

    with open('final_classification.json', 'r') as f:
        data = json.load(f)
    with open('sequence_cluster_dict.json', 'r') as f:
        data1 = json.load(f)
    with open('clusters_dict.json', 'r') as f:
        data2 = json.load(f)
    with open('final_classification.json', 'r') as f:
        data3= json.load(f)
    def align_score(seq1, seq2):
        
        match = 1
        mismatch = -1
        gap = -1
        
        
        n = len(seq1)
        m = len(seq2)
        score = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            score[i][0] = i * gap
        for j in range(m + 1):
            score[0][j] = j * gap
            
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                diag = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
                up = score[i-1][j] + gap
                left = score[i][j-1] + gap
                score[i][j] = max(diag, up, left)
        return score[n][m]

    def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_penalty=-1):
        
        rows = len(seq1) + 1
        cols = len(seq2) + 1
        score = [[0] * cols for _ in range(rows)]

        
        for i in range(rows):
            score[i][0] = i * gap_penalty
        for j in range(cols):
            score[0][j] = j * gap_penalty

        
        for i in range(1, rows):
            for j in range(1, cols):
                match = score[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score)
                delete = score[i - 1][j] + gap_penalty
                insert = score[i][j - 1] + gap_penalty
                score[i][j] = max(match, delete, insert)
        alignment_score = score[rows - 1][cols - 1]

        return alignment_score



    # query=input()
    df=pd.read_csv("merged_final24.csv")
    df["score"]=0
    for i in range(len(df["Sequence"])):
        score=align_score(query,df["Sequence"][i])
        df["score"][i]=score
    sorted_df = df.sort_values(by='score')
    sorted_df = df.sort_values(by='score', ascending=False)
    df=df.head(5)

    df["Cluster"]=0
    for i in range(len(df["Sequence"])):
        df["Cluster"][i]=data1[df["Cultivar ID"][i]]

    x=dict()
    for i in set(df["Subpopulation"]):
        x[i]=list(df["Subpopulation"]).count(i)
    x = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))
    x=list(x.keys())
    y = dict()
    for i in set(df["Cluster"]):
        if i in df["score"]:
            y[i] = (list(df["Cluster"]).count(i), df["score"][i])
        else:
            y[i] = (list(df["Cluster"]).count(i), 0)
    y = dict(sorted(y.items(), key=lambda item: (item[1][0], item[1][1])))
    y = list(y.keys())
    y=y[0]

    z=data2[str(y)][0]
    pp=list(data3[z]['Subpopulation'].keys())
    pp

    for i in x:
        if(i in pp):
            x=i
    ansp=data3[z]["Subpopulation"][x]
    ansp_split = ansp.split("-")
    minh, maxh = float(ansp_split[0]), float(ansp_split[1])
    if(ans<maxh and ans>minh):
        return "correct"
    
    else:
        return "wrong"
    


