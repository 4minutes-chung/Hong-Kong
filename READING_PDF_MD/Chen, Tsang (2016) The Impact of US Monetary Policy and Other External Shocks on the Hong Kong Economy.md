# Chen, Tsang (2016) The Impact of US Monetary Policy and Other External Shocks on the Hong Kong Economy

## Page 1

Electronic copy available at: http://ssrn.com/abstract=2797976 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
HONG KONG INSTITUTE FOR MONETARY RESEARCH 
THE IMPACT OF US MONETARY POLICY AND 
OTHER EXTERNAL SHOCKS ON THE HONG 
KONG ECONOMY: A FACTOR-AUGMENTED VAR 
APPROACH 
Hongyi Chen and Andrew Tsang 
HKIMR Working Paper No.09/2016 
 
June 2016 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 2

Electronic copy available at: http://ssrn.com/abstract=2797976 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Hong Kong Institute for Monetary Research 
香港金融研究中心 
(a company incorporated with limited liability) 
 
All rights reserved. 
Reproduction for educational and non-commercial purposes is permitted provided that the source is acknowledged. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 3

The Impact of US Monetary Policy and Other External Shocks on 
the Hong Kong Economy: A Factor-augmented VAR Approach 
 
Hongyi Chen* 
Hong Kong Institute for Monetary Research 
 
and 
 
Andrew Tsang** 
Hong Kong Institute for Monetary Research 
 
June 2016 
 
 
Abstract 
 
 
This paper uses the factor-augmented VAR (FAVAR) framework to study the impact on the Hong Kong 
economy of the diverging monetary policies by the Fed, ECB and BoJ as well as the Mainland 
economy slowdown. The empirical results show that changes in US monetary policy mainly affect 
interest rate-sensitive sectors in Hong Kong; while real variables such as real GDP growth, 
unemployment rate are more sensitive to the economic slowdown in Mainland China. Monetary easing 
from the ECB and BoJ to some extent offsets the tightening of the Fed. The transmission channels of 
external shocks are through trade and capital markets. It is estimated that the combined effect of the 
four external shocks will on average lower Hong Kong’s quarterly GDP growth by 0.6 percentage 
points and quarterly inflation by 0.2 percentage points in the first 4 quarters. However, Hong Kong’s 
financial stability, particularly with regard to loan quality, banks’ capital and liquidity, is well maintained 
by macroprudential policies suggesting that Hong Kong’s financial system is resilient to external 
shocks. 
 
JEL classification: C3, E5, E3  
 
Keywords: Hong Kong economy, monetary policy, factor-augmented VAR 
                                                     
* Email address: hchen@hkma.gov.hk 
** Email address: ahctsang@hkma.gov.hk 
The views expressed in this paper are those of the authors, and do not necessarily reflect those of the Hong Kong Institute for 
Monetary Research, its Council of Advisers, or the Board of Directors. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 4

1 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
1. 
Introduction 
Hong Kong as a small open economy has been greatly affected by global shocks. With the linked 
exchange rate system and free capital mobility, Hong Kong essentially adopts the Fed’s monetary 
policy. Changes in the Fed’s monetary policy will affect different sectors of the Hong Kong economy. As 
an international financial center with open capital markets, the monetary policies of other major central 
banks also have an impact. It is likely that monetary policies among the major central banks will 
diverge over the next few years with the US Fed expected to tighten but the ECB and BoJ maintaining 
a looser monetary stance, which will have differential effects on the Hong Kong economy. Hong Kong’s 
real sector is also closely connected to Mainland China, and the growth slowdown of Mainland China 
will also have serious impact on Hong Kong. 
 
This paper studies how external shocks are transmitted to the different sectors of the Hong Kong 
economy. Specifically, this paper attempts to address the following questions:  
 
How the changes in the Fed’s monetary policy are transmitted to different sectors of the Hong Kong 
economy, especially the financial sector and real estate sector? With several rounds of large scale 
quantitative easing (QE) by the Fed, how is Hong Kong’s financial stability affected?  
 
With the coming divergence of monetary policies among major global central banks, what will be the 
overall impact on the Hong Kong economy, especially the exchange rate? What is the combined effect 
of diverging monetary policies across the world on the Hong Kong economy and its financial stability?  
 
How will the growth slowdown of Mainland China affect the Hong Kong economy? How will it add to the 
effects of diverging monetary policies?  
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 5

2 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Vector autoregression (VAR) is a typical method to study the impact of monetary policy changes on 
macroeconomic variables. However, because of a degrees of freedom problem, only a small number 
of macroeconomic variables can be included in a VAR. Therefore standard VAR analysis can only 
evaluate the impact of monetary policy changes on the included variables. In order to analyze the large 
number of data series available, Bernanke et al. (2005) suggests a factor-augmented vector 
autoregression (FAVAR) approach, which can incorporate a larger amount of information in a 
comprehensive analysis.  
 
FAVAR is able extract a few factors from a large number of data series and estimate a VAR system 
using the extracted factors together with a few observable variables. The observable variables could 
be monetary policy shocks or Mainland China’s GDP growth indicator. Through an impulse response 
analysis, it can show the dynamic responses of the factors to external shocks allowing the researcher 
to back out the dynamic response of the original data series to external shocks. The main advantage of 
FAVAR is that it can incorporate a large data set without having to make choices about which data 
series should be included in a VAR system, and the dynamic responses of all the data series can be 
backed out. The factors extracted can be used to represent abstract concepts such real activity, 
financial stability, etc. Therefore it is an ideal framework for a comprehensive analysis of the impact of 
monetary policy changes on different sectors of an economy. The impact of external shocks can be 
analysed individually or in the aggregate.   
 
Two approaches have been suggested in the literature to estimate the FAVAR. The first approach is a 
two-step approach. This approach first extracts the factors from the large data set through principal 
component analysis and then selects the main factors to include in the VAR system together with 
shock variables. The second approach is a likelihood-based Gibbs sampling approach. This approach 
has to assume independent normal errors and uses the Bayesian method to estimate coefficients in 
one step. It is computationally more demanding. In this paper, we mainly use the principal component 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 6

3 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
approach (two-step approach) but use the Gibbs sampling approach (single-step approach) for 
robustness check.  
 
Given that Hong Kong is a small open economy with the Hong Kong dollar pegged to the US dollar 
under a currency board system, the monetary policy shocks of the Fed can be considered exogenous. 
The same is true for the monetary policy shocks of ECB and BoJ and the economic slowdown in 
Mainland China. Therefore it is arguably true that a VAR might not be necessary because Hong Kong’s 
economic variables would not be able to affect the shock variables. However, in order to analyze the 
dynamic impact of external shocks, a VAR is the most appropriate framework. To take into 
consideration the exogeneity of these external shocks, in the following FAVAR analysis, we put zero 
restrictions on the FAVAR coefficients to rule out feedback effects (it is worth noting at this point, that 
the results do not change if these restrictions are relaxed1). As a robustness check, we also run a 
standard VAR to compare the empirical results. 
 
The main findings of this paper are the following. The impact of US monetary policy on the Hong Kong 
economy is mainly on interest rate sensitive sectors, for instance, the property sector, Hang Seng 
Index and Hong Kong dollar effective exchange rate. This shows that the market has confidence on 
Hong Kong’s linked exchange rate system. The real sector is mainly influenced by the business cycle 
of Mainland China. Quantitative easing (QE) by the ECB and BoJ reinforces appreciation pressures on 
the Hong Kong dollar, however, it neutralizes somewhat capital outflows from a tightening in US 
monetary policy. The additional impact of QE by the ECB and BoJ on the real sector is not obvious. 
Hong Kong’s macroprudential policy measures are shown to be quite effective in defending the 
financial stability of Hong Kong in the context of large scale QEs, and anticipated future divergence in 
the monetary policy stance of the major global central banks.  
 
                                                     
1 The coefficients turn out to be insignificant, which confirms that the spillback effect from the Hong Kong economy is minimal. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 7

4 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
The rest of the paper is organized as follows: Section 2 reviews the literature. Section 3 introduces the 
FAVAR framework and data. Section 4 summarizes the empirical results. Section 5 provides a 
robustness check. Section 6 concludes. 
 
2. 
Literature Review 
This paper follows two strands of literature on the international transmission of shocks. The first line of 
literature is on how external shocks from the US or Mainland China transmit to Hong Kong. He, Liao 
and Wu (2014) study Hong Kong’s business cycle synchronisation with the US and China, and find that 
Hong Kong’s short run business cycle is more synchronised with the US but that its long run growth 
co-moves with that of Mainland China. He, Wong, Tsang and Ho (2015) study how asynchronous 
monetary policies are transmitted through the supply of international dollar credit by a global bank and 
find that the bank’s risk-taking attitude, credit risk exposure and the business model of their overseas 
branches are important factors affecting the extent to which unconventional monetary policies are 
transmitted internationally. N’Diaye and Ahuja (2012) attempt to quantify the trade and financial 
spillovers on the Hong Kong economy from a growth slowdown in the euro area and Mainland China, 
and find that Hong Kong’s output growth could fall by as much as 1.5 times the decline in euro area 
output growth. In the event of a hard landing in China, Hong Kong’s output growth could fall by about 3 
percentage points below its baseline in the first two years.  
 
The second line of literature is the FAVAR literature. Since Bernanke, Boivin and Ellasz (2005) 
popularized the FAVAR method, a large literature has developed using the FAVAR to study the 
transmission of monetary shocks both domestically and internationally. Ho, Zhang and Zhou (2014) 
used FAVAR to study how quantitative easing (QE) by the Fed spills over to China through hot money 
inflows, and finds that the decline in the US policy rate has led to a significant increase in China’s 
regulated interest rates and housing investment. Fernald, Spiegel and Swanson (2014) use FAVAR to 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 8

5 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
study the effectiveness of China’s monetary policy and find that interest rate channel is gaining in 
importance. Mumtaz and Surico (2009) used FAVAR to study the transmission of international shocks. 
Zuniga (2011) uses FAVAR to study the US monetary policy transmission to Mexico and Brazil, and 
finds that the interest rate is the main transmission channel and has some impact via a trade channel. 
Dahlhaus, Hess and Reza (2014) use FAVAR to study the US monetary policy transmission to the 
Canadian economy and finds that QE by the Fed boosts Canadian output, mainly through a financial 
channel. Finally Belviso and Milani (2006) develop a structural FAVAR to help interpret factors 
extracted from a large data set, and use the framework to study the effects of monetary policy on a 
wide range of macroeconomic variables.  
 
This paper contributes to the literature in the following two ways. First, it is the first paper to analyze the 
dynamic impact of external shocks on a wide range of different sectors of the Hong Kong economy, 
whereas the literature usually focuses on one or two macroeconomic variables only. Second, it 
analyses the combined effect of monetary policy shocks arising from changes in the stance of the 
major central banks and a slowdown in the economy of Mainland China, in contrast to the FAVAR 
literature which typically focuses on a particular shock. 
 
3. 
Econometric Framework and Data 
The FAVAR framework used in this paper is based on Bernanke, Boivin and Eliasz (2005), which 
combines dynamic factor analysis with VAR analysis.  
 
a. Model Setup 
 
Assume that a large number of observable macroeconomic variables of an economy are driven by a 
few common factors, which are not observable, and external shocks, which are observable, with the 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 9

6 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
following measurement equation:  
 
 
 
𝑿𝒕= 𝚲𝒓𝑹𝒕+ 𝚲𝒇𝑭𝒕+ 𝜺𝒕 
 
