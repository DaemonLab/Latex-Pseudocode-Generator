# Latex-Pseudocode-Generator

### About
This project aims to create a tool that takes the input of a C++ function and returns a pseudocode snippet written in LaTeX, that can be used inside a LaTeX document.

### Requirements
A web application that has a text area where the user can enter the function, hit a submit button, and get the output which can be copied for further use.
Include as much language support as possible, and include a detailed documentation of all the accepted keywords, and how they will get converted. Also remember to convert the comments to LaTeX.
Here is an example of how a function might look like.
```tex
\usepackage{algorithm}
\usepackage{algpseudocode}
\begin{algorithm}
\caption{Level Order Traversal}
\begin{algorithmic}
\Procedure{levelOrderTraversal}{root}
  \If{root == NULL}
    \State \Return
  \EndIf
  \State nodeQueue
  \Comment{queue of Nodes}
  \State Enqueue(nodeQueue, root)
  \While{nodeQueue $\neq \phi$ }
    \State node $\gets$ head[nodeQueue]
    \State \textbf{print} d[node]
    \Comment{data $\gets$ d, parent $\gets$ $\phi$}
    \State Dequeue(nodeQueue)
    \If{l[node] $\neq \phi$}
      \State Enqueue(nodeQueue, l[node])
      \Comment{left child $\gets$ l}
    \EndIf
      \If{r[node] $\neq \phi$}
      \State Enqueue(nodeQueue, r[node])
      \Comment{right child $\gets$ r}
    \EndIf
  \EndWhile
\EndProcedure
\end{algorithmic}
\end{algorithm}
```
which renders as

<img width="429" alt="image" src="https://user-images.githubusercontent.com/77713537/210036832-47d2b3c7-6810-4ce6-a588-1ecec8fcd54c.png">

### Ideas
- Use string processing to break down code into blocks in a hierarchical manner. For example, first identify all the code inside the function, then at one level deeper, and so on. Then for all the different blocks, convert them into LaTeX by declaring a set of rules against every keyword and statement type (declaration, loop, if-else, etc.). 
- For example, `int i = 0;` becomes `\State i $\gets$ 0`.
- Including indentation in the generated LaTeX code would be great!


