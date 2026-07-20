"""Zweistufige Referenzseite: Themenkatalog plus kanonische Vertiefung."""

import streamlit as st

from utils.theming import kapitel_kopf
from utils.topics import load_topics

kapitel_kopf(
    "📚",
    "Referenzen & Quellen",
    "Einstiegsliteratur für eure Projekte und Quellen zum Weiterdenken",
)

st.markdown("## Quellen für euren Projekteinstieg")
st.markdown(
    "Öffnet euren Track, um die beiden empfohlenen Einstiegsquellen und eine "
    "optionale Vertiefung zusammen zu sehen. Hier könnt ihr außerdem bequem "
    "in den Quellen der anderen Gruppen stöbern."
)

for topic in load_topics():
    with st.expander(f"{topic.emoji} {topic.title}"):
        for label, source in [
            ("Einstieg", topic.required_sources[0]),
            ("Einstieg", topic.required_sources[1]),
            ("Optional", topic.optional_source),
        ]:
            st.markdown(
                f"**{label}: [{source.title}]({source.url})**  \n"
                f"{source.authors} · {source.description}"
            )

st.markdown("## Weiterführende und kanonische Literatur")
st.markdown(
    """
Wenn ihr einen Begriff nachschlagen, eine Methode genauer verstehen oder eine
Originalarbeit lesen möchtet, findet ihr hier weitere Standardwerke. Die
Quellen aus den Projekt-Tracks werden nicht noch einmal aufgeführt.

### Machine Learning und Explainable AI

- G. James, D. Witten, T. Hastie & R. Tibshirani (2021), *An Introduction to
  Statistical Learning*, 2. Aufl., Springer. [Frei online](https://www.statlearning.com/)
- T. Hastie, R. Tibshirani & J. Friedman (2009), *The Elements of Statistical
  Learning*, 2. Aufl., Springer. [Frei online](https://hastie.su.domains/ElemStatLearn/)
- I. Goodfellow, Y. Bengio & A. Courville (2016), *Deep Learning*, MIT Press.
  [Frei online](https://www.deeplearningbook.org/)
- M. Nielsen (2015), *Neural Networks and Deep Learning*.
  [Frei online](http://neuralnetworksanddeeplearning.com/)
- S. Lundberg & S.-I. Lee (2017), *A Unified Approach to Interpreting Model
  Predictions*. [arXiv](https://arxiv.org/abs/1705.07874)
- M. T. Ribeiro, S. Singh & C. Guestrin (2016), *“Why Should I Trust You?”:
  Explaining the Predictions of Any Classifier*.
  [arXiv](https://arxiv.org/abs/1602.04938)
- E. Kıcıman, R. Ness, A. Sharma & C. Tan (2023), *Causal Reasoning and Large
  Language Models*. [arXiv](https://arxiv.org/abs/2305.00050)

### Kausalinferenz

- J. Pearl & D. Mackenzie (2018), *The Book of Why*.
  [Buchseite](https://bayes.cs.ucla.edu/WHY/)
- J. Pearl, M. Glymour & N. P. Jewell (2016), *Causal Inference in Statistics:
  A Primer*. [Buchseite](https://bayes.cs.ucla.edu/PRIMER/)
- J. Pearl (2009), *Causality*, 2. Aufl.
  [Buchseite](https://bayes.cs.ucla.edu/BOOK-2K/)
- J. Peters, D. Janzing & B. Schölkopf (2017), *Elements of Causal Inference*.
  [Open Access](https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/)
- G. W. Imbens & D. B. Rubin (2015), *Causal Inference for Statistics, Social,
  and Biomedical Sciences*. [Buchseite](https://doi.org/10.1017/CBO9781139025751)
- M. Huber (2023), *Causal Analysis*. [Buchseite](https://mitpress.mit.edu/9780262545914/causal-analysis/)
- J. D. Angrist & J.-S. Pischke (2009), *Mostly Harmless Econometrics*.
  [Buchseite](https://www.mostlyharmlesseconometrics.com/)
- D. Card & A. B. Krueger (1994), *Minimum Wages and Employment*.
  [NBER Working Paper](https://www.nber.org/papers/w4509)
- V. Chernozhukov et al. (2018), *Double/Debiased Machine Learning for
  Treatment and Structural Parameters*. [DOI](https://doi.org/10.1111/ectj.12097)
- P. Bach et al. (2022), *DoubleML: An Object-Oriented Implementation of Double
  Machine Learning in Python*. [JMLR](https://www.jmlr.org/papers/v23/21-0862.html)
- V. Chernozhukov et al. (2024), *Applied Causal Inference Powered by ML and AI*.
  [Frei online](https://causalml-book.org/)

### Bayesianische Statistik, SEM und Surveys

- A. Gelman et al. (2013), *Bayesian Data Analysis*, 3. Aufl.
  [Frei online](http://www.stat.columbia.edu/~gelman/book/)
- C. M. Bishop (2006), *Pattern Recognition and Machine Learning*.
  [Buchseite](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/)
- Y. Gal (2016), *Uncertainty in Deep Learning*.
  [Dissertation](https://www.cs.ox.ac.uk/people/yarin.gal/website/thesis/thesis.pdf)
- R. B. Kline (2023), *Principles and Practice of Structural Equation Modeling*,
  5. Aufl. [Buchseite](https://www.guilford.com/books/Principles-and-Practice-of-Structural-Equation-Modeling/Rex-Kline/9781462551910)
- D. C. Mutz (2011), *Population-Based Survey Experiments*.
  [Buchseite](https://press.princeton.edu/books/paperback/9780691144528/population-based-survey-experiments)

### Software

- [DoubleML](https://docs.doubleml.org/) – Double Machine Learning
- [scikit-learn](https://scikit-learn.org/) – Machine Learning in Python
- [PyMC](https://www.pymc.io/) und [Stan](https://mc-stan.org/) – probabilistische Modellierung
- [shap](https://shap.readthedocs.io/) und [lime](https://github.com/marcotcr/lime) – Explainable ML
- [semopy](https://semopy.com/) und [lavaan](https://lavaan.ugent.be/) – Strukturgleichungsmodelle
"""
)
