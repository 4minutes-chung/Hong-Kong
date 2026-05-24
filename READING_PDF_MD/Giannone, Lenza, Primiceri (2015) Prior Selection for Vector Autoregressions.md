# Giannone, Lenza, Primiceri (2015) Prior Selection for Vector Autoregressions

## Page 1

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
Domenico Giannone, Michele Lenza, and Giorgio E. Primiceri*
Abstract—Vector autoregressions (VARs) are ﬂexible time series models
that can capture complex dynamic interrelationships among macroeco-
nomic variables. However, their dense parameterization leads to unstable
inference and inaccurate out-of-sample forecasts, particularly for models
with many variables. A solution to this problem is to use informative pri-
ors in order to shrink the richly parameterized unrestricted model toward
a parsimonious naıve benchmark, and thus reduce estimation uncertainty.
This paper studies the optimal choice of the informativeness of these priors,
which we treat as additional parameters, in the spirit of hierarchical model-
ing. This approach, theoretically grounded and easy to implement, greatly
reduces the number and importance of subjective choices in the setting of
the prior. Moreover, it performs very well in terms of both out-of-sample
forecasting—as well as factor models—and accuracy in the estimation of
impulse response functions.
I.
Introduction
I
N this paper, we study the choice of the informativeness of
the prior distribution on the coefﬁcients of the following
VAR model:
yt = C + B1yt−1 + · · · + Bpyt−p + εt,
(1)
εt ∼N (0, Σ) ,
where yt is an n × 1 vector of endogenous variables, εt is an
n × 1 vector of exogenous shocks, and C, B1, . . . , Bp, and Σ
are matrices of suitable dimensions containing the model’s
unknown parameters.
With ﬂat priors and conditioning on the initial p observa-
tions, the posterior distribution of β ≡vec([C, B1, . . . , Bp]′)
is centered at the ordinary least square (OLS) estimate of
the coefﬁcients, and it is easy to compute. It is well known,
however, that working with ﬂat priors leads to inadmissible
estimators (Stein, 1956) and yields poor inference, partic-
ularly in large-dimensional systems (see, e.g., Sims, 1980;
Litterman, 1986). One typical symptom of this problem is
the fact that these models generate inaccurate out-of-sample
predictions due to the large estimation uncertainty of the
parameters.
In order to improve the forecasting performance of VAR
models, Litterman (1980) and Doan, Litterman, and Sims
(1984) have proposed combining the likelihood function
with some informative prior distributions. Using the frequen-
tist terminology, these priors are successful because they
Received for publication October 2, 2012. Revision accepted for publica-
tion May 16, 2014. Editor: Mark W. Watson.
* Giannone: Universitá LUISS, Université Libre de Bruxelles, and CEPR;
Lenza: European Central Bank and Université Libre de Bruxelles; Prim-
iceri: Northwestern University, CEPR, and NBER.
We thank Liseo Brunero, Guenter Coenen, Gernot Doppelhofer, Raf-
faella Giacomini, Dimitris Korobilis, Frank Schorfheide, Chris Sims, Raf
Wouters, and participants in several conferences and seminars for comments
and suggestions. D.G. is grateful to the Actions de Recherche Concertes
(contract ARC-AUWB/2010-15/ULB-11) and G.P. to the Alfred P. Sloan
Foundation for ﬁnancial support. The views expressed in this paper are our
own and do not necessarily reﬂect the views of the Eurosystem.
A supplemental appendix is available online at http://www.mitpress
journals.org/doi/suppl/10.1162/REST_a_00483.
effectively reduce the estimation error while generating only
relatively small biases in the estimates of the parameters.
For a more formal illustration of this point from a Bayesian
perspective, we consider the following (conditional) prior
distribution for the VAR coefﬁcients,
β|Σ ∼N (b, Σ ⊗Ωξ) ,
where the vector b and the matrix Ω are known and ξ is a
scalar parameter controlling the tightness of the prior infor-
mation. The conditional posterior of β can be obtained by
multiplying this prior by the likelihood function. Taking
the initial p observations of the sample as given, a stan-
dard assumption that we maintain through the paper, without
explicitly conditioning on these observations, the posterior
takes the form
β|Σ, y ∼N
ˆβ (ξ) , ˆV (ξ)

,
ˆβ (ξ) ≡vec
ˆB (ξ)

,
ˆB (ξ) ≡

x′x + (Ωξ)−1−1 
x′y + (Ωξ)−1 ♭

,
ˆV (ξ) ≡Σ ⊗

x′x + (Ωξ)−1−1 ,
where y ≡

yp+1, . . . , yT
′, x
≡[xp+1, . . . , xT]′, xt
≡
[1, y′
t−1, . . . , y′
t−p]′, and ♭is a matrix obtained by reshaping
the vector b in such a way that each column corresponds
to the prior mean of the coefﬁcients of each equation (i.e.,
b ≡vec (♭)). Notice that if we choose a lower ξ, the prior
becomes more informative, the posterior mean of β moves
toward the prior mean, and the posterior variance falls.
In this context, one natural way to assess the impact of
different priors on the model’s ability to ﬁt the data is to
evaluate their effect on the model’s out-of-sample forecasting
performance, summarized by the probability of observing
low forecast errors. To this end, rewrite equation (1) as
yt = Xtβ + εt,
where Xt ≡In ⊗x′
t and In denotes an n × n identity matrix.
At time T, the distribution of the one-step-ahead forecast is
given by
yT+1|Σ, y ∼N

XT+1ˆβ (ξ) , XT+1 ˆV (ξ) X′
T+1 + Σ

,
whose variance depends on both the posterior variance of the
coefﬁcients and the volatility of the innovations. It is then
easy to see that neither very high nor very low values of
ξ are likely to be ideal. On the one hand, if ξ is too low
and the prior very dogmatic, density forecasts will be con-
centrated around XT+1b. This results in a low probability of
observing small forecast errors unless the prior mean hap-
pens to be in a close neighborhood of the likelihood peak
(and there is no reason to believe that this is the case in gen-
eral). On the other hand, if ξ is too high and the prior too
The Review of Economics and Statistics, May 2015, 97(2): 436–451
© 2015 by the President and Fellows of Harvard College and the Massachusetts Institute of Technology
doi:10.1162/REST_a_00483
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 2

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
437
uninformative, the model generates highly dispersed density
forecasts, especially in high-dimensional VARs, because of
high estimation uncertainty. This also lowers the probabil-
ity of observing small forecast errors, despite the fact that
the distance between yT+1 and XT+1ˆβ (ξ) might be small. In
sum, neither ﬂat nor dogmatic priors maximize the ﬁt of the
model, which makes the choice of the informativeness of the
prior distribution a crucial issue.
The literature has proposed a number of heuristic method-
ologies to set the informativeness of the prior distribution
on the VAR coefﬁcients. For example, Litterman (1980) and
Doan et al. (1984) set the tightness of the prior by maximiz-
ing the out-of-sample forecasting performance of the model
over a presample. Ba´nbura, Giannone, and Reichlin (2010)
propose instead to control for overﬁtting by choosing the
shrinkage parameters that yield a desired in-sample ﬁt.1
From a purely Bayesian perspective, however, the choice
of the informativeness of the prior distribution is conceptually
identical to the inference on any other unknown parameter of
the model. Suppose, for instance, that a model is described
by a likelihood function p (y|θ) and a prior distribution pγ (θ),
where θ is the vector of the model’s parameters and γ collects
the hyperparameters, that is, those coefﬁcients that param-
eterize the prior distribution but do not directly affect the
likelihood.2 It is then natural to choose these hyperparameters
by interpreting the model as a hierarchical model, replacing
pγ (θ) with p (θ|γ), and evaluating their posterior (Berger,
1985; Koop, 2003). Such a posterior can be obtained by
applying Bayes’ law, which yields
p (γ|y) ∝p (y|γ) · p (γ) ,
where p (γ) denotes the prior density on the hyperparameters,
also known as the hyperprior, while p (y|γ) is the so-called
marginal likelihood (ML) and corresponds to
p (y|γ) =

p (y|θ, γ) p (θ|γ) dθ.
(2)
In other words, the ML is the density of the data as a function
of the hyperparameters γ, obtained after integrating out the
uncertainty about the model’s parameters θ. Conveniently, in
the case of VARs with conjugate priors, the ML is available
in closed form.
Conducting formal inference on the hyperparameters is
theoretically grounded and also has several appealing inter-
pretations. For example, with a ﬂat hyperprior, the shape of
the posterior of the hyperparameters coincides with the ML,
which is a measure of out-of-sample forecasting performance
of a model (see Geweke, 2001; Geweke & Whiteman, 2006).
More speciﬁcally, the ML corresponds to the probability den-
sity that the model generates zero forecast errors, which can
1 A number of papers have subsequently followed either the ﬁrst (Robert-
son & Tallman, 1999; Wright, 2009; Giannone et al., 2014) or the second
strategy (Giannone, Lenza, & Reichlin, 2008; Bloor & Matheson, 2011;
Carriero, Kapetanios, & Marcellino, 2009; Koop, 2013).
2 The distinction between parameters and hyperparameters is mostly
ﬁctitious and made only for convenience.
be seen by rewriting the ML as a product of conditional
densities:
p (y|γ) =
T
t=p+1
p

