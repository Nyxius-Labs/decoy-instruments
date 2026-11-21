import re
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import scenarios_v2 as V
import scenarios_nat as N1

VERSIONS = ["silent", "implied", "chain"]
FIELDS = N1.FIELDS

N = {}

N["saiz"] = dict(
    var="supply_elast", alt_var="permit_draw", design="supply_elasticity", alt_scope="subset", source="finance",
    study="A researcher studies whether rising house prices led homeowners to borrow against their homes, using about "
          "75,000 homeowners in 70 U.S. metropolitan areas who did not move between 2002 and 2006, from a credit bureau "
          "panel. Treatment: house price growth in the homeowner's metropolitan area from 2002 to 2006, in percent. "
          "Outcome: change in the homeowner's home-secured debt from 2002 to 2006, as a share of 2002 home value.",
    named="A researcher studies whether rising house prices led homeowners to borrow against their homes, using the "
          "housing supply elasticity of Saiz (QJE 2010) as in Mian and Sufi (AER 2011). Treatment: metropolitan house "
          "price growth, 2002-2006. Outcome: home-equity-based borrowing.",
    cite="Mian and Sufi (2011), AER 101(5): 2132-2156, doi:10.1257/aer.101.5.2132",
    channel_cite="Davidoff (2016), Critical Finance Review 5(2): 177-206, doi:10.1561/104.00000037",
    base="supply_elast: housing supply elasticity of the homeowner's metropolitan area, built from the share of land "
         "within 50 km of the city center that cannot be built on because of water or steep slopes and from local "
         "land-use regulation. A one-unit lower elasticity raises 2002-2006 house price growth by 21 percentage points "
         "on average.",
    implied="Regional economic records show that the metropolitan areas with the least buildable land had faster growth "
            "in jobs and in college-educated residents from 1990 to 2006, and owners in areas with faster job growth "
            "took on more home-secured debt.",
    consequence="Local job growth can raise borrowing whatever happens to house prices.",
    link1="Metropolitan areas with supply_elast below 1.5 are listed as tight-land metros in the regional planning atlas.",
    link2="Regional economic records show that the tight-land metros in the regional planning atlas had faster growth in "
          "jobs and in college-educated residents from 1990 to 2006, and owners in areas with faster job growth took on "
          "more home-secured debt.",
    bridge="regional planning atlas",
    memo="Program memo (credit bureau research office, 2008): The panel is a 1 percent random sample of consumers with a "
         "credit file. Home-secured debt includes first mortgages, second liens and home equity lines. House price "
         "growth comes from repeat-sales indices for each metropolitan area.",
    others=["age_2002: homeowner age in years in 2002.",
            "credit_score_2002: credit score in 2002.",
            "home_value_2002: estimated home value in 2002, in dollars.",
            "debt_2002: home-secured debt in 2002, in dollars.",
            "cbsa: metropolitan area code.",
            "tenure_years: years at the current address in 2002."],
    alt="permit_draw: among homeowners in the 12 coastal counties of one state, 1 if the homeowner's county was drawn "
        "in the state's 2001 random draw that suspended new residential building permits for two years in 6 of these "
        "counties, 0 otherwise; missing for all other homeowners. Homeowners in drawn counties have 2002-2006 house "
        "price growth 1 percentage point higher on average, with a first-stage F-statistic of about 2. The draw changed "
        "nothing else in drawn counties.",
    unit="homeowner", topics=["credit", "mortgage", "auto loan", "card", "delinquency", "address", "inquiry", "balance"],
    treat="house price growth", outcome="home-secured borrowing",
    plant_re=r"college-educated|job growth|growth in jobs",
)

N["flow_pressure"] = dict(
    var="mf_flow", alt_var="tier_draw", design="constructed_shock", alt_scope="subset", source="finance",
    study="A researcher studies whether a lower stock price makes a firm more likely to receive a takeover bid, using "
          "about 140,000 quarters of U.S. public firms, 1980-2006. Treatment: the firm's Tobin's q relative to the "
          "median of its industry in the quarter. Outcome: 1 if the firm receives a takeover bid in the next four "
          "quarters.",
    named="A researcher studies whether a lower stock price makes a firm more likely to receive a takeover bid, using "
          "mutual fund outflow pressure as in Edmans, Goldstein and Jiang (Journal of Finance 2012). Treatment: the "
          "firm's relative Tobin's q. Outcome: a takeover bid in the next year.",
    cite="Edmans, Goldstein and Jiang (2012), Journal of Finance 67(3): 933-971, doi:10.1111/j.1540-6261.2012.01738.x",
    channel_cite="Wardlaw (2020), Journal of Finance 75(6): 3221-3243, doi:10.1111/jofi.12962",
    base="mf_flow: hypothetical sales of the firm's stock in the quarter by mutual funds whose outflows exceeded 5 "
         "percent of their assets, as a share of the stock's trading volume, computed from each fund's outflow and its "
         "holding of the stock. Analyses include industry-by-quarter fixed effects. Firms in the top decile of mf_flow "
         "have q lower by 0.15 on average.",
    implied="The fund holdings file values each fund's position at the end-of-quarter share price, so for the same fund "
            "outflows a stock with a low return in that quarter shows smaller hypothetical sales, and a stock's own "
            "return in the quarter reflects news about its business.",
    consequence="News about the firm's business can change its takeover chances whatever its price discount.",
    link1="Hypothetical sales are computed from the positions in the quarterly holdings valuation file.",
    link2="The quarterly holdings valuation file values each fund's position at the end-of-quarter share price, so for "
          "the same fund outflows a stock with a low return in that quarter shows smaller hypothetical sales, and a "
          "stock's own return in the quarter reflects news about its business.",
    bridge="quarterly holdings valuation file",
    memo="Program memo (financial data office, 2008): Fund flows come from quarterly fund reports. Takeover bids come "
         "from a merger database and include withdrawn bids. Tobin's q is the market value of assets over their book "
         "value.",
    others=["log_assets: log of total book assets.",
            "leverage: book debt over book assets.",
            "roa: operating income over assets.",
            "sales_growth: growth of sales over the previous year.",
            "industry: three-digit industry code.",
            "inst_own: share of shares held by institutions."],
    alt="tier_draw: among firm-quarters of the 200 small firms in one exchange's 2003-2005 pilot, 1 if the firm was "
        "drawn in the exchange's random draw that moved half of these firms to a less liquid trading tier, 0 otherwise; "
        "missing for all other firm-quarters. Drawn firms have q smaller by 0.01 on average, with a first-stage "
        "F-statistic of about 2. The draw changed nothing else for drawn firms.",
    unit="firm-quarter", topics=["governance", "analyst", "dividend", "board", "audit", "segment", "listing", "patent"],
    treat="relative Tobin's q", outcome="takeover bid",
    plant_re=r"end-of-quarter share price|own return|low return",
)

N["mtv"] = dict(
    var="mtv_share_08", alt_var="promo_draw", design="shift_share", alt_scope="subset", source="labor",
    study="A researcher studies whether watching the MTV reality show 16 and Pregnant lowered teen births, using 206 "
          "U.S. television media markets, quarterly from 2008 to 2010. Treatment: ratings of the show in the market, in "
          "viewers per 100 teens. Outcome: births per 1,000 women aged 15 to 19 in the market, nine months later.",
    named="A researcher studies whether watching 16 and Pregnant lowered teen births, using pre-show MTV viewership as "
          "in Kearney and Levine (AER 2015). Treatment: ratings of the show. Outcome: teen birth rates.",
    cite="Kearney and Levine (2015), AER 105(12): 3597-3632, doi:10.1257/aer.20140012",
    channel_cite="Jaeger, Joyce and Kaestner (2020), Journal of Business and Economic Statistics 38(2): 317-326, "
                 "doi:10.1080/07350015.2018.1497510",
    base="mtv_share_08: the market's MTV viewership share in 2008, before the show first aired in June 2009, multiplied "
         "by an indicator for quarters after June 2009. Analyses include market and quarter fixed effects. Markets with "
         "a 1-point higher 2008 MTV share have show ratings 0.2 points higher.",
    implied="Census and labor-force tables show that the markets with high 2008 MTV viewership had larger Black and "
            "Hispanic population shares and larger rises in unemployment during the 2008-2010 recession, and teen "
            "birth rates in these groups were already falling faster before the show aired.",
    consequence="Population composition and the recession can change teen birth rates whatever the show's ratings.",
    link1="Markets with a 2008 MTV share above the national median are listed as high-MTV markets in the network's "
          "market planning file.",
    link2="Census and labor-force tables show that the high-MTV markets in the network's market planning file had larger "
          "Black and Hispanic population shares and larger rises in unemployment during the 2008-2010 recession, and "
          "teen birth rates in these groups were already falling faster before the show aired.",
    bridge="market planning file",
    memo="Program memo (network research office, 2011): Ratings come from household meters in each media market. Birth "
         "counts come from vital statistics and are assigned to markets by county of residence.",
    others=["tv_households: television households in the market.",
            "cable_share: share of households with cable or satellite service.",
            "internet_share: share of households with home internet.",
            "abortion_providers: abortion providers per 100,000 women.",
            "state: state code of the market's largest county.",
            "quarter: calendar quarter."],
    alt="promo_draw: among the 24 markets of one regional cable system, 1 if the market was drawn in the system's 2009 "
        "random draw that gave the show's premiere free promotional airtime on all the system's channels, 0 otherwise; "
        "missing for all other markets. Drawn markets have show ratings 0.1 points higher on average, with a "
        "first-stage F-statistic of about 2. The draw changed nothing else in drawn markets.",
    unit="market-quarter", topics=["ratings", "channel", "advertising", "program", "household", "device", "time slot", "audience"],
    treat="show ratings", outcome="teen birth rate",
    plant_re=r"Hispanic|\bBlack\b|unemployment",
)

N["rural_banks"] = dict(
    var="post77_x_fin61", alt_var="fee_draw", design="policy_break", alt_scope="subset", source="development",
    study="A researcher studies whether opening bank branches in rural areas reduced rural poverty, using 16 major "
          "Indian states from 1961 to 2000. Treatment: bank branches opened in rural locations that had no bank, per "
          "100,000 people. Outcome: the share of the rural population below the poverty line.",
    named="A researcher studies whether rural bank branches reduced rural poverty in India, using the 1977 branch "
          "licensing rule as in Burgess and Pande (AER 2005). Treatment: rural branches in unbanked locations. "
          "Outcome: rural poverty.",
    cite="Burgess and Pande (2005), AER 95(3): 780-795, doi:10.1257/0002828054201242",
    channel_cite="Buliskeria and Baxa (2022), Journal of Applied Econometrics 37(6): 1266-1274, doi:10.1002/jae.2922",
    base="post77_x_fin61: the state's bank branches per person in 1961 multiplied by the number of years since 1977, for "
         "1977-1989. From 1977 to 1990 a licensing rule required banks to open four branches in unbanked locations for "
         "each branch opened in a location that already had one. Analyses include state and year fixed effects. States "
         "with fewer branches per person in 1961 opened 2.1 more rural branches per 100,000 people per decade after "
         "1977.",
    implied="Planning commission records show that national rural anti-poverty programs launched in 1978-1980 directed "
            "more spending per person to the states that had fewer bank branches per person in 1961.",
    consequence="Anti-poverty spending can change rural poverty whatever the number of bank branches.",
    link1="States in the bottom half of 1961 bank branches per person are listed as lagging states in the 1977 banking "
          "survey.",
    link2="Planning commission records show that national rural anti-poverty programs launched in 1978-1980 directed "
          "more spending per person to the lagging states in the 1977 banking survey.",
    bridge="1977 banking survey",
    memo="Program memo (central bank statistics office, 2001): Branch counts come from the central bank's branch "
         "register. Poverty shares come from national household consumption surveys, interpolated between survey "
         "rounds.",
    others=["rural_pop: rural population in millions.",
            "state_income: state income per person, in 1961 rupees.",
            "literacy: literacy rate.",
            "land_ineq: land ownership inequality index.",
            "state: state code.",
            "year: calendar year."],
    alt="fee_draw: among state-years from 1982 to 1990, 1 if the state was drawn in the central bank's 1981 random draw "
        "that chose 8 of the 16 states for a waiver of branch licensing fees in unbanked rural locations, 0 otherwise; "
        "missing for all earlier state-years. Drawn states opened 0.2 more rural branches per 100,000 people on "
        "average, with a first-stage F-statistic of about 2. The waiver changed nothing else in drawn states.",
    unit="state-year", topics=["credit", "deposit", "agriculture", "wage", "consumption", "price", "rainfall", "election"],
    treat="rural bank branches", outcome="rural poverty",
    plant_re=r"anti-poverty",
)