(1) 
 
where Xt is a 𝑁 ×  1 vector of observable macroeconomic variables, Rt is an 𝑀 ×  1 vector of 
observable shock variables, which could include external shocks, like measures of the monetary policy 
stance. 𝚲𝒓 is a 𝑁 ×  𝑀 matrix of coefficients. Ft is a 𝐾 ×  1 vector of unobservable common factors. 
The number of factors (K) is much smaller than N, usually ranges from 3 to 5. 𝚲𝒇 is a 𝑁 ×  𝐾 matrix 
of factor loadings. 𝜺𝒕 is a 𝑁 ×  1 vector of idiosyncratic (series-specific) shocks. Suppose the 
dynamics of (Rt, Ft,) is given by a VAR 
 
[𝑹𝒕
𝑭𝒕] = 𝜱(𝑳) [𝑹𝒕−𝟏
𝑭𝒕−𝟏] + 𝜼𝒕 
 
(2) 
 
where 𝛷(𝐿) is a lag polynomial of finite order as in standard VAR, and the error term 𝜼𝒕 is i.i.d. with 
mean zero. 
 
This paper will start by including a single measure of the US monetary policy stance in Rt to evaluate 
the impact of US monetary policy changes on the Hong Kong economy. Besides being affected by US 
monetary policy, the Hong Kong economy is also influenced by the monetary policies of other major 
central banks such as the ECB and BoJ, and economic growth in Mainland China. The paper then 
examines the effects of individual shocks such as monetary policy changes by the  ECB and BoJ, and 
an economic slowdown in Mainland China. To see the combined effect of monetary policies of the Fed, 
ECB and BoJ and changes in economic growth in Mainland China, the analysis is extended to include 
measures of the monetary policy stance in the Euro Area and Japan and Mainland China GDP growth 
in Rt. Since financial stability and capital flows have been a major concern to policy makers in Hong 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 10

7 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Kong, this paper also studies the impact of diverging monetary policies among the major global central 
banks and a Mainland China economic slowdown on these two areas by including measures of 
financial stability and capital flows in the vector of Xt. 
 
To take into consideration that Hong Kong is a small open economy, which does not have much 
influence on the decisions of monetary policies of major central banks, we restrict the VAR by putting a 
block of zeros in the coefficient matrix to rule out feedback effects, which is similar to the setting in 
Dahlhaus, Hess and Reza (2014).2 Therefore, the dynamics of (Rt, Ft,) is specified as the following 
with Rt ordered first, which shows that Ft does not affect Rt contemporaneously. We identify the model 
following the standard Cholesky decomposition.3  
 
[𝑹𝒕
𝑭𝒕] = ⌈𝒃𝟏𝟏(𝑳)
𝟎
𝒃𝟐𝟏(𝑳)
𝒃𝟐𝟐(𝑳)⌉[𝑹𝒕−𝟏
𝑭𝒕−𝟏] + 𝜼𝒕 
 
(3) 
 
b. Estimation 
 
The above FAVAR framework can be estimated by two approaches; a two-step (principal component) 
approach and a single-step (Bayesian likelihood/Gibb sampling) approach. According to Bernanke, 
Boivin and Eliasz (2005), these two approaches produce qualitatively similar results. For the two-step 
(principal component) approach, the first step involves extracting principal components from the large 
dataset Xt to obtain consistent estimates of common factors (𝑭𝒕).4 Given that a US monetary policy 
shock is an external shock to Hong Kong economy, this paper, in contrast to Bernanke, Boivin and 
Eliasz (2005), does not separate the macroeconomic variables into fast- and slow-moving variables.5  
                                                     
2 The result does not change if this restriction is relaxed. 
3 The combination of block of zeros restriction and applying Cholesky decomposition could restrict the US monetary policy 
shock and other external shocks to be completely exogenous from the perspective of Hong Kong. 
4 The data need to be standardized when obtaining the principal component analysis. 
5 Bernanke, Boivin and Eliasz (2005) introduced the classification of fast- and slow-moving variables (the former are assumed to 
respond to external shock contemporaneously, while the latter are not) because the estimated common factors (𝑭̂𝒕) include the 
effects of Rt, hence they are correlated with variables in Rt. Given that the VAR in the second step uses recursive ordering, the 
estimated common factors (𝑭̂𝒕) and the shock variables (Rt) are required to have no direct dependence. So Bernanke, Boivin 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 11

8 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
In the second step, equation (3) is estimated by a standard VAR method, with the estimates of 𝑭𝒕 The 
VAR system is identified using a Cholesky decomposition. The variables in the system are recursively 
ordered with the US monetary policy shock or other external shocks ordered before the factors to 
reflect the assumption that the Hong Kong economy factors reacts to external shocks in the same 
period, but not vice versa. 
 
Alternatively, the FAVAR can be estimated using a single-step (Gibb sampling) approach. That is, 
equations (1) and (3) are jointly estimated by a likelihood-based Gibbs sampling techniques, which is a 
Bayesian method developed by Geman and Geman (1984), with the assumption of independent 
normal errors. However, this approach is computationally very demanding. Some later literature such 
as Boivin et al. (2009) only uses a two-step (principal component) approach, which is computationally 
much simpler and easy to implement. In this paper, we also estimate the model using a single-step 
(Gibb sampling) approach as a robustness check. 
 
Belviso and Milani (2006) argue that factors from a standard FAVAR are not identified and therefore 
lack economic interpretation. They propose a structural FAVAR model, in which they first classified the 
observable macroeconomic and financial variables into I groups by sectors, then for each group of 
variables, one principal component is extracted, thought to be a structural factor. Equation (1) is then 
rewritten in the following way: 
 
[
 
 
 𝑿𝒕
𝟏
𝑿𝒕
𝟐
…
𝑿𝒕
𝑰]
 
 
 
= 𝚲𝒓𝑹𝒕+
[
 
 
 
 𝚲𝟏
𝒇
0
⋯
0
0
𝚲𝟐
𝒇
⋯
0
⋯
⋯
⋯
⋯
0
⋯
⋯
𝚲𝑰
𝒇]
 
 
 
 
[
 
 
 𝑭𝒕
𝟏
𝑭𝒕
𝟐
…
𝑭𝒕
𝑰]
 
 
 
+ 𝜺𝒕  
(4) 
                                                                                                                                                                     
and Eliasz (2005) uses this classification to remove the direct dependence of 𝑭̂𝒕 on policy or external shocks Rt. Since the 
shocks in this paper are external shocks to the Hong Kong economy, such classification is not necessary for the VAR analysis. 
Indeed, the results do no change much if we estimate the VAR equation (3) following the procedure in Bernanke, Boivin and 
Eliasz (2005) by separating the variables into slow-moving or fast-moving categories. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 12

9 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
Where 𝐗𝒕
𝒊 is a 𝑛𝑖 ×  1 matrix of variables in specific group i. The total number of variables is N. 𝑭𝒕
𝒊, is 
a 1 ×  1 vector of unobservable factor extracted from the specific group i, the total number of groups 
is I. 𝚲𝒊
𝒇 is a 𝑛𝑖 ×  1 matrix of factor loadings of the 𝑛𝑖 variables in the group i. 𝜺𝒕 is a 𝑁 ×  1 vector 
of idiosyncratic (series-specific) shocks.  
 
In this way, they claimed that 𝑭𝒕
𝒊 represents a specific sector with clear economic interpretation. 𝑭𝒕
𝒊 is 
used in the dynamic equation. The model is then estimated by a Bayesian approach. In the robustness 
check section of this paper, we estimate a similar structural model, but use the two-step (principal 
components) approach.  
 
c. Data 
 
Similar to Bernanke, Boivin and Eliasz (2005), we collect 116 series on the Hong Kong economy. All 
series are quarterly. The sample period is from 1998 Q4 to 2015 Q1. This is the period for which we 
have a balanced panel of data for all series. All data series are transformed into stationary series and 
seasonally adjusted where necessary. A unique feature of this data set is that we include financial 
stability indicators and capital flow indicators, besides standard macroeconomic series, in order to 
investigate how external shocks affect financial stability in Hong Kong given that Hong Kong is a very 
open economy, and an international financial center with free capital flow. A detailed description of the 
data is in Table 1.  
 
For the external shock variables, we include four indicators. They are monetary policy rate indicators 
for the Fed, ECB and BoJ, and real GDP growth for Mainland China. After the policy rates reached the 
Zero Lower Bound (ZLB), and major central banks started quantitative easing (QE), the actual policy 
rates, which were close to zero failed to be good indicators of the monetary policy stance. In order to 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 13

10 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
measure the monetary policy stance, Wu and Xia (2016) develop a method to calculate a shadow 
federal funds rate series to proxy the Fed’s policy stance after late 2008, when the Fed’s policy rate 
reached ZLB; this series has been updated by the Atlanta Fed. Lombardi and Zhu (2014), Krippner 
(2013) also develop a similar series using his own methods. Indeed, before monetary policy rates 
reached the ZLB, shadow rates and policy rates were similar. In this paper, we use series computed by 
the method of Wu and Xia (2016) for both the US and the ECB’s monetary policy stances.6 The Bank 
of Japan (BoJ) started QE much earlier (March 2001). We use a series computed by the method in 
Krippner (2013) for the BoJ’s monetary policy stance.7 Figure 1 shows the shadow policy rates of 
major central banks. For China’s quarterly GDP series, we use data from CEIC with our own 
calculations to extend the data series.8 
 
4. 
Empirical Results 
 
We present the empirical results by first showing the principal components for the key Hong Kong 
economic variables. It can be seen that these principal components are highly correlated with specific 
sectors of the economy. We then show the impulse responses of 32 major economic variables to an 
individual shock of the change in monetary policy by the US Fed, ECB or BoJ, or a Mainland economy 
slowdown in models with only one shock. We extend the analysis to a full model including all four 
shocks to see the combined impact of diverging monetary policies and a Mainland slowdown on Hong 
Kong economic and financial variables. In the next section, we provide some robustness checks. 
 
                                                     
6 The data can be downloaded from C. Wu’s website: http://faculty.chicagobooth.edu/jing.wu/research/data/WX.html 
7 The shadow rates calculated by Krippner can be downloaded from Krippner’s website: 
http://www.rbnz.govt.nz/research_and_publications/research_programme/additional_research/comparison-of-international-mon
etary-policy-measures.html 
8 Official data for quarterly real GDP level of China started from 2012, and we calculated earlier data by using the series of 
quarterly year-on-year changes of real GDP. Then we apply the seasonal adjustment to the series and calculate the 
quarter-on-quarter change of the seasonally adjusted series. This series is generally in line with the official seasonally adjusted 
quarterly real GDP growth, which started only from 2010. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 14

11 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
a. Principal Components for the Hong Kong economic variables 
 
 
In the two-step approach of FAVAR framework, a small number of factors are extracted from a large 
number of macroeconomic series by principal component analysis.9 In this paper, we extract five 
factors for the FAVAR analysis. These five factors explain around 60% of the variation in our 116 data 
series. Although the factors cannot be identified exactly, from Table 2, we can see the following pattern 
by looking at the correlation of the factors with the actual data series: Factor one is mainly correlated 
with variables related to the property market with a correlation often exceeding 75%. It also correlates 
with variables related to inflation, loans and financial stability. Factor two is highly correlated with 
variables related to real activity, the stock market and financial stability.10 Factor three is highly 
correlated with interest rate variables. Factor four is highly correlated with variables related to the 
exchange rate, interest rates and the stock market. Factor five is highly correlated with variables 
related to the money supply. 
 