yt|yt−1, γ

.
As a consequence, maximizing the posterior of the hyper-
parameters corresponds to maximizing the one-step-ahead
out-of-sample forecasting ability of the model.
Moreover, the strategy of estimating hyperparameters by
maximizing the ML (i.e., their posterior under a ﬂat hyper-
prior) is an empirical Bayes method (Robbins, 1956), which
has a clear frequentist interpretation. On the other hand, the
full posterior evaluation of the hyperparameters (as advo-
cated, for example, by Lopes, Moreira, & Schmidt, 1999, for
VARs) can be thought of as conducting Bayesian inference on
the population parameters of a random effects model or, more
generally, of a hierarchical model (see, Gelman et al., 2004).
Finally, the hierarchical structure also implies that the
unconditional prior for the parameters θ has a mixed dis-
tribution:
p (θ) =

p (θ|γ) p (γ) dγ.
Mixed distributions have generally fatter tails than each of
the component distributions p (θ|γ), a property that robusti-
ﬁes inference. In fact, when the prior has fatter tails than the
likelihood, the posterior is less sensitive to extreme discrep-
ancies between prior and likelihood (Berger, 1985; Berger &
Berliner, 1986).
A.
Contribution
In this paper, we adopt the hierarchical modeling approach
to make inference about the informativeness of the prior
distribution of Bayesian vector autoregressions (BVARs)
estimated on postwar U.S. macroeconomic data. We con-
sider a combination of the conjugate priors most commonly
used in the literature (the Minnesota, sum-of-coefﬁcients, and
dummy-initial-observation priors), and document that this
estimation strategy generates accurate out-of-sample predic-
tions in terms of both point and density forecasts. The key
to success lies in the fact that this procedure automatically
selects the appropriate amount of shrinkage: tighter priors
when the model involves many unknown coefﬁcients relative
to the available data and looser priors in the opposite case.
Indeed, we derive an expression for the ML showing that it
takes duly into account the trade-off between in-sample ﬁt
and model complexity.
Because of this feature, the hierarchical BVAR improves
over naıve benchmarks and ﬂat-prior VARs, even for small-
scale models, for which the optimal shrinkage is low but
not 0. In addition, the hierarchical BVAR outperforms the
most popular ad hoc procedures to select hyperparame-
ters (Litterman, 1980; Ba´nbura et al., 2010). Finally, we
ﬁnd that the forecasting performance of the model typically
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 3

438
THE REVIEW OF ECONOMICS AND STATISTICS
improves as we include more variables, and it is comparable
to that of factor models. This is remarkable because the lat-
ter are among the most successful forecasting methods in the
literature.
Our second contribution is documenting that this hierar-
chical BVAR approach performs very well also in terms of
accuracy of the estimation of impulse response functions
in identiﬁed VARs. We conduct two experiments to make
this point. First, we study the transmission of an exogenous
increase in the federal funds rate in a large-scale model with
22 variables. The estimates of the impulse responses that we
obtainarebroadlyinlinewiththeusualnarrativeoftheeffects
of an exogenous tightening in monetary policy. This ﬁnding,
together with the result that the same large-scale model pro-
duces good forecasts, indicates that our approach is able to
effectively deal with the curse of dimensionality. However,
in this empirical exercise, there is no way of formally check-
ing the accuracy of the estimated impulse response functions,
sincewedonothaveadirectlyobservablecounterpartofthese
objects in the data. Therefore, we conduct a second exercise,
which is a controlled Monte Carlo experiment. We simulate
data from a microfounded, medium-scale, dynamic stochas-
tic general equilibrium model estimated on U.S. postwar data.
We then use the simulated data to estimate our hierarchi-
cal BVAR and compare the implied impulse responses to
monetary policy shocks to those of the true data-generating
process. This experiment lends strong support to our model.
The surprising ﬁnding is in fact that the hierarchical Bayesian
procedure generates very little bias, while drastically increas-
ing the efﬁciency of the impulse response estimates relative
to standard ﬂat-prior VARs.
B.
Related Literature
Hierarchical modeling (or empirical Bayes, that is, its fre-
quentistversion)hasbeensuccessfullyadoptedinmanyﬁelds
(Berger, 1985; Gelman et al., 2004, for an overview). It
has also been advocated by the ﬁrst proponents of BVARs
(Doan et al., 1984, Sims & Zha, 1998, and, more recently,
Canova, 2007, and Del Negro & Schorfheide, 2011), but
seldom formally implemented in this context. Exceptions to
this statement are Lopes et al. (1999), who use a hierarchi-
cal approach to estimate a small-scale VAR of the Brazilian
economy with a Minnesota prior, and Ni and Sun (2003),
who exploit an appealing but restrictive hierarchical struc-
ture where the hyperparameter controlling the variance of
the prior can be integrated out analytically from the prior and
the posterior of the VAR coefﬁcients.
Del Negro and Schorfheide (2004) and Del Negro et al.
(2007) also use the ML to choose the tightness of a prior
for VARs derived from the posterior density of a dynamic
stochastic general equilibrium model. In the context of time-
varying VARs, the ML has been used by Primiceri (2005) and
Belmonte, Koop, and Korobilis (2014) to choose the infor-
mativeness of the prior distribution for the time variation of
coefﬁcients and volatilities. Relative to these authors, our
focus is on BVARs with standard conjugate priors, for which
the posterior of the hyperparameters is available in closed
form.
Closer to our framework, Phillips (1995) chooses the
hyperparameters of the Minnesota prior for VARs using the
asymptotic posterior odds criterion of Phillips and Ploberger
(1994), which is also related to the ML. Del Negro and
Schorfheide (2004, 2011), Carriero, Kapetanios, and Mar-
cellino (2010) and Carriero, Clark, and Marcellino (2011)
have used the ML to select the variance of a Minnesota prior
from a grid of possible values. We generalize this approach to
the optimal selection of a variety of commonly adopted prior
distributions for BVARs. This includes the prior on the sum of
coefﬁcients proposed by Doan et al. (1984), which turns out
to be crucial to enhance the forecasting performance of the
model. Moreover, relative to these studies, we take an explicit
hierarchical modeling approach that allows us to take the
uncertainty about hyperparameters into account and evaluate
the density forecasts of the model.
More important, we also complement the model’s fore-
casting evaluation with an assessment of the performance of
hierarchical BVARs for impulse response estimation, which
is new in the literature.
Finally, we document that our approach works well for
models of very different scale, including three-variable VARs
andmuchlarger-scaleones. Inthisrespect, ourworkrelatesto
the growing literature on forecasting using factors extracted
from large information sets (Forni et al., 2000; Stock & Wat-
son, 2002b), large Bayesian VARs (Ba´nbura et al., 2010;
Koop, 2013), and empirical Bayes regressions with large
sets of predictors (Knox, Stock, & Watson, 2000; Korobilis,
2013).
The rest of the paper is organized as follows. Sections II
and III provide some additional details about the computation
and interpretation of the ML and the priors and hyperpriors
used in our investigation. Sections IV and V focus instead on
the empirical application to macroeconomic forecasting and
impulse response estimation. Section VI concludes.
II.
The Choice of Hyperparameters for BVARs
In the previous section, we argued that the most natural
way of choosing the hyperparameters of a model is based on
their posterior distribution. This posterior is proportional to
the product of the hyperprior and the ML. The hyperprior is
a level 2 prior on the hyperparameters, while the ML is the
likelihood of the observed data as a function of the hyper-
parameters, which can be obtained by integrating out the
model’s coefﬁcients, as in equation (2).
Although this procedure can be applied very generally, in
this paper we restrict our attention to prior distributions for
VAR coefﬁcients belonging to the following normal-inverse-
Wishart family:
Σ ∼IW (Ψ; d) ,
(3)
β|Σ ∼N (b, Σ ⊗Ω) ,
(4)
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 4

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
439
where the elements Ψ, d, b, and Ω are typically functions of
a lower-dimensional vector of hyperparameters γ. We focus
on these priors for two reasons. First, this class includes
the priors most commonly used by the literature on BVARs
(see the surveys of Koop & Korobilis, 2010; Del Negro &
Schorfheide, 2011; Karlsson, 2012).3 Second, the prior, equa-
tions (3 and 4), is conjugate and has the advantage that the ML
of the BVAR can be computed in closed form as a function
of γ.
In online appendix A, we prove that
p (y|γ) ∝


