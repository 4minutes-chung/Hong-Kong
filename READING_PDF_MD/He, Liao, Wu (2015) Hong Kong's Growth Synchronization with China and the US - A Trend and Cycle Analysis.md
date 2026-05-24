# He, Liao, Wu (2015) Hong Kong's Growth Synchronization with China and the US - A Trend and Cycle Analysis

## Page 1

Hong Kong’s growth synchronization with China and the US:
A trend and cycle analysis§
Dong He a,1, Wei Liao a,1, Tommy Wu b,*
a International Monetary Fund, United States
b Hong Kong Monetary Authority, Hong Kong SAR
1. Introduction
Hong Kong has become increasingly integrated with the economy of mainland China. Headline numbers of trade and
ﬁnancial ﬂows seem to suggest that mainland China is now playing a dominant role in driving Hong Kong’s economic cycles.
Yet, these headline ﬁgures, particularly of trade data, have masked the underlying driving forces behind the cross-border
ﬂows in goods and services. Indeed, given the Mainland’s status as the ‘‘world’s factory,’’ a good chunk of production goes to
serving ﬁnal demand from foreign countries rather than domestic demand on the Mainland itself. And ﬂuctuations in ﬁnal
demand from foreign economies have been very much driven by ﬂuctuations of the US economy, reﬂecting its status as the
Journal of Asian Economics 40 (2015) 10–28
A R T I C L E 
I N F O
Article history:
Received 19 December 2014
Received in revised form 13 August 2015
Accepted 22 August 2015
Available online 31 August 2015
JEL classiﬁcation:
C32
E21
E32
F44
Keywords:
Business cycle synchronization
Permanent income hypothesis
Stochastic trend
Structural vector autoregression
A B S T R A C T
This paper investigates the synchronization of Hong Kong’s economic growth with
mainland China and the US. We identify trends of economic growth based on the
permanent income hypothesis. Speciﬁcally, we ﬁrst conﬁrm whether real consumption in
Hong Kong and mainland China satisﬁes the permanent income hypothesis, at least in a
weak form. We then identify the permanent and transitory components of income of each
economy using a simple state-space model. We use structural vector autoregression
models to analyze how permanent and transitory shocks originating from mainland China
and the US affect the Hong Kong economy, and how such inﬂuences evolve over time. Our
main ﬁndings suggest that transitory shocks from the US remain a major driving force
behind Hong Kong’s business cycle ﬂuctuations. On the other hand, permanent shocks
from mainland China have a larger impact on Hong Kong’s trend growth.
 2015 Elsevier Inc. All rights reserved.
§ The authors would like to thank our colleagues at the Hong Kong Monetary Authority, the Hong Kong Institute for Monetary Research and the
International Monetary Fund for their helpful discussions and comments. We would especially like to thank Ka-Fai Li and anonymous referees for their
useful suggestions, and Rondy Wong for excellent research assistance. The views expressed in this paper are those of the authors, and do not necessarily
reﬂect those of the Hong Kong Monetary Authority, International Monetary Fund, Hong Kong Institute for Monetary Research, its Council of Advisers, or the
Board of Directors. All errors are ours.
* Corresponding author at: Hong Kong Monetary Authority, 55th Floor, Two International Finance Centre, 8 Finance Street, Central, Hong Kong SAR.
Tel.: +852 2878 8070.
E-mail addresses: dhe@imf.org (D. He), wliao@imf.org (W. Liao), ttowu@hkma.gov.hk (T. Wu).
1 Address: International Monetary Fund, 700 19th St. NW, Washington DC 20431, United States.
Contents lists available at ScienceDirect
Journal of Asian Economics
http://dx.doi.org/10.1016/j.asieco.2015.08.003
1049-0078/ 2015 Elsevier Inc. All rights reserved.

![Page 1 image 1](assets/He%2C%20Liao%2C%20Wu%20%282015%29%20Hong%20Kong%27s%20Growth%20Synchronization%20with%20China%20and%20the%20US%20-%20A%20Trend%20and%20Cycle%20Analysis/page-001-img-01.jpeg)

![Page 1 image 2](assets/He%2C%20Liao%2C%20Wu%20%282015%29%20Hong%20Kong%27s%20Growth%20Synchronization%20with%20China%20and%20the%20US%20-%20A%20Trend%20and%20Cycle%20Analysis/page-001-img-02.jpeg)

![Page 1 image 3](assets/He%2C%20Liao%2C%20Wu%20%282015%29%20Hong%20Kong%27s%20Growth%20Synchronization%20with%20China%20and%20the%20US%20-%20A%20Trend%20and%20Cycle%20Analysis/page-001-img-03.jpeg)

## Page 2

largest economy in the world. Given Hong Kong’s linked exchange rate system (LERS), with the Hong Kong dollar pegging to
the US dollar, and its unique geographic location as a gateway between mainland China and the rest of the world, an
interesting and important question naturally arises: are Hong Kong’s business cycles more synchronized with those of the
Mainland economy or the US?
This paper studies the relative importance of mainland China and the US in driving Hong Kong’s economic cycles. On the
one hand, economic integration can be expected to intensify trade and ﬁnancial linkages between Hong Kong and the
Mainland, which can lead to a higher degree of the output co-movement. On the other hand, the US remains an important
source of inﬂuence for Hong Kong, particularly from the perspective of ﬁnal demand. In particular, US is the largest trading
partner of East Asia region, and the second largest trading partner of Hong Kong after mainland China. More importantly, as
discussed in Genberg (2005), the world macroeconomic conditions can very well be proxied by US macroeconomic
conditions. Global monetary conditions are also strongly inﬂuenced by US monetary policy stance, as clearly evidenced by
the impacts of US unconventional monetary policy on global capital ﬂows and asset price movements in the post-global
ﬁnancial crisis era. In addition, US inﬂuence can affect Hong Kong indirectly through trade with mainland China, as global
demand of Chinese goods and services are heavily inﬂuenced by the US as well.
The LERS reinforces the transmission of shocks from the US to the Hong Kong economy since Hong Kong shares a common
monetary policy with the US under the ﬁxed exchange rate regime. As a small open economy with free ﬂow of capital, it is
appropriate for Hong Kong to adopt the currency board system. In theory, it is most appropriate to peg the Hong Kong dollar
to the currency of an economy whose business cycles have the strongest synchronization with those of Hong Kong. As such, it
is useful to revisit the question of business cycle synchronization of the Hong Kong economy. Although there has been some
conjecture that the Hong Kong economy might have become more closely linked with the Mainland economy than with the
US, only a few studies such as Genberg et al. (2006) have analyzed this issue in a rigorous manner.
From a supply side perspective, the Hong Kong economy has successfully transformed itself from a manufacturing-
focused economy into a service-based economy in the past 20 years. Most of its manufacturing activity migrated north to
Guangdong province in mainland China. By contrast, ﬁnancial and business services have ﬂourished, and Hong Kong has
become a major international ﬁnancial center. At the same time, export and import related trade services have become the
largest source of value-added and employment. This process of transformation toward a service-based economy with higher
productivity has coincided and been very much driven by the rise of mainland China as a major trading nation and one of the
most important destinations of foreign direct investment in the global economy.
From a demand perspective, Hong Kong has primarily served as a gateway for trade and ﬁnancial ﬂows between the
Mainland and the rest of the world, and Hong Kong’s cyclical conditions are very much tied to ﬂuctuations in the volume of
ﬂows of goods, services, and capital between the Mainland and its major trading partners. Such a ‘‘bridge’’ role is likely to
remain important for Hong Kong’s economic future, even though trade and ﬁnancial ﬂows that are more closely linked to
developments in domestic demand on the Mainland will gain increasing signiﬁcance (see Genberg & He (2008)).
These two different perspectives point to the possibility that, in principle, the trend and cyclical components of Hong
Kong’s output growth may be driven by different external forces. We hypothesize that mainland China has been a more
important force in driving Hong Kong’s trend growth, but the US has maintained its position as a dominant force in driving
Hong Kong’s cyclical ﬂuctuations. This would be consistent with the observation by He and Liao (2012) that synchronized
supply shocks have contributed more to the observed synchronization in output ﬂuctuations among the Asian economies
than demand shocks.
We investigate the co-movement of output of Hong Kong, mainland China, and the US in terms of both stochastic trends
and the transitory cycles of income. Stochastic economic growth theory suggests that shocks to trend income are a result of
ﬂuctuations in the stochastic trend of productivity, which have a permanent impact on an economy. In contrast, transitory
productivity shocks and demand shocks only cause temporary ﬂuctuations of the economy in a cyclical manner.2 To
decompose output movements into trend and cycle, we take a theory-guided method and use real GDP data along with
consumption data to estimate the stochastic income trend of the economy of Hong Kong, mainland China, and the US,
respectively. This identiﬁcation strategy is built on Fama (1992), Cochrane (1994), Kim and Piger (2002), and Aguiar and
Gopinath (2007), in which real income and consumption data are used together to identify permanent income. In particular,
Aguiar and Gopinath (2007) show that using trends and cycles of income that are identiﬁed based on the permanent income
hypothesis in a business cycle model can well ﬁt the stylized facts of business cycles in emerging markets. We do not use
conventional ﬁltering techniques such as the HP ﬁlter to detrend the GDP time series because, as discussed in Cogley and
Nason (2000) and Estrella (2007), ﬁlters can yield inferior results and might artiﬁcially generate business cycle dynamics
even when there are none in the original data.
We ﬁrst conﬁrm whether real consumption in Hong Kong and mainland China satisﬁes the permanent income
hypothesis. Next, we derive the permanent and transitory component of income for Hong Kong, mainland China, and the US
2 While aging population would change the aggregate labor supply structure, here we argue that aging would change the extensive margin of labor
willing to work rather than the intensive margin. In other words, the marginal rate of substitution between labor and leisure is constant for each household.
Aging would work through the supply side as the number of workers decline in aggregate. Its effect enters into household’s consumption/savings choice
through decrease in income due to decline in aggregate production. In other words, even though aging has permanent effect, we think of it not as a
permanent demand shock (e.g. permanent shock to the labor supply elasticity or the marginal rate of substitution (MRS) between consumption and leisure)
but as a change in factor supply into the aggregate production function of an economy.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
11

