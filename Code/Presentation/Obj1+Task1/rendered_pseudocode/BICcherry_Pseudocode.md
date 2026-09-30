\textbf{Algorithm 2: BIC-cherry + classical expansion}\par\smallskip
\begin{algorithmic}[1]
\Require properly coloured digraph $(G,\sigma)$ on $L$ with the sicor-in-hub property
\Ensure leaf-coloured network $(N,\sigma)$
\State $V(N) \gets L\cup\{\rho\}$;\ \ $E(N) \gets \emptyset$
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{BIC-cherry network}
  \State add $p_{xy}$ with edges $(\rho,p_{xy}),\,(p_{xy},x),\,(p_{xy},y)$
\EndFor
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{expansion}
  \ForAll{$(a,b)\in\big((x,y),(y,x)\big)$ with $(a,b)\notin E(G)$}
    \State $b' \gets \Call{FindCandidate}{G,a,b}$
    \State add new vertex $q$ with edges $(p_{xy},q),\,(q,a),\,(q,b')$ \Comment{$[ab:ab']$}
  \EndFor
\EndFor
\State \Return $(N,\sigma)$
\Statex
\Function{FindCandidate}{$G,a,b$}
  \State $C \gets \{v\in L\setminus\{b\} : \sigma(v)=\sigma(b)\}$
  \State \Return random element of $C$
\EndFunction
\end{algorithmic}



\textbf{Algorithm 3: BIC-cherry + restricted expansion}\par\smallskip
\begin{algorithmic}[1]
\Require properly coloured digraph $(G,\sigma)$ on $L$ with the sicor-in-hub property
\Ensure leaf-coloured network $(N,\sigma)$
\State $V(N) \gets L\cup\{\rho\}$;\ \ $E(N) \gets \emptyset$
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{BIC-cherry network}
  \State add $p_{xy}$ with edges $(\rho,p_{xy}),\,(p_{xy},x),\,(p_{xy},y)$
\EndFor
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{expansion}
  \ForAll{$(a,b)\in\big((x,y),(y,x)\big)$ with $(a,b)\notin E(G)$}
    \State $b' \gets \Call{FindCandidate}{G,a,b}$
    \State add new vertex $q$ with edges $(p_{xy},q),\,(q,a),\,(q,b')$ \Comment{$[ab:ab']$}
  \EndFor
\EndFor
\State \Return $(N,\sigma)$
\Statex
\Function{FindCandidate}{$G,a,b$}
  \State $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G)\}$
         \Comment{$\neq\emptyset$ if $(G,\sigma)$ is sink-free}
  \State \Return random element of $C$
\EndFunction
\end{algorithmic}



\textbf{Algorithm 4: BIC-cherry + prioritised expansion}\par\smallskip
\begin{algorithmic}[1]
\Require properly coloured digraph $(G,\sigma)$ on $L$ with the sicor-in-hub property
\Ensure leaf-coloured network $(N,\sigma)$
\State $V(N) \gets L\cup\{\rho\}$;\ \ $E(N) \gets \emptyset$
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{BIC-cherry network}
  \State add $p_{xy}$ with edges $(\rho,p_{xy}),\,(p_{xy},x),\,(p_{xy},y)$
\EndFor
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{expansion}
  \ForAll{$(a,b)\in\big((x,y),(y,x)\big)$ with $(a,b)\notin E(G)$}
    \State $b' \gets \Call{FindCandidate}{G,a,b}$
    \State add new vertex $q$ with edges $(p_{xy},q),\,(q,a),\,(q,b')$ \Comment{$[ab:ab']$}
    \State remove edge $(p_{xy},a)$ \Comment{shortcut}
  \EndFor
\EndFor
\State \Return $(N,\sigma)$
\Statex
\Function{FindCandidate}{$G,a,b$}
  \State $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G),\ (v,a)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L\setminus\{b\} : \sigma(v)=\sigma(b),\ (v,a)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L\setminus\{b\} : \sigma(v)=\sigma(b)\}$
  \State \Return random element of $C$
\EndFunction
\end{algorithmic}


\textbf{Algorithm 5: BIC-cherry + mode-aware expansion}\par\smallskip
\begin{algorithmic}[1]
\Require properly coloured digraph $(G,\sigma)$ on $L$ with the sicor-in-hub property,
         mode $\in\{\text{strict},\text{weak}\}$
\Ensure leaf-coloured network $(N,\sigma)$
\State $V(N) \gets L\cup\{\rho\}$;\ \ $E(N) \gets \emptyset$
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{BIC-cherry network}
  \State add $p_{xy}$ with edges $(\rho,p_{xy}),\,(p_{xy},x),\,(p_{xy},y)$
\EndFor
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{expansion}
  \State $(x',y') \gets (\bot,\bot)$
  \State \textbf{if} mode $=$ strict \textbf{and} $(x,y),(y,x)\notin E(G)$ \textbf{then}
         $(x',y') \gets \Call{FindJointCandidates}{G,x,y}$
  \ForAll{$(a,b)\in\big((x,y),(y,x)\big)$ with $(a,b)\notin E(G)$}
    \State \textbf{if} $b'=\bot$ \textbf{then} $b' \gets \Call{FindCandidate}{G,a,b,\text{mode}}$
    \State add new vertex $q$ with edges $(p_{xy},q),\,(q,a),\,(q,b')$ \Comment{$[ab:ab']$}
    \State remove edge $(p_{xy},a)$ \Comment{shortcut}
  \EndFor