V posterior
ε
−1 V prior
ε

T−p+d
2
	



Fit
·
T
t=p+1
Vt|t−1
−1
2
	



Penalty for model complexity
,
(5)
where V posterior
ε
and V prior
ε
are the posterior and prior
means (or modes) of the residual variance and Vt|t−1 ≡
EΣ[var(yt|yt−1, Σ)] is the variance (conditional on Σ) of
the one-step-ahead forecast of y, averaged across all pos-
sible a priori realizations of Σ. While exact closed-form
expressions for these objects are provided in the appendix,
here we stress that the ML consists of two crucial terms.
The ﬁrst term depends on the in-sample ﬁt of the model,
and it increases when the posterior residual variance falls
relative to the prior variance. Thus, everything else equal,
the ML criterion favors hyperparameter values that generate
smaller residuals. The second term in equation (5) is instead
a penalty for model complexity. This term penalizes models
with imprecise out-of-sample forecasts due to either large a
priori residual variances or high uncertainty of the parame-
ter estimates. These models have a higher a priori chance of
capturing any possible behavior of the data, while at the same
time assigning very low probability to all possible outcomes.
This feature is the essence of overﬁtting and is penalized by
the ML criterion. Therefore, the ML captures the standard
trade-off between model ﬁt and complexity.
The fact that the ML is available in closed form simpli-
ﬁes inference substantially, because it makes it easy to either
maximize or simulate the posterior of the hyperparameters.
As we pointed out in section I, the advantage of the approach
based on the maximization is that, under a ﬂat hyperprior, it
is an empirical Bayes procedure and has a classical interpre-
tation. It also coincides with selecting hyperparameters that
maximize the one-step-ahead out-of-sample forecasting per-
formance of the model. The full posterior simulation allows
us to account for the estimation uncertainty of the hyperpa-
rameters and has an interpretation of Bayesian hierarchical
3 Some recent studies have also proposed alternative priors for VARs that
do not belong to this family. See, for example, Del Negro and Schorfheide
(2004), Villani (2009), Jarocinski and Marcet (2010), and Koop (2013).
modeling. This approach can be implemented using a sim-
ple Markov chain Monte Carlo algorithm. In particular, we
use a Metropolis step to draw the low-dimensional vector of
hyperparameters. Conditional on a value of γ, the VAR coef-
ﬁcients [β, Σ] can then be drawn from their posterior, which
is normal-inverse-Wishart. Online appendix B presents the
details of this procedure.
We now turn to the empirical application of our method-
ology.
III.
Priors and Hyperpriors
This section describes the speciﬁc priors that we employ
in our empirical analysis. For the sake of comparability with
previous studies, we choose the most popular prior densities
adopted by the existing literature for the estimation of BVARs
in levels. However, it is important to stress that our method is
not conﬁned to these priors, but applies more generally to all
priors belonging to the class deﬁned by equations (3 and 4).
As in Kadiyala and Karlsson (1997), we set the degrees
of freedom of the inverse-Wishart distribution to d = n + 2,
the minimum value that guarantees the existence of the prior
mean of Σ (it is equal to Ψ/(d −n −1)). In addition, we
take Ψ to be a diagonal matrix with an n × 1 vector ψ on
the main diagonal. We treat ψ as a hyperparameter, which
differs from the existing literature that has been ﬁxing this
parameter using sample information. As for the conditional
gaussian prior for β, we combine three prior densities.
The baseline prior is a version of the so-called Minnesota
prior, introduced in Litterman (1979, 1980). This prior is cen-
tered on the assumption that each variable follows a random
walk process, possibly with drift, which is a parsimonious yet
“reasonable approximation of the behavior of an economic
variable” (Litterman, 1979, p. 20). More precisely, this prior
is characterized by the following ﬁrst and second moments,
E

(Bs)ij |Σ

=

1 if i = j and s = 1
0 otherwise
cov

(Bs)ij , (Br)hm |Σ

=
⎧
⎪⎨
⎪⎩
λ2 1
s2
Σih
ψj/(d−n−1) if m = j and
r = s
0
otherwise
,
and can be easily cast into the form of equation (4). Notice
that the variance of this prior is lower for the coefﬁcients
associated with more distant lags and that coefﬁcients asso-
ciated with the same variable and lag in different equations
are allowed to be correlated. Finally, the key hyperparameter
is λ, which controls the scale of all the variances and covari-
ances and effectively determines the overall tightness of this
prior.
The literature following Litterman’s work introduced
reﬁnements of the Minnesota prior to further “favor unit
roots and cointegration, which ﬁts the beliefs reﬂected in
the practices of many applied macroeconomists” (Sims &
Zha, 1998, p. 958). Loosely speaking, the objective of these
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 5

440
THE REVIEW OF ECONOMICS AND STATISTICS
additional priors is to reduce the importance of the determin-
istic component implied by the VARs estimated conditioning
on the initial observations (Sims, 1992a). This determinis-
tic component is deﬁned as τt ≡Ep

yt|y1, . . . , yp, ˆβ

, that
is, the expectation of future ys given the initial conditions
and the value of the estimated VAR coefﬁcients. According
to Sims (1992a), in unrestricted VARs, τt has a tendency to
exhibit temporal heterogeneity, a markedly different behavior
at the beginning and the end of the sample, and to explain an
implausibly high share of the variation of the variables over
the sample. As a consequence, priors limiting the explanatory
power of this deterministic component have been shown to
improve the forecasting performance of BVARs.
The ﬁrst prior of this type is known as a sum-of-coefﬁcients
prior and was originally proposed by Doan et al. (1984). Fol-
lowing the literature, it is implemented using Theil mixed
estimation, with a set of n artiﬁcial observations—one for
each variable—stating that a no-change forecast is a good
forecast at the beginning of the sample. More precisely, we
construct the following set of dummy observations:
y+
n×n
= diag
 ¯y0
μ

x+
n×(1+np) =

0
n×1, y+, . . . , y+

,
where ¯y0 is an n × 1 vector containing the average of the ﬁrst
p observations for each variable and the expression diag(v)
denotes the diagonal matrix with the vector v on the main
diagonal. These artiﬁcial observations are added on top of the
data matrices y ≡

yp+1, . . . , yT
′ and x ≡[xp+1, . . . , xT]′,
which are then used for inference. The prior implied by
these dummy observations is centered at 1 for the sum of
coefﬁcients on own lags for each variable and at 0 for the
sum of coefﬁcients on other variables’ lags. It also intro-
duces correlation among the coefﬁcients on each variable in
each equation. The hyperparameter μ controls the variance
of these prior beliefs: as μ →∞, the prior becomes unin-
formative, while μ →0 implies the presence of a unit root
in each equation and rules out cointegration.
The fact that, in the limit, the sum-of-coefﬁcients prior
is not consistent with cointegration motivates the use of an
additionalpriorthatwasintroducedbySims(1993),knownas
the dummy-initial-observation prior. It is implemented using
the following dummy observation,
y++
1×n
= ¯y′
0
δ
x++
1×(1+np) =
1
δ, y++, . . . , y++