b. The US interest rate hike 
 
Figure 2 presents impulse responses of 32 selected major Hong Kong macroeconomic and financial 
variables (Panel A), and capital flow and financial stability variables (Panel B), to a US monetary 
tightening. The US monetary policy tightening is defined as a 25-basis-point increase in the US policy 
rate in this analysis. It is generally expected that the US Fed will raise interest rate by 25 basis points in 
each interest rate hike11 (around a half of the standard deviation of the differences in US federal fund 
rate over the sample period) in the anticipated US monetary policy normalization.  
                                                     
9 Since the FAVAR framework requires stationary variables, all non-stationary variables are differenced. Please refer to Table 1 
for the detailed description of data transformation. 
10 The high correlation between Factor 2 with real activities and financial stability may imply the high correlation between growth 
and financial stability. However, this may not be true. As shown in equation (1), different economic and financial stability 
variables may have different relationship with different factors and the shock variables. Indeed, below estimation results suggest 
that Hong Kong’s financial stability variables are more resilient than macroeconomic variables to the external shocks. 
11 Fischer (2015). As discussed above, it is very clear the US Fed raise the interest rate in the coming years, the monetary policy 
shock in this paper is defined as an anticipated interest rate hike rather than an unexpected change in monetary stance. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 15

12 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
The VAR model (equation (3)) includes 5 factors plus the US shadow policy rate with 4 lags. The charts 
show the impulse responses of selected variables to a US monetary policy tightening up to 16 quarters 
in which the impulse responses represent changes of the variables in VAR. The red solid line indicates 
the estimated median response. The solid blue and green lines represent a 68 percent bootstrap 
confidence interval, and the dashed blue and green lines represent a 90 percent bootstrap confidence 
interval based on a 1,000 bootstrap samples.12 In the impulse response exercise, a standard deviation 
unit is used and the US monetary policy change is transformed into units of standard deviations of the 
changes in the US federal fund rate. As stated above, the US monetary policy change is assumed to 
be a 25-basis-point increase in the federal funds rate, which is about 0.5 standard deviations of 
changes in the US monetary policy rate over the sample period. It should be noted that the impulse 
responses are in standard deviation units. 
 
Following a US monetary tightening, Hong Kong’s financial variables generally react significantly. The 
Hong Kong dollar NEER appreciates by 0.58% in one quarter. Hong Kong interbank interest rates go 
up immediately following an increase in the US interest rate. Under the linked exchange rate system 
with full capital mobility, Hong Kong’s monetary policy follows the Fed’s policy. It is well expected that 
the Hong Kong dollar exchange rate and interbank interest rates will follow the movements in their US 
dollar counterparts. Our empirical results confirm this point. This also shows that financial markets 
have confidence in the stability of Hong Kong’s linked exchange rate system, otherwise the local 
market interest rate and exchange rate will diverge from the direction of movements in their 
counterparts in the US. With regard to the stock market, the Hang Seng index (HSI) has a significant 
but temporary negative response that only lasts one quarter, then rebounds before the impact 
eventually goes to zero, which means that Hong Kong’s stock market quickly digests the news in a US 
monetary policy change.  
                                                     
12 The generating method for the confidence interval is the same as that used in Bernanke et al. (2005). 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 16

13 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
A tightening of US monetary policy also has significant impact on Hong Kong’s monetary and inflation 
variables but has little impact on real variables. Growth in M1 shows an immediate and significant 
decline. Growth in total loans also drops immediately and growth in M3 declines initially but the impact 
gradually dies down. In contrast to the results of Bernarke et al. (2005), we do not find a price puzzle13 
in Hong Kong. Underlying CPI (excluding the effect of one-off relief measures) drops an average of 
0.04 percentage points in the first four quarters after a US tightening. Prices in Hong Kong are very 
flexible. They usually adjust to shocks very quickly. For real activity, changes in the PMI and growth in 
GDP do not see a significant impact but growth in retail sales drops by 0.08 percentage points in the 
first quarter. In the external sector, growth in the value of imports and exports shows a marginal 
decrease. The unemployment rate shows some increases, but it is not significant. 
 
In the property market, the impact of a US monetary tightening is mixed. The residential property 
transaction and R&VD residential property price index do not show a significant reaction to a US 
monetary tightening. However, the growth in the Centa City Index14 shows a cumulative decline of 
0.3% in the first year after a US monetary tightening. Specifically, the percentage growth in the price of 
a large flat decreases by 0.56%, while that of a small flat decreases by 0.24%. Hong Kong’s property 
market usually is very sensitive to interest rate changes. With only a one-time 25-basis-point increase 
in the policy rate, this impact does not seem very large. Usually after a full interest rate tightening cycle, 
the growth in property prices shows a significant slowdown or even becomes negative.  
The impulse responses of selected variables of capital flow and financial stability to a US monetary 
tightening are shown in Panel B of Figure 2. The tightening in the US monetary policy has a significant 
impact on capital flows and leverage, but the impact on loan quality, banks’ capital asset ratio and loan 
                                                     
13 In VAR literature, a monetary policy tightening is found to be followed by an increase in the price level (Bernanke et. al., 2005). 
In the robustness checking section next, we do see a price puzzle when using standard VAR model (also see Figure 13). This 
shows Sims’ explanation that standard VAR does not control for all necessary information might be correct. 
14 Besides R&VD residential property price index (official index for all residential properties), Centa City Index is also a commly 
used property price index in Hong Kong. It is an average property price index for secondary private residential property based on 
all transaction records as registered with the Land Registry. The index is calculated and released by Centaline Property Agency 
Limited monthly. Details of the index can be found here: http://www1.centadata.com/cci/notes_e.htm 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 17

14 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
to deposit ratio is limited. Specifically, using percentage changes in the monetary base as a proxy of 
capital flows, these show a significant drop in the first year and a half after a US monetary tightening. 
Changes in current account and capital account balances also show significant decreases after a 
tightening. For financial stability, changes in household leverage, which is defined as household loans 
(sum of residential mortgage, credit card and other personal loans) over the nominal GDP, show a 
significant drop in the first year after the interest rate hike. However, loan-to-GDP ratio, new mortgage 
loans and the market LTV do not see a significant change in response to a US monetary tightening. 
The latter result is in line with Wong et al. (2014) that shows the Hong Kong market LTV is mainly 
explained by the domestic LTV policy. The classified loan ratio drops significantly and temporarily, 
while the drop in the credit card delinquency ratio is not significant. Net interest margins show a 
significant but temporary drop. For the banks’ capital and liquidity, the CAR ratio does not show a 
significant change, while the liquidity indicator, HKD loan-to-deposit ratio declines in the first year. The 
above results show that Hong Kong’s loans and capital flows are sensitive to US interest rate changes, 
however, Hong Kong’s financial stability variables are mainly controlled by local macroprudential 
policies.  
 
Table 3 shows a variance decomposition of the above 32 selected variables. Column II reports the 
fraction of the variances of forecast errors of selected Hong Kong variables explained by US monetary 
policy changes at a 16-quarter horizon. The results suggest that US monetary policy has bigger impact 
on interbank interest rate and capital flows, and a much smaller impact on other Hong Kong economic 
variables.15 Column III shows the explanatory power (R2) of the common factors16 for the selected 
variables. The common factors explain a large part of variability of the selected variables, particular for 
                                                     
15 The calculation of the fraction of the variance of forecasting error explained by the external shock is same as that used by 
Bernanke et. al., 2005. For example, the fraction of forecasting error variance of variable x in 16 quarters explained by the US 
monetary shock is expressed as 
𝑣𝑎𝑟(𝑥𝑡+16−𝑥̂𝑡+16|𝑡|𝜀𝑡
𝑈𝑆)
𝑣𝑎𝑟(𝑥𝑡+16−𝑥̂𝑡+16|𝑡) , where 𝑥𝑡+16 is the actual value of x in 16 quarters after time t (time of 
shock), 𝑥̂𝑡+16|𝑡 is the forecasting value of x in 16 quarters by using information up to time t, 𝑣𝑎𝑟(𝑥𝑡+16 −𝑥̂𝑡+16|𝑡) is the total 
variance of forecasting error of x and 𝑣𝑎𝑟(𝑥𝑡+16 −𝑥̂𝑡+16|𝑡|𝜀𝑡
𝑈𝑆) is the variance of forecasting error of x due to the US monetary 
policy shock. 
16 The common factor includes the five principal components and the US monetary policy shock variable. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 18

15 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
real activity and property market variables. This result shows that the extracted factors can be used to 
analyse business cycle movements. 
 
In order to highlight the contribution of US monetary policy changes to the growth of real activity, a 
historical decomposition of the real activity factor (factor 2) is calculated based on the five-factor 
FAVAR model. Figure 3 plots the actual series of factor 2 against the counterfactual series without US 
monetary policy changes. For most of the sample period, the counterfactual series follow the actual 
series closely. This shows that, for most of the time, the impact of US monetary policy changes on real 
activity factor is small. There are at least four episodes in the sample period when the two series 
diverge quite significantly. The first episode is around the middle of 2001, where counterfactual growth 
is much lower than actual growth. This is because that the counterfactual growth rate excludes the 
effect of an easing in monetary policy after the burst of the technology stock bubble. The second 
episode happens in late 2009. Again, counterfactual growth is lower than actual growth because, after 
the onset of the global financial crisis, the Fed quickly cut the policy rate to zero to mitigate the impact 
of the crisis. The third episode happens between 2012 and 2013. This is the period during which the 
Fed’s three rounds of QEs has a big impact. It can be seen that the counterfactual line is significantly 
lower than the actual line. For all these three episodes, the easing of US monetary policy contributes 
positively to the growth rate of real economic activities summarized in factor 2. The fourth period starts 
in 2014, when the Fed’s tapering and withdrawal of QE raises an expectation of monetary policy 
normalization. Here the counterfactual growth rate lies above the actual line. This shows that without 
tapering or a withdrawal of the Fed’s QE, the growth rate of real factors would have been higher. All 
these four episodes show that autonomous monetary policy actions by the Fed do have a real impact 
on the Hong Kong economy (Romer and Romer (1989)). However, this impact usually comes with a 
lag. On the other hand, during normal times, the contribution of monetary policy changes to real activity 
is small. The result is consistent with that from the variance decomposition, which shows that the 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 19

16 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
impact of US monetary policy changes on Hong Kong real economic variables in general is relatively 
small.  
 
c. Monetary Easing from ECB and BoJ 
 
Figure 4 and Figure 5 provide the impulse responses of the 32 Hong Kong variables to individual 
shocks, namely the ECB and BoJ easing. The VAR system now includes the five common factors and 
one shock variable, being either the ECB’s shadow policy rate or BoJ’s shadow policy rate. Both 
shocks are defined as a 25 basis point cut in policy rates.  
 
From Figure 4, Panel A, it can be seen that after the ECB easing, the Hong Kong dollar NEER 
appreciates and the 3-month HIBOR rate goes down. The impact on the Hang Seng index, M1 and 
PMI are not significant. Real GDP, retail sales, import and export all go down and the unemployment 
rate goes up. Property prices go down initially and the impact quickly dies out. Panel B of Figure 4 
shows that the monetary base increases initially owing to capital inflows. Household leverage and the 
market LTV both rise because of more liquidity. The impact on other financial stability variables is not 
significant. Overall, an easing by the ECB causes more liquidity to flow to Hong Kong, however, the 
reaction of real economic variables such as GDP growth and unemployment rate are rather negative. 
One possible reason for these counter-intuitive results is that the main transmission channel from the 
Euro area to Hong Kong is through trade. When the ECB lowers the policy rate, the real economy in 
Euro area is rather weak and it is the inter-regional trade slow down which causes GDP growth in 
Hong Kong to slow down and the unemployment rate to go up. This transmission channel is very 
different to that of US monetary policy changes, where the financial channel is also significant.  
 