N["aid_growth"] = dict(
    var="aid_hat", alt_var="ida_draw", design="constructed", alt_scope="subset", source="development",
    study="A researcher studies whether foreign aid raises economic growth, using 76 aid-receiving countries over "
          "1960-2000. Treatment: aid received as a share of GDP, averaged over the period. Outcome: average annual "
          "growth of GDP per person.",
    named="A researcher studies whether foreign aid raises growth, using the constructed aid instrument of Rajan and "
          "Subramanian (REStat 2008). Treatment: aid as a share of GDP. Outcome: growth of GDP per person.",
    cite="Rajan and Subramanian (2008), Review of Economics and Statistics 90(4): 643-665, doi:10.1162/rest.90.4.643",
    channel_cite="Bazzi and Clemens (2013), AEJ: Macroeconomics 5(2): 152-186, doi:10.1257/mac.5.2.152",
    base="aid_hat: aid as a share of GDP predicted from donor-recipient pairs' colonial ties, common language and the "
         "recipient's size relative to the donor. A 1-point higher aid_hat goes with 0.8 points higher actual aid on "
         "average.",
    implied="Trade statistics show that aid_hat is high mainly for countries with small populations, its correlation "
            "with log population is -0.93, and countries with small populations grow differently through their higher "
            "trade openness and narrower export mix.",
    consequence="Country size can change growth whatever the amount of aid.",
    link1="Countries in the top third of aid_hat are listed as high-allocation recipients in the donor coordination "
          "report.",
    link2="Trade statistics show that the high-allocation recipients in the donor coordination report are mostly "
          "countries with small populations, and countries with small populations grow differently through their "
          "higher trade openness and narrower export mix.",
    bridge="donor coordination report",
    memo="Program memo (development data office, 2006): Aid is net official development assistance from donor reports. "
         "GDP per person is in constant international dollars.",
    others=["init_gdp: log GDP per person in 1960.",
            "life_exp: life expectancy at birth in 1960.",
            "inst_quality: institutional quality index.",
            "tropics: share of land area in the tropics.",
            "region: world region.",
            "inflation: average inflation rate."],
    alt="ida_draw: among the 30 countries within 10 percent of the 1987 lending-eligibility income threshold, 1 if the "
        "country was drawn in the lender's random draw that kept 15 of them eligible for concessional loans for five "
        "more years, 0 otherwise; missing for all other countries. Drawn countries received aid 0.3 points of GDP "
        "higher on average, with a first-stage F-statistic of about 2. The draw changed nothing else for drawn "
        "countries.",
    unit="country", topics=["inflation", "debt", "schooling", "investment", "budget", "exchange rate", "election", "health"],
    treat="aid share of GDP", outcome="growth of GDP per person",
    plant_re=r"population|openness|export mix",
)

N["hausman"] = dict(
    var="price_other_cities", alt_var="freight_draw", design="other_markets", alt_scope="subset", source="io",
    study="A researcher studies how strongly the demand for ready-to-eat cereal brands responds to their prices, using "
          "weekly scanner sales of 25 brands in 30 U.S. cities, 1988-1992, summed to quarters. Treatment: the brand's "
          "average price in the city in the quarter. Outcome: log quantity of the brand sold in the city in the "
          "quarter.",
    named="A researcher studies cereal demand, using the same brand's prices in other cities as in Hausman (1996). "
          "Treatment: the brand's price in the city. Outcome: log quantity sold.",
    cite="Hausman (1996), in Bresnahan and Gordon (eds.), The Economics of New Goods, University of Chicago Press, "
         "pp. 207-248",
    channel_cite="Bresnahan (1996), comment in the same volume",
    base="price_other_cities: the brand's average price in the other cities of the same region in the quarter. Analyses "
         "include brand-by-city and quarter fixed effects. A 1 percent higher price in other cities goes with a 0.8 "
         "percent higher price in the city.",
    implied="Marketing records show that each brand's national television advertising campaigns ran in all cities at "
            "the same time, and quarters with a national campaign had both higher brand prices and higher demand in "
            "every city.",
    consequence="National demand shifts can change sales in a city whatever the price there.",
    link1="Quarters in which a brand's price in other cities was above its yearly average are listed as peak quarters "
          "in the manufacturer's pricing calendar.",
    link2="Marketing records show that each brand's national television advertising campaigns ran in all cities during "
          "the peak quarters in the manufacturer's pricing calendar, raising demand for the brand in every city.",
    bridge="manufacturer's pricing calendar",
    memo="Program memo (market research office, 1994): Sales and prices come from store scanners in a sample of "
         "supermarkets in each city. Prices are revenue over units sold, net of coupons.",
    others=["store_count: number of sample stores in the city.",
            "income_city: median household income in the city.",
            "segment: cereal segment (family, kids, adult, health).",
            "firm: manufacturer code.",
            "shelf_share: brand share of cereal shelf space.",
            "city: city code."],
    alt="freight_draw: among the 1991-1992 quarters, 1 if the city's distribution center was drawn in the rail "
        "carrier's 1990 random draw for a freight surcharge on cereal shipments, 0 otherwise; missing for all earlier "
        "quarters. Brands in drawn cities have prices 0.4 percent higher on average, with a first-stage F-statistic of "
        "about 2. The surcharge changed nothing else in drawn cities.",
    unit="brand-city-quarter", topics=["store", "coupon", "display", "package", "shelf", "promotion", "inventory", "sales"],
    treat="brand price", outcome="log quantity sold",
    plant_re=r"advertising|campaign",
)

N["catholic"] = dict(
    var="catholic_relig", alt_var="tuition_draw", design="family_trait", alt_scope="subset", source="education",
    study="A researcher studies whether attending a Catholic high school raises the chance of finishing high school, "
          "using about 12,000 U.S. students first surveyed in 10th grade in 1980 and followed for four years. "
          "Treatment: attended a Catholic high school in 10th grade. Outcome: graduated from high school by 1984.",
    named="A researcher studies whether attending a Catholic high school raises graduation, using Catholic religion as "
          "in Evans and Schwab (QJE 1995). Treatment: Catholic high school attendance. Outcome: high school "
          "graduation.",
    cite="Evans and Schwab (1995), QJE 110(4): 941-974, doi:10.2307/2946645",
    channel_cite="Altonji, Elder and Taber (2005), Journal of Human Resources 40(4): 791-821, doi:10.3368/jhr.XL.4.791",
    base="catholic_relig: 1 if the student's family reports its religion as Catholic, 0 otherwise. Catholic students "
         "are 13 percentage points more likely to attend a Catholic high school.",
    implied="Among students who attended public high schools, Catholic students graduated at higher rates than other "
            "students with the same family background and 10th-grade test scores.",
    consequence="Religious upbringing can change graduation whatever school the student attends.",
    link1="Students with catholic_relig equal to 1 are coded as parish-registered students in the diocese enrollment "
          "file.",
    link2="Among students who attended public high schools, the parish-registered students in the diocese enrollment "
          "file graduated at higher rates than other students with the same family background and 10th-grade test "
          "scores.",
    bridge="diocese enrollment file",
    memo="Program memo (education statistics office, 1986): Students were sampled within schools. Graduation is "
         "confirmed from transcripts where available and from the follow-up survey otherwise.",
    others=["female: 1 if female.",
            "parent_ed: highest grade completed by either parent.",
            "fam_income: family income category in 1980.",
            "test_10: 10th-grade test score.",
            "urban: 1 if the school is in a central city.",
            "region: census region."],
    alt="tuition_draw: among 8th-graders in the 12 cities of a 1978 archdiocese pilot, 1 if the student was drawn in "
        "the pilot's random draw for a Catholic high school tuition voucher, 0 otherwise; missing for all other "
        "students. Drawn students are 2 percentage points more likely to attend a Catholic high school, with a "
        "first-stage F-statistic of about 2. The voucher changed nothing else.",
    unit="student", topics=["course", "homework", "absence", "sport", "job", "aspiration", "teacher", "discipline"],
    treat="Catholic high school attendance", outcome="high school graduation",
    plant_re=r"public high school",
)

N["twins"] = dict(
    var="twin2", alt_var="allowance_draw", design="birth_event", alt_scope="subset", source="labor",
    study="A researcher studies whether growing up in a larger family lowers children's schooling, using about 50,000 "
          "first-born children in families with at least two births, from the Israeli census. Treatment: number of "
          "children in the family. Outcome: the first-born child's years of schooling at age 25.",
    named="A researcher studies whether family size lowers children's schooling, using twin births as in Angrist, Lavy "
          "and Schlosser (Journal of Labor Economics 2010). Treatment: number of children. Outcome: schooling of the "
          "first-born.",
    cite="Angrist, Lavy and Schlosser (2010), Journal of Labor Economics 28(4): 773-824, doi:10.1086/653830",
    channel_cite="Bhalotra and Clarke (2019), Review of Economics and Statistics 101(5): 853-864, "
                 "doi:10.1162/rest_a_00789",
    base="twin2: 1 if the second birth in the family was a twin birth, 0 otherwise. Families with twin2 equal to 1 have "
         "0.6 more children on average.",
    implied="Birth-registry health records show that mothers who had twins at the second birth were taller, smoked less "
            "and received more prenatal care than other mothers, and children of mothers in better health complete "
            "more schooling.",
    consequence="The mother's health can change children's schooling whatever the number of children.",
    link1="Families with twin2 equal to 1 are listed as multiple-birth families in the birth-registry linkage file.",
    link2="Birth-registry health records show that the mothers of the multiple-birth families in the birth-registry "
          "linkage file were taller, smoked less and received more prenatal care than other mothers, and children of "
          "mothers in better health complete more schooling.",
    bridge="birth-registry linkage file",
    memo="Program memo (census bureau, 2003): Children are linked to parents through household rosters. Schooling is "
         "reported in the census and checked against school records for a subsample.",
    others=["female_child: 1 if the first-born is female.",
            "mother_age_first: mother's age at first birth.",
            "mother_ed: mother's years of schooling.",
            "father_ed: father's years of schooling.",
            "ethnicity: parents' ethnic origin group.",
            "birth_year: first-born's year of birth."],
    alt="allowance_draw: among families in the 3 towns of a 1975 pilot, 1 if the family was drawn in the pilot's random "
        "draw for a larger child allowance from the third child on, 0 otherwise; missing for all other families. Drawn "
        "families have 0.03 more children on average, with a first-stage F-statistic of about 2. The allowance changed "
        "nothing else.",
    unit="child", topics=["school", "household", "residence", "language", "military", "employment", "sibling", "marriage"],
    treat="number of children", outcome="first-born's years of schooling",
    plant_re=r"taller|smok|prenatal",
)