## Page 3

by applying a simple state-space model on consumption and output data. We then make use of a hierarchical, structural
vector autoregression model to analyze how the permanent and transitory shocks originating from mainland China and the
US affect the Hong Kong economy, and how such inﬂuences evolve over time.
Our main ﬁndings suggest that the transitory shocks from the US remain a major driving force behind Hong Kong’s
business cycle ﬂuctuations. On the other hand, our results show that Hong Kong and mainland China share a strong co-
movement in terms of long-run trend growth. Permanent shocks originating from the Mainland have a substantial inﬂuence
on Hong Kong’s trend growth, likely reﬂecting the on-going progress of economic and social integration between the two
economies.
This paper is organized as follows. In Section 2, we provide some stylized facts on economic integration between Hong
Kong, mainland China, and the US. In Section 3, we estimate the stochastic income trend for each economy. Section 4
analyzes how permanent and transitory shocks from the Mainland and US affect the Hong Kong economy, and Section 5
concludes.
2. Stylized facts on economic integration
Commentary in the popular press has often argued that the inﬂuence of mainland China on the Hong Kong economy has
become dominant, especially over the past decade, as trade and ﬁnancial linkages have become increasingly tighter.
However, the headline ﬁgures are only informative about export destinations, rather than the origin of ﬁnal demand for
exports. It is noteworthy that a signiﬁcant proportion of the goods that are exported to the Mainland are re-exported to serve
the ﬁnal demand from advanced economies.
To illustrate the point, headline trade ﬁgures suggest that the share of Hong Kong’s merchandize and services exports to
the Mainland increased from about 33% in 2000 to 51% in 2012, while the US share declined slightly from 23% to 21% over the
same period. However, the picture looks very different if we exclude the import content and only account for the value-
added of exports. Appendix A describes how to compute value-added exports. As shown in Fig. 1, the share of merchandize
exports to the Mainland in value-added terms increased from 13% in 2000 to about 22% in 2012. The US share, though having
declined from about 34% a decade ago, was still around 25% in 2012. The US share would be even larger if we took into
account its inﬂuence on other export markets of Hong Kong, such as the euro area. These observations suggest that the
impact of US ﬁnal demand shocks could still be the dominating force that drives ﬂuctuations in the external demand for
goods in Hong Kong. Meanwhile, the US share in Hong Kong’s services exports excluding tourism services remained larger
than the Mainland’s share as shown in Fig. 2. This implies that the ﬁnal demand from the US in non-tourism services exports
remained larger than the demand from mainland China.
A point worth mentioning is that, within the category of Hong Kong’s ﬁnancial services export, US demand had been
rather stable over the past decade, accounted for 33% of the total in 2012 as shown in Fig. 3. Contrary, the Mainland’s share
remained low and had reached merely 4% in 2012. This fact is in contrast to the general misconception that the demand for
ﬁnancial services in Hong Kong is largely Mainland-driven. Indeed, Hong Kong has been transforming into an international
ﬁnancial center by providing intermediation services between users of funds and global investors. On the one hand, Hong
Kong ﬁnancial sector has become more productive in expanding the supply of ﬁnancial products, including initial public
offerings (IPOs) and renminbi bonds, to raise funds for Mainland corporations. On the other hand, Hong Kong has been
targeting overseas investors who are trying to gain exposure to Mainland-related ﬁnancial assets. In other words, overseas
investors have been driving the demand for Mainland-related ﬁnancial products supplied through Hong Kong, while the on-
going ﬁnancial integration between Hong Kong and Mainland can be considered a supply-side factor that contributes to
rising productivity of the Hong Kong economy.
0
5
10
15
20
25
30
35
40
200 0 2001 2002 20
 
03 20
 
04 200 5 200 6 2007 2008 20
 
09 201 0 201 1 201 2
The  US
Mainland  China
%
Fig. 1. Shares in Hong Kong merchandize exports (value-added).
Sources: CEIC; Hong Kong Census and Statistics Department (C&SD) and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
12

## Page 4

Reﬂecting the on-going ﬁnancial integration between Hong Kong and mainland China, Figs. 4 and 5 show that the
importance of the Mainland as a source of inward foreign direct investment (FDI) and as a destination of outward foreign
direct investment (ODI) has been increasing; in comparison, the US shares have been stable or declining in recent years.
Meanwhile, the stock market capitalization of Mainland companies in Hong Kong has increased since 2005, as shown in
0
5
10
15
20
25
30
35
40
200 0 2001 2002 2003 20
 
04 20
 
05 20
 
06 200 7 2008 2009 2010 20
 
11 20
 
12
The US
Main land  China
%
Fig. 2. Shares in Hong Kong services exports excluding tourism (value-added).
Sources: C&SD and authors’ estimates.
0
10
20
30
40
50
60
70
200 0 2001 2002 20
 
03 200 4 2005 2006 20
 
07 200 8 200 9 2010 2011 20
 
12
The U
 
S
Mainland China
%
Fig. 3. Shares in Hong Kong ﬁnancial services exports (value-added).
Sources: C&SD and authors’ estimates.
0
5
10
15
20
25
30
35
40
45
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
China 
US
% of tota l
Fig. 4. Hong Kong’s inward FDI positions by origin.
Sources: CEIC; C&SD and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
13

## Page 5

Fig. 6. The issuance of offshore renminbi bonds has increased substantially since 2010 as Hong Kong has evolved into a major
offshore renminbi center, as illustrated in Fig. 7.
At the same time, mainland China plays a dominant role as a tourism services export destination. Stripping out import
content, tourism services exports to the Mainland rose from 28% of total tourism services exports in 2000 to over 66% in
2012, whereas the US share dropped from 11% to 4% over the same period, as illustrated in Fig. 8. The secular trend in tourism
0
5
10
15
20
25
30
35
40
45
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
China 
US
% of tota l
Fig. 5. Hong Kong’s outward FDI positions by destination.
Sources: CEIC; C&SD and authors’ estimates.
0
10
20
30
40
50
60
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
% of  tota
 
l
Fig. 6. Share of mainland companies in Hong Kong stock market capitalization.
Sources: CEIC; HKEx and authors’ estimates.
0
20
40
60
80
100
120
2007 
2008 
200 9
20
 
10 
201 1
201
 
2 
2013
RMB  bn
Non-financ
 
ial ins
 
tit ution s
Financia
 
l insti tutio ns
Ministr y of  Finance
 
, China
Fig. 7. Issuance of offshore renminbi bonds in Hong Kong.
Source: Newswires.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
14

## Page 6

services exports to mainland China not only reﬂects the Mainland’s demand for Hong Kong’s tourism services, but has also
contributed to Hong Kong’s transformation toward a service-based economy over the past decade from a supply-side
perspective.
In sum, the size of Hong Kong’s service sector has been rising along with the increase in labor productivity as shown in
Fig. 9. This rise in labor productivity has been underpinned by strong total factor productivity (TFP) growth as a result of the
expansion of the service export sector. As suggested by Leung et al. (2009), a large part of TFP growth might have been
boosted by the increasing ﬁnancial linkages between Hong Kong and the Mainland given the high value-added content of
ﬁnancial services. These facts together point to the possibility that mainland China has been a major force affecting Hong
Kong’s trend growth.
3. Estimating trends and cycles
3.1. Model motivation
We adopt a theory-based method to identify trends and cycles in output data. A standard stochastic growth model can
help illustrate this point. In a basic one-sector growth model, output ðYtÞ is produced by capital ðKtÞ and labor ðLtÞ, and is
subject to exogenous growth in labor-augmenting technology, or trend productivity growth ðAtÞ:
Yt ¼ eztK1a
t
ðAtLtÞa
where a is the labor share, zt is a transitory productivity shock which has zero mean, and:
At ¼ egtAt1 ¼
Y
t
s¼0
egs
 
0
10
20
30
40
50
60
70
200 0 2001 2002 20
 
03 200 4 2005 2006 20
 
07 200 8 200 9 2010 2011 20
 
12
The US
Mainlan d Ch
 