For the impulse responses of an easing by the Bank of Japan, Figure 5 shows that the Hong Kong 
dollar NEER depreciates and 3-month HIBOR goes down initially. The impact on the Hang Seng index, 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 20

17 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
loans, inflation, PMI is limited. The impact on real variables such as real GDP growth, retail sales, 
imports and exports, unemployment rate is also very small. Property prices across all categories go up. 
For the financial stability variables, the monetary base goes up initially, which means there are capital 
inflows. Household leverage, the loan to deposit ratio and new mortgage loans also rise, while other 
variables do not react significantly. This shows that shocks from the BoJ affect Hong Kong mainly 
through interest rate arbitrage and liquidity inflows. The impulse responses of real economic variables 
are not significant. The reaction of the Hong Kong dollar NEER is a bit counter-intuitive, instead of 
appreciating after the easing by BoJ, the Hong Kong dollar depreciates. One possible reason is that 
Japanese yen is appreciating for most of the sample period, even with the zero interest rate policy of 
the BoJ. 
 
d. A Mainland China’s GDP shock 
 
He, Liao and Wu (2014), Genberg, Liu and Jin (2006) argue that the Hong Kong economy is 
increasingly affected by the shocks emanated from Mainland China. This reflects an on-going progress 
of economic and social integration between the two economies. In this sub-section, we add the 
quarterly real GDP growth of Mainland China to the VAR system to see how shocks in China’s 
economic growth affect Hong Kong’s economic variables. We first study the impulse responses only 
including Mainland growth variable in the Rt, then compare the results from the model with both US 
monetary policy shocks and Mainland growth variables.17 The shock of a Mainland slowdown is 
defined 
as 
0.25-percentage-point 
contraction 
of 
Mainland 
GDP 
growth 
(which 
is 
a 
one-percentage-point reduction in China GDP growth in annual rate). 
 
Figure 6 shows that the main impact of a Mainland economic slowdown are on real GDP growth, retail 
sales, imports, exports and unemployment rate. All the above variables except the unemployment rate 
                                                     
17 This means Rt in equations (1) to (3) includes both the US shadow policy rate and Mainland China GDP growth. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 21

18 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
go down significantly, while the unemployment rate increases dramatically. The 3-month HIBOR and 
Hang Seng index also declines, but Hong Kong dollar NEER appreciates because of the weakening of 
RMB. The impact on financial stability variables is generally not significant.  
 
To compare the above result, we include both US monetary policy variable and Mainland growth 
variable in the VAR system and turn on only the Mainland growth shock. Figure 7 shows that Hong 
Kong’s real activity variables decline significantly immediately after a 0.25-percentage-point 
contraction shock in China’s quarterly GDP growth. The magnitude of the decline is much bigger than 
that arising from a tightening of the US monetary policy only. Hong Kong real GDP decreases by 0.7 
percentage points in the first quarter, compared to a 0.08 percentage points decline following a US 
monetary tightening shock, The PMI decreases by 1.15 compared to 0.02, retails sales decrease by 
0.56% compared to 0.77% and external trade drops by around 1.5% compared to less than 0.5%. The 
unemployment rate is slightly higher at 0.1% compared to 0.02%.  
 
Again 3-month HIBOR declines immediately, possibly due to the relaxation of pressure on liquidity 
following a contraction shock in Mainland China GDP. The HKD NEER increases, and the stock 
market declines. The property market (except for large properties) does not show a significant change. 
In addition, capital flows and financial stability (Panel B of Figure 7) are generally unaffected by this 
shock. 
This shows that a shock from Mainland GDP growth mainly affects Hong Kong’s real variables, not so 
much nominal variables.  
 
To summarize, we find that Hong Kong’s interest rate and exchange rate mainly follow their US 
counterparts. An increase in US monetary policy rates mainly affects Hong Kong’s monetary and 
financial variables. Real economic variables are mainly affected by shocks from Mainland growth. 
Shocks from monetary policy from ECB and BoJ play marginal roles. Shocks from the ECB mainly 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 22

19 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
transmit through international trade, while shocks from the BoJ mainly transmit through international 
capital markets by interest rate and exchange rate arbitrage.  
 
Hong Kong as an international financial center with open capital markets, it is constantly influenced by 
shocks arising from the rest of the world economy. In the next part, we analyse the aggregate impact of 
simultaneous shocks from monetary policies of the Fed, ECB, BoJ and a Mainland economy slowdown. 
We do it in a VAR system with all four shock variables. Together with the five common factors, the VAR 
system now has 9 variables18. Again, we take four lags.  
 
e. Diverging Monetary Policies 
 
This sub-section studies the impact of diverging monetary policies on the Hong Kong economy. 
Currently the Fed has raised the Fed fund target rate to 0.25% – 0.50%, the ECB and BoJ have 
imposed negative interest rates on bank reserves. What is the joint impact of these diverging monetary 
policies on Hong Kong? Will the effects of diverging monetary policies cancel out each other?  
 
In the following impulse response analysis, we assume a 25-basis-point decrease in shadow policy 
rates by both ECB and BoJ, and a 25-basis-point increase in the policy rate of the Fed. Figures 8 – 10 
provide the impulse responses of an individual monetary policy change in the full VAR model of 9 
variables with other shock variables turned off. These are broadly similar to those in Figures 2, 4 and 5. 
Figure 11 provides the combined effect of these monetary policy changes with the Mainland economic 
slowdown shock turned off. It is interesting to see that when three monetary policy variables are added 
to the system, the combined effect is broadly similar to that with only the US monetary policy variable. 
This is not surprising given that with free capital mobility Hong Kong’s monetary policy follows exactly 
                                                     
18 This means Rt in equations (1) to (3) includes the shadow monetary policy rates of the Fed, ECB and BoJ, plus Mainland GDP 
growth. 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 23

20 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
the Fed’s policy. Therefore, the effect of the Fed tightening dominates the impulse responses. While an 
easing policy by the Bank of Japan to some extent neutralizes a tightening policy by the Fed, an easing 
by ECB plays a very marginal role. This may be because traditionally Japanese banks have more 
exposure to the Hong Kong economy. Businesses in Hong Kong take advantage of low interest rates in 
Japan to arbitrage in order to save funding cost. On the other hand, ECB monetary policy affects the 
Hong Kong economy through a real economy channel such as international trade. Usually the reason 
for easing by the ECB is because of weakness in the real economy in the Euro Area. This in turn 
weakens external demand of Hong Kong from Euro area. That is why in the impulse responses, the 
effect of monetary easing by ECB is sometimes in the same direction as that of tightening by the Fed. 
For example, in Figure 9, the impulse response of easing by the ECB suggests that it reduces real 
GDP growth, the growth of both imports and exports, the growth in housing prices and raises the 
unemployment rate. It also raises the nominal effective exchange rate through a weakening of the euro. 
For other variables, the impulse responses are not statistically significant.  
 
From Panel A of Figure 11, it can be seen that the HKD nominal effective exchange rate appreciates 
significantly in the first year. The total appreciation is 1.26% in the first year, which is higher than the 
0.35% with only US monetary policy change. This is understandable because the easing by the ECB 
weakens the euro. Since the Hong Kong dollar is pegged to the US dollar, the movement of the Hong 
Kong dollar exchange rate against the currencies other than the US dollar mainly reflects the 
appreciation of the US dollar against other currencies. 
 
From Panel B of Figure 11, it can be seen that growth in the monetary base and the current account go 
down, but the capital account shows an initial increase. Compared with Panel B of Figure 8, capital 
outflows (the change in the monetary base and capital account balance are used as proxies) are lower. 
This shows that the easing by the BoJ and ECB neutralizes the effect of tightening by the Fed. Capital 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 24

21 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
outflows to the US are offset by capital inflows from Japan. This result is in line with He, Wong, Tsang 
and Ho (2015).  
 
The 3-month interbank rate increases during the first year following a Fed tightening. Growth in 
property prices, the money supply and inflation also declines. The most interesting result is the 
combined effect on real variables. Growth in real GDP, retail sales, imports and exports goes down, 
while that of unemployment goes up. This result shows that the combined effects are more or less the 
sum of individual effects. Given that the monetary shocks are generally exogenous to each other, this 
result is not surprising.  
 
For the financial stability variables, the impact from monetary policy shocks dies out within the first year. 
Shocks from the BoJ increase household leverage and the market LTV ratio, and new mortgage loans. 
Shocks from the ECB have a very small marginal effect. Overall, the financial stability variables are 
mainly affected by local macroprudential policies.  
 
With diverging monetary policies of major central banks, what is the combined impact together with a 
growth slowdown in Mainland China? Now we add back the contraction shock of Mainland GDP 
growth of 0.25 percentage point in one quarter. Figure 12 shows the impulse responses of the 
aggregate effects including a negative shock in Mainland growth. Comparing with Figure 11, real GDP 
growth in Hong Kong goes down even further, the unemployment goes up by much more. Both imports 
and exports decline by more. The differences in the effect on inflation and other financial variables are 
not significant. This further confirms our view that a Mainland GDP growth shock mainly affects Hong 
Kong’s real economic variables. Specifically, Hong Kong quarterly GDP growth will be lower by around 
0.4 percentage points on average in the first year with only diverging monetary policy shocks. But it will 
be lowered by 0.6 percentage points if there is an additional negative shock in Mainland GDP growth 
However, Mainland China’s economic slowdown has only a very limited additional impact on Hong 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 25

22 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Kong’s inflation. The quarterly decrease in inflation is only 0.2 percentage points on average in the first 
year for scenarios with or without a Mainland China economic slowdown. For the property market, the 
average quarterly decrease in the Centa City Index is 1.4 percentage points without the negative 
growth shock from the Mainland, and is 1.8 percentage points with the negative shock. Table 4 reports 
the variance decomposition and R2 of 32 selected variables at a 16-quarter horizon in the full model 
with all four shocks. It can be seen that the common factors (including five principal components and 
four shock variables) can explain the main part of the variance of the selected variables. The R2 for 
most of the variables is higher than 60%. The notable exception is capital account balance, for which 
the R2 is quite low. With free capital mobility in Hong Kong, the capital account balance is very volatile 
and sensitive to market sentiment. For most of the 32 variables, the variance decomposition shows 
that shocks arising from Fed policy and Mainland growth carry a higher percentage in the variance of 
the forecast error. Shocks from monetary policies arising from the ECB and BoJ mainly affect financial 
variables, despites the percentages being lower.  
 
To summarize, the combined effect of diverging monetary policies among the major global central 
banks and a Mainland GDP slowdown will drive up Hong Kong’s dollar nominal effective exchange rate, 
lower GDP growth, raise the unemployment rate, and lower the property prices. Hong Kong’s financial 
stability is well managed by the local macroprudential policies in the context of global shocks.  
 
 
5. 
Robustness Check 
 
This section, we estimate four alternative models for robustness checks. The models are estimated 
with only the US monetary policy variable.  
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 26

23 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
a. Standard VAR model 
 