N["school_laws"] = dict(
    var="csl_years", alt_var="consol_draw", design="law_change", alt_scope="subset", source="labor",
    study="A researcher studies the earnings return to schooling, using about 600,000 white U.S.-born men born 1905-1949 "
          "from the 1950-1990 censuses. Treatment: years of completed schooling. Outcome: log weekly wage.",
    named="A researcher studies the return to schooling, using state compulsory schooling and child labor laws as in "
          "Acemoglu and Angrist (NBER Macroeconomics Annual 2000). Treatment: years of schooling. Outcome: log weekly "
          "wage.",
    cite="Acemoglu and Angrist (2000), NBER Macroeconomics Annual 15: 9-59, doi:10.1086/654403",
    channel_cite="Stephens and Yang (2014), AER 104(6): 1777-1792, doi:10.1257/aer.104.6.1777",
    base="csl_years: years of schooling required by the compulsory attendance and child labor laws of the man's state "
         "of birth when he was 14. Analyses include state-of-birth and year-of-birth fixed effects. Each additional "
         "required year raises completed schooling by 0.1 year on average.",
    implied="Historical school reports show that the states that raised required schooling also lengthened the school "
            "term, raised teacher pay and lowered pupils per teacher for the same birth cohorts, gains concentrated in "
            "the South.",
    consequence="School quality can change wages whatever the years of schooling completed.",
    link1="Birth cohorts in states whose csl_years rose by at least one year are listed as reform cohorts in the state "
          "education digest.",
    link2="Historical school reports show that the reform cohorts in the state education digest also had longer school "
          "terms, higher teacher pay and fewer pupils per teacher than other cohorts, gains concentrated in the South.",
    bridge="state education digest",
    memo="Program memo (census microdata office, 1995): The samples pool the 1950-1990 public use files. Weekly wage is "
         "annual earnings divided by weeks worked.",
    others=["age: age in the census year.",
            "census_year: census year.",
            "married: 1 if currently married.",
            "urban: 1 if living in an urban area.",
            "birth_state: state of birth.",
            "residence_state: state of residence."],
    alt="consol_draw: among men born in 1940-1945 in the 12 rural counties of one state, 1 if the man's birth county was "
        "drawn in the state's 1946 random draw that gave 6 of these counties a new consolidated high school, 0 "
        "otherwise; missing for all other men. Men from drawn counties complete 0.03 more years of schooling on "
        "average, with a first-stage F-statistic of about 2. The draw changed nothing else in drawn counties.",
    unit="respondent", topics=["employment", "occupation", "industry", "household", "veteran", "migration", "commute", "disability"],
    treat="years of schooling", outcome="log weekly wage",
    plant_re=r"school term|teacher pay|pupils per teacher",
)

N["tax_change"] = dict(
    var="pred_ntr", alt_var="credit_draw", design="simulated_policy", alt_scope="subset", source="public",
    study="A researcher studies how strongly taxable income responds to marginal tax rates, using about 45,000 U.S. "
          "tax returns observed three years apart in a panel, 1979-1990. Treatment: change in the log net-of-tax rate "
          "(one minus the marginal tax rate) over the three years. Outcome: change in log taxable income over the same "
          "three years.",
    named="A researcher studies the elasticity of taxable income, using predicted tax changes as in Gruber and Saez "
          "(Journal of Public Economics 2002). Treatment: change in the log net-of-tax rate. Outcome: change in log "
          "taxable income.",
    cite="Gruber and Saez (2002), Journal of Public Economics 84(1): 1-32, doi:10.1016/S0047-2727(01)00085-8",
    channel_cite="Weber (2014), Journal of Public Economics 117: 90-103, doi:10.1016/j.jpubeco.2014.05.004",
    base="pred_ntr: change in the log net-of-tax rate the return would have had over the three years if its real income "
         "had stayed at the base-year level, computed from the tax schedules. Analyses control for log base-year "
         "income. A 1-point higher pred_ntr goes with a 0.6-point higher actual change.",
    implied="Tax panel studies show that returns with unusually high base-year income relative to the two years before "
            "had lower taxable income growth over the next three years, as transitory income disappeared.",
    consequence="Transitory income in the base year can change later income growth whatever the tax rate.",
    link1="Returns whose base-year income exceeded the average of the two years before by more than 20 percent are "
          "flagged as spike returns in the panel's return-history file.",
    link2="Tax panel studies show that the spike returns in the panel's return-history file had lower taxable income "
          "growth over the next three years than other returns, as transitory income disappeared.",
    bridge="return-history file",
    memo="Program memo (tax statistics office, 1993): The panel follows a stratified random sample of returns. Taxable "
         "income is defined consistently across the tax law changes of 1981 and 1986.",
    others=["married: 1 if filing jointly.",
            "dependents: number of dependents.",
            "age: age of the primary filer.",
            "itemizer: 1 if the return itemizes deductions.",
            "state: state of residence.",
            "base_year: base year of the three-year pair."],
    alt="credit_draw: among returns in one state's 1985-1987 pilot, 1 if the return was drawn in the state's random "
        "draw for a temporary credit that lowered its marginal tax rate, 0 otherwise; missing for all other returns. "
        "Drawn returns have net-of-tax rate changes 0.5 percent higher on average, with a first-stage F-statistic of "
        "about 2. The credit changed nothing else.",
    unit="return", topics=["deduction", "wage", "dividend", "capital gain", "business", "pension", "charity", "mortgage"],
    treat="change in the log net-of-tax rate", outcome="change in log taxable income",
    plant_re=r"transitory|unusually high base-year",
)

