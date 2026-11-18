# 4KB chess for make.fun tiny-chess-01 | MIT
import json,os,sys,urllib.request as u
E=os.environ["MAKEFUN_ENV_URL"]
V=dict(p=100,n=320,b=330,r=500,q=900,k=20000)
# PST mid
P=[0]*8+[50]*8+[10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5]+[0]*8
N=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
B=[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20]
R=[0,0,0,5,5,0,0,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0]
Q=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,5,0,0,0,0,-10,-10,5,5,5,5,5,0,-10,0,0,5,5,5,5,0,-5,-5,0,5,5,5,5,0,-5,-10,0,5,5,5,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
K=[20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30]
T=dict(p=P,n=N,b=B,r=R,q=Q,k=K)
def post(p,b):
 r=u.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with u.urlopen(r)as o:return json.load(o)
def bd(fen):
 B={}
 for i,r in enumerate(fen.split()[0].split("/")):
  f=0
  for c in r:
   if c.isdigit():f+=int(c)
   else:B[f+(7-i)*8]=c;f+=1
 return B,fen.split()[1]
def sc(B,s):
 e=0
 for i,p in B.items():
  v=V[p.lower()]+T[p.lower()][i if p.isupper() else i^56]
  e+=v if p.isupper()else -v
 return e if s=="w"else -e
def choose(fen,L):
 B,s=bd(fen)
 def rk(m):
  a,b=ord(m[0])-97+(8-int(m[1]))*8,ord(m[2])-97+(8-int(m[3]))*8
  mv=B[a].lower();tk=B.get(b)
  if not tk and mv=="p"and m[0]!=m[2]:tk="p"
  return (-(V[tk.lower()]if tk else 0),-(V[m[4]]if len(m)>4 else 0),V[mv],m)
 return min(L,key=rk)
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
 print(g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