Figure 13 compares the impulse responses of the standard VAR model with five selected variables 
with that of the same five variables from the FAVAR model with only US monetary policy changes. It 
can be seen that for the monetary base and household leverage, both models show that initial 
responses are negative after a US monetary tightening. The responses from the FAVAR model are 
much bigger and more volatile. In general, for all five variables, the responses are more volatile from 
the FAVAR model. This volatility comes from the fact that FAVAR model includes more information. In 
the standard VAR model, Hong Kong inflation initially goes up after US tightening, which is similar to 
the price puzzle investigated in Bernanke et al. (2005); while in the FAVAR model, inflation initially goes 
down before it goes up again. Hong Kong’s inflation, property prices and GDP growth are affected by 
factors more other than just US monetary policy. Therefore, the impulse responses from US monetary 
policy changes only capture part of the dynamics. For variables sensitive to interest rates, such as the 
monetary base and household leverage, including more information in the model makes the impulse 
responses more accurate in terms of capturing the actual dynamics of the economic variables.  
 
b. Sub-sample analysis: Periods from Crisis (since 2008) 
 
This sub-section looks at sub-sample estimation beginning with the global financial crisis in 2008. 
Figure 14 shows the impulse responses of 32 selected variables of the sub-sample analysis with only 
the US monetary policy variable and three factors from the principal component analysis. We choose 
three factors because of the short sample. Compared with Figure 2, it can be seen that the impact of a 
US monetary tightening is broadly similar to that using the full sample, although the responses are a bit 
smaller.  
 
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 27

24 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
c. Gibbs Sampling approach (single-step approach) 
 
As discussed in Section 3, the FAVAR framework can also be estimated by the Gibbs Sampling 
approach (single-step approach). Figure 15 shows the impulse responses of the 32 selected variables 
to a US monetary policy tightening using a single-step (Gibbs Sampling) approach. Compared with the 
results shown in Figure 2, the results from the single-step approach are very similar. Given that this 
approach is computationally very demanding, we only use the two-step estimation approach in the 
analysis presented above. 
 
d. Structural FAVAR 
 
Figure 16 shows the impulse responses of a structural FAVAR model using the principal components 
by groups. In this model, seven factors, which are extracted from seven groups of Hong Kong 
economic variables by principal components, are included in the VAR system. These include a 
financial factor, monetary and inflation factor, real activity factor, international trade factor, property 
market factor, capital flow factor, and financial stability factor. The impulse responses of the 32 
selected variables are similar to those from the five-factor (extracted from all 116 Hong Kong variables) 
model in Figure 2, except for the NEER (which shows insignificant change), trade (both exports and 
imports increase) and the property market (prices show initial increase). The structural FAVAR may 
help to identify factors and provide some economic meaning, however, the factors only take into 
account the information of the variables within the individual groups. This may partly reduce the benefit 
of using a FAVAR, which aims to include as much information as possible in estimation.  
 
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 28

25 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
6. 
Conclusions 
 
Hong Kong as an international financial center is subject to constant external influences. It’s open 
capital markets and linked exchange rate system means that monetary policy changes of the Fed, 
ECB and BoJ will have a significant impact on the Hong Kong economy. The anticipated divergence in 
the monetary policy stance of the major central banks around the World – with the Fed poised to 
further tighten and the ECB and BoJ continue their QEs and negative interest rate policies – and a 
Mainland economy slowdown will affect the Hong Kong economy. But their combined effect is hard to 
gauge.  
 
This paper aims to provide a comprehensive analysis of the impact of these different shocks on the 
Hong Kong economy using a FAVAR model. We first estimate the impacts of a single shock. Then we 
estimate the aggregate impact of combining the above shocks. Our main empirical findings are as 
follows. 
 
 
We find that a US monetary policy tightening raises the Hong Kong dollar exchange rate and HIBOR, 
leading to capital outflows. It generally lowers inflation and growth in property prices. Its impact on real 
economic variables is, however, not significant. A monetary easing by the ECB drives up the exchange 
rate, lowers the HIBOR, and increases inflation, capital inflows and leverage. However, its impact on 
real variables is negative: GDP growth goes down, unemployment goes up, and property price growth 
goes down. This could be because the transmission channel is mainly through international trade. An 
easing by the BoJ lowers the exchange rate because of a strong yen. It lowers the HIBOR, raises 
money supply and growth in property prices. It also raises GDP growth and lowers the unemployment 
rate, and increases capital inflows and leverage. A Mainland slowdown raises the exchange rate, 
money supply, lowers Hang Seng Index, GDP growth and growth in imports and exports. Its impact on 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 29

26 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
property prices, however, is not significant. For all these shocks, the impact on financial stability 
variables is moderate suggesting that Hong Kong’s financial stability is well maintained by 
macroprudential policies.  
 
Since these shocks are exogenous, the combined effect of diverging monetary policies is more or less 
the sum of individual effect. So the effects on financial variables to some extent offset each other. The 
Hong Kong dollar NEER shows moderate appreciation. The growth in real GDP slows down and the 
unemployment rate goes up. With shocks from Mainland slowdown, the growth in real GDP goes down 
further and unemployment rises by more. Again financial stability is well maintained.  
 
These results suggest that a normalization of US monetary policy combined with continued 
quantitative easing policies by the ECB and BoJ could have an overall negative impact on the Hong 
Kong economy. This may be significantly amplified by a simultaneous slowdown in growth in Mainland 
China. However, our results suggest that Hong Kong’s financial stability – as reflected in loan quality, 
banks’ capital and liquidity – may be resilient to the combined effect of all of the above external shocks, 
although these will have some temporary effects on the economy. 
 
  
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 30

27 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
References 
 
 
Belviso, F. and F. Milaniy (2006), “Structural Factor-Augmented VARs (SFAVARs) and the Effects of 
Monetary Policy”, Topics in Macroeconomics 6(3), pp.1443–1443. 
 
Bernanke, B.S., J. Boivin, and P. Eliasz (2005), “Measuring the Effects of Monetary Policy: A 
Factor-Augmented Vector Autoregressive (FAVAR) Approach”, Quarterly Journal of Economics, 120(1), 
pp. 387–422. 
 
Boivin, J., M. P. Giannoni and I. Mihov (2009), “Sticky Prices and Monetary Policy: Evidence from 
Disaggregated US Data”, American Economic Review, 99(1), pp. 350–384. 
 
Dahlhaus, T., K. Hess and A. Reza (2014), “International Transmission Channels of U.S. Quantitative 
Easing: Evidence from Canada”, Bank of Canada Working Paper 2014-43. 
 
Dumrongrittikul, T., H. Anderson and F. Vahid (2014), “The Effects of Productivity Gains in Asian 
Emerging Economies: A Global Perspective”, Department of Econometrics and Business Statistics, 
Monash University, Working Paper 23/14. 
 
Fernald, J., M. M. Spiegel and E. T. Swanson (2014), “Monetary Policy Effectiveness in China: 
Evidence from a FAVAR Model”, Federal Reserve Bank of San Francisco Working Paper 2014-07. 
 
Fischer, S. (2015), “Conducting Monetary Policy with a Large Balance Sheet”, Remarks at the 2015 
U.S. Monetary Policy Forum, 27 Febrary 2015. 
 
Fu, D., L. L. Taylor and M. K. Yücel (2003), “Fiscal Policy and Growth”, Research Department, Federal 
Reserve Bank of Dallas Working Paper 0301. 
 
Geman, S. and D. Geman (1984), “Stochastic Relaxation, Gibbs Distributions and the Bayesian 
Restoration of Images”, IEEE Transactions on Pattern Analysis and Machine Intelligence, 6, pp. 721–
41. 
 
Genberg, H., L. Liu and X. Jin (2006), “Hong Kong’s Economic Integration and Business Cycle 
Synchronisation with Mainland China and the US,” HKMA Working Paper 11/2006. 
 
He, D., W. Liao and T. Wu (2014), “Hong Kong’s Growth Synchronisation with China and the U.S.: A 
Trend and Cycle Analysis”, HKIMR Working Paper 15/2014. 
 
He, D., E. Wong, A. Tsang and K. Ho (2015), “Asynchronous Monetary Policies and International Dollar 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 31

28 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Credit”, HKIMR Working Paper 19/2015. 
 
Ho, S. W., J. Zhang and H. Zhou (2014), “Hot Money and Quantitative Easing: The Spillover Effects of 
U.S. Monetary Policy on Chinese Housing, Equity and Loan Markets”, Federal Reserve Bank of Dallas 
Working Paper No. 211. 
 
Krippner, L. (2013), “Measuring the stance of monetary policy in zero lower bound Environments”, 
Economics Letters, 118(1), pp. 135–138. 
 
Lombardi, M. and F. Zhu (2014), “A shadow policy rate to calibrate US monetary policy at the zero 
lower bound”, BIS Working Paper, No. 452. 
 
Mumtaz, H. and P. Surico (2009), “The Transmission of International Shocks: A Factor-Augmented 
VAR Approach”, Journal of Money, Credit and Banking, 41(s1), pp. 71–100. 
 
N’Diaye, P. and A. Ahuja (2012), “Trade and Financial Spillover on Hong Kong SAR from a Downturn in 
Europe and Mainland China”, IMF Working Paper WP/12/81. 
 
Romer, C.D. and D.H. Romer (1989), “Does Monetary Policy Matter? A New Test in the Spirit of 
Friedman and Schwartz”, in Olivier Blanchard and Stanley Fisher, eds., NBER Macroeconomics 
Annual (Cambridge MA: MIT Press, 1989) 
 
Wong, E., A. Tsang and S. Kong (2014), “How Does Loan-To-Value Policy Strengthen Banks’ 
Resilience to Property Price Shocks – Evidence from Hong Kong”, HKIMR Working Paper 03/2014. 
 
Wu, J. and F. Xia (2016), “Measuring the macroeconomic impact of monetary policy at the Zero Lower 
Bound”, forthcoming in Journal of Money, Credit, and Banking. 
 
Zuniga, M. C. (2011), “International Monetary Transmission, a Factor-Augmented Vector 
Autoregressive (FAVAR) Approach: The Cases of Mexico and Brazil”, Business and Economics 
Journal, Volume 2011: BEJ-26. 
 
 
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 32

29 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Table 1 Data Description 
 