,
which states that a no-change forecast for all variables is a
good forecast at the beginning of the sample. The hyperpa-
rameter δ controls the tightness of the prior implied by this
artiﬁcial observation. As δ →∞, the prior becomes uninfor-
mative. And, as δ →0, all the variables of the VAR are forced
to be at their unconditional mean, or the system is character-
ized by the presence of an unspeciﬁed number of unit roots
without drift. As such, the dummy-initial-observation prior
is consistent with cointegration.
Summing up, the setting of these priors depends on the
hyperparameters λ, μ, δ, and ψ, which we treat as additional
parameters. As hyperpriors for λ, μ, and δ, we choose gamma
densities with mode equal to 0.2, 1, and 1, the values recom-
mended by Sims and Zha (1998), and standard deviations
equal to 0.4, 1, and 1, respectively. Finally, the choice of the
hyperprior for each element of the vector ψ/ (d −n −1),
that is, the prior mean of the main diagonal of Σ, should
be loosely related to the scale of the variables in the model.
We pick an inverse-Gamma with scale and shape equal to
(0.02)2 because it seems appropriate for our data expressed
in annualized log-terms (see table 1). This hyperprior peaks
at approximately (0.02)2, and it is proper but quite disperse
since it does not have either a variance or a mean. We work
with proper hyperpriors because they guarantee the proper-
ness of the posterior and, from a frequentist perspective, the
admissibility of the estimator of the hyperparameters, a dif-
ﬁcult property to check for the case of hierarchical models
(Berger, Strawderman, & Dejung, 2005). Another appeal-
ing feature of nonﬂat hyperpriors is that they help stabilize
inference when the ML happens to have little curvature with
respect to some hyperparameters. For example, we have
noticedthatthiscansometimesoccurforthehyperparameters
of the sum-of-coefﬁcients or the dummy-initial-observation
priors in larger-scale models. This being said, we stress
that our hyperpriors are relatively diffuse and our empirical
results are conﬁrmed when using completely ﬂat, improper
hyperpriors.
IV.
Forecasting Evaluation of BVAR Models
The assessment of the forecasting performance of econo-
metric models has become standard in macroeconomics,
even when the main objective of the study is not to provide
accurate out-of-sample predictions. This is because the fore-
casting evaluation can be thought of as a model validation
procedure. In fact, if model complexity is introduced with
a proliferation of parameters, instabilities due to estimation
uncertainty might completely offset the gains obtained by
limiting model misspeciﬁcation. Out-of-sample forecasting
reﬂects both parameter uncertainty and model misspeciﬁca-
tion and reveals whether the beneﬁts due to ﬂexibility are
outweighed by the fact that the more general model also
captures nonprominent features of the data.
Our out-of-sample evaluation is based on the U.S. data set
constructed by Stock and Watson (2008). We work with three
different VAR models, including progressively larger sets of
variables:4
4 The complete database in Stock and Watson (2008) includes 149 quar-
terlyvariablesfrom1959Q1to2008Q4.Sinceseveralvariablesaremonthly,
we follow Stock and Watson (2008) and transform them into quarterly by
taking averages.
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 6

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
441
Table 1.—Description of the Database
Transformations
Transformations
Small
Medium
Large
Variables
Mnemonic
BVAR
Factor Model
BVAR
BVAR
BVAR
Real GDP
RGDP
4·logs
log-diff.
x
x
x
GDP deﬂator
PGDP
4·logs
log-diff.
x
x
x
Federal funds rate
FedFunds
raw
diff.
x
x
x
Consumer price index
CPI-ALL
4·logs
log-diff.
x
Commodity price
Com:spotprice(real)
4·logs
log-diff.
x
Industrial production
IP:total
4·logs
log-diff.
x
Employment
Emp:total
4·logs
log-diff.
x
Employment in the services sector
Emp:services
4·logs
log-diff.
x
Real consumption
Cons
4·logs
log-diff.
x
x
Real investment
Inv
4·logs
log-diff.
x
Real residential investment
Res.Inv
4·logs
log-diff.
x
Nonresidential investment
NonResInv
4·logs
log-diff.
x
Personal consumption Expenditures, price index
PCED
4·logs
log-diff.
x
Gross private domestic investment, price index
PGPDI
4·logs
log-diff.
x
Capacity utilization
CapacityUtil
raw
diff.
x
Consumer expectations
Consumerexpect
raw
diff.
x
Hours worked
Emp.Hours
4·logs
log-diff.
x
x
Real compensation per hours
RealComp/Hour
4·logs
log-diff.
x
x
One-year bond rate
1yrT-bond
raw
diff.
x
Five-years bond rate
5yrT-bond
raw
diff.
x
SP500
S&P500
4·logs
log-diff.
x
Effective exchange rate
Exrate:avg
4·logs
log-diff.
x
M2
M2
4·logs
log-diff.
x
1. A Small-scale model—the prototypical monetary
VAR—with three variables, i.e. GDP, the GDP deﬂator,
and the federal funds rate.
2. A Medium-scale model, which includes the variables
used for the estimation of the DSGE model of Smets
and Wouters (2007) for the U.S. economy. In other
words,weaddconsumption,investment,hoursworked,
and wages to the small model.
3. A Large-scale model, with 22 variables, using a data
set that nests the previous two speciﬁcations and
also includes a number of important additional labor
market, ﬁnancial, and monetary variables.
Further details on the database are reported in table 1.
The variables enter the models in annualized log levels
(i.e., we take logs and multiply by 4), except those already
deﬁned in terms of annualized rates, such as interest rates,
which are taken in levels. The number of lags in all the VARs
is set to ﬁve.
Using each of these three data sets, we produce the BVAR
forecasts recursively for two horizons (one and four quar-
ters), starting with the estimation sample that ranges from
1959Q1 to 1974Q4. More precisely, using data from 1959Q1
to 1974Q4, we generate draws from the posterior predictive
density of the model for 1975Q1 (one quarter ahead) and
1975Q4 (one year ahead). We then iterate the same proce-
dure updating the estimation sample, one quarter at a time,
until the end of the sample, 2008Q4. At each iteration, we
also reestimate the posterior distribution of the hyperparam-
eters. The outcome of this procedure is a time series of 137
density forecasts for each of the two forecast horizons.
We start by assessing the accuracy of our models in terms
of point forecasts, deﬁned as the median of the predictive
density at each point in time. We then turn to the evaluation
of the density forecasts to assess how accurately different
models capture the uncertainty around the point forecasts.
For each variable, the target of our evaluation is deﬁned
in terms of the h-period annualized average growth rates,
zh
i,t+h = 1
h[ yi,t+h −yi,t]. For variables speciﬁed in log levels,
this is approximately the average annualized growth rate over
the next h quarters, while for variables not transformed in
logs, this is the average quarterly change over the next h
quarters.
We compare the forecasting performance of the BVAR
to a VAR with ﬂat prior, estimated by OLS (we refer to
this model as VAR or ﬂat-prior VAR)5 and a random walk
with drift, which is the model implied by a dogmatic Min-
nesota prior (we refer to this model as RW). We also compare
the point forecasts of the BVAR to those of a single equa-
tion model, augmented with factors extracted from a large
data set using principal components.6 Factor models offer
a parsimonious representation for macroeconomic variables
while retaining the salient features of the data that notori-
ously strongly comove. Hence, factor-augmented regressions
are widely used in order to deal with the curse of dimension-
ality, since a large set of potential predictors can be replaced
in the regressions by a much smaller number of factors.
Factor-based approaches are a benchmark in the literature
and have been shown to produce accurate forecasts exploit-
ing large cross-sections of data. Speciﬁcally, we focus on
the factor-based forecasting approach of Stock and Watson
5 Precisely, the ﬂat-prior VAR is estimated using a standard uninforma-
tive reference prior proportional to |Σ|−(n+1)/2, which makes the posterior
distribution of β equivalent to the sampling distribution of its OLS estimator.
6 The principal components are extracted from the entire set of 149
variables described in Stock and Watson (2008).
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 7