ina
%
Fig. 8. Shares in Hong Kong tourism services exports (value-added).
Sources: C&SD and authors’ estimates.
80
90
100
110
120
130
140
150
2000 20
 
01 2002 2003 2004 2005 2006 200 7 2008 200 9 2010 2011 20
 
12
87
88
89
90
91
92
93
94
Total Services Ou 
tput / GDP (RH
 
S)
Lab our  Produc tivity
2000 = 100 
%
Fig. 9. Hong Kong’s labor productivity and service sector growth.
Sources: CEIC; C&SD and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
15

## Page 7

where the productivity trend At follows a random walk and gt is the shock to the stochastic trend. The realization of gt affects
At permanently, so output is a nonstationary process containing a stochastic trend.
The representative agent maximizes a standard lifetime utility function by choosing consumption ðCtÞ and labor ðLtÞ:
U ¼
X
1
t¼0
btuðCt; et; 1  LtÞ
where et denotes consumption shocks such as preference shocks following Smets and Wouters (2003) and Benhabib and
Wen (2004), which is a demand shock with a temporary effect. Agents optimally respond to productivity and demand shocks
by smoothing their consumption over time, and their response can be different when facing a permanent or transitory shock.
This comes to the permanent income hypothesis. The strict form of the hypothesis suggests that consumption only responds
to permanent shocks, conditional on the agents’ information on the type of shock. If a balanced growth path exists in the
above model, output and consumption will grow at a rate determined by trend growth ðgtÞ. In other words, output and
consumption will share a common stochastic trend.
Guidance from this theoretical model can help to identify permanent and transitory shocks to output that are
indistinguishable in the raw data. Speciﬁcally, we can treat the common stochastic trend shared by output and consumption
as a measure of permanent income. Previous studies have used consumption and output data to identify a trend component
ðAtÞ of output using the permanent income hypothesis as an identiﬁcation scheme, see for example Fama (1992), Cochrane
(1994), Kim and Piger (2002), and Aguiar and Gopinath (2007). Following this literature, we make use of a simple state-space
model to identify the common stochastic trend between output and consumption as the ‘‘permanent income.’’ The difference
between actual output and the estimated permanent income is the ‘‘transitory income.’’ As a robustness check, we follow
Kim and Piger (2002) who use consumption as a proxy for the stochastic trend of output, and decompose output into its trend
and cycle accordingly as shown in Appendix D.
Next, we investigate whether consumption data in Hong Kong and mainland China is consistent with the permanent
income hypothesis. We then introduce a state-space model that we use to decompose output into trend and cycle.
3.2. Tests for permanent income hypothesis
The data we use are real GDP and real consumption for Hong Kong, mainland China, and the US at quarterly frequency.
The sample period ends in the second quarter of 2013. Seasonally adjusted real GDP data for Hong Kong starts from the ﬁrst
quarter of 1973, and the series for the US starts from the ﬁrst quarter of 1947.3 The quarterly real GDP series for mainland
China is constructed based on several GDP and deﬂator series, and requires our own compilation. The constructed series
begins from the ﬁrst quarter of 1978.4
As for real consumption data, we use headline real personal consumption expenditure (PCE) for Hong Kong and the US.
Since quarterly real consumption data for mainland China is not available, we use the interpolation procedures described in
Chow and Lin (1971) and Bloem, Dippelsman, and Maehle (2001) to estimate the quarterly real consumption based on real
retail sales and annual real consumption data. The real retail sales series starts from the ﬁrst quarter of 1985.5
The use of US consumption and output data to construct permanent income has been well studied in the literature. We
therefore assume that the permanent income hypothesis holds for US consumption, at least in a weak form. To test whether the
hypothesis holds for consumption in Hong Kong and mainland China, we investigate whether a common stochastic trend
between output and consumption exists by (1) testing the stationarity of the gap between output and consumption, (2)
conducting the Johnasen cointegration tests, and (3) estimating a vector error correction model (VECM) to test if consumption is
not predictable by anticipated transitory income change and follows a random walk as suggested by Hall (1978).
The simplest way of testing whether output and consumption are cointegrated is to test whether the gap between the two
is stationary. The gap is given by ˆzt ¼ yt  ˆa  ˆbct, where yt and ct are the logarithm of real GDP and consumption,
respectively, and ˆa and ˆb are the OLS estimates from a simple regression of output on consumption, both in logarithmic
terms.
Table 1 shows unit root test results on the log of real GDP, log consumption, and the gap between the two for Hong Kong
and mainland China, respectively.6 We cannot reject a unit root for output and consumption data for Hong Kong and
3 Seasonally adjusted real GDP data for Hong Kong only goes back to the ﬁrst quarter of 1990, so we use X12-ARIMA to perform seasonal adjustment on
Hong Kong real GDP data between 1973 and 1989.
4 The series used for constructing the real GDP series for mainland China includes quarterly real GDP growth data which is not available until after the
fourth quarter of 2010, year-on-year real GDP growth which goes back to the fourth quarter of 1999, year-to-date year-on-year growth which goes back to
the fourth quarter of 1991, quarterly nominal GDP data which starts from 1978, and annual nominal and real GDP growth which helps to generate a proxy
for the GDP deﬂator for the period between 1978 and 1991.
5 Real retail sales data are constructed using the nominal retail sales data deﬂated by the consumer price inﬂation. An index of annual real consumption is
constructed using annual real consumption growth with 2002 as the base year. Note that even though real retail sales is cointegrated with real GDP
according to cointegration tests that we conduct, the series does not represent value-added consumption, unlike the PCE series used for Hong Kong and the
US. The resulting estimate of the stochastic trend may not necessarily capture real permanent income in terms of value-added. The use of estimated real
consumption data, however, can circumvent this problem.
6 The output-consumption gap for Hong Kong is ˆzt ¼ yt þ 0:07  0:97ct. The gap for mainland China is ˆzt ¼ yt  1:7  1:18ct.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
16

## Page 8

mainland China at the 5% level. But as one might suspect, we can conﬁdently reject a unit root in the ﬁrst difference of output
and consumption for both economies at the 1% level, meaning that these series are integrated of order one, or I(1). We also
reject a unit root for the output-consumption gap at the 5% level, implying cointegration, or the existence of a stochastic
trend, between output and consumption for both economies.
Next, we conduct a Johansen cointegration test and show that there exists a cointegrating vector in each pair of output
and consumption data. The results are reported in Table 2. The null hypothesis of no cointegrating vector between output
and consumption is rejected at the 5% level in the case of Hong Kong, and at the 5% and 10% level in the case of mainland
China according to different test statistics. The null hypothesis of one cointegrating vector is not rejected in all tests. This
again conﬁrms that output and consumption share a common stochastic trend in both economies.
The permanent income hypothesis suggests that consumption responds to changes in permanent income, but has
minimal response to changes in transitory income. In other words, consumption cannot be predicted by short-term income
ﬂucutations if the permanent income hypothesis holds. To ﬁnd out whether the hypothesis holds, we estimate a VECM of
consumption and output, where the long-run relationship between the two variables is controlled for. We make use of the
theoretic cointegration vector of (1, 1) implied by the strict form of permanent income hypothesis and run a VECM by
restricting the long-run equation coefﬁcient on output following Cochrane (1994). We also estimate an unrestricted version
of a VECM for comparison.
Tables 3 and 4 show the VECM results for Hong Kong and mainland China. The error correction coefﬁcients suggest that at
quarterly frequency, Hong Kong’s consumption adjusts by 7–8% of the deviation from its long-run level, whereas the speed of
adjustment is 9–10% in mainland China. The speed of adjustment is faster than those found in Cochrane (1994) and Morley
(2007) for the case of the US, but is consistent with the evidence based on other economies (see Zarinah & Jenny Pereira
(2012) for an example of Malaysia). A plausible explanation is that, as suggested in Aguiar and Gopinath (2007), trend growth
is the primary source of ﬂuctuations in emerging markets. Therefore, deviations from trend growth are rather small, and the
adjustment time needed would be rather short. Short adjustment time translates into fast speed of adjustment for
consumption to revert back to its trend.
Next, we focus on testing if consumption responds to anticipated transitory income changes. We expect no response if the
permanent income hypothesis holds, as in Hall (1978). Our results, however, suggest that consumption does respond to
changes in transitory income. The coefﬁcient on the ﬁrst lag of output growth in the consumption growth equation is positive
and signiﬁcant at the 5% level under the restricted VECM in the case of Hong Kong, and is positive and signiﬁcant in both
VECMs in the case of mainland China. The results suggest that after controlling for the long-term relationship between
consumption and output, a 1 percentage point increase in lagged transitory output can still predict a 0.2 percentage point
increase in Hong Kong’s consumption, and a 0.16 to 0.18 percentage point increase in the Mainland’s consumption.
Even though our results suggest that consumption in Hong Kong and mainland China does not strictly follow the
permanent income hypothesis, we should not simply accept the failure of this hypothesis in explaining the consumption
Table 1
Unit root and cointegrations test for Hong Kong output and consumption.
Hong Kong 
Mainland China
Lags of differencesa
p-valueb
Lags of differences 
p-value
yt
8 
0.3648 
7 
0.0851
ct
3 
0.7817 
2 
0.4361
ˆzt
11 
0.0147 
13 
0.0022
Dyt
– 
0.0000 
– 
0.0000
Dct
– 
0.0000 
– 
0.0000
Notes: (a) Chosen by a general-to-specifc rule, starting with a maximum of 14 lags and reducing if the last lag is not signiﬁcant at the 10% level for a standard
t-test. (b) Test regressions for yt and ct include a constant and a time trend, and the statistics is MacKinnon p-values. The test regression for ˆzt only includes a
constant, and the reported statistics is Phillips and Ouliaris p-value.
Table 2
Johansen cointegration tests for output and consumption.
Trace statistics 
Hong Kong 
Mainland China
Null hypothesis: 
p-valuea
p-value
No cointegrating vectors 
0.0281 
0.0591
At most one cointegrating vector 
0.9009 
0.7054
Maximum eigenvalue statistics
Null hypothesis:
No cointegrating vectors 
0.0081 
0.0416
At most one cointegrating vector 
0.9009 
0.7054
Note: (a) MacKinnon–Haug–Michelis p-value.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
17

## Page 9

data. First, the cointegration tests above suggest that a common stochastic trend exists between output and consumption in
both economies. Recall from the stochastic growth model that the common stochastic trend represents the underlying
permanent productivity trend and hence the permanent income trend of an economy. Second, although the coefﬁcient on
lagged output growth is positive and signiﬁcant, a magnitude of 0.2 or less is not particularly big. We can compare these to,
for example, an estimate of 0.5 in Campbell and Mankiw (1989) based on the US data, which implies that half of the US
consumers are the so-called ‘‘rule-of-thumb’’ consumers who consume their current rather than permanent income.
A plausible explanation behind the positive impact of anticipated transitory income changes on consumption is that there
are two types of consumers: liquidity-constrained consumers who respond to transitory income shocks, and unconstrained
ones who respond to changes in permanent income only. Recent studies by Benito and Mumtaz (2006) and Faruqui and
Torchani (2012) use British and Canadian household data, respectively, to identify the proportion of households who face
liquidity constraints based on a life-cycle/permanent income hypothesis framework. Both studies ﬁnd that after controlling
for the grouping of unconstrained and constrained (20–40% of total) households, consumption of the constrained households
responds positively to lagged income growth, while consumption of the unconstrained households does not. Following this
Table 3
VECM of output and consumption for Hong Kong.
Restricted 
Unrestricted
Dct
Dyt
Dct
Dyt
Error correction coefﬁcient 
0.082
(0.051)
0.073
(0.047)
0.071
(0.028)
0.012
(0.026)
Dyt1
0.198
(0.094)
0.023
(0.085)
0.143
(0.096)
0.022
(0.089)
Dyt2
0.046
(0.095)
0.098
(0.086)
0.003
(0.096)
0.097
(0.088)
Dyt3
0.122
(0.091)
0.195
(0.083)
0.089
(0.091)
0.200
(0.085)
Dct1
0.321
(0.082)
0.217
(0.074)
0.282
(0.081)
0.233
(0.075)
Dct2
0.120
(0.090)
0.134
(0.082)
0.142
(0.088)
0.149
(0.082)
Dct3
0.297
(0.081)
0.017
(0.073)
0.309
(0.080)
0.025
(0.074)
Constant 
0.000
(0.005)
0.000
(0.004)
0.001
(0.004)
0.005
(0.004)
R2
0.4313 
0.4028 
0.4458 
0.3940
Note: Standard errors reported in parentheses.
Table 4
VECM of output and consumption for mainland China.
Restricted 
Unrestricted
Dct
Dyt
Dct
Dyt
Error correction coefﬁcient 
0.091
(0.030)
0.094
(0.049)
0.096
(0.029)
0.076
(0.048)
Dyt1
0.177
(0.060)
0.174
(0.096)
0.155
(0.058)
0.201
(0.095)
Dyt2
0.105
(0.055)
0.154
(0.088)
0.090
(0.054)
0.174
(0.088)
Dyt3
0.142
(0.054)
0.402
(0.087)
0.131
(0.053)
0.419
(0.087)
Dyt4
0.167
(0.059)
0.114
(0.095)
0.164
(0.058)
0.105
(0.096)
Dct1
0.145
(0.095)
0.140
(0.153)
0.121
(0.094)
0.162
(0.155)
Dct2
0.204
(0.095)
0.268
(0.154)
0.228
(0.095)
0.287
(0.156)
Dct3
0.024
(0.096)
0.314
(0.156)
0.002
(0.097)
0.327
(0.159)
Dct4
0.064
(0.088)
0.521
(0.142)
0.082
(0.088)
0.528
(0.145)
Constant 
0.004
(0.006)
0.004
(0.009)
0.005
(0.006)
0.006
(0.009)
R2
0.7805 
0.6875 
0.7839 
0.6841
Note: Standard errors reported in parentheses.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
18

## Page 10

logic, our small coefﬁcients on lagged income growth can be interpreted as capturing the consumption behavior of liquidity-
constrained households, while the rest behave as predicted by the permanent income hypothesis.
3.3. Trends versus cycles: a structural identiﬁcation
In this section we describe how we estimate permanent income for Hong Kong, mainland China, and the US using
quarterly data. Following the literature, we estimate permanent income using an unobserved component (UC) model which
has a modeling structure resembling a stochastic growth model framework for decomposing output into its permanent and
transitory components.
We decompose real output into its trend and transitory component by estimating the following UC model:
yi
t ¼ ti
t þ ui
yt
ci
t ¼ ¯ci þ gi
cti
t þ ui
ct
ti
t ¼ mi þ ti
t1 þ vi
t
where yi
t is the logarithm of real GDP of economy i 2 fHK; CN; USg, ci
t is the logarithm of consumption. ti
t is the economy-
speciﬁc stochastic trend. ui
yt and ui
ct are the transitory components of yi
t and ci
t, respectively. ¯ci reﬂects the long-run impact of
taxes and private saving on consumption as suggested by Morley (2007), and gi
c is the marginal propensity to consume out of
permanent income. The stochastic trend ti
t follows a random walk process with an economy-speciﬁc drift mi, and vi
t is the
shock to the stochastic trend. The transitory components of income and consumption follow unobservable ﬁnite-order
autoregressive (AR) processes:
fi
yðLÞui
yt ¼ ei
yt
fi
cðLÞui
ct ¼ ei
ct
where ei
yt and ei
ct are shocks to transitory income and consumption, respectively. The lag polynomials are normalized by
setting fi
j;0 ¼ 1 for j 2 fy; cg. We deﬁne Q ¼ fvi
t; ei
yt; ei
ctg and assume that Q  iid Nð0; VÞ, where shocks can be correlated
with each other. In our estimation, we assume AR(1) processes for the transitory component of income and consumption.
The estimation results from the UC model for Hong Kong, mainland China, and the US can be found in Appendix B.
Figs. 10–12 plot the quarter-on-quarter growth of output, consumption and our estimates of permanent income for Hong
Kong, mainland China, and the US, respectively. As illustrated in these ﬁgures, the growth rate of consumption and
permanent income can be quite different. To derive our measure of transitory income, we subtract our estimated permanent
income from the real output data for each economy.
4. Transmission of permanent and transitory shocks
4.1. The transmission of transitory shocks
In this section, we analyze how transitory shocks are transmitted between Hong Kong, mainland China, and the US. We
need to take into account the dynamic interactions between macroeconomic variables across the three economies in a
parsimonious empirical model, and we also need to consider a structure to govern the propagation of shocks across
-8
-4
0
4
8
12
197 3 1976 197 9 198 2 1985 1988 199 1 199 4 1997 200 0 200 3 2006 2009 201 2
GDP 
Consumption 
Permanent inco me
% qoq
Fig. 10. Growth of GDP, consumption, and permanent income for Hong Kong.
Sources: CEIC and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
19

## Page 11

economies according to the hierarchy of inﬂuences. Structural vector autoregression (SVAR) is ideal for such analysis since it
has a dynamic modeling structure in a reduced-form setting, while allowing for the identiﬁcation of structural shocks
without imposing many restrictions; unlike structural macroeconomic models (such as dynamic stochastic general
equilibrium (DSGE) models) which are highly stylized and may impose some restrictions that are rather difﬁcult to justify.
We estimate a hierarchical SVAR model following Genberg (2005) and Genberg et al. (2006), which is given by:
AHH
0
AHC
0
AHU
0
0 
ACC
0
ACU
0
0 
AUC
0
AUU
0
0
@
1
A
XHK
t
XCN
t
XUS
t
0
@
1
A ¼
AHHðLÞ 
AHCðLÞ 
AHUðLÞ
0 
ACCðLÞ 
ACUðLÞ
0 
AUCðLÞ 
AUUðLÞ
0
B
@
1
C
A
XHK
t1
XCN
t1
XUS
t1
0
@
1
A þ
uHK
t
uCN
t
uUS
t
0
@
1
A
where A0 and A(L) are structural coefﬁcients, and Xi
t for i 2 fHK; CN; USg is a block of macroeconomic variables for Hong Kong,
mainland China, or the US. Each block includes transitory output and inﬂation of the respective economy, while the US block
also includes the 3-month US Treasury bill rates. ui
t is a corresponding vector of shocks. The equations on transitory output
and inﬂation of each economy represent the reduced-form aggregate demand curve and the Phillips curve. We treat the US
interest rate as the global interest rate. Due to the linked exchange rate regime, Hong Kong short-term interest rate follows
that of the US so it is not included in the model. Also, since mainland China has maintained a relatively closed capital account
over the sample period, we assume that its monetary policy affects output and inﬂation of its own economy but without
direct impact on other economies. Hence the interest rate of mainland China is not included in the model.
The SVAR model ranks the variables in such an order so that it can capture the increasing importance of mainland China in
the global economy in the past two decades. Speciﬁcally, not only can shocks from the US affect mainland China and Hong
Kong, but shocks from mainland China can also affect the US. Since Hong Kong is a small open economy, it is affected by
shocks from both mainland China and the US, but not vice versa, which explains the zero restrictions in the coefﬁcient matrix
on the right hand side of the equation.
We take into account the period during and after the Asian Financial Crisis and assess how the economic linkages among
the three economies have evolved. We estimate the SVAR model in two sub-periods: between 1985Q1 and 1997Q2, and
between 2003Q4 and 2013Q2. We skipped the period between Asian ﬁnancial crisis and the SARS outbreak when the Hong
-10
-8
-6
-4
-2
0
2
4
6
8
10
12
14
1985 1987 1989 1991 1993 1995 1997 1999 200
 
1 2003 200
 
5 2007 200
 
9 2011 2013
GDP
Con
 
sumpt ion 
Permanent  income
% qoq
Fig. 11. Growth of GDP, consumption, and permanent income for mainland China.
Sources: CEIC and authors’ estimates.
-4
-2
0
2
4
6
1947 1951 1955 1959 19 
63 1967 197 1 1975 1979 198
 
3 198
 
7 199
 
1 199
 
5 19 
99 200
 
3 200
 
7 2011
GDP 
Consumpt ion 
Permanent  income
% qoq
Fig. 12. Growth of GDP, consumption, and permanent income for US.
Sources: CEIC and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
20

## Page 12

Kong economy went through a prolonged period of deﬂation and deleveraging after the burst of signiﬁcant property price
bubble. Tests of structural break shows that the period between 1997Q3 and 2003Q3 is signiﬁcantly different from the other
two sub-periods. Indeed, by including this period into the sample, we ﬁnd that regression results are not sensible and would
distort the analysis. We argue that Hong Kong’s business cycle during this period is desynchronized with the US or mainland
China due to the extended period needed for recovery after the deep downturn as a consequence of the crisis, which did not
affect the US or mainland China.
The results on variance decomposition of the forecast errors on Hong Kong’s transitory output and inﬂation are shown in
Table 5. Shocks originating from Hong Kong dominate the impact on its own output and inﬂation variations over a short-
term horizon during both sample periods.7 However, US shocks exert a much larger impact on the Hong Kong economy in the
longer run. For instance, when we look at a 20-quarter horizon, US shocks can explain about 57% of Hong Kong’s output
ﬂuctuations in the earlier period, and about 48% in the latter period, both of which are larger than the contributions from
shocks originating from mainland China and Hong Kong. The long-run inﬂuence of Mainland shocks on Hong Kong’s inﬂation
becomes larger in the latter period, explaining 36% of the variations in inﬂation, while the US inﬂuence still accounts for
about 37% after dominating in the earlier period.8
4.2. The transmission of permanent shocks
As shown in the previous section, we ﬁnd that the Mainland plays a smaller role in driving Hong Kong’s business cycle
ﬂuctuations than the US. However, given the continuing economic and ﬁnancial integration between Hong Kong and the
Mainland, the Mainland’s inﬂuence on Hong Kong may have become more important at the trend cycle frequency. As
discussed in Section 2, Hong Kong and the Mainland are bonded through ﬁnancial integration and FDI ﬂows. In particular, a
large part of TFP growth has been boosted by increasing ﬁnancial linkages, for instance, through the expansion in the supply
of Mainland-related ﬁnancial products in Hong Kong’s ﬁnancial markets. This might have caused trend growth in Hong Kong
and mainland China to become more synchronized.
To formally study the transmission of permanent shocks across borders, we estimate the following SVAR model:
bHH
0
bHC
0
bHU
0
0 
bCC
0
bCU
0
0 
bUC
0
bUU
0
0
@
1
A
ˆtHK
t
ˆtCN
t
ˆtUS
t
0
B
@
1
C
A ¼
bHHðLÞ 
bHCðLÞ 
bHUðLÞ
0 
bCCðLÞ 
bCUðLÞ
0 
bUCðLÞ 
bUUðLÞ
0
B
@
1
C
A
ˆtHK
t1
ˆtCN
t1
ˆtUS
t1
0
B
@
1
C
A þ
eHK
t
eCN
t
eUS
t
0
@
1
A
where ˆti
t for i 2 fHK; CN; USg denotes the permanent income series estimated using the state-space models discussed in
Section 3.3. Unlike the model for transitory shocks, the model for permanent shocks only includes permanent income and
without inﬂation of the three economies and the US interest rate. This is because we assume that the long-run aggregate
supply curve is vertical so that permanent income is invariant to price level, and monetary policy has no long run effect,
consistent with the New Keynesian literature.
Table 6 reports the results of variance decompositions of the forecast errors of Hong Kong’s permanent income. In
contrast to the results relating to transitory shocks, the Mainland is more important than the US in explaining variations in
Hong Kong’s trend growth. The long-run inﬂuence of US permanent shocks on Hong Kong declined from about 36% between
1985Q1 and 1997Q2 to 30% during the 2003Q4-2013Q2 period. On the other hand, the long-run impact of the Mainland’s
permanent shocks on Hong Kong’s trend growth variations increased signiﬁcantly from about 15% to about 65% in the latter
period.9
7 Impulse responses suggest that the output shocks are demand shocks as opposed to transitory supply shocks since the impulse responses of an
economy’s transitory output and inﬂation move in the same direction in the face of a shock to its own transitory output for all three economies in the
sample.
8 Table C1 in Appendix C shows that at the 20-quarter horizon, the variance decompositions of Hong Kong’s output in the latter period are inside the
conﬁdence bands of 16th and 84th percentile in the earlier period. This means that the contributions of shocks from the US, mainland China, and Hong Kong
to Hong Kong’s transitory output have not changed signiﬁcantly between the two periods at the 20-quarter horizon. However, Table C1 also shows that at
the 20-quarter horizon, US and mainland’s shares of Hong Kong’s inﬂation variations in the latter period are outside of the conﬁdence bands in the earlier
period, meaning that they have changed signiﬁcantly over time.
9 As shown in Table C2 in Appendix C, at the 20-quarter horizon, the variance decompositions in the latter period are outside of the conﬁdence bands of
16th and 84th percentile in the earlier period. This means that US, mainland China, and Hong Kong’s contributions have all changed signiﬁcantly between
the two periods at the 20-quarter horizon. Appendix D shows the results of variance decompositions of the forecast errors of Hong Kong’s transitory and
permanent income based on an alternative identiﬁcation scheme for the SVAR model, and uses a measure of permanent income based on cointegration as a
robustness check. The results are largely consistent with the key results discussed in this section. Appendix E shows the variance decompositions results
based on the baseline model described in this section but with the transitory and permanent income constructed using the HP ﬁlter. The results look
different from those presented in this section and should be interpreted with caution. As discussed in the introduction, the use of conventional ﬁltering
techniques can yield inferior results and might artiﬁcially generate business cycle dynamics even when there are none in the original data, particularly
given the weakness of HP ﬁlter in identifying the rather unusual trend and cycle movements during and after the global ﬁnancial crisis. For instance, US
trend output measured using the HP ﬁlter gradually drags toward the actual output in the data after the deep recession, hence reducing the negative output
gap through a slower trend output even if the true potential output might have been much higher. The theory-guided method that we took here can
circumvent this problem, since more data series are used in accordance with economic theory for the decomposition of transitory and permanent income
instead of using a univariate approach which ignores other relevant economic information beside real output itself.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
21

## Page 13

In sum, while the US inﬂuence remains a dominant force behind Hong Kong’s short-term business cycle variations,
mainland China has become a more dominant inﬂuence driving Hong Kong’s trend growth.10
5. Conclusions
In this paper we take a theory-guided method to disentangle the stochastic trend and the transitory component of output
in Hong Kong, mainland China, and the US, and to investigate the interaction between these economies in terms of common
trends and cycles. We ﬁnd that US transitory shocks have remained a dominant force in driving Hong Kong’s business cycle
ﬂuctuations, and that transitory shocks from mainland China have played a less important role. However, when it comes to
the permanent shocks, the picture is the opposite: permanent shocks from the Mainland explain a much larger portion of the
volatility in Hong Kong’s trend output than those from the US.
Our ﬁndings suggest that, at the business cycle frequency, Hong Kong remains more synchronized with the US than
with mainland China. Since it is the similarity of cyclical shocks that matters most for the choice of exchange rate
regime, the LERS, which links the Hong Kong dollar to the US dollar, continues to be appropriate for the foreseeable
future. On the other hand, Hong Kong has beneﬁted from the rise of mainland China as a major trading nation and a
prime destination of FDI by transforming itself from a manufacturing economy to a service economy characterized by
higher productivity. Active exchange of human capital and knowledge has been propagating longer-term productivity
progress across the border.
Table 5
Variance decompositions of transitory shocks for Hong Kong.
Output 
Price
Horizon (in quarters) 
US 
CN 
HK 
US 
CN 
HK
1985Q1–1997Q2
1 
13.562 
16.346 
70.092 
33.387 
1.737 
64.877
4 
31.646 
17.629 
50.725 
49.719 
7.331 
42.950
10 
52.055 
13.300 
34.645 
58.304 
7.590 
34.106
20 
57.084 
13.680 
29.237 
59.266 
7.795 
32.938
2003Q4–2013Q2
1 
16.500 
8.574 
74.926 
36.998 
9.709 
53.293
4 
37.856 
18.007 
44.137 
34.778 
36.291 
28.931
10 
52.416 
18.104 
29.481 
36.855 
35.910 
27.234
20 
47.622 
28.657 
23.721 
37.012 
35.992 
26.996
Table 6
Variance decomposition of permanent shocks for Hong Kong.
TREND_US 
TREND_CN 
TREND_HK
1985Q1–1997Q2
1 
2.766 
7.558 
89.676
4 
11.757 
14.539 
73.704
10 
26.385 
19.767 
53.848
20 
35.779 
14.702 
49.520
2003Q4–2013Q2
1 
4.935 
4.735 
90.330
4 
15.650 
42.683 
41.667
10 
31.818 
58.990 
9.192
20 
29.808 
65.270 
4.922
10 We make use of the SVARs at hand and conduct a variance decomposition analysis for the mainland China economy, and draw policy implications upon
the results in Appendix F.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
22

## Page 14

Appendix A. The construction of value-added exports
A.1. Merchandize exports
Merchandize exports to a destination in value-added terms is the sum of domestic exports and re-export margins to a
destination, and commissions from offshore trade to the destination. We adjust all the components to value-added terms before
computing merchandize exports by destination.
A.1.1. Domestic exports
To derive estimates of Hong Kong’s domestic exports to mainland China in value-added terms, we subtract outward processing
domestic exports from headline domestic exports using data from Hong Kong Census and Statistics Department (C&SD), and then
further strip out other types of processing trade that we have estimated using China Custom data from China’s National Bureau of
Statistics (NBS). We then subtract the proportion of sales that can be attributable to purchases of materials and supplies based on
the data from C&SD.
For Hong Kong’s domestic exports to the US in value-added terms, we add to the headline domestic exports to the US from
C&SD data with our estimates of Hong Kong processing trade to mainland China that are re-exported to the US based on China
Custom data. This captures total ﬁnal demand for Hong Kong’s domestic exports from the US that is missing from the headline
ﬁgures. Again we subtract the proportion of sales attributable to purchases of materials and supplies based on the data from C&SD.
Total domestic exports in value-added terms is headline total domestic exports subtracting outward processing domestic
exports and the proportion of sales attributable to purchases of materials and supplies based on C&SD data.
A.1.2. Re-exports
The adjustments to re-exports are similar to those made to domestic exports. Here we make use of the outward process re-
exports data for consistency. To derive total re-exports and re-exports by destination in value-added terms, we estimate the rate
of re-export margins based on offshore trade statistics from C&SD, and apply them to the adjusted re-export ﬁgures to proxy
exporters’ commissions earned from re-exports.
A.1.3. Commissions from offshore trade
Total offshore trade commission, and commission earned by destination, are from the data of gross margins from merchanting
in C&SD’s Offshore Trade in Goods tables.
A.2. Services exports
We use headline services exports for all categories except for tourism services. This is because a large part of tourism services
exports is expenditure on shopping which involves import content. We adjust tourism services exports by stripping out the
import content in visitors’ shopping expenditure based on data from the Hong Kong Tourism Board.
Table A1 contains our estimates of mainland China and US shares in Hong Kong merchandize exports, services exports
excluding tourism, tourism services exports and ﬁnancial services exports, all in value-added terms.
Table A1
Mainland China and US shares in Hong Kong exports in value-added terms.
% of total 
Merchandize 
Services (excluding
tourism)
Tourism services 
Financial services
Year 
Mainland China 
US 
Mainland China 
US 
Mainland China 
US 
Mainland China 
US
2000 
13.1 
33.8 
14.0 
25.3 
28.0 
10.5 
2.2 
30.4
2001 
15.7 
31.8 
13.9 
25.5 
34.1 
9.5 
2.5 
33.5
2002 
16.8 
30.8 
16.3 
23.6 
45.2 
8.6 
2.3 
32.9
2003 
17.5 
29.8 
15.4 
23.2 
55.6 
7.6 
3.5 
39.3
2004 
18.2 
26.7 
14.6 
23.9 
50.6 
8.9 
2.8 
29.8
2005 
18.5 
25.9 
14.4 
23.8 
48.8 
8.6 
2.5 
31.1
2006 
19.6 
24.7 
12.8 
24.7 
48.2 
7.9 
3.5 
31.9
2007 
20.9 
23.3 
13.2 
24.6 
49.0 
7.6 
3.2 
32.0
2008 
20.5 
22.5 
13.1 
24.8 
52.5 
6.5 
3.8 
34.5
2009 
19.5 
23.7 
14.0 
24.9 
59.8 
4.9 
4.2 
33.2
2010 
20.4 
24.8 
15.1 
24.3 
59.7 
4.9 
5.8 
33.8
2011 
21.1 
23.0 
15.9 
22.8 
63.4 
4.6 
5.1 
33.6
2012 
21.8 
24.7 
16.0 
22.5 
66.5 
4.0 
4.2 
33.4
Sources: C&SD and authors’ estimates.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
23

## Page 15

Appendix B. Coefﬁcient estimates of state-space models
Table B1 shows the coefﬁcient estimates from the unobserved component (UC) model using output and consumption data for
Hong Kong, mainland China, and the US.
Appendix C. Variance decomposition with conﬁdence band
To examine whether the variance decompositions in Tables 5 and 6 have changed signiﬁcantly over time, we constructed
bootstrapped conﬁdence bands of variance decompositions in the ﬁrst period. For a particular variable, if the share of variance
contributed from a shock origination at a particular horizon in the second period falls within the bootstrapped conﬁdence band of
the same shock origination and horizon in the ﬁrst period, then the change of that variance decomposition is insigniﬁcant. Vice-
versa is true. The bootstrapped conﬁdence bands and the original results in Tables 5 and 6 are shown in Tables C1 and C2 below.
Note that the conﬁdence bands correspond to the 16th and 84th percentile.
Table B1
Coefﬁcient estimates of the unobserved component (UC) models.
Hong Kong 
Mainland China 
US
gi
c
1.075
(0.100)
0.869
(0.074)
0.993
(0.050)
fi
y;1
0.023
(0.086)
0.184
(0.095)
0.068
(0.064)
fi
c;1
0.456
(0.080)
0.331
(0.124)
0.439
(0.085)
siv
0.365
(0.000)
0.415
(0.000)
0.377
(0.000)
siey
1.822
(0.007)
2.114
(0.005)
0.700
(0.000)
siec
2.079
(0.008)
1.107
(0.001)
0.479
(0.000)
riv;ey
0.194
(0.015)
0.175
(0.069)
0.266
(0.000)
riv;ec
0.264
(0.001)
0.299
(0.002)
0.447
(0.000)
siey;ec
0.439
(0.000)
0.118
(0.222)
0.562
(0.000)
Note: Standard errors of shocks (siv, siey, siec) are multiplied by 100. ri denotes correlation between shocks.
Table C1
Variance decompositions of transitory shocks with conﬁdence bands.
Output 
Price
Horizon (in quarters) 
US 
CN 
HK 
US 
CN 
HK
1985Q1–1997Q2
1 
13.562 
16.346 
70.092 
33.387 
1.737 
64.877
(7.4, 25.2) 
(13.3, 22.6) 
(62.6, 76.6) 
(25.0, 47.4) 
(0.0, 7.1) 
(56.5, 74.1)
4 
31.646 
17.629 
50.725 
49.719 
7.331 
42.950
(19.8, 53.0) 
(11.4, 29.0) 
(38.2, 63.6) 
(36.9, 69.5) 
(0.1, 18.9) 
(30.4, 57.7)
10 
52.055 
13.300 
34.645 
58.304 
7.590 
34.106
(39.5, 76.9) 
(6.7, 27.2) 
(18.0, 53.3) 
(44.2, 83.6) 
(0.0, 28.3) 
(19.2, 54.0)
20 
57.084 
13.680 
29.237 
59.266 
7.795 
32.938
(42.6, 82.9) 
(3.7, 30.9) 
(13.2, 49.9) 
(43.7, 90.0) 
(0.0, 33.1) 
(17.4, 55.0)
2003Q4–2013Q2
1 
16.500 
8.574 
74.926 
36.998 
9.709 
53.293
4 
37.856 
18.007 
44.137 
34.778 
36.291 
28.931
10 
52.416 
18.104 
29.481 
36.855 
35.910 
27.234
20 
47.622 
28.657 
23.721 
37.012 
35.992 
26.996
Note: Conﬁdence bands of 16th and 84th percentile of the variance decompositions in the earlier period are in parenthesis.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
24