This appendix summarises the 4 external shock variables and 116 Hong Kong macroeconomic and 
financial variables included in the estimation. The sample period is from 1998 Q4 to 2015 Q2. The data 
series are seasonally adjusted if necessary. The transformation codes are 1 – no transformation; 2 – 
first difference; 4 – logarithm; 5 – first difference of logarithm. An asterisk * next to the mnemonic 
denotes a variable assumed to be slow-moving (see footnote 4). 
 
 
Variable
Source
Transformation
External shocks
US shadow policy rate
Wu and Xia (2014)
2
Euro Area shadow policy rate
Wu and Xia (2014)
2
Japan shadow policy rate
Krippner (2013)
2
Mainland China GDP
CEIC and author's estimation
5
Exchange rate
HKD REER
HKMA
5
HKD/Euro
HKMA
5
HKD/USD
HKMA
5
HKD/RMB
HKMA
5
HKD/JPY
HKMA
5
HKD NEER
HKMA
5
Interest rate
3-month HIBOR
HKMA
2
6-month HIBOR
HKMA
2
12-month HIBOR
HKMA
2
Yield of 3-month Exchange Fund bills and notes
HKMA
2
Yield of 6-month Exchange Fund bills and notes
HKMA
2
Yield of 12-month Exchange Fund bills and notes
HKMA
2
Yield of 5-year Exchange Fund bills and notes
HKMA
2
Yield of 10-year Exchange Fund bills and notes
HKMA
2
Stock
Hang Seng Index
CEIC
5
Hang Seng Finance Index
CEIC
5
Hang Seng China Enterprises (H Share) Index
CEIC
5
Total market capitalization
CEIC
5
P/E ratio for Hang Seng Index
CEIC
1
P/E ratio for Hang Seng Finance Index
CEIC
1
P/E ratio for all Hong Kong stocks
CEIC
1
Dividend yield ratio for Hang Seng Index
CEIC
1
Dividend yield ratio for Hang Seng Finance Index
CEIC
1
Dividend yield ratio for all Hong Kong stocks
CEIC
1
Stock market turnover
CEIC
5
Loans
Total loans
HKMA
5
Hong Kong Dollar loans
HKMA
5
Foreign currency loans
HKMA
5
Money
M1
HKMA
5
M2
HKMA
5
M3
HKMA
5
Currency in circulation
HKMA
5
Price
CPI: meals away from home*
C&SD
5
CPI: food, excluding meals away from home*
C&SD
5
CPI: alcoholic drinks and tobacco*
C&SD
5
CPI: clothing and footwear*
C&SD
5
CPI: durable goods*
C&SD
5
CPI: miscellaneous goods*
C&SD
5
CPI: Transport*
C&SD
5
CPI*
C&SD
5
CPI: Housing*
C&SD
5
CPI: electricity, gas and water*
C&SD
5
CPI: miscellaneous services*
C&SD
5
GDP deflator*
C&SD
5
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 33

30 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
Output
PMI*
Bloomberg
2
Real GDP*
C&SD
5
Real GDP: private consumption*
C&SD
5
Real GDP: gross fixed capital formation*
C&SD
5
Real GDP: government consumption*
C&SD
5
Inventory-to-GDP ratio*
C&SD and author's calculation
1
Real GDP: exports of goods*
C&SD
5
Real GDP: exports of services*
C&SD
5
Real GDP: imports of goods*
C&SD
5
Real GDP: imports of services*
C&SD
5
Retail sales
Retail sales value*
C&SD
5
Retail sales volume*
C&SD
5
Labour
Labour force participation rate*
C&SD
1
Unemployment rate*
C&SD
2
Median weekly working hours*
C&SD
1
Youth unemployment rate (age: 15-19)*
C&SD
2
Median duration of unemployment*
C&SD
1
Nominal wage index*
C&SD
5
Real wage index*
C&SD
5
Property market
Property sales and purchases value
R&VD
5
Property sales and purchases volume
R&VD
5
Property price index: residential
R&VD
5
Property price index for large residential properties
R&VD
5
Property price index for small residential properties
R&VD
5
Centa City Leading Index
Centa
5
Centa City Index
Centa
5
Centa City Leading Index for mass estate
Centa
5
Centa City Leading Index for large properties
Centa
5
Centa City Leading Index for small properties
Centa
5
Centa City Index for mass estate
Centa
5
Centa City Index for large properties
Centa
5
Centa City Index for small properties
Centa
5
Property rental index: residential
R&VD
5
Property rental index for large residential properties
R&VD
5
Property rental index for small residential properties
R&VD
5
Property price index: office
R&VD
5
Property price index: grade A office
R&VD
5
Property price index: grade A office in core districts
R&VD
5
Property rental index: office
R&VD
5
Property rental index: grade A office
R&VD
5
Property price index: retail premise
R&VD
5
Property rental index: retail premise
R&VD
5
Property price index: flatted factories
R&VD
5
Property rental index: flatted factories
R&VD
5
Trade
Trade balance (% of total export)
C&SD
1
Terms of trade index
C&SD
5
Import values
C&SD
5
Export values
C&SD
5
Quantum index for import
C&SD
5
Quantum index for export
C&SD
5
Unit value index for import*
C&SD
5
Unit value index for export*
C&SD
5
Capital flow indicators
Monetary base (capital flow)
HKMA
5
Current account balance (% of GDP)*
C&SD and author's calculation
2
Capital account balance (% of GDP)*
C&SD and author's calculation
2
Financial Stability indicators
HSI Volatility Index (VHSI)
Bloomberg
5
New mortgage loans
HKMA
5
Average market LTV ratio for new mortgage loans
HKMA
2
Average contract life for new mortgage loans (no. of months)
HKMA
2
Problem loan ratio for mortgage loans
HKMA and author's calculation
2
Classified loan ratio (gross)*
HKMA
1
Overdue (>3 months) and rescheduled loan ratio*
HKMA
1
Net interest margin*
HKMA
1
Bad debt charge as percentage of average total assets*
HKMA
1
Cost-to-income ratio*
HKMA
1
Capital adequacy ratio (CAR)*
HKMA
1
Credit card loans*
HKMA
4
Credit card delinquency ratio*
HKMA
1
Household leverage*
HKMA, C&SD and author's culculation
2
Loan-to-GDP ratio*
HKMA, C&SD and author's culculation
2
Loan-to-deposit (LTD) ratio
HKMA and author's calculation
2
HKD Loan-to-deposit (LTD) ratio
HKMA and author's calculation
2
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 34

31 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Table 2 Correlation of individual variables to the extracted factors 
 
Factor 1
Factor 2
Factor 3
Factor 4
Factor 5
Exchange rate
HKD REER
-8%
-56%
14%
-40%
-9%
HKD/Euro
22%
30%
-28%
26%
5%
HKD/USD
18%
16%
24%
2%
41%
HKD/RMB
43%
-7%
2%
40%
6%
HKD/JPY
-14%
22%
-25%
50%
-6%
HKD NEER
-34%
-41%
30%
-43%
-1%
Interest rate
3-month HIBOR
37%
-24%
73%
-39%
-5%
6-month HIBOR
36%
-26%
72%
-41%
-3%
12-month HIBOR
38%
-28%
69%
-44%
-1%
Yield of 3-month Exchange Fund bills and notes
33%
-25%
65%
-48%
13%
Yield of 6-month Exchange Fund bills and notes
34%
-26%
66%
-51%
11%
Yield of 12-month Exchange Fund bills and notes
36%
-25%
64%
-54%
9%
Yield of 5-year Exchange Fund bills and notes
34%
-12%
47%
-60%
0%
Yield of 10-year Exchange Fund bills and notes
31%
-5%
41%
-58%
0%
Stock
Hang Seng Index
11%
47%
-28%
-34%
-53%
Hang Seng Finance Index
5%
48%
-30%
-29%
-44%
Hang Seng China Enterprises (H Share) Index
-1%
29%
-17%
-39%
-46%
Total market capitalization
26%
59%
-24%
-23%
-43%
P/E ratio for Hang Seng Index
19%
76%
24%
14%
5%
P/E ratio for Hang Seng Finance Index
9%
78%
27%
19%
7%
P/E ratio for all Hong Kong stocks
32%
69%
27%
22%
-3%
Dividend yield ratio for Hang Seng Index
-24%
-49%
-30%
-43%
1%
Dividend yield ratio for Hang Seng Finance Index
-41%
-47%
-14%
-42%
9%
Dividend yield ratio for all Hong Kong stocks
-52%
-37%
-29%
-35%
8%
Stock market turnover
16%
34%
-16%
-21%
-41%
Loans
Total loans
73%
-41%
-3%
18%
-15%
Hong Kong Dollar loans
49%
-35%
8%
8%
-12%
Foreign currency loans
78%
-28%
-10%
24%
-13%
Money
M1
-3%
16%
-48%
-19%
-7%
M2
25%
-8%
-11%
-8%
-70%
M3
26%
-10%
-11%
-8%
-70%
Currency in circulation
6%
0%
-3%
-6%
-9%
Price
CPI: meals away from home
58%
-61%
-20%
20%
-4%
CPI: food, excluding meals away from home
60%
-38%
-12%
37%
9%
CPI: alcoholic drinks and tobacco
4%
-11%
-39%
-25%
0%
CPI: clothing and footwear
34%
-21%
0%
-11%
-21%
CPI: durable goods
33%
3%
-29%
24%
-25%
CPI: miscellaneous goods
36%
-1%
-29%
39%
-4%
CPI: Transport
53%
-18%
12%
32%
6%
CPI
66%
-62%
-6%
20%
-3%
CPI: Housing
44%
-67%
-1%
5%
-5%
CPI: electricity, gas and water
27%
8%
0%
13%
12%
CPI: miscellaneous services
51%
-20%
10%
31%
0%
GDP deflator
42%
-40%
-19%
5%
-35%
Output
PMI
10%
47%
-7%
-37%
-27%
Real GDP
49%
57%
29%
-10%
-29%
Real GDP: private consumption
55%
28%
-3%
-26%
-31%
Real GDP: gross fixed capital formation
-7%
1%
2%
22%
-8%
Real GDP: government consumption
-8%
5%
-11%
17%
-33%
Inventory-to-GDP ratio
35%
3%
34%
8%
10%
Real GDP: exports of goods
32%
55%
31%
5%
-21%
Real GDP: exports of services
23%
42%
21%
1%
-19%
Real GDP: imports of goods
39%
57%
34%
3%
-21%
Real GDP: imports of services
34%
25%
10%
0%
-23%
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 35

32 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
 
 
Retail sales
Retail sales value
68%
12%
2%
11%
-11%
Retail sales volume
53%
21%
4%
2%
-11%
Labour
Labour force participation rate
-53%
36%
7%
-13%
8%
Unemployment rate
-64%
-21%
-37%
-16%
13%
Median weekly working hours
7%
39%
43%
22%
12%
Youth unemployment rate (age: 15-19)
-36%
-4%
-16%
-20%
-12%
Median duration of unemployment
15%
65%
17%
-15%
22%
Nominal wage index
61%
-34%
-12%
17%
-9%
Real wage index
-8%
4%
-3%
10%
10%
Property market
Property sales and purchases value
29%
22%
-11%
-39%
6%
Property sales and purchases volume
33%
30%
-39%
-28%
9%
Property price index: residential
86%
14%
-34%
-21%
18%
Property price index for large residential properties
80%
35%
-25%
-20%
20%
Property price index for small residential properties
86%
12%
-35%
-21%
18%
Centa City Leading Index
75%
31%
-44%
-15%
21%
Centa City Index
79%
28%
-33%
-22%
26%
Centa City Leading Index for mass estate
72%
28%
-50%
-17%
22%
Centa City Leading Index for large properties
77%
39%
-30%
-2%
23%
Centa City Leading Index for small properties
74%
28%
-47%
-17%
21%
Centa City Index for mass estate
79%
24%
-34%
-25%
27%
Centa City Index for large properties
79%
42%
-25%
-11%
20%
Centa City Index for small properties
79%
25%
-35%
-24%
26%
Property rental index: residential
87%
8%
10%
9%
6%
Property rental index for large residential properties
78%
11%
30%
21%
8%
Property rental index for small residential properties
88%
8%
7%
7%
6%
Property price index: office
86%
26%
-13%
-5%
10%
Property price index: grade A office
79%
34%
-9%
-6%
12%
Property price index: grade A office in core districts
76%
34%
-9%
-10%
24%
Property rental index: office
69%
-32%
38%
29%
-5%
Property rental index: grade A office
64%
-32%
40%
31%
-1%
Property price index: retail premise
84%
19%
-16%
-21%
9%
Property rental index: retail premise
76%
-10%
14%
11%
-24%
Property price index: flatted factories
89%
-6%
11%
-5%
-2%
Property rental index: flatted factories
81%
-24%
7%
14%
-12%
Trade
Trade balance (% of total export)
-45%
57%
27%
13%
0%
Terms of trade index
-32%
-30%
-21%
-5%
-22%
Import values
54%
53%
34%
11%
-19%
Export values
45%
49%
34%
14%
-24%
Quantum index for import
41%
60%
33%
6%
-22%
Quantum index for export
30%
56%
33%
10%
-24%
Unit value index for import
69%
-10%
17%
35%
-6%
Unit value index for export
58%
-28%
7%
35%
-17%
Capital flow indicators
Monetary base (capital flow)
-15%
-8%
-28%
-6%
-25%
Current account balance (% of GDP)
-14%
-2%
20%
31%
-26%
Capital account balance (% of GDP)
-2%
-3%
4%
12%
-3%
Financial Stability indicators
HSI Volatility Index (VHSI)
-10%
-16%
8%
39%
-7%
New mortgage loans
31%
39%
-39%
-29%
3%
Average market LTV ratio for new mortgage loans
-18%
10%
-14%
-13%
5%
Average contract life for new mortgage loans (no. of months)
30%
-7%
-22%
1%
7%
Problem loan ratio for mortgage loans
-58%
10%
-33%
10%
-8%
Classified loan ratio (gross)
60%
-69%
-20%
-4%
-18%
Overdue (>3 months) and rescheduled loan ratio
-59%
64%
20%
8%
16%
Net interest margin
-58%
59%
21%
20%
17%
Bad debt charge as percentage of average total assets
-63%
54%
-14%
16%
-4%
Cost-to-income ratio
39%
-48%
-24%
-14%
-5%
Capital adequacy ratio (CAR)
-42%
40%
1%
-9%
12%
Credit card loans
42%
-74%
-25%
-11%
-18%
Credit card delinquency ratio
-62%
62%
9%
-4%
21%
Household leverage
6%
12%
-52%
-4%
7%
Loan-to-GDP ratio
55%
-38%
-15%
7%
-4%
Loan-to-deposit (LTD) ratio
59%
-43%
1%
9%
27%
HKD Loan-to-deposit (LTD) ratio
44%
-22%
19%
19%
63%
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 36

