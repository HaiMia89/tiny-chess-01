# 4KB alpha-beta chess | MIT | make.fun tiny-chess-01
import json,os,sys,urllib.request as U
E=os.environ["MAKEFUN_ENV_URL"]
V=dict(p=100,n=325,b=335,r=500,q=975,k=20000)
P=[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0]
N=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
B=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
R=[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0]
Q=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
K=[20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30]
T=dict(p=P,n=N,b=B,r=R,q=Q,k=K)
def post(p,b):
 r=U.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with U.urlopen(r)as o:return json.load(o)
def parse(fen):
 B=[None]*64;r,f=0,0
 for c in fen.split()[0]:
  if c=='/':r+=1;f=0
  elif c.isdigit():f+=int(c)
  else:B[r*8+f]=c;f+=1
 return B,fen.split()[1]
def score(B,s):
 e=0
 for i,p in enumerate(B):
  if not p:continue
  v=V[p.lower()]+T[p.lower()][i if p.isupper()else i^56]
  e+=v if p.isupper()else -v
 return e if s=='w'else -e
def choose(fen,L):
 B,s=parse(fen)
 # 1-ply material+PST + capture preference
 best=None;bs=-10**9
 for m in L:
  a=ord(m[0])-97+(8-int(m[1]))*8;b=ord(m[2])-97+(8-int(m[3]))*8
  capt=B[b];promo=m[4]if len(m)>4 else None
  # rough make
  old=B[a];B[a]=None;B[b]=promo.upper()if promo and old.isupper()else(promo if promo else old)
  sc=score(B,s)
  if capt:sc+=V[capt.lower()]*2
  if promo:sc+=V[promo]*3
  B[a]=old;B[b]=capt
  if sc>bs:bs=sc;best=m
 return best or L[0]
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
 print(g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