442
THE REVIEW OF ECONOMICS AND STATISTICS
Table 2.—MSFE of Point Forecasts
Small (S)
Medium (M)
Large (L)
Horizons
Variables
VAR
BVAR
VAR
BVAR
VAR
BVAR
Factor M
RW
One quarter
Real GDP
13.49
9.61
19.15
7.97
8.18
7.29
10.23
GDP deﬂator
1.53
1.32
2.26
1.35
1.10
1.14
5.19
Federal funds rates
1.61
1.04
1.82
1.03
1.00
1.25
1.06
One year
Real GDP
5.40
3.85
12.10
3.42
3.97
3.52
3.98
GDP deﬂator
1.61
1.45
2.25
1.58
0.96
1.01
4.65
Federal funds rates
0.58
0.32
0.56
0.31
0.36
0.32
0.31
The table reports the mean squared forecast errors of the BVARs and the competing models (VAR: ﬂat-prior VAR, RW: random walk in levels with drift: factor M: factor augmented regression), for each variable and
horizon. The evaluation sample is 1975Q1–2008Q4 for the one-quarter-ahead forecasts and 1975Q4–2008Q4 for the one-year-ahead forecasts.
(2002a, 2002b), whose implementation details are reported
in online appendix C. Finally, later, we compare the forecast-
ing performance of our hierarchical BVAR to more heuristic
procedures for the choice of hyperparameters.
A.
Point Forecasts
Table 2 analyzes the accuracy of point forecasts by report-
ing the mean squared forecast errors (MSFE) of real GDP,
the GDP deﬂator, and the federal funds rate.
Comparing models of different size, notice that it is not
possible to estimate the large-scale VAR with a ﬂat prior. In
addition, the VAR forecasts worsen substantially when mov-
ing from the small- to the medium-scale model. This outcome
indicates that the gains from exploiting larger information
sets are completely offset by an increase in estimation error.
On the contrary, the forecast accuracy of the BVARs does
not deteriorate when increasing the scale of the model and
sometimes even improves substantially (as it is the case for
inﬂation). In this sense, the use of priors seems to be able to
turn the curse into a blessing of dimensionality. Moreover,
BVAR forecasts are systematically more accurate than the
ﬂat-prior VAR forecasts for all the variables and horizons
that we consider.
The comparison with the RW model is also favorable to
the BVARs, with the possible exception of the forecasts of
the federal funds rate at the one-year horizon. The improve-
ment of BVARs over the RW, the prior model, indicates that
our inference-based choice of the hyperparameters leads to
the use of informative priors, but not excessively so, letting
the data shape the posterior beliefs about the model’s coefﬁ-
cients. Finally, notice that the performance of the prior model
is particularly poor for inﬂation. In fact Atkeson and Oha-
nian (2001) show that a random walk for the growth rate
of the GDP deﬂator is a more appropriate naıve benchmark
model. Speciﬁcally, they propose to forecast inﬂation over
the subsequent year using the inﬂation rate over the past
year. The MSFE of this alternative simple model for inﬂation
at a four-quarter horizon is 1.24, which is smaller than that
obtained with the random walk in levels or with the small and
medium BVARs, but higher than the corresponding MSFE of
the large-scale BVAR.
Table 2 also suggests that the BVAR predictions are com-
petitive with those of the factor model. This outcome is in
line with the ﬁndings of De Mol, Giannone, and Reichlin
(2008) and indicates that factor-augmented and Bayesian
regressions capture the same features of the data. In fact,
De Mol et al. (2008) have shown that Bayesian shrinkage
and regressions augmented with principal components are
strictly connected.
B.
Density Forecasts
The point forecast evaluation of the section IVA is a use-
ful tool to discriminate among models, but it disregards the
uncertainty assigned by each model to its point prediction.
For this reason, we now turn to the evaluation of the den-
sity forecasts. We measure the accuracy of a density forecast
using the log-predictive score, which is simply the logarithm
of the predictive density generated by a model, evaluated at
the realized value of the time series. Therefore, if model A has
a higher average log predictive score than model B, it means
thatvaluesclosetotheactualrealizationsofatimeserieswere
a priori more likely according to model A relative to model
B. We measure the log-predictive score using a gaussian
approximation of the predictive density for all models.
Table 3 reports the average difference between the log pre-
dictive scores of the BVARs and the competing models (the
ﬂat-prior VAR and RW models), for each variable and hori-
zon. A positive number indicates that the density forecasts
produced by our proposed procedure are more accurate than
those of the alternative models. In addition, the HAC esti-
mate of its standard deviation (in parentheses) gives a rough
idea of the statistical signiﬁcance and the volatility of this
difference.7
Table 3 makes clear that the BVAR forecasts outperform
those of the RW and ﬂat-prior VAR also when evaluating the
whole density.
C.
Inspecting the Mechanism
In this section, we provide some intuition about why
the hierarchical procedure described previously generates
accurate forecasts. As we discussed at length in section I,
VAR models require the estimation of many free parameters,
which, when using a ﬂat prior, leads to high-estimation
7 Notice that the associated t-statistic corresponds to the statistic of
Amisano and Giacomini (2007) with standard normal distribution when
the models are estimated using a rolling scheme. This is not the case in our
exercise, since we use a recursive estimation procedure.
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 8

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
443
Table 3.—Average Difference of Log-Scores
Small (S)
Medium (M)
Large (L)
Versus
Versus
Versus
Versus
Versus
Versus
Horizons
Variables
VAR
RW
VAR
RW
VAR
RW
One quarter
Real GDP
0.10
0.06
0.30
0.16
0.17
(0.04)
(0.05)
(0.05)
(0.06)
(0.06)
GDP deﬂator
0.04
0.74
0.15
0.73
0.81
(0.03)
(0.09)
(0.06)
(0.09)
(0.09)
Federal funds rates
0.08
0.06
0.11
0.07
0.09
(0.06)
(0.08)
(0.10)
(0.08)
(0.10)
One year
Real GDP
0.10
0.00
0.40
0.06
0.03
(0.07)
(0.09)
(0.12)
(0.09)
(0.13)
GDP deﬂator
0.05
1.00
0.01
0.88
1.18
(0.10)
(0.33)
(0.22)
(0.36)
(0.30)
Federal funds rates
0.28
0.07
0.25
0.05
−0.03
(0.08)
(0.07)
(0.10)
(0.09)
(0.12)
The table reports the average difference between the log-predictive scores of the BVARs and the competing models (the ﬂat-prior VAR and RW models) for each variable and horizon. The HAC estimate of the standard
deviation of the difference between the log-predictive scores of the BVARs and the competing models is reported in parentheses. The evaluation sample is 1975Q1 to 2008Q4 for the one-quarter-ahead forecasts and
1975Q4 to 2008Q4 for the one-year-ahead forecasts.
uncertainty and overﬁtting. It is therefore beneﬁcial to shrink
the model parameters toward a parsimonious prior model.
The key to the success of the hierarchical BVAR is that it
automatically infers the appropriate amount of shrinkage by
selecting the tightness of the prior distribution. For exam-
ple, the procedure will select looser priors for models with
fewer parameters and tighter priors for models with many
parameters relative to the available data.
To illustrate this point, consider a much simpliﬁed ver-
sion of our model, that is, a BVAR with only a Minnesota
prior, and the prior mean of the diagonal elements of Σ set
equal to the variance of the residuals of an AR(1) for each
variables (as in Kadiyala & Karlsson, 1997). This model is
convenient because it involves only one hyperparameter, the
hyperparameter λ governing the overall standard deviation
of the Minnesota prior. For each data set—small, medium,
and large—we estimate our hierarchical BVAR on the full
sample and compute the posterior distribution of the hyper-
parameter λ. These posteriors are plotted in ﬁgure 1, along
with the hyperprior. Notice that in line with intuition, the pos-
terior mode (and variance) of λ decreases with the size of the
model. In other words, the larger the size of the BVAR, the
more likely it is that we should shrink the model toward the
parsimonious speciﬁcation implied by the Minnesota prior.
D.
Comparison with Alternative Methods
Given the good forecasting performance of our inference-
based methodology for choosing the hyperparameters (as
goodasthatoffactormodels),asectiondiscussingtherelative
performance of alternative methods seems warranted. How-
ever, formal alternatives to the marginal likelihood are absent
in the literature. For instance, the Bayesian or the Akaike
information criteria cannot be adopted because their penal-
ization for model complexity involves only the number of
parameters and does not depend on the value of the hyper-
parameters. As a consequence, both of these criteria would
favor models with loose priors that maximize the model
in-sample ﬁt.
Figure 1.—Posterior Distribution of the Hyperparameter Governing
the Standard Deviation of the Minnesota Prior
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0
10
20
30
40
50
60
Large
Medium
Small
Hyperprior
The ﬁgure reports the posterior distribution of the hyperparameter λ, the parameter governing the stan-
dard deviation of the Minnesota prior in the small, medium, and large BVARs and its prior distribution.
The posterior distribution is obtained using the whole sample.
An informal method to choose the hyperparameters is to
maximize the model forecasting performance over a presam-
ple, as in Litterman (1980). An alternative possibility is to
control for overﬁtting by targeting a desired in-sample ﬁt, as
in Ba´nbura et al. (2010). These heuristic procedures can be
interpreted as rough empirical Bayes estimators, and their ad
hoc nature might partly explain why Bayesian VARs have
encountered a number of opponents, especially among non-
Bayesian researchers. These approaches obviously raise a
number of questions: What is the right size of the presam-
ple and the forecasting horizon? Should we minimize the
MSFE or control for the in-sample ﬁt of all the variables
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 9