33 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Table 3 Contribution of the US monetary policy shock to the variance of forecasting errors of 
selected variables 
  
Note: The column titled “Variance decomposition” reports the fraction of the variance of the forecast error, at 
the 16-quarter horizon, explained by the US monetary policy shock variable. “R2” refers to the fraction of the 
variance of the variable explained by the common factors, which includes five principal components and the 
US monetary policy shock variable. 
 
 
 
Variables
Variance decomposition
R2
HKD NEER
0.044
0.492
3-month HIBOR
0.319
0.487
Hang Seng Index
0.086
0.684
Loans
0.084
0.620
M1
0.149
0.268
M3
0.304
0.615
CPI
0.090
0.687
PMI
0.059
0.435
Real GDP
0.148
0.730
Retail sales
0.065
0.488
Import values
0.127
0.738
Export values
0.160
0.634
Unemployment rate
0.159
0.610
Property sales and purchases volume
0.031
0.430
Property price index: residential
0.036
0.985
Property price index for large residential properties
0.032
0.960
Property price index for small residential properties
0.038
0.977
Centa City Index
0.041
0.977
Centa City Index for large properties
0.029
0.972
Centa City Index for small properties
0.043
0.970
Monetary base (capital flow)
0.420
0.238
Current account balance (% of GDP)
0.148
0.221
Capital account balance (% of GDP)
0.091
0.018
Household leverage
0.352
0.272
Loan-to-GDP ratio
0.100
0.396
New mortgage loans
0.034
0.480
Average market LTV ratio for new mortgage loans
0.110
0.068
Classified loan ratio
0.062
0.744
Credit card delinquency ratio
0.165
0.693
Net interest margin
0.177
0.700
Capital adequacy ratio (CAR)
0.231
0.286
HKD Loan-to-deposit (LTD) ratio
0.173
0.653
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 37

34 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Table 4 Contributions of various shock variables to the variance of forecasting errors of selected 
variables 
  
Note: The column titled “Variance decomposition” reports the fraction of the variance of the forecast error, at 
the 16-quarter horizon, explained by the individual shock variable (monetary policy shocks by the Fed, ECB 
and BoJ, and Mainland China GDP). “R2” refers to the fraction of the variance of the variable explained by 
the common factors, which includes five principal components plus four shock variables. 
 
 
 
Variables
R2
US
shadow
rate
Euro
Area
shadow
rate
Japan
shadow
rate
Mainland
China
GDP
HKD NEER
0.032
0.037
0.030
0.402
0.507
3-month HIBOR
0.291
0.087
0.038
0.168
0.472
Hang Seng Index
0.092
0.100
0.174
0.071
0.693
Loans
0.116
0.132
0.045
0.218
0.626
M1
0.096
0.255
0.073
0.089
0.304
M3
0.255
0.119
0.123
0.102
0.615
CPI
0.099
0.098
0.107
0.105
0.718
PMI
0.092
0.224
0.118
0.114
0.488
Real GDP
0.219
0.096
0.054
0.125
0.730
Retail sales
0.089
0.237
0.049
0.213
0.512
Import values
0.179
0.134
0.075
0.134
0.740
Export values
0.190
0.163
0.081
0.087
0.660
Unemployment rate
0.215
0.112
0.069
0.162
0.614
Property sales and purchases volume
0.080
0.185
0.132
0.095
0.451
Property price index: residential
0.035
0.064
0.071
0.134
0.986
Property price index for large residential properties
0.046
0.072
0.071
0.166
0.970
Property price index for small residential properties
0.036
0.064
0.071
0.132
0.979
Centa City Index
0.039
0.075
0.065
0.138
0.979
Centa City Index for large properties
0.026
0.059
0.068
0.171
0.975
Centa City Index for small properties
0.042
0.076
0.066
0.133
0.973
Monetary base (capital flow)
0.331
0.111
0.121
0.092
0.289
Current account balance (% of GDP)
0.186
0.272
0.047
0.032
0.253
Capital account balance (% of GDP)
0.179
0.320
0.173
0.085
0.048
Household leverage
0.329
0.046
0.148
0.159
0.371
Loan-to-GDP ratio
0.098
0.156
0.080
0.187
0.423
New mortgage loans
0.069
0.250
0.143
0.088
0.523
Average market LTV ratio for new mortgage loans
0.102
0.224
0.273
0.072
0.117
Classified loan ratio
0.075
0.019
0.061
0.251
0.735
Credit card delinquency ratio
0.168
0.102
0.038
0.112
0.698
Net interest margin
0.120
0.019
0.080
0.062
0.718
Capital adequacy ratio (CAR)
0.118
0.040
0.234
0.422
0.373
HKD Loan-to-deposit (LTD) ratio
0.175
0.054
0.134
0.092
0.698
Variance decomposition
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 38

35 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 1 Policy Rates and Shadow Policy Rates 
A. The US (Fed) 
 
B. Euro Area (ECB) 
 
C. Japan (BoJ) 
 
Sources: CEIC, Wu and Xia (2014) and Krippner (2014). 
Electronic copy available at: https://ssrn.com/abstract=2797976

![Page 38 image 1](assets/Chen%2C%20Tsang%20%282016%29%20The%20Impact%20of%20US%20Monetary%20Policy%20and%20Other%20External%20Shocks%20on%20the%20Hong%20Kong%20Economy/page-038-img-01.jpeg)

![Page 38 image 2](assets/Chen%2C%20Tsang%20%282016%29%20The%20Impact%20of%20US%20Monetary%20Policy%20and%20Other%20External%20Shocks%20on%20the%20Hong%20Kong%20Economy/page-038-img-02.jpeg)

![Page 38 image 3](assets/Chen%2C%20Tsang%20%282016%29%20The%20Impact%20of%20US%20Monetary%20Policy%20and%20Other%20External%20Shocks%20on%20the%20Hong%20Kong%20Economy/page-038-img-03.jpeg)

## Page 39

36 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 2 Impulse responses for selected Hong Kong variables to the monetary policy shock of the 
Fed 
 
A: Macroeconomic and financial variables 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
HKD NEER
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
3-month HIBOR
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.3
-0.2
-0.1
0.0
0.1
0.2
0.3
0.4
0
4
8
12
16
Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
M1
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M3
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Real GDP
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Retail Sales
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Unemployment Rate
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Property Transaction
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Large)
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Centa City Index (CCI)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Large)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
CCI (Small)
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Imports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 40

37 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Monetary Base
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Current Account Balance
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Capital Account Balance
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
New Mortgage Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Classified Loan Ratio
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CAR
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Credit Card Delinquency
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 41

38 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 3 Contribution of US monetary Policy to Hong Kong Economic Activity 
 
 
 
Electronic copy available at: https://ssrn.com/abstract=2797976

![Page 41 image 1](assets/Chen%2C%20Tsang%20%282016%29%20The%20Impact%20of%20US%20Monetary%20Policy%20and%20Other%20External%20Shocks%20on%20the%20Hong%20Kong%20Economy/page-041-img-01.jpeg)

## Page 42

39 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 4 Impulse responses for selected Hong Kong variables to the monetary policy shock of ECB 
 
A: Macroeconomic and financial variables 
 
 
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0.5
0
4
8
12
16
HKD NEER
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
3-month HIBOR
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.4
-0.3
-0.2
-0.1
0.0
0.1
0.2
0
4
8
12
16
Loans
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
PMI
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Real GDP
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Retail Sales
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Unemployment Rate
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Transaction
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Price
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Property Price (Large)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Price (Small)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Centa City Index (CCI)
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
CCI (Large)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Exports
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Euro Area Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 43

40 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Monetary Base
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Current Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Capital Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
New Mortgage Loans
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Market LTV
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Classified Loan Ratio
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CAR
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 44

41 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 5 Impulse responses for selected Hong Kong variables to the monetary policy shock of BoJ 
 
A: Macroeconomic and financial variables 
 
 
 
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD NEER
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
3-month HIBOR
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.4
-0.2
0.0
0.2
0.4
0.6
0
4
8
12
16
Loans
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Real GDP
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Retail Sales
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Unemployment Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Transaction
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price (Small)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Centa City Index (CCI)
-1
-0.5
0
0.5
1
0
4
8
12
16
CCI (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Small)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Exports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Japan Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 45

42 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Monetary Base
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Current Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Capital Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
New Mortgage Loans
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Market LTV
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Classified Loan Ratio
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CAR
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 46

43 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 6 Impulse responses for selected Hong Kong variables to Mainland China GDP shock 
 
A: Macroeconomic and financial variables 
 
 
 
 
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
HKD NEER
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
3-month HIBOR
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.3
-0.2
-0.1
0.0
0.1
0.2
0
4
8
12
16
Loans
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
PMI
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Real GDP
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Retail Sales
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0.5
0
4
8
12
16
Unemployment Rate
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Transaction
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price (Large)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price (Small)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Centa City Index (CCI)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CCI (Large)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Exports
-0.4
-0.3
-0.2
-0.1
0
0.1
0
4
8
12
16
Mainland China GDP
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 47

44 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Monetary Base
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Current Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Capital Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
New Mortgage Loans
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Classified Loan Ratio
-0.2
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
Net Interest Margin
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
CAR
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Credit Card Delinquency
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 48

45 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 7 Impulse responses for selected Hong Kong variables to the Mainland China GDP shock in 
the model with both US monetary policy shock and Mainland growth 
 