## Page 16

Appendix D. Variance decompositions from an alternative model
As a robustness check, we construct an alternative measure of stochastic permanent income trend and re-estimate the SVAR
models. Speciﬁcally, Mainland data have relatively short time series. This makes identifying the stochastic trend using an
unobserved component model statistically less reliable. To check the robustness of our results, we assume that consumption itself
is the stochastic trend for an economy. Speciﬁcally, based on the consumption function ci
t ¼ ¯ci þ gi
cti
t þ ui
ct for i 2 ðHK; CN; USÞ, we
estimate the loading of the output gi
c on the trend ti
t. Note that consumption for mainland China throughout this section of
Appendix is proxied by real retail sales. For simplicity, the shocks from the US can affect mainland China, but not vice versa,
following Genberg (2005). In other words, we set AUC
0
and AUCðLÞ to 0 in the SVAR system shown in Section 4.1, and bUC
0
and bUCðLÞ
to 0 in the SVAR system shown in Section 4.2.
We estimate the cointegrating coefﬁcients using the Stock-Watson Dynamic OLS (DOLS) method. The estimates of the
cointegrating coefﬁcient are reported in Table D1. The numbers in parenthesis below each estimate are adjusted R2, the Akaike
Information Criterion (AIC), and the Schwarz Information Criterion (BIC), respectively. In general, we prefer a high R2, and low AIC
and BIC. We select the best model based on AIC and BIC criteria, as well as likelihood ratio test. We use the selected estimates for
the factor loadings on trends to compute the transitory components as shown in Table D2.11
Table C2
Variance decomposition of permanent shocks with conﬁdence bands.
TREND_US 
TREND_CN 
TREND_HK
1985Q1–1997Q2
1 
2.766 
7.558 
89.676
(2.3, 4.3) 
(1.2, 14.8) 
(82.4, 96.3)
4 
11.757 
14.539 
73.704
(11.3, 13.4) 
(7.6, 22.0) 
(66.1, 80.8)
10 
26.385 
19.767 
53.848
(25.7, 28.8) 
(11.9, 27.8) 
(45.4, 61.9)
20 
35.779 
14.702 
49.520
(34.0, 40.5) 
(5.5, 23.5) 
(39.2, 60.0)
2003Q4–2013Q2
1 
4.935 
4.735 
90.330
4 
15.650 
42.683 
41.667
10 
31.818 
58.990 
9.192
20 
29.808 
65.270 
4.922
Note: Conﬁdence bands of 16th and 84th percentile of the variance decompositions in the earlier period are in
parenthesis.
Table D1
Estimating the cointegration relation.
Mainland China 
US 
Hong Kong
OLS 
1.0473
(0.9956, 6.79 6.84)
0.9057
(0.9978, 2.93, 2.98)
1.0327
(0.9718, 6.28, 6.33)
DOLS with 1 lag/lead 
1.0578
(0.9960, 6.66 6.78)
0.9113
(0.9980, 2.84, 2.97)
1.0473
(0.9725, 6.27, 6.39)
DOLS with 2 lags/leads 
1.0626
(0.9962, 6.61 6.78)
0.9127
(0.9982, 2.84, 3.01)
1.0567
(0.9728, 6.26, 6.43)
DOLS with 3 lags/leads 
1.0664
(0.9963, 6.56, 6.79)
0.9140
(0.9980, 2.85, 3.08)
1.0691
(0.9732, 6.24, 6.47)
DOLS with 4 lags/leads 
1.0699
(0.9964, 6.50, 6.79)
0.9159
(0.9981, 2.86, 3.13)
1.0805
(0.9733, 6.24, 6.52)
DOLS with 5 lags/leads 
1.0751
(0.9968, 6.39, 6.73)
0.9177
(0.9981, 2.87, 3.19)
1.0917
(0.9734, 6.24, 6.57)
DOLS with 6 lags/leads 
1.0790
(0.9969, 6.34, 6.74)
DOLS with 7 lags/leads 
1.0828
(0.9970, 6.29, 6.75)
Note: The numbers in parenthesis below each estimate are adjusted R2, the Akaike Information Criterion (AIC), and the Schwarz Information Criterion (BIC),
respectively. Bold values are the selected estimates for the factor loadings on trends to compute the transitory components.
11 The parameter estimates from the DOLS is super-consistent, with the rate of convergence given by the sample size instead of its square root (see Stock &
Watson (1993)). Moreover, DOLS is asymtotically equivalent to a fully–modiﬁed ordinary least squares estimator (FM-OLS) from Phillips and Hansen (1990)
which corrects for the generated-regressors bias. As such, even though we are using estimates from the ﬁrst stage regression as inputs to the SVAR analysis,
our estimates do not subject to the generated-regressors bias.
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
25

## Page 17

We re-estimate the SVAR model described in Section 4.1 using the alternative measure of transitory outputs, inﬂation rates of
the three economies, as well as the 3-month US Treasury bill rates, at quarterly frequency. We set AUC
0
and AUCðLÞ to 0 in the SVAR
system as discussed earlier in this section of the Appendix. We also re-estimate the SVAR model described in Section 4.2 to study
the transmission of permanent shocks across economies using the alternative measure of permanent income, but we set bUC
0
and
bUCðLÞ to 0 in the SVAR system to prevent Mainland’s shocks from affecting the US. Table D3 reports the variance decomposition of
the forecast errors on Hong Kong’s output and inﬂation equation. US transitory shocks had a large impact on Hong Kong before
1997, explaining more than 50% of Hong Kong’s output ﬂuctuations in a 4-quarter horizon, and even larger over a longer horizon.
In the latter sample period, US shocks are still important in explaining Hong Kong’s business cycles, but the magnitude of their
impact is smaller at all horizons. The effect of Mainland shocks on Hong Kong’s real economy also drops, implying that Hong
Kong’s economic integration with the Mainland did not increase output co-movement between the two economies at the business
cycle frequency. Nevertheless, consistent with our baseline results where we used transitory income generated from state-space
models, US transitory shocks remain a dominant force in driving Hong Kong’s business cycle.
Table D2
Transitory components of outputsa.
˜yCN
t
¼ yCN
t
 1:0751  cCN
t
˜yUS
t
¼ yUS
t
 0:9113  cUS
t
˜yHK
t
¼ yHK
t
 1:0691  cHK
t
a The permanent income hypothesis
implies a cointegrating vector of (1, 1).
By performing a t-test with the null
hypothesis of ˆb ¼ 1 (or 1 depending
on the way the equation is set up), all
three coefﬁcients in Table D2 are statisti-
cally different from 1 (or 1). However,
this result is not inconsistent with the
literature nor with our results in Section
3.2 because cointegration tests do suggest
a common stochastic trend exists be-
tween each pair of output and consump-
tion, 
but 
the 
permanent 
income
hypothesis does not hold in its strict form
as discussed in Section 3.2.
Table D3
Variance decompositions of transitory shocks for Hong Kong (alternative model).
Output 
Price
Horizon (in quarters) 
US 
CN 
HK 
US 
CN 
HK
1985Q1–1997Q2
1 
17.919 
3.258 
78.823 
24.251 
11.864 
63.885
4 
53.869 
10.413 
35.718 
30.291 
31.424 
38.285
20 
83.846 
12.712 
3.442 
64.344 
21.104 
14.552
1999Q1–2012Q4
1 
15.582 
1.688 
82.730 
14.063 
0.325 
85.612
4 
34.619 
6.450 
58.931 
20.447 
16.486 
63.067
20 
51.925 
5.750 
42.325 
13.229 
26.790 
59.981
Table D4
Variance decomposition of permanent shocks for Hong Kong (alternative model).
Output
Horizon (in quarters) 
Trend_US 
Trend_CN 
Trend_HK
1985Q1–1997Q2
1 
8.303 
35.371 
56.326
4 
12.921 
39.359 
47.719
20 
13.543 
39.141 
47.315
1997Q3–2003Q4
1 
2.413 
2.494 
95.093
4 
9.028 
15.498 
75.474
20 
9.379 
18.791 
71.831
2004Q1–2013Q2
1 
11.015 
23.924 
65.061
4 
13.183 
32.967 
53.851
20 
11.606 
42.724 
45.670
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
26

## Page 18