444
THE REVIEW OF ECONOMICS AND STATISTICS
Table 4.—MSFE of Alternative Methods Relative to Hierarchical Model
Small (S)
Medium (M)
Large (L)
Horizons
Variables
LIT
BGR
SZ
LIT
BGR
SZ
LIT
BGR
SZ
One quarter
Real GDP
1.04
1.02
1.19
1.09
1.06
1.12
1.09
0.96
GDP deﬂator
1.87
1.09
1.67
1.44
1.11
1.46
1.97
0.97
Federal funds rates
1.32
1.01
1.01
0.99
0.99
1.19
1.02
0.98
One year
Real GDP
1.16
1.10
1.15
1.17
1.14
1.32
0.97
0.87
GDP deﬂator
1.61
1.23
1.57
1.62
1.21
1.55
2.73
1.04
Federal funds rates
1.13
0.97
1.13
1.03
1.00
1.03
0.83
0.92
The table reports the MSFE of three alternative methods to select the tightness of the prior distributions relative to the MSFE of the hierarchical model. Numbers larger than 1 indicate that the MSFE of the alternative
method (LIT: method described in Litterman, 1980; BGR: method described in Ba´nbura et al., 2010; SZ: ﬁxed hyperparameters in Sims & Zha, 1998) is larger than the corresponding MSFE of the hierarchical model.
The evaluation sample is 1975Q1 to 2008Q4 for the one-quarter-ahead forecasts and 1975Q4 to 2008Q4 for the one-year-ahead forecasts. By construction, the MSFE of the BGR method for the small-scale model (not
reported here; see table 2) is identical to that of the ﬂat-prior VAR.
or just those of interest? Moreover, these procedures make
it hard to conduct inference incorporating hyperparameter
uncertainty. Despite these limitations, these are the most pop-
ular approaches in the literature, and we have compared them
to our methodology.
Concerning the ﬁrst method, we have repeated our fore-
casting experiment by choosing at each point in time the
hyperparameters that maximize the past forecasting ability of
the VAR. In particular, to follow Litterman (1980) as closely
as possible, the measure of out-of-sample forecasting perfor-
mance is the Theil-U statistic, computed over the previous
ﬁve years and averaged across variables and forecasting hori-
zons (1 to 4). As for the second method, we have replicated
Ba´nbura et al. (2010) by setting the hyperparameters in the
medium and large BVARs to match the average in-sample ﬁt
of the small VAR with ﬂat priors.8
Table 4 reports the MSFE of the Litterman (1980) (LIT)
and Ba´nbura et al. (2010) (BGR) methods relative to ours.
A value over 1 indicates that our method outperforms the
alternatives. The general ﬁnding is that the performance of
these two approaches is similar, and considerably worse than
our methodology, particularly for forecasting inﬂation.
Finally, note that some authors do not even perform an
informal search for the optimal hyperparameters, but simply
use values from previous studies. For example, a common
choice are the hyperparameters of Sims and Zha (1998),
which are also the values around which we center our
hyperpriors. We have experimented with these ﬁxed hyper-
parameters and, quite interestingly, have found that they
improve over the heuristic procedures of Litterman (1980)
and Ba´nbura et al. (2010), in our empirical application. In
fact, as shown in table 4 (columns SZ), the MSFE is only up
to20percentworsethanourmethodforthesmallandmedium
BVAR, and comparable to our method, if not slightly better,
for the large BVAR.
This result suggests that the overall tightness implied by
the ﬁxed hyperparameters of Sims and Zha (1998) is too low
for the small- and medium-scale VARs, while it is approxi-
mately “correct” for the large VAR. In order to support this
interpretation, we have also experimented with an “extra-
large” VAR model with 35 variables, for which we would
8 Ba´nbura et al. (2010) deﬁne the in-sample ﬁt as the percentage deviation
of the in-sample MSFE from the MSFE of the no-change forecast.
expect the priors of Sims and Zha (1998) to be too loose.9
In line with this intuition, the forecasting performance of the
BVAR of Sims and Zha (1998) deteriorates relative to ours.
In particular, it becomes marginally worse (between 2 and 4
percentage across variables) at the one-quarter horizon and
sensibly worse at the one-year horizon especially for the fed-
eral funds rate and the GDP deﬂator (with an 11 percentage
and a 29 percentage higher MSFE, respectively).
In addition, it is worth noticing that the speciﬁc values
of the hyperparameters that Sims and Zha (1998) used are
not guaranteed to work well for other applications—possibly
outside the range of U.S. macroeconomic time series—and
cannot be applied to different priors. On the contrary, the
main appeal of our methodology is that it can be used in a
wide range of models and applications, requiring little human
judgement in the search for reasonable ranges of hyperpa-
rameters. Consequently, there is also less need for extensive
robustness checks that characterize empirical works using
more ad hoc methodologies.
V.
Structural BVARs and Estimation of Impulse
Response Functions
The forecast accuracy of the hierarchical modeling pro-
cedure proposed in this paper is quite remarkable and in
line with the interpretation of the marginal likelihood as a
measure of out-of-sample forecasting performance. How-
ever, VARs are used in the literature not only for forecasting
but also as a tool to identify structural shocks and assess their
transmission mechanism. Inspired by an important insight of
statistical decision theory—the separation between loss func-
tions and probability models—we now present evidence that
the same hierarchical modeling strategy also delivers accu-
rate estimates of the impulse response functions to structural
shocks.
More speciﬁcally, in this section, we perform two exer-
cises. First, we estimate the impulse responses to monetary
policy shocks using our large-scale BVAR with 22 variables,
9 The extra-large model is constructed by adding the following thirteen
variables to the large VAR: real durable consumption, total housing starts,
purchasing managers index (PMI), new orders of consumer goods and mate-
rials, real exports, real imports, exports price index, imports price index,
unemployment rate, Moody’s AAA corporate bond yields, Moody’s BAA
corporate bond yields, business loans, and consumer credit outstanding.
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 10

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
445
Figure 2.—Impulse Responses of Real Variables
RGDP
0
5
10
15
20
−1
−0.5
0
Cons
0
5
10
15
20
−1
−0.5
0
Real Comp/Hour
0
5
10
15
20
−1
−0.5
0
Emp: total
0
5
10
15
20
−1
−0.5
0
Emp: services
0
5
10
15
20
−1
−0.5
0
Emp. Hours
0
5
10
15
20
−1
−0.5
0
IP: total
0
5
10
15
20
−1
−0.5
0
Capacity Util
0
5
10
15
20
−1
−0.5
0
Consumer expect
0
5
10
15
20
−2
0
2
Res.Inv
0
5
10
15
20
−3
−2
−1
0
1
NonResInv
0
5
10
15
20
−3
−2
−1
0
1
The ﬁgure reports the 16th, 50th, and 84th percentiles (dashed lines) of the distribution of the impulse response functions of the large BVAR to a 1 standard deviation monetary policy shock. The gray area refers to
the corresponding error bands for the ﬂat-prior VAR.
estimated over the entire available sample. The analysis of the
effects of monetary policy innovations is widespread in the
literature because, among other things, it allows discriminat-
ing between competing theoretical models of the economy
(Christiano, Eichenbaum, & Evans, 1999). The purpose of
this ﬁrst exercise is to demonstrate that our hierarchical pro-
cedure allows us to obtain plausible estimates of impulse
response functions even when working with large-scale mod-
els, which is not the case for ﬂat-prior VARs. However,
we do not have an observable counterpart of these impulse
responses in the data that can be used to directly check their
accuracy. This motivates our second exercise, a controlled
Monte Carlo experiment. In a nutshell, we simulate artiﬁ-
cial data sets from a dynamic stochastic general equilibrium
(DSGE) model and assess the gains in accuracy for the esti-
mation of impulse responses to monetary policy shocks of
our hierarchical procedure over ﬂat-prior VARs.
Concerning our ﬁrst exercise, the monetary policy shock is
identiﬁed using a relatively standard recursive identiﬁcation
scheme, assuming that prices and real activity do not react
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 11

446
THE REVIEW OF ECONOMICS AND STATISTICS
Figure 3.—Impulse Responses of Nominal Variables
PGDP
0
5
10
15
20
−1
−0.8
−0.6
−0.4
−0.2
0
0.2
CPI−ALL
0
5
10
15
20
−1
−0.8
−0.6
−0.4
−0.2
0
0.2
PCED
0
5
10
15
20
−1
−0.8
−0.6
−0.4
−0.2
0
0.2
PGPDI
0
5
10
15
20
−1.4
−1.2
−1
−0.8
−0.6
−0.4
−0.2
0
0.2
Com: spot price (real)
0
5
10
15
20
−3
−2.5
−2
−1.5
−1
−0.5
0
0.5
The ﬁgure reports the 16th, 50th, and 84th percentiles (dashed lines) of the distribution of the impulse response functions of the large BVAR to a 1 standard deviation monetary policy shock. The gray area refers to
the corresponding error bands for the ﬂat-prior VAR.
contemporaneously to the monetary policy shock. The only
variables that can react contemporaneously to monetary pol-
icy shocks are the ﬁnancial variables (bond rates and stock
prices), the exchange rate, and M2, while the policy rate does
notreactcontemporaneouslytoﬁnancialvariables(seeChris-
tiano et al., 1999). Figures 2, 3, and 4 report the median and
the 16th and 84th percentiles of the posterior distribution of
the impulse responses to a monetary policy shock estimated
in the large-scale model, using the full sample. The distribu-
tion of the impulse responses encompasses both uncertainty
on the parameters and hyperparameters.
A 1-standard deviation (approximately 60 basis points)
exogenous increase in the federal funds rate generates a
substantial contraction in GDP, employment, and all other
variables related to economic activity. Monetary aggregates
also decrease on impact, indicating strong liquidity effects.
Moreover, stock prices decline, the exchange rate appreci-
ates, and the yield curve ﬂattens. Prices decrease with a delay.
Notice that with the exception of the CPI, the response of
prices does not exhibit the so-called price puzzle, that is, a
counterintuitive positive response to a monetary contraction,
which is instead typical of VARs with small information sets
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 12

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
447
Figure 4.—Impulse Responses of Financial Variables
FedFunds
5
10
15
20
−0.2
0
0.2
0.4
0.6
1 yr T−bond
5
10
15
20
−0.2
0
0.2
0.4
0.6
5 yr T−bond
5
10
15
20
−0.2
0
0.2
0.4
0.6
S&P 500
5
10
15
20
−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
Ex rate: avg
5
10
15
20
0
0.5
1
1.5
2
M2
5
10
15
20
−1
−0.5
0
0.5
1
The ﬁgure reports the 16th, 50th, and 84th percentiles (dashed lines) of the distribution of the impulse response functions of the large BVAR to a 1 standard deviation monetary policy shock. The gray area refers to
the corresponding error bands for the ﬂat-prior VAR.
(on this point, see Sims, 1992b; Bernanke, Boivin, & Eliasz,
2005; Ba´nbura et al., 2010).
For comparison, ﬁgures 2, 3, and 4 also report the corre-
sponding quantiles of the distribution of impulse responses
of a VAR estimated with ﬂat priors (gray shaded areas). It is
evident that these error bands reﬂect a considerable amount
of estimation uncertainty, and their width does not allow any
meaningful conclusions about the effects of an exogenous
monetary tightening. In addition, even when initially signif-
icant, these impulse responses tend to revert to 0 at a very
fast pace, a symptom of a possibly severe small-sample bias
toward stationarity. These results are all in line with intuition,
and hence lend support to our hierarchical procedure. But
there is no formal way to assess the accuracy of this estima-
tion, since there is no counterpart of these responses directly
observable in the data. This is why we now turn to our second
exercise.
In our controlled Monte Carlo experiment, we adopt
a medium-scale DSGE model to simulate 500 artiﬁcial
time series of length of 200 quarters, for seven macrovari-
ables: output (Y), consumption (C), investment (I), hours
worked (H), wages (W), prices (P), and the short-term inter-
est rate (R). For each data set, we estimate the impulse
responses to a monetary policy shock with our hierarchical
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 13