N["trade_geo"] = dict(
    var="geo_trade", alt_var="customs_draw", design="geography", alt_scope="subset", source="development",
    study="A researcher studies whether trade raises income, using 150 countries in 1985. Treatment: exports plus "
          "imports as a share of GDP. Outcome: log income per person.",
    named="A researcher studies whether trade raises income, using geography-predicted trade as in Frankel and Romer "
          "(AER 1999). Treatment: trade share of GDP. Outcome: log income per person.",
    cite="Frankel and Romer (1999), AER 89(3): 379-399, doi:10.1257/aer.89.3.379",
    channel_cite="Rodriguez and Rodrik (2000), NBER Macroeconomics Annual 15: 261-325, doi:10.1086/654419",
    base="geo_trade: trade share predicted from a gravity model of bilateral trade using distance between countries, "
         "land area, common borders and whether the country has a coastline. A 10-point higher geo_trade goes with a "
         "9-point higher actual trade share on average.",
    implied="Geographic data show that the countries with high geo_trade lie farther from the equator, where malaria and "
            "other tropical diseases are rare, and disease burdens change income through workers' health.",
    consequence="Health and climate can change income whatever the trade share.",
    link1="Countries with geo_trade above the median are listed as well-connected countries in the geographic atlas.",
    link2="Geographic data show that the well-connected countries in the geographic atlas lie farther from the equator, "
          "where malaria and other tropical diseases are rare, and disease burdens change income through workers' "
          "health.",
    bridge="geographic atlas",
    memo="Program memo (international data office, 1990): Trade and GDP come from national accounts in current prices. "
         "Income per person is in purchasing-power-parity dollars.",
    others=["population: log population.",
            "land_area: log land area.",
            "landlocked: 1 if the country has no coastline.",
            "region: world region.",
            "colony: 1 if a former colony.",
            "language: main official language group."],
    alt="customs_draw: among the 20 countries of a 1980 regional customs pilot, 1 if the country was drawn in the "
        "pilot's random draw that cut its border processing fees by half, 0 otherwise; missing for all other countries. "
        "Drawn countries have trade shares 1 point higher on average, with a first-stage F-statistic of about 2. The "
        "draw changed nothing else.",
    unit="country", topics=["inflation", "schooling", "investment", "budget", "exchange rate", "election", "debt", "telephone"],
    treat="trade share", outcome="log income per person",
    plant_re=r"malaria|tropical disease|equator",
)

N["bartik"] = dict(
    var="bartik", alt_var="plant_draw", design="shift_share", alt_scope="subset", source="labor",
    study="A researcher studies how much local wages rise when local labor demand grows, using 722 U.S. commuting zones "
          "over the decades 1980-1990 and 1990-2000. Treatment: growth of employment in the zone over the decade. "
          "Outcome: growth of the zone's average weekly wage over the decade.",
    named="A researcher studies the local labor supply elasticity, using a Bartik instrument as in Bartik (1991) and "
          "Goldsmith-Pinkham, Sorkin and Swift (AER 2020). Treatment: local employment growth. Outcome: local wage "
          "growth.",
    cite="Bartik (1991), Who Benefits from State and Local Economic Development Policies?, W.E. Upjohn Institute, "
         "doi:10.17848/9780585223940",
    channel_cite="Goldsmith-Pinkham, Sorkin and Swift (2020), AER 110(8): 2586-2624, doi:10.1257/aer.20181047",
    base="bartik: the zone's 1980 employment shares by industry multiplied by national employment growth of each "
         "industry over the decade, excluding the zone. Analyses include zone and decade fixed effects. A 1-point "
         "higher bartik goes with 1.1 points higher employment growth on average.",
    implied="Census tables show that the zones with large 1980 shares in oil and gas extraction and the other industries "
            "that drive most of the predicted growth also had large and rising shares of immigrant workers, and "
            "immigrant inflows change local wages through labor supply.",
    consequence="Labor supply from immigration can change wages whatever the growth of labor demand.",
    link1="Zones in the top fifth of bartik are listed as high-exposure zones in the regional industry report.",
    link2="Census tables show that the high-exposure zones in the regional industry report had large and rising shares "
          "of immigrant workers, and immigrant inflows change local wages through labor supply.",
    bridge="regional industry report",
    memo="Program memo (census microdata office, 2004): Employment and wages come from the decennial census samples "
         "aggregated to commuting zones. Industry codes are harmonized across census years.",
    others=["pop_1980: log population of the zone in 1980.",
            "college_share: share of adults with a college degree in 1980.",
            "female_lfp: female labor force participation in 1980.",
            "manuf_share: manufacturing employment share in 1980.",
            "state: state of the zone's largest county.",
            "decade: decade of the change."],
    alt="plant_draw: among the 30 zones that bid in a 1985 federal random draw for 15 defense plants, 1 if the zone was "
        "drawn to receive a plant, 0 otherwise; missing for all other zones. Drawn zones have employment growth 0.3 "
        "points higher on average, with a first-stage F-statistic of about 2. The plant changed nothing else in drawn "
        "zones.",
    unit="zone-decade", topics=["housing", "commute", "establishment", "payroll", "rent", "school", "construction", "retail"],
    treat="employment growth", outcome="wage growth",
    plant_re=r"immigra|oil and gas",
)