However, one should interpret these results with caution. Since the second sub-period also includes the period after the Asian
Financial Crisis when the Hong Kong economy went through deﬂation and deleveraging until 2003, the results may have been
distorted as the crisis had desynchronized the Hong Kong economy with the US and mainland China. Tests of structural break
support this fact.
Table D4 reports the variance decompositions of the forecast errors on Hong Kong’s permanent income equation. In contrast to
the results of transitory shocks, permanent shocks from mainland China were more important than the US in determining Hong
Kong’s trend growth, similar to our baseline analysis. A permanent shock to the Mainland leads to a notable shift in Hong Kong’s
output trend.
Appendix E. Variance decompositions based on HP-ﬁltered data
In this section of the Appendix, we construct alternative measures of transitory and permanent income using the HP ﬁlter and
re-estimate the SVAR models described in Section 4. Table E1 shows that at the 20-quarter horizon, US shocks can explain about
81% of Hong Kong’s output ﬂuctuations in the earlier period, and decreases to 47% in the latter period. The contribution from
mainland shocks to Hong Kong’s business cycles increases considerably from 7% to 46% over the two periods, contrary to the
results in Table 5 in which the increase in mainland contribution is much smaller. Table E2 shows that at the 20-quarter horizon,
US inﬂuence on Hong Kong’s trend growth variations increases from 49% to a dominating share of 96%, in contrast to the results in
Table 6 in which the mainland share dominates at 65% in the latter period.
As discussed in the introduction, the use of conventional ﬁltering techniques can yield inferior results and might artiﬁcially
generate business cycle dynamics even when there are none in the original data (also see Cogley and Nason (2000) and Estrella
(2007) for further discussion). Due to the weakness of HP ﬁlter in identifying the rather unusual trend and cycle movements
during and after the global ﬁnancial crisis, it is difﬁcult to say whether this result is sensible. For instance, US trend output
measured using the HP ﬁlter gradually drags toward the actual output in the data after the deep recession, hence reducing the
negative output gap through a slower trend output even if the true potential output might have been much higher. The theory-
guided method that we took (see Section 3) can circumvent the problem from using conventional ﬁltering techniques, since more
data series are used in accordance with economic theory for the decomposition of transitory and permanent income instead of
using a univariate approach which ignores other relevant economic information beside real output itself.
Appendix F. Transmission of Shocks on mainland China economy
In this section, we analyze the transmission of transitory and permanent shocks on the Mainland economy based on the
variance decomposition results from the baseline model presented in Section 4. Since the shocks from Hong Kong do not affect the
Table E1
Variance decompositions of transitory shocks for Hong Kong (HP-ﬁltered data).
Output 
Price
Horizon (in quarters) 
US 
CN 
HK 
US 
CN 
HK
1985Q1–1997Q2
1 
47.924 
7.004 
45.072 
37.163 
18.740 
44.097
4 
62.047 
4.791 
33.162 
57.884 
15.204 
26.910
10 
75.040 
8.552 
16.407 
67.016 
12.508 
20.476
20 
80.632 
7.468 
11.901 
69.064 
11.926 
19.011
2003Q4–2013Q2
1 
31.025 
19.144 
49.831 
26.016 
6.421 
67.563
4 
43.582 
41.023 
15.396 
37.460 
25.568 
36.973
10 
42.101 
46.378 
11.521 
40.754 
28.830 
30.416
20 
46.652 
46.145 
7.202 
42.139 
33.242 
24.620
Table E2
Variance decomposition of permanent shocks for Hong Kong (HP-ﬁltered data).
TREND_US 
TREND_CN 
TREND_HK
1985Q1–1997Q2
1 
33.611 
7.277 
59.112
4 
33.015 
1.681 
65.304
10 
14.497 
5.227 
80.276
20 
48.551 
4.059 
47.390
2003Q4–2013Q2
1 
31.781 
21.590 
46.630
4 
4.585 
25.949 
69.466
10 
74.665 
3.187 
22.148
20 
95.592 
1.450 
2.958
D. He et al. / Journal of Asian Economics 40 (2015) 10–28 
27

## Page 19

Mainland economy, we estimate the model using full sample period from 1985Q1 to 2013Q2 given that the Mainland and US
economy were not affected by the Asian Financial Crisis. We will then discuss the policy implications from these results.
The results on variance decomposition of the forecast errors on mainland China’s output and inﬂation are shown in Table F1.
Shocks originating from mainland China dominate the impact on its own transitory output and inﬂation variations at all horizons,
but are decreasing as the horizons get longer. Table F2 shows that variations of Mainland’s trend growth is dominated by its own
permanent shocks.
Our result on the low degree of business cycle synchronization between mainland China and the US is consistent with He and
Liao (2012). Given that Mainland’s business cycle is mainly driven by domestic transitory shocks, it is desirable for the Mainland
economy to maintain a high degree of monetary policy autonomy. This means that it would be beneﬁcial for the Mainland
economy to continue to increase its exchange rate ﬂexibility as it further opens its capital account according to the ‘‘Impossible
Trinity’’.
In other words, mainland China has a relatively closed economy and its monetary policy stance could be at times very different
from global monetary policy. Given the nature of Hong Kong as a small economy that is widely opened to global economic
activities and ﬁnancial ﬂows, it remains appropriate for Hong Kong to share a common monetary policy with the US under the
LERS.
References
Aguiar, M., & Gopinath, G. (2007). Emerging market business cycles: The cycle is the trend. Journal of Political Economy, 115, 69–102.
Benhabib, J., & Wen, Y. (2004). Indeterminacy, aggregate demand, and the real business cycle. Journal of Monetary Economics, 51(3), 503–530.
Benito, A., & Mumtaz, H. (2006). Consumption excess sensitivity, liquidity constraints and the collateral role of housing. In Bank of England Working Paper no. 306.
Bloem, A. M., Dippelsman, R. J., & Maehle, N. (2001). Manual for quarterly national accounts: Concepts, data sources, and compilations. Washington DC: International
Monetary Fund, Publication Services.
Campbell, J. Y., & Mankiw, N. G. (1989). Consumption, income and interest rates: Reinterpreting the time series evidence. NBER Macroeconomics Annual, 4, 185–
246.
Chow, G. C., & Lin, A. (1971). Best linear unbiased interpolation, distribution and extrapolation of time series by related series. Review of Economics and Statistics, 53,
372–375.
Cochrane, J. H. (1994). Permanent and transitory components of GNP and stock prices. Quarterly Journal of Economics, 109, 241–263.
Cogley, T., & Nason, J. (2000). Effects of the Hodrick–Prescott ﬁlter on trend and difference stationary time series implications for business cycle research. Journal of
Economic Dynamics and Control, 19(1–2), 253–278.
Estrella, A. (2007). Extracting Business Cycle Fluctuations: What Do Time Series Filters Really Do?’’ FRB of New York Staff Report No.289.
Fama, E. F. (1992). Transitory variation in investment and output. Journal of Monetary Economics, 30, 467–480.
Faruqui, U., & Torchani, S. How Important Are Liquidity Constraints for Canadian Households? Evidence from Micro-Data. Bank of Canada Discussion Paper 2012-
9.
Genberg, H. (2005). External Shocks, Transmission Mechanisms and Deﬂation in Asia, BIS Working Papers No.187.
Genberg, H., Liu, L., & Jin, X. (2006). ‘‘Hong Kong’s Economic Integration and Business Cycle Synchronization with Mainland China and the US,’’ HKMA Working
Paper 11/2006.
Genberg, H., & He, D. (2008). Macroeconomic linkages between Hong Kong and mainland China. Hong Kong: City University of Hong Kong Press.
Hall, R. E. (1978). Stochastic implications of the life cycle-permanent income hypothesis: Theory and evidence. Journal of Political Economy, 86(6), 971–987.
He, D., & Liao, W. (2012). Asian business cycle synchronization. Paciﬁc Economic Review, 17(1), 106–135.
Kim, C.-J., & Piger, J. (2002). Common stochastic trends, common cycles, and asymmetry in economic ﬂuctuations. Journal of Monetary Economics, 49, 1189–1211.
Leung, F., Han, G., & Chow, K. (2009). Financial Services Sector as a Driver of Productivity Growth in Hong Kong, HKMA Working Paper 14/2009.
Morley, J. (2007). The Slow Adjustment of Aggregate Consumption to Permanent Income. Journal of Money, Credit and Banking, 39(2–3), 615–638.
Phillips, P. C. B., & Hansen, B. E. (1990). Statistical inference in instrumental variables regression with I(1) processes. Review of Economic Studies, 57, 99–125.
Smets, F., & Wouters, R. (2003). An estimated dynamic stochastic general equilibrium model of the Euro area. Journal of the European Economic Association, 1(5),
1123–1175.
Stock, J. H., & Watson, M. W. (1993). A Simple estimator of cointegrating vectors in higher order integrated systems. Econometrica, 61(4), 783–820.
Zarinah, Y., & Jenny Pereira, G. P. P. (2012). Consumption invariant to economic downturn? Evidence on the propensity to consume. International Journal of Trade,
Economics and Finance, 3(6), 468–471.
Table F1
Variance decompositions of transitory shocks for mainland China.
1985Q1–2013Q2 
Output 
Price
Horizon (in quarters) 
US 
CN 
US 
CN
1 
7.447 
92.553 
2.752 
97.248
4 
15.564 
84.436 
8.023 
91.977
10 
19.671 
80.330 
24.542 
75.458
20 
23.795 
76.204 
30.343 
69.656
Table F2
Variance decomposition of permanent shocks for mainland China.
1985Q1–2013Q2 
TREND_US 
TREND_CN
1 
5.382 
94.618
4 
2.608 
97.392
10 
0.638 
99.362
20 
0.243 
99.757
D. He et al. / Journal of Asian Economics 40 (2015) 10–28
28