448
THE REVIEW OF ECONOMICS AND STATISTICS
Figure 5.—Impulse Responses on Simulated Data
0
5
10
15
20
−0.25
−0.2
−0.15
−0.1
−0.05
0
Y
DSGE
BVAR
VAR
0
5
10
15
20
−0.1
−0.05
0
C
0
5
10
15
20
−0.8
−0.6
−0.4
−0.2
0
I
0
5
10
15
20
−0.25
−0.2
−0.15
−0.1
−0.05
0
H
0
5
10
15
20
−0.25
−0.2
−0.15
−0.1
−0.05
0
W
0
5
10
15
20
−0.25
−0.2
−0.15
−0.1
−0.05
0
P
0
5
10
15
20
0
0.2
0.4
0.6
0.8
R
The ﬁgure reports the impulse responses to a monetary policy shock in the DSGE model used to generate the data and the median across Monte Carlo replications of the BVAR and the VAR impulse responses.
BVAR model and a ﬂat-prior VAR and compare these
estimates to the true impulse responses of the theoretical
model.
The DSGE that we use to simulate the data is identical to
Justiniano, Primiceri, and Tambalotti (2010), with the excep-
tion that the behavior of the private sector is predetermined
with respect to the monetary policy shock, as in Christiano
et al. (2005). This justiﬁes the use of a recursive scheme for
the identiﬁcation of monetary policy shocks in the BVAR
and the VAR. Finally, the DSGE is parameterized using the
posterior mode of the unknown coefﬁcients, estimated using
U.S. data on output growth, consumption growth, investment
growth, hours, wage inﬂation, price inﬂation, and the federal
funds rate, as in Justiniano et al. (2010). This is a good lab-
oratory to study the question at hand, since it is well known
that this class of medium-scale DSGE models ﬁts the data
quite well (Smets & Wouters, 2007).
Figure 5 reports the theoretical DSGE impulse responses
to a monetary policy shock (solid line) and the average across
replications of the median responses using our hierarchi-
cal procedure (dashed line) and the ﬂat-prior VAR (dotted
line). Both the BVAR and the VAR responses replicate the
shape of the true impulse responses quite well. In general,
the bias introduced by using an informative prior is not
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 14

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
449
Figure 6.—Ratio of MSE: VAR versus BVAR
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
Y
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
C
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
I
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
H
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
W
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
P
0
5
10
15
20
0
0.5
1
1.5
2
2.5
3
R
The ﬁgure reports the ratio of the MSE of the VAR over the MSE of the BVAR. Values larger than 1 indicate that the MSE of the VAR is larger than that of the BVAR.
substantially larger than the small sample bias of the ﬂat-prior
VAR.10
However, the difference between the average median
across replications and the theoretical impulse response, the
bias, represents only one dimension of accuracy. In order to
take into account the standard deviation of the errors across
replications, we need to look at the average squared error
across replications.
10 We have also computed the impulse responses to a monetary policy
shock in the theoretical VAR(5) representation of the DSGE model. These
responses are extremely similar to the DSGE responses.
For each replication, we compute the overall error as the
difference between the theoretical response and the estimated
median response across variables and horizons. Then, for
each variable and horizon, we take the average of the squared
errors across replications (MSE). Figure 6 reports the ratio
between the MSE for the ﬂat-prior VAR and the hierarchical
BVAR.
Such a ratio is greater than 1 for most variables and hori-
zons, indicating that the hierarchical BVAR yields substantial
accuracy gains. For instance, depending on the horizon,
the impulse responses of output, consumption, investment,
hours, and wages based on the BVAR can be about twice as
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 15

450
THE REVIEW OF ECONOMICS AND STATISTICS
accurate. An important exception is the response of the fed-
eral funds rate, which is estimated to be too persistent and to
decay too slowly when using informative priors (see ﬁgures 5
and 6). Further experimentation reveals that this excessively
persistent behavior is due to the sum-of-coefﬁcients prior.
While this prior is very important to enhance the forecast-
ing performance of the model, the outcomes in ﬁgures 5 and
6 suggest that more sophisticated priors might be needed to
discipline the behavior of the model at low frequencies. It is
also reasonable to expect that these more sophisticated priors
should be based on insights coming from economic theory
(on this point, see, Del Negro & Schorfheide, 2004; Villani,
2009), since it is well known that the data are less informative
about low-frequency trends.
VI.
Conclusion
In this paper, we have studied the problem of how to
choose the informativeness of a variety of commonly used
prior distributions for VAR models. Our approach con-
sists of treating the coefﬁcients of the prior as additional
parameters, in the spirit of hierarchical modeling. We have
shown that this approach is theoretically grounded, easy
to implement, and performs very well in terms of out-of-
sample forecasting and accuracy in the estimation of impulse
response functions. Moreover, it greatly reduces the num-
ber and importance of subjective choices in the setting of
the prior. In sum, this hierarchical modeling procedure is
beneﬁcial for both reduced-form and structural analysis with
VARs. Moreover, this approach may prove particularly use-
ful also for the increasingly large literature on DSGE models.
It is in fact typical in this literature to validate a theoretical
model by comparing its ﬁt and impulse responses to those of
VARs.
REFERENCES
Amisano, G., and R. Giacomini, “Comparing Density Forecasts via
Weighted Likelihood Ratio Tests,” Journal of Business and Eco-
nomic Statistics 25 (2007), 177–190.
Atkeson, A., and L. E. Ohanian, “Are Phillips Curves Useful for Forecasting
Inﬂation?” Quarterly Review, Federal Reserve Bank of Minneapolis
(Winter), 2–11.
Ba´nbura, M., D. Giannone, and L. Reichlin, “Large Bayesian VARs,”
Journal of Applied Econometrics 25 (2010), 71–92.
Belmonte, M., G. Koop, and D. Korobilis, “Hierarchical Shrinkage in
Time-Varying Parameter Models,” Journal of Forecasting 33 (2014),
80–94.
Berger, J. O., Statistical Decision Theory and Bayesian Analysis (Berlin:
Springer-Verlag, 1985).
Berger, J. O., and L. Berliner, “Robust Bayes and Empirical Bayes Anal-
ysis with # -Contaminated Priors,” Annals of Statistics 14 (1986),
461–486.
Berger, J. O., W. Strawderman, and T. Dejung, “Posterior Property and
Admissibility of Hyperpriors in Normal Hierarchical Models,”
Annals of Statistics 33 (2005), 606–646.
Bernanke, B., J. Boivin, and P. S. Eliasz, “Measuring the Effects of Mon-
etary Policy: A Factor-Augmented Vector Autoregressive (FAVAR)
Approach,” Quarterly Journal of Economics 120 (2005), 387–422.
Bloor, C., and T. Matheson, “Real-Time Conditional Forecasts with
Bayesian VARs: An Application to New Zealand,” North American
Journal of Economics and Finance 22 (2011), 26–42.
Canova, F., Methods for Applied Macroeconomic Research (Princeton, NJ:
Princeton University Press, 2007).
Carriero, A., T. Clark, and M. Marcellino, “Bayesian VARs: Speciﬁcation
Choices and Forecast Accuracy,” Federal Reserve Bank of Cleveland
working paper 1112 (2011).
Carriero, A., G. Kapetanios, and M. Marcellino, “Forecasting Exchange
Rates with a Large Bayesian VAR,” International Journal of
Forecasting 25 (2009), 400–417.
——— “Forecasting Government Bond Yields,” CEPR discussion papers
7796 (2010).
Christiano, L. J., M. Eichenbaum, and C. L. Evans, “Monetary Policy
Shocks: What Have We Learned and to What End?” (pp. 65–
148), in by J. B. Taylor and M. Woodford, eds., Handbook of
Macroeconomics (New York: Elsevier, 1999).
——— “Nominal Rigidities and the Dynamic Effects of a Shock to
Monetary Policy,” Journal of Political Economy 113 (2005), 1–45.
De Mol, C., D. Giannone, and L. Reichlin, “Forecasting Using a Large
Number of Predictors: Is Bayesian Shrinkage a Valid Alternative
to Principal Components?” Journal of Econometrics 146 (2008),
318–328.
Del Negro, M., and F. Schorfheide, “Priors from General Equilibrium
Models for VARS,” International Economic Review 45 (2004),
643–673.
——— “Bayesian Macroeconometrics” (pp. 293–389), in J. Geweke,
G. Koop, and H. van Dijk, eds., The Oxford Handbook of Bayesian
Econometrics (New York: Oxford University Press, 2011).
Del Negro, M., F. Schorfheide, F. Smets, and R. Wouters, “On the Fit of New
Keynesian Models,” Journal of Business and Economic Statistics 25
(2007), 123–143.
Doan, T., R. Litterman, and C. A. Sims, “Forecasting and Conditional Pro-
jection Using Realistic Prior Distributions,” Econometric Reviews 3
(1984), 1–100.
Forni, M., M. Hallin, M. Lippi, and L. Reichlin, “The Generalized
Dynamic Factor Model: Identiﬁcation and Estimation,” this review
82 (2000), 540–554.
Gelman, A., J. B. Carlin, H. S. Stern, and D. B. Rubin, Bayesian Data
Analysis, 2nd ed. (Boca Raton, FL: Chapman and Hall CRC, 2004).
Geweke, J., “Bayesian Econometrics and Forecasting,” Journal of Econo-
metrics 100 (2001), 11–15.
Geweke, J., and C. Whiteman, “Bayesian Forecasting” (pp. 3–80), in
G. Elliott, C. Granger, and A. Timmermann, eds., Handbook of
Economic Forecasting (New York: Elsevier, 2006).
Giannone, D., M. Lenza, D. Momferatou, and L. Onorante “Short-Term
Inﬂation Projections: A Bayesian Vector Autoregressive approach,”
International Journal of Forecasting 30 (2014), 635–644.
Giannone, D., M. Lenza, and L. Reichlin, “Explaining the Great Moder-
ation: It Is Not the Shocks,” Journal of the European Economic
Association 6 (2008), 621–633.
Jarocinski, M., and A. Marcet, “Autoregressions in Small Samples, Pri-
ors about Observables and Initial Conditions,” ECB working paper
series 1263 (2010).
Justiniano, A., G. E. Primiceri, and A. Tambalotti, “Investment Shocks
and Business Cycles,” Journal of Monetary Economics 57 (2010),
132–145.
Kadiyala, K. R., and S. Karlsson, “Numerical Methods for Estima-
tion and Inference in Bayesian VAR-Models,” Journal of Applied
Econometrics 12 (1997), 99–132.
Karlsson, S., “Forecasting with Bayesian Vector Autoregressions,” Ore-
bro University, Swedish Business School working papers 2012:12
(2012).
Knox, T., J. H. Stock, and M. W. Watson, “Empirical Bayes Forecasts
of One Time Series Using Many Predictors,” Econometric Society
World Congress 2000 contributed papers 1421 (2000).
Koop, G., Bayesian Econometrics (Chichester: John Wiley, 2003).
——— “Forecasting with Medium and Large Bayesian VARs,” Journal of
Applied Econometrics 28 (2013), 177–203.
Koop, G., and D. Korobilis, “Bayesian Multivariate Time Series Meth-
ods for Empirical Macroeconomics,” Foundations and Trends in
Econometrics 3 (2010), 267–358.
Korobilis,D.,“HierarchicalShrinkagePriorsforDynamicRegressionswith
Many Predictors,” International Journal of Forecasting 29 (2013),
43–59.
Litterman, R., “Techniques of Forecasting Using Vector Autoregressions,”
Federal Reserve of Minneapolis working paper 115 (1979).
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026

## Page 16

PRIOR SELECTION FOR VECTOR AUTOREGRESSIONS
451
——— “A Bayesian Procedure for Forecasting with Vector Autoregres-
sion,” MIT, Department of Economics working paper (1980).
——— “Forecasting with Bayesian Vector Autoregressions: Five Years of
Experience,” Journal of Business and Economic Statistics 4 (1986),
25–38.
Lopes, H. F., A.R.B. Moreira, and A. M. Schmidt, “Hyperparameter Esti-
mation in Forecast Models,” Comput. Stat. Data Anal. 29 (1999),
387–410.
Ni, S., and D. Sun, “Noninformative Priors and Frequentist Risks of
Bayesian Estimators of Vector-Autoregressive Models,” Journal of
Econometrics 115 (2003), 159–197.
Phillips, P. C., “Automated Forecasts of Asia-Paciﬁc Economic Activity,”
Cowles Foundation discussion papers (1995).
Phillips, P. C., and W. Ploberger, “Posterior Odds Testing for a Unit Root
with Data-Based Model Selection,” Econometric Theory 10 (1994),
774–808.
Primiceri, G. E., “Time Varying Structural Vector Autoregressions
and Monetary Policy,” Review of Economic Studies 72 (2005),
821–852.
Robbins, H., “An Empirical Bayes Approach to Statistics” (pp. 157–163),
in Proceedings of the Third Berkeley Symposium on Mathematical
Statistics and Probability, Vol. 1: Contributions to the Theory of
Statistics (Berkely: Univeristy of California Press, 1956).
Robertson, J. C., and E. W. Tallman, “Vector Autoregressions: Forecasting
and Reality,” Economic Review, issue Q1 (1999), 4–18.
Sims, C. A., “Macroeconomics and Reality,” Econometrica 48 (1980),
1–48.
Sims, C. A. “Bayesian Inference for Multivariate Time Series with Trend,”
Princeton University mimeograph (1992a).
——— “Interpreting the Macroeconomic Time Series Facts: The Effects
of Monetary Policy,” European Economic Review 36 (1992b), 975–
1000.
——— “A Nine-Variable Probabilistic Macroeconomic Forecasting
Model” (pp. 179–212), in James H. Stock and Mark W. Watson,
eds., Business Cycles, Indicators and Forecasting (Cambridge, MA:
National Bureau of Economic Research, 1993).
Sims, C. A., and T. Zha, “Bayesian Methods for Dynamic Multivariate
Models,” International Economic Review 39 (1998), 949–968.
Smets, F., and R. Wouters, “Shocks and Frictions in US Business Cycles: A
Bayesian DSGE Approach,” American Economic Review 97 (2007),
586–606.
Stein, C., “Inadmissibility of the Usual Estimator for the Mean of a
Multivariate Normal Distribution” (pp. 197–206), in Proc. Third
Berkeley Symp. on Math. Statist. and Prob. (Berkeley: University of
California, 1956).
Stock, J. H., and M. W. Watson, “Forecasting Using Principal Compo-
nents from a Large Number of Predictors,” Journal of the American
Statistical Association 97 (2002a), 147–162.
——— “Macroeconomic Forecasting Using Diffusion Indexes,” Journal of
Business and Economics Statistics 20 (2002b), 147–162.
——— “Forecasting in Dynamic Factor Models Subject to Structural Insta-
bility,” in J. Castle and N. Shephard, eds., The Methodology and
Practice of Econometrics, A Festschrift in Honour of Professor
David F. Hendry (New York: Oxford University Press, 2008).
Villani, M., “Steady-State Priors for Vector Autoregressions,” Journal of
Applied Econometrics 24 (2009), 630–650.
Wright, J. H., “Forecasting US Inﬂation by Bayesian Model Averaging,”
Journal of Forecasting 28 (2009), 131–144.
Downloaded from http://direct.mit.edu/rest/article-pdf/97/2/436/1917922/rest_a_00483.pdf by University of Toronto user on 20 May 2026