A: Macroeconomic and financial variables 
 
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
HKD NEER
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
3-month HIBOR
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.3
-0.2
-0.1
0.0
0.1
0.2
0
4
8
12
16
Loans
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Real GDP
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Retail Sales
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Unemployment Rate
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Transaction
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Price
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Price (Large)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Property Price (Small)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Centa City Index (CCI)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CCI (Large)
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Exports
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Mainland China GDP
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 49

46 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Monetary Base
-0.5
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Current Account Balance
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Capital Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
New Mortgage Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Classified Loan Ratio
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Net Interest Margin
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CAR
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 50

47 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 8 Impulse responses for selected Hong Kong variables to the monetary policy shock of the 
Fed in the full model 
 
A: Macroeconomic and financial variables 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD NEER
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
3-month HIBOR
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.3
-0.2
-0.1
0.0
0.1
0.2
0.3
0.4
0.5
0
4
8
12
16
Loans
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M3
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0.5
0
4
8
12
16
CPI
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Real GDP
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Retail Sales
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Unemployment Rate
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Transaction
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price (Large)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Centa City Index (CCI)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Large)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 51

48 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Monetary Base
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Current Account Balance
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Capital Account Balance
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
New Mortgage Loans
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Classified Loan Ratio
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
CAR
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 52

49 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 9 Impulse responses for selected Hong Kong variables to the monetary policy shock of ECB 
in the full model 
 
A: Macroeconomic and financial variables 
 
-1
-0.5
0
0.5
1
0
4
8
12
16
HKD NEER
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
3-month HIBOR
-1
-0.5
0
0.5
1
0
4
8
12
16
Hang Seng Index
-1.2
-1.0
-0.8
-0.6
-0.4
-0.2
0.0
0.2
0.4
0
4
8
12
16
Loans
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M1
-1
-0.5
0
0.5
1
0
4
8
12
16
M3
-1.5
-1
-0.5
0
0.5
0
4
8
12
16
CPI
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
PMI
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Real GDP
-1
-0.5
0
0.5
1
0
4
8
12
16
Retail Sales
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Unemployment Rate
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Transaction
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Price
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Price (Large)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Price (Small)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Centa City Index (CCI)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
CCI (Large)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
CCI (Small)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Imports
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Exports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Euro Area Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 53

50 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Monetary Base
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Current Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Capital Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
New Mortgage Loans
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Market LTV
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Classified Loan Ratio
-0.4
-0.2
0
0.2
0.4
0.6
0.8
1
0
4
8
12
16
Net Interest Margin
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CAR
-0.5
0
0.5
1
1.5
0
4
8
12
16
Credit Card Delinquency
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Household Leverage
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Loan-to-GDP Ratio
-1
-0.5
0
0.5
1
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 54

51 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 10 Impulse responses for selected Hong Kong variables to the monetary policy shock of BoJ 
in the full model 
 
A: Macroeconomic and financial variables 
 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD NEER
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
3-month HIBOR
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Hang Seng Index
-0.4
-0.3
-0.2
-0.1
0.0
0.1
0.2
0.3
0
4
8
12
16
Loans
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Real GDP
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Retail Sales
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Unemployment Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Transaction
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Small)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Centa City Index (CCI)
-1
-0.5
0
0.5
1
0
4
8
12
16
CCI (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Exports
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Japan Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 55

52 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
 
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Monetary Base
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Current Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Capital Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
New Mortgage Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Classified Loan Ratio
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CAR
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Household Leverage
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 56

53 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 11 Aggregate impact of monetary policy shocks of the Fed, ECB and BoJ on selected Hong 
Kong variables in the full model with Mainland economic slowdown turned off 
 
A: Macroeconomic and financial variables 
 
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
HKD NEER
-1
-0.5
0
0.5
1
0
4
8
12
16
3-month HIBOR
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Hang Seng Index
-1.5
-1.0
-0.5
0.0
0.5
1.0
0
4
8
12
16
Loans
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M1
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
M3
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
CPI
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
PMI
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Real GDP
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Retail Sales
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Unemployment Rate
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Transaction
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Price
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Property Price (Large)
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Property Price (Small)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Centa City Index (CCI)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
CCI (Large)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
CCI (Small)
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Imports
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Euro Area Shadow Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Japan Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 57

54 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-1
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Monetary Base
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Current Account Balance
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Capital Account Balance
-1
-0.5
0
0.5
1
0
4
8
12
16
New Mortgage Loans
-1
-0.5
0
0.5
1
0
4
8
12
16
Market LTV
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Classified Loan Ratio
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Net Interest Margin
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
1
0
4
8
12
16
CAR
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Credit Card Delinquency
-1
-0.5
0
0.5
1
0
4
8
12
16
Household Leverage
-1
-0.5
0
0.5
1
0
4
8
12
16
Loan-to-GDP Ratio
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 58

55 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 12 Aggregate impact of monetary policy shocks of the Fed, ECB and BoJ and Mainland 
economic slowdown on selected Hong Kong variables in the full model 
 
A: Macroeconomic and financial variables 
 
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
HKD NEER
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
3-month HIBOR
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Hang Seng Index
-1.5
-1.0
-0.5
0.0
0.5
1.0
0
4
8
12
16
Loans
-1
-0.5
0
0.5
1
0
4
8
12
16
M1
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
M3
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
CPI
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
PMI
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Real GDP
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Retail Sales
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Unemployment Rate
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Property Transaction
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Property Price
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Property Price (Large)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Property Price (Small)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Centa City Index (CCI)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
CCI (Large)
-2
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
CCI (Small)
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Imports
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Euro Area Shadow Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Japan Shadow Rate
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Mainland China GDP
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 59

56 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-1
-0.5
0
0.5
1
0
4
8
12
16
Monetary Base
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Current Account Balance
-1
-0.5
0
0.5
1
0
4
8
12
16
Capital Account Balance
-1
-0.5
0
0.5
1
0
4
8
12
16
New Mortgage Loans
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Market LTV
-1.5
-1
-0.5
0
0.5
1
0
4
8
12
16
Classified Loan Ratio
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Net Interest Margin
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
1
0
4
8
12
16
CAR
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
Credit Card Delinquency
-1
-0.5
0
0.5
1
0
4
8
12
16
Household Leverage
-1
-0.5
0
0.5
1
0
4
8
12
16
Loan-to-GDP Ratio
-1.5
-1
-0.5
0
0.5
1
1.5
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 60

57 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 13 Comparison of standard VAR model and FAVAR model – impulse responses for 
selected Hong Kong macroeconomic variables to the monetary policy shock of the Fed 
 
 
Note: The red line indicates the estimated impulse response based on standard 6-variable VAR model, and 
the blue line is the estimated impulse response based on 5-factor FAVAR model (same as the 
corresponding charts in Figure 2). All the charts are in standard deviation units. 
 
-0.20
-0.15
-0.10
-0.05
0.00
0.05
0.10
0.15
0
4
8
12
16
CPI
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Real GDP
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price
-0.20
-0.15
-0.10
-0.05
0.00
0.05
0.10
0.15
0
4
8
12
16
Monetary Base
-0.3
-0.2
-0.2
-0.1
-0.1
0.0
0.1
0.1
0
4
8
12
16
Household Leverage
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 61

58 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 14 Impulse responses for selected Hong Kong variables to the monetary policy shock of the 
Fed (since 2008) 
 
A: Macroeconomic and financial variables 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD NEER
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0.5
0
4
8
12
16
3-month HIBOR
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Hang Seng Index
-0.4
-0.2
0.0
0.2
0.4
0.6
0
4
8
12
16
Loans
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M1
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M3
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
PMI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Real GDP
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Retail Sales
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Unemployment Rate
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Transaction
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Price (Small)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Centa City Index (CCI)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
CCI (Large)
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 62

59 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-1
-0.5
0
0.5
1
0
4
8
12
16
Monetary Base
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Current Account Balance
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Capital Account Balance
-1
-0.5
0
0.5
1
0
4
8
12
16
New Mortgage Loans
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Market LTV
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Classified Loan Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Net Interest Margin
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CAR
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Credit Card Delinquency
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Household Leverage
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 63

60 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 15 Impulse responses for selected Hong Kong variables to the monetary policy shock of the 
Fed (estimated by Gibbs Sampling approach) 
 
A: Macroeconomic and financial variables 
 
 
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
HKD NEER
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
3-month HIBOR
-1
-0.5
0
0.5
1
0
4
8
12
16
Hang Seng Index
-0.6
-0.4
-0.2
0.0
0.2
0.4
0
4
8
12
16
Loans
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
M1
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
M3
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
CPI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
PMI
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Real GDP
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Retail Sales
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Unemployment Rate
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Property Transaction
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price
-0.4
-0.2
0
0.2
0.4
0.6
0.8
1
0
4
8
12
16
Property Price (Large)
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Property Price (Small)
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Centa City Index (CCI)
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Large)
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
CCI (Small)
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Imports
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 64

61 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
 
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Monetary Base
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Current Account Balance
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Capital Account Balance
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
New Mortgage Loans
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Market LTV
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Classified Loan Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Net Interest Margin
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
CAR
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Credit Card Delinquency
-0.8
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Household Leverage
-0.6
-0.4
-0.2
0
0.2
0.4
0
4
8
12
16
Loan-to-GDP Ratio
-0.6
-0.4
-0.2
0
0.2
0.4
0.6
0.8
1
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 65

62 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
Figure 16 Impulse responses for selected Hong Kong variables to the monetary policy shock of the 
Fed (estimated by Structual FAVAR, factors extracted from variables by groups) 
 
A: Macroeconomic and financial variables 
 
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
HKD NEER
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
3-month HIBOR
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Hang Seng Index
-0.2
-0.2
-0.1
-0.1
0.0
0.1
0.1
0.2
0.2
0
4
8
12
16
Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
M1
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
M3
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
CPI
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
PMI
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Real GDP
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Retail Sales
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Unemployment Rate
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Property Transaction
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price (Large)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Property Price (Small)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Centa City Index (CCI)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CCI (Large)
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
CCI (Small)
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Imports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
Exports
-0.4
-0.2
0
0.2
0.4
0.6
0
4
8
12
16
US Shadow Rate
Electronic copy available at: https://ssrn.com/abstract=2797976

## Page 66

63 
Hong Kong Institute for Monetary Research  
 
 
 
 
     
 
 
Working Paper No.09/2016 
B: Capital flow and financial stability variables 
 
Note: The red line indicates the estimated median response. The solid blue and green lines represent the 
68 percent bootstrap confidence interval, and the dashed blue and green lines represent the 90 percent 
bootstrap confidence interval based on 1,000 bootstrap samples. All the charts are in standard deviation 
units. 
 
 
 
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Monetary Base
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0
4
8
12
16
Current Account Balance
-0.4
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
0.4
0
4
8
12
16
Capital Account Balance
-0.2
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
New Mortgage Loans
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Market LTV
-0.1
-0.05
0
0.05
0.1
0
4
8
12
16
Classified Loan Ratio
-0.2
-0.15
-0.1
-0.05
0
0.05
0.1
0
4
8
12
16
Net Interest Margin
-0.1
-0.05
0
0.05
0.1
0.15
0.2
0
4
8
12
16
CAR
-0.2
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0
4
8
12
16
Credit Card Delinquency
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
Household Leverage
-0.2
-0.15
-0.1
-0.05
0
0.05
0.1
0.15
0
4
8
12
16
Loan-to-GDP Ratio
-0.3
-0.2
-0.1
0
0.1
0.2
0
4
8
12
16
HKD LTD ratio
Electronic copy available at: https://ssrn.com/abstract=2797976