\EndFor
\State \Return $(N,\sigma)$
\Statex
\Function{FindCandidate}{$G,a,b,\text{mode}$}
  \State $C \gets \emptyset$
  \State \textbf{if} mode $=$ weak \textbf{then}
         $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G),\ (v,a)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L\setminus\{b\} : \sigma(v)=\sigma(b),\ (v,a)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then}
         $C \gets \{v\in L\setminus\{b\} : \sigma(v)=\sigma(b)\}$
  \State \Return random element of $C$
\EndFunction
\Statex
\Function{FindJointCandidates}{$G,x,y$}
  \State $X_1 \gets \{v\in L : \sigma(v)=\sigma(x),\ (y,v)\in E(G)\}$
  \State $Y_1 \gets \{v\in L : \sigma(v)=\sigma(y),\ (x,v)\in E(G)\}$
  \State $S \gets \{(x',y')\in X_1\times Y_1 : (x',y')\notin E(G),\ (y',x')\notin E(G)\}$
  \State \textbf{if} $S\neq\emptyset$ \textbf{then} \Return random element of $S$
  \State $X_2 \gets \{v\in L\setminus\{x\} : \sigma(v)=\sigma(x)\}$
  \State $Y_2 \gets \{v\in L\setminus\{y\} : \sigma(v)=\sigma(y)\}$
  \State $S \gets \{(x',y')\in X_2\times Y_2 : (x',y')\notin E(G),\ (y',x')\notin E(G)\}$
  \State \textbf{if} $S\neq\emptyset$ \textbf{then} \Return random element of $S$
  \State \textbf{if} $X_1\times Y_1\neq\emptyset$ \textbf{then} \Return random element of $X_1\times Y_1$
  \State \textbf{if} $X_2\times Y_2\neq\emptyset$ \textbf{then} \Return random element of $X_2\times Y_2$
  \State \Return $(\bot,\bot)$
\EndFunction
\end{algorithmic}



\textbf{Algorithm 6: BIC-cherry + multilayered expansion (weak)}\par\smallskip
\begin{algorithmic}[1]
\Require coloured digraph $(G,\sigma)$ on $L$, maximal number of layers $K$ (default $K=|L|$)
\Ensure leaf-coloured network $(N,\sigma)$
\State $V(N) \gets L\cup\{\rho\}$;\ \ $E(N) \gets \emptyset$;\ \ $W \gets \emptyset$
\State \textbf{if} $|L|=2$ \textbf{then} add edges $(\rho,x)$ for all $x\in L$ and \Return $(N,\sigma)$
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{BIC-cherry network}
  \State add $p_{xy}$ with edges $(\rho,p_{xy}),\,(p_{xy},x),\,(p_{xy},y)$
\EndFor
\ForAll{$\{x,y\}\subseteq L$ with $\sigma(x)\neq\sigma(y)$} \Comment{expansion, layer 1}
  \ForAll{$(a,b)\in\big((x,y),(y,x)\big)$ with $(a,b)\notin E(G)$}
    \State $(b',r) \gets \Call{FindCandidate}{G,a,b}$
    \State add new vertex $q$ with edges $(p_{xy},q),\,(q,a),\,(q,b')$ \Comment{$[ab:ab']$}
    \State remove edge $(p_{xy},a)$ \Comment{shortcut}
    \State \textbf{if not} $r$ \textbf{then} $W \gets W\cup\{(b',a,q)\}$ \Comment{pending correction}
  \EndFor
\EndFor
\State $\ell \gets 2$
\While{$W\neq\emptyset$ \textbf{and} $\ell\le K$} \Comment{layers $2,3,\dots$}
  \State $W' \gets \emptyset$
  \ForAll{$(a,b,u)\in W$}
    \State $(b',r) \gets \Call{FindCandidate}{G,a,b}$
    \State add new vertex $q$ with edges $(u,q),\,(q,a),\,(q,b')$
    \State remove edge $(u,a)$
    \State \textbf{if not} $r$ \textbf{then} $W' \gets W'\cup\{(b',a,q)\}$
  \EndFor
  \State $W \gets W'$;\ \ $\ell \gets \ell+1$
\EndWhile
\State \Return $(N,\sigma)$
\Statex
\Function{FindCandidate}{$G,a,b$}
  \State $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G),\ (v,a)\in E(G)\}$
  \State \textbf{if} $C\neq\emptyset$ \textbf{then} \Return (random element of $C$, true)
  \State $C \gets \{v\in L : \sigma(v)=\sigma(b),\ (a,v)\in E(G)\}$
  \State \textbf{if} $C=\emptyset$ \textbf{then} \textbf{error} \Comment{$(G,\sigma)$ not sink-free}
  \State $C^{*} \gets \{v\in C : \exists\, w\in L \text{ with } \sigma(w)=\sigma(a),\ (v,w)\in E(G),\ (w,v)\in E(G)\}$
  \State \textbf{if} $C^{*}\neq\emptyset$ \textbf{then} $C \gets C^{*}$
  \State \Return (random element of $C$, false)
\EndFunction
\end{algorithmic}