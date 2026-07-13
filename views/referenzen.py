"""Referenzen & Quellen: alle in den Kapiteln zitierten Werke mit Links."""

import streamlit as st

from utils.theming import kapitel_kopf

kapitel_kopf(
    "📚",
    "Referenzen & Quellen",
    "Alle in den Kapiteln zitierten Bücher und Paper, mit Links zu PDF oder Buchseite",
)

st.markdown(
    """
Diese Seite sammelt sämtliche Quellen aus den Abschnitten „Weiterführende
Literatur“ der Kapitel. Viele der Bücher sind von den Autoren kostenlos
online bereitgestellt, die übrigen Links führen zur offiziellen Buch- oder
Artikelseite.
"""
)

st.markdown("## Machine Learning")
st.markdown(
    """
- G. James, D. Witten, T. Hastie & R. Tibshirani (2021), *An Introduction to
  Statistical Learning*, 2. Aufl., Springer.
  [Frei online](https://www.statlearning.com/)
- T. Hastie, R. Tibshirani & J. Friedman (2009), *The Elements of Statistical
  Learning*, 2. Aufl., Springer.
  [Frei online](https://hastie.su.domains/ElemStatLearn/)
- I. Goodfellow, Y. Bengio & A. Courville (2016), *Deep Learning*, MIT Press.
  [Frei online](https://www.deeplearningbook.org/)
- M. Nielsen (2015), *Neural Networks and Deep Learning*, Online-Buch.
  [Frei online](http://neuralnetworksanddeeplearning.com/)
- C. Molnar, *Interpretable Machine Learning*.
  [Frei online](https://christophm.github.io/interpretable-ml-book/)
- S. Lundberg & S.-I. Lee (2017), *A Unified Approach to Interpreting Model
  Predictions*, NeurIPS. [arXiv](https://arxiv.org/abs/1705.07874)
- M. T. Ribeiro, S. Singh & C. Guestrin (2016), *"Why Should I Trust You?":
  Explaining the Predictions of Any Classifier*, KDD.
  [arXiv](https://arxiv.org/abs/1602.04938)
- E. Kıcıman, R. Ness, A. Sharma & C. Tan (2023), *Causal Reasoning and Large
  Language Models: Opening a New Frontier for Causality*.
  [arXiv](https://arxiv.org/abs/2305.00050)
- M. Zečević, M. Willig, D. S. Dhami & K. Kersting (2023), *Causal Parrots:
  Large Language Models May Talk Causality But Are Not Causal*, Transactions
  on Machine Learning Research. [arXiv](https://arxiv.org/abs/2308.13067)
"""
)

st.markdown("## Kausalinferenz")
st.markdown(
    """
- S. Cunningham (2021), *Causal Inference: The Mixtape*, Yale University
  Press. [Frei online](https://mixtape.scunning.com/)
- M. Facure, *Causal Inference for the Brave and True*.
  [Frei online](https://matheusfacure.github.io/python-causality-handbook/landing-page.html)
- J. Pearl & D. Mackenzie (2018), *The Book of Why*, Basic Books.
  [Buchseite](https://bayes.cs.ucla.edu/WHY/)
- J. Pearl, M. Glymour & N. P. Jewell (2016), *Causal Inference in
  Statistics: A Primer*, Wiley.
  [Buchseite](https://bayes.cs.ucla.edu/PRIMER/)
- J. Pearl (2009), *Causality: Models, Reasoning, and Inference*, 2. Aufl.,
  Cambridge University Press.
  [Buchseite](https://bayes.cs.ucla.edu/BOOK-2K/)
- J. Peters, D. Janzing & B. Schölkopf (2017), *Elements of Causal
  Inference*, MIT Press.
  [Buchseite mit Open-Access-PDF](https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/)
- G. W. Imbens & D. B. Rubin (2015), *Causal Inference for Statistics,
  Social, and Biomedical Sciences: An Introduction*, Cambridge University
  Press. [Buchseite](https://doi.org/10.1017/CBO9781139025751)
- J. D. Angrist & J.-S. Pischke (2009), *Mostly Harmless Econometrics*,
  Princeton University Press.
  [Buchseite](https://www.mostlyharmlesseconometrics.com/)
- M. Huber (2023), *Causal Analysis: Impact Evaluation and Causal Machine
  Learning with Applications in R*, MIT Press.
  [Buchseite](https://mitpress.mit.edu/9780262545914/causal-analysis/)
- D. Card & A. B. Krueger (1994), *Minimum Wages and Employment: A Case
  Study of the Fast-Food Industry in New Jersey and Pennsylvania*, American
  Economic Review 84(4), 772–793.
  [NBER Working Paper](https://www.nber.org/papers/w4509)
- V. Chernozhukov, D. Chetverikov, M. Demirer, E. Duflo, C. Hansen,
  W. Newey & J. Robins (2018), *Double/Debiased Machine Learning for
  Treatment and Structural Parameters*, The Econometrics Journal 21(1),
  C1–C68. [DOI](https://doi.org/10.1111/ectj.12097)
- P. Bach, V. Chernozhukov, M. S. Kurz & M. Spindler (2022), *DoubleML: An
  Object-Oriented Implementation of Double Machine Learning in Python*,
  Journal of Machine Learning Research 23(53), 1–6.
  [JMLR](https://www.jmlr.org/papers/v23/21-0862.html)
"""
)

st.markdown("## Bayesianische Statistik, SEM und Surveys")
st.markdown(
    """
- R. McElreath (2020), *Statistical Rethinking*, 2. Aufl., CRC Press.
  [Buchseite](https://xcelab.net/rm/)
- A. Gelman, J. B. Carlin, H. S. Stern, D. B. Dunson, A. Vehtari &
  D. B. Rubin (2013), *Bayesian Data Analysis*, 3. Aufl., CRC Press.
  [Frei online](http://www.stat.columbia.edu/~gelman/book/)
- A. B. Downey (2021), *Think Bayes*, 2. Aufl., O'Reilly.
  [Frei online](https://allendowney.github.io/ThinkBayes2/)
- R. B. Kline (2023), *Principles and Practice of Structural Equation
  Modeling*, 5. Aufl., Guilford Press.
  [Buchseite](https://www.guilford.com/books/Principles-and-Practice-of-Structural-Equation-Modeling/Rex-Kline/9781462551910)
- D. C. Mutz (2011), *Population-Based Survey Experiments*, Princeton
  University Press.
  [Buchseite](https://press.princeton.edu/books/paperback/9780691144528/population-based-survey-experiments)
"""
)

st.markdown("## Software")
st.markdown(
    """
- [DoubleML](https://docs.doubleml.org/) (Python/R), Double Machine Learning
- [scikit-learn](https://scikit-learn.org/), Machine Learning in Python
- [PyMC](https://www.pymc.io/) und [Stan](https://mc-stan.org/), probabilistische Modellierung
- [shap](https://shap.readthedocs.io/) und [lime](https://github.com/marcotcr/lime), Explainable ML
- [semopy](https://semopy.com/) (Python) und [lavaan](https://lavaan.ugent.be/) (R), Strukturgleichungsmodelle
"""
)