ORDER = list(N)
CITES = {"saiz": (991, 131), "flow_pressure": (616, 75), "mtv": (291, 49), "rural_banks": (1320, 1), "aid_growth": (1566, 553),
         "hausman": (0, 0), "catholic": (798, 448), "twins": (605, 58), "school_laws": (481, 255), "tax_change": (612, 165),
         "trade_geo": (6323, 2093), "bartik": (0, 2459)}
for _k, (_a, _b) in CITES.items():
    N[_k]["famous"] = max(_a, _b) >= N1.FAMOUS_THRESHOLD
N["hausman"]["famous"] = True


@contextmanager
def registered(key):
    had = key in V.S
    old = V.S.get(key)
    V.S[key] = N[key]
    try:
        yield
    finally:
        if had:
            V.S[key] = old
        else:
            del V.S[key]


def agent_parts(key, version, arm="neutral", threat=True):
    with registered(key):
        return V.agent_parts(key, version, arm, threat)


def answer_key(key, version):
    with registered(key):
        return V.answer_key(key, version)


def parse_pick(key, t):
    with registered(key):
        return V.parse_pick(key, t)


def named_plant(key, t):
    with registered(key):
        return V.named_plant(key, t)


def outcome(key, version, t, fix_valid=False):
    with registered(key):
        return V.outcome(key, version, t, fix_valid=fix_valid)


prose = V.prose


def check():
    names = {s["var"] for s in V.S.values()} | {s["alt_var"] for s in V.S.values()}
    names |= {s["var"] for s in N1.N.values()} | {s["alt_var"] for s in N1.N.values()}
    for k, s in N.items():
        for f, typ in FIELDS.items():
            assert f in s and isinstance(s[f], typ), (k, f)
        assert len(s["others"]) == 6 and all(":" in o for o in s["others"]), k
        assert s["base"].startswith(s["var"] + ":") and s["alt"].startswith(s["alt_var"] + ":"), k
        assert "among" in s["alt"] and "missing" in s["alt"] and "F-statistic of about 2" in s["alt"], k
        assert not V.GENERIC.search(s["plant_re"]), k
        pr = re.compile(s["plant_re"], re.I)
        for fld in ("implied", "link2"):
            assert pr.search(s[fld]), (k, fld)
        for txt in [s["base"], s["alt"], s["memo"], s["study"], s["named"], s["link1"]] + s["others"]:
            assert not pr.search(txt), (k, "plant in clean text", txt[:70])
        assert s["bridge"] in s["link1"] and s["bridge"] in s["link2"], k
        assert s["var"] not in s["link2"], k
        for fld in ("implied", "link1", "link2", "consequence"):
            assert s["alt_var"] not in s[fld], (k, fld)
        for nm in (s["var"], s["alt_var"]):
            assert nm not in names, (k, nm)
            names.add(nm)
        for v in VERSIONS:
            p, m, t = agent_parts(k, v)
            assert s["var"] in m and s["alt"] in p + m, (k, v)
            if v == "silent":
                assert not pr.search(p + m), (k, "silent prompt contains the plant")
            if v == "chain":
                assert s["link1"] in m and s["link2"] in m and not pr.search(s["base"] + " " + s["link1"]), k
        assert agent_parts(k, "implied")[0] == agent_parts(k, "silent")[0], (k, "cache prefix")
    return True


if __name__ == "__main__":
    print(check(), len(N), "cases;", sum(s["famous"] for s in N.values()), "famous")
