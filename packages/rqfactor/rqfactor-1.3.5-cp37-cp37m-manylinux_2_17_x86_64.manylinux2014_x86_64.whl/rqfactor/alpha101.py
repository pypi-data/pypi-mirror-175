from . import *


__all__ = [
    'ALPHA_',
    'ALPHAS'
]


''' input data '''

# standard definitions for daily price and volume data
# - type : <class 'pandas.core.frame.DataFrame'>
# - columns
#   example : <class 'str'>
#   type : 300024.XSHE
# - index
#   type : <class 'pandas.tslib.Timestamp'>
#   example : 2017-02-03 00:00:00
# - value type :
#   type( x['300024.XSHE']['2017-02-03'] ) == numpy.float64

OPEN = Pricing.open
CLOSE = Pricing.close
LOW = Pricing.low
HIGH = Pricing.high
VOLUME = Pricing.volume
RETURNS = (CLOSE - REF(CLOSE, 1)) / REF(CLOSE, 1)
CAP = Fundamentals.market_cap
VWAP = Pricing.total_turnover / Pricing.volume


def ADV(n):
    return MA(VOLUME, n)


''' functions and operators '''

# MIN(x, y) = Parallel minimum of vectors x and y
# MAX(x, y) = Parallel maximum of vectors x and y

# RANK(x) = cross-sectional rank
# DELAY(x, n) = value of x n days ago
# DELTA(x, n) = today’s value of x minus the value of x n days ago

# SUM(x, n) = time-series sum over the past n days
# PRODUCT(x, n) = time-series product over the past n days

# TS_MIN(x, n) = time-series min over the past n days
# TS_MAX(x, n) = time-series max over the past n days
# TS_ARGMAX(x, n) = which day ts_max(x, n) occurred on
# TS_ARGMIN(x, n) = which day ts_min(x, n) occurred on
# TS_RANK(x, n) =  time-series rank in the past n days

# COVARIANCE(a, b, n) = time-serial covariance of a and b for the past n days
# CORRELATION(a, b, n) =  time-serial correlation of a and b for the past n days
# STDDEV(x, n) =  moving time-series standard deviation over the past n days
# SCALE(x, a) = cross sectional rescale, default to 1

# DECAY_LINEAR(x, n) =
#   weighted moving average over the past n days
#   with linearly decaying weights n, n – 1, ..., 1
#   (rescaled to sum up to 1)

# INDNEUTRALIZE(x, g) =
#   x cross-sectionally neutralized against groups g
#   (subindustries, industries, sectors, etc.)
#   i.e., x is cross-sectionally demeaned within each group g
# INDCLASS = a generic placeholder for a binary industry classification
#   such as GICS, BICS, NAICS, SIC, etc.,
#   in indneutralize(x, INDCLASS.level),
#   where level = sector, industry, subindustry, etc.
#   Multiple INDCLASS in the same alpha need not correspond to the same industry classification.

# INDUSTRY_NEUTRALIZE(x) = simplified INDNEUTRALIZE(x, g)

# note about the use of INDUSTRY_NEUTRALIZE(x) :
#   in original alpha101,
#   instead of simple INDUSTRY_NEUTRALIZE(x)
#   INDNEUTRALIZE(x, g) is used,
#
#      where g denotes <GROUP-LEVEL> :
#        <GROUP-LEVEL> = <INDCLASS>.<LEVEL>
#        <INDCLASS> = GICS
#                   | BICS
#                   | NAICS
#                   | SIC
#                   | etc.
#        <LEVEL> = SECTOR | INDUSTRY | SUBINDUSTRY
#
#   if data are available, we might change <INDCLASS> to :
#        <INDCLASS> = SHENWAN
#                   | etc.
#
#   for now, we simply use INDUSTRY_NEUTRALIZE(x)
#   which is equal to INDNEUTRALIZE(x, SHENWAN.INDUSTRY)


''' alphas '''


def ALPHA_(n):
    g = globals()
    alpha_name = 'alpha{:03}'.format(n)
    if alpha_name in g:
        return g[alpha_name]
    else:
        return None


def ALPHAS():
    g = globals()
    results = {}
    for key, value in g.items():
        if key == 'ALPHA_' or key == 'ALPHAS':
            continue

        if 'alpha' in key:
            results['WorldQuant_{}'.format(key)] = value

    return results


alpha001 = (RANK(TS_ARGMAX(SIGNEDPOWER(IF((RETURNS < 0), STDDEV(RETURNS, 20), CLOSE), 2.), 5)) - 0.5)

alpha002 = (-1 * CORRELATION(RANK(DELTA(LOG(VOLUME), 2)), RANK(((CLOSE - OPEN) / OPEN)), 6))

alpha003 = (-1 * CORRELATION(RANK(OPEN), RANK(VOLUME), 10))

alpha004 = (-1 * TS_RANK(RANK(LOW), 9))

alpha005 = (RANK((OPEN - (SUM(VWAP, 10) / 10))) * (-1 * ABS(RANK((CLOSE - VWAP)))))

alpha006 = (-1 * CORRELATION(OPEN, VOLUME, 10))

alpha007 = IF((ADV(20) < VOLUME), ((-1 * TS_RANK(ABS(DELTA(CLOSE, 7)), 60)) * SIGN(DELTA(CLOSE, 7))), (-1 * 1))

alpha008 = (-1 * RANK(((SUM(OPEN, 5) * SUM(RETURNS, 5)) - DELAY((SUM(OPEN, 5) * SUM(RETURNS, 5)), 10))))

alpha009 = IF((0 < TS_MIN(DELTA(CLOSE, 1), 5)), DELTA(CLOSE, 1), (IF((TS_MAX(DELTA(CLOSE, 1), 5) < 0), DELTA(CLOSE, 1), (-1 * DELTA(CLOSE, 1)))))

alpha010 = RANK(IF((0 < TS_MIN(DELTA(CLOSE, 1), 4)), DELTA(CLOSE, 1), IF((TS_MAX(DELTA(CLOSE, 1), 4) < 0), DELTA(CLOSE, 1), (-1 * DELTA(CLOSE, 1)))))

alpha011 = ((RANK(TS_MAX((VWAP - CLOSE), 3)) + RANK(TS_MIN((VWAP - CLOSE), 3))) * RANK(DELTA(VOLUME, 3)))

alpha012 = (SIGN(DELTA(VOLUME, 1)) * (-1 * DELTA(CLOSE, 1)))

alpha013 = (-1 * RANK(COVARIANCE(RANK(CLOSE), RANK(VOLUME), 5)))

alpha014 = ((-1 * RANK(DELTA(RETURNS, 3))) * CORRELATION(OPEN, VOLUME, 10))

alpha015 = (-1 * SUM(RANK(CORRELATION(RANK(HIGH), RANK(VOLUME), 3)), 3))

alpha016 = (-1 * RANK(COVARIANCE(RANK(HIGH), RANK(VOLUME), 5)))

alpha017 = (((-1 * RANK(TS_RANK(CLOSE, 10))) * RANK(DELTA(DELTA(CLOSE, 1), 1))) * RANK(TS_RANK((VOLUME / ADV(20)), 5)))

alpha018 = (-1 * RANK(((STDDEV(ABS((CLOSE - OPEN)), 5) + (CLOSE - OPEN)) + CORRELATION(CLOSE, OPEN, 10))))

alpha019 = ((-1 * SIGN(((CLOSE - DELAY(CLOSE, 7)) + DELTA(CLOSE, 7)))) * (1 + RANK((1 + SUM(RETURNS, 250)))))

alpha020 = (((-1 * RANK((OPEN - DELAY(HIGH, 1)))) * RANK((OPEN - DELAY(CLOSE, 1)))) * RANK((OPEN - DELAY(LOW, 1))))

alpha021 = IF((((SUM(CLOSE, 8) / 8) + STDDEV(CLOSE, 8)) < (SUM(CLOSE, 2) / 2)), (-1 * 1), IF(((SUM(CLOSE, 2) / 2) < ((SUM(CLOSE, 8) / 8) - STDDEV(CLOSE, 8))), 1, IF(((1 < (VOLUME / ADV(20))) | ((VOLUME / ADV(20)) == 1)), 1, (-1 * 1))))

alpha022 = (-1 * (DELTA(CORRELATION(HIGH, VOLUME, 5), 5) * RANK(STDDEV(CLOSE, 20))))

alpha023 = IF(((SUM(HIGH, 20) / 20) < HIGH), (-1 * DELTA(HIGH, 2)), 0)

alpha024 = IF((((DELTA((SUM(CLOSE, 100) / 100), 100) / DELAY(CLOSE, 100)) < 0.05) | ((DELTA((SUM(CLOSE, 100) / 100), 100) / DELAY(CLOSE, 100)) == 0.05)), (-1 * (CLOSE - TS_MIN(CLOSE, 100))), (-1 * DELTA(CLOSE, 3)))

alpha025 = RANK(((((-1 * RETURNS) * ADV(20)) * VWAP) * (HIGH - CLOSE)))

alpha026 = (-1 * TS_MAX(CORRELATION(TS_RANK(VOLUME, 5), TS_RANK(HIGH, 5), 5), 3))

alpha027 = IF((0.5 < RANK((SUM(CORRELATION(RANK(VOLUME), RANK(VWAP), 6), 2) / 2.0))), (-1 * 1), 1)

alpha028 = SCALE(((CORRELATION(ADV(20), LOW, 5) + ((HIGH + LOW) / 2)) - CLOSE))

alpha029 = (MIN(PRODUCT(RANK(RANK(SCALE(LOG(SUM(TS_MIN(RANK(RANK((-1 * RANK(DELTA((CLOSE - 1), 5))))), 2), 1))))), 1), 5) + TS_RANK(DELAY((-1 * RETURNS), 6), 5))

alpha030 = (((1.0 - RANK(((SIGN((CLOSE - DELAY(CLOSE, 1))) + SIGN((DELAY(CLOSE, 1) - DELAY(CLOSE, 2)))) + SIGN((DELAY(CLOSE, 2) - DELAY(CLOSE, 3)))))) * SUM(VOLUME, 5)) / SUM(VOLUME, 20))

alpha031 = ((RANK(RANK(RANK(DECAY_LINEAR((-1 * RANK(RANK(DELTA(CLOSE, 10)))), 10)))) + RANK((-1 * DELTA(CLOSE, 3)))) + SIGN(SCALE(CORRELATION(ADV(20), LOW, 12))))

alpha032 = (SCALE(((SUM(CLOSE, 7) / 7) - CLOSE)) + (20 * SCALE(CORRELATION(VWAP, DELAY(CLOSE, 5), 230))))

alpha033 = RANK((-1 * ((1 - (OPEN / CLOSE))**1)))

alpha034 = RANK(((1 - RANK((STDDEV(RETURNS, 2) / STDDEV(RETURNS, 5)))) + (1 - RANK(DELTA(CLOSE, 1)))))

alpha035 = ((TS_RANK(VOLUME, 32) * (1 - TS_RANK(((CLOSE + HIGH) - LOW), 16))) * (1 - TS_RANK(RETURNS, 32)))

alpha036 = (((((2.21 * RANK(CORRELATION((CLOSE - OPEN), DELAY(VOLUME, 1), 15))) + (0.7 * RANK((OPEN - CLOSE)))) + (0.73 * RANK(TS_RANK(DELAY((-1 * RETURNS), 6), 5)))) + RANK(ABS(CORRELATION(VWAP, ADV(20), 6)))) + (0.6 * RANK((((SUM(CLOSE, 200) / 200) - OPEN) * (CLOSE - OPEN)))))

alpha037 = (RANK(CORRELATION(DELAY((OPEN - CLOSE), 1), CLOSE, 200)) + RANK((OPEN - CLOSE)))

alpha038 = ((-1 * RANK(TS_RANK(CLOSE, 10))) * RANK((CLOSE / OPEN)))

alpha039 = ((-1 * RANK((DELTA(CLOSE, 7) * (1 - RANK(DECAY_LINEAR((VOLUME / ADV(20)), 9)))))) * (1 + RANK(SUM(RETURNS, 250))))

alpha040 = ((-1 * RANK(STDDEV(HIGH, 10))) * CORRELATION(HIGH, VOLUME, 10))

alpha041 = (((HIGH * LOW)**0.5) - VWAP)

alpha042 = (RANK((VWAP - CLOSE)) / RANK((VWAP + CLOSE)))

alpha043 = (TS_RANK((VOLUME / ADV(20)), 20) * TS_RANK((-1 * DELTA(CLOSE, 7)), 8))

alpha044 = (-1 * CORRELATION(HIGH, RANK(VOLUME), 5))

alpha045 = (-1 * ((RANK((SUM(DELAY(CLOSE, 5), 20) / 20)) * CORRELATION(CLOSE, VOLUME, 2)) * RANK(CORRELATION(SUM(CLOSE, 5), SUM(CLOSE, 20), 2))))

alpha046 = IF((0.25 < (((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10))), (-1 * 1), IF(((((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10)) < 0), 1, ((-1 * 1) * (CLOSE - DELAY(CLOSE, 1)))))

alpha047 = ((((RANK((1 / CLOSE)) * VOLUME) / ADV(20)) * ((HIGH * RANK((HIGH - CLOSE))) / (SUM(HIGH, 5) / 5))) - RANK((VWAP - DELAY(VWAP, 5))))

alpha048 = (INDUSTRY_NEUTRALIZE(((CORRELATION(DELTA(CLOSE, 1), DELTA(DELAY(CLOSE, 1), 1), 250) * DELTA(CLOSE, 1)) / CLOSE)) / SUM(((DELTA(CLOSE, 1) / DELAY(CLOSE, 1))**2), 250))

alpha049 = IF(((((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10)) < (-1 * 0.1)), 1, ((-1 * 1) * (CLOSE - DELAY(CLOSE, 1))))

alpha050 = (-1 * TS_MAX(RANK(CORRELATION(RANK(VOLUME), RANK(VWAP), 5)), 5))

alpha051 = IF(((((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10)) < (-1 * 0.05)), 1, ((-1 * 1) * (CLOSE - DELAY(CLOSE, 1))))

alpha052 = ((((-1 * TS_MIN(LOW, 5)) + DELAY(TS_MIN(LOW, 5), 5)) * RANK(((SUM(RETURNS, 240) - SUM(RETURNS, 20)) / 220))) * TS_RANK(VOLUME, 5))

alpha053 = (-1 * DELTA((((CLOSE - LOW) - (HIGH - CLOSE)) / (CLOSE - LOW)), 9))

alpha054 = ((-1 * ((LOW - CLOSE) * (OPEN**5))) / ((LOW - HIGH) * (CLOSE**5)))

alpha055 = (-1 * CORRELATION(RANK(((CLOSE - TS_MIN(LOW, 12)) / (TS_MAX(HIGH, 12) - TS_MIN(LOW, 12)))), RANK(VOLUME), 6))

alpha056 = (0 - (1 * (RANK((SUM(RETURNS, 10) / SUM(SUM(RETURNS, 2), 3))) * RANK((RETURNS * CAP)))))

alpha057 = (0 - (1 * ((CLOSE - VWAP) / DECAY_LINEAR(RANK(TS_ARGMAX(CLOSE, 30)), 2))))

alpha058 = (-1 * TS_RANK(DECAY_LINEAR(CORRELATION(INDUSTRY_NEUTRALIZE(VWAP), VOLUME, 4), 8), 6))

alpha059 = (-1 * TS_RANK(DECAY_LINEAR(CORRELATION(INDUSTRY_NEUTRALIZE(((VWAP * 0.728317) + (VWAP * (1 - 0.728317)))), VOLUME, 4), 16), 8))

alpha060 = (0 - (1 * ((2 * SCALE(RANK(((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME)))) - SCALE(RANK(TS_ARGMAX(CLOSE, 10))))))

alpha061 = (RANK((VWAP - TS_MIN(VWAP, 16))) < RANK(CORRELATION(VWAP, ADV(180), 18)))

alpha062 = ((RANK(CORRELATION(VWAP, SUM(ADV(20), 22), 10)) < RANK(((RANK(OPEN) + RANK(OPEN)) < (RANK(((HIGH + LOW) / 2)) + RANK(HIGH))))) * -1)

alpha063 = ((RANK(DECAY_LINEAR(DELTA(INDUSTRY_NEUTRALIZE(CLOSE), 2), 8)) - RANK(DECAY_LINEAR(CORRELATION(((VWAP * 0.318108) + (OPEN * (1 - 0.318108))), SUM(ADV(180), 37), 14), 12))) * -1)

alpha064 = ((RANK(CORRELATION(SUM(((OPEN * 0.178404) + (LOW * (1 - 0.178404))), 13), SUM(ADV(120), 13), 17)) < RANK(DELTA(((((HIGH + LOW) / 2) * 0.178404) + (VWAP * (1 - 0.178404))), 4))) * -1)

alpha065 = ((RANK(CORRELATION(((OPEN * 0.00817205) + (VWAP * (1 - 0.00817205))), SUM(ADV(60), 9), 6)) < RANK((OPEN - TS_MIN(OPEN, 14)))) * -1)

alpha066 = ((RANK(DECAY_LINEAR(DELTA(VWAP, 4), 7)) + TS_RANK(DECAY_LINEAR(((((LOW * 0.96633) + (LOW * (1 - 0.96633))) - VWAP) / (OPEN - ((HIGH + LOW) / 2))), 11), 7)) * -1)

alpha067 = ((RANK((HIGH - TS_MIN(HIGH, 2)))**RANK(CORRELATION(INDUSTRY_NEUTRALIZE(VWAP), INDUSTRY_NEUTRALIZE(ADV(20)), 6))) * -1)

alpha068 = ((TS_RANK(CORRELATION(RANK(HIGH), RANK(ADV(15)), 9), 14) < RANK(DELTA(((CLOSE * 0.518371) + (LOW * (1 - 0.518371))), 1))) * -1)

alpha069 = ((RANK(TS_MAX(DELTA(INDUSTRY_NEUTRALIZE(VWAP), 3), 5))**TS_RANK(CORRELATION(((CLOSE * 0.490655) + (VWAP * (1 - 0.490655))), ADV(20), 5), 9)) * -1)

alpha070 = ((RANK(DELTA(VWAP, 1))**TS_RANK(CORRELATION(INDUSTRY_NEUTRALIZE(CLOSE), ADV(50), 18), 18)) * -1)

alpha071 = MAX(TS_RANK(DECAY_LINEAR(CORRELATION(TS_RANK(CLOSE, 3), TS_RANK(ADV(180), 12), 18), 4), 16), TS_RANK(DECAY_LINEAR((RANK(((LOW + OPEN) - (VWAP + VWAP)))**2), 16), 4))

alpha072 = (RANK(DECAY_LINEAR(CORRELATION(((HIGH + LOW) / 2), ADV(40), 9), 10)) / RANK(DECAY_LINEAR(CORRELATION(TS_RANK(VWAP, 4), TS_RANK(VOLUME, 19), 7), 3)))

# Modify DELTA(VWAP, 4.72775) to DELTA(VWAP, 5)
alpha073 = (MAX(RANK(DECAY_LINEAR(DELTA(VWAP, 5), 3)), TS_RANK(DECAY_LINEAR(((DELTA(((OPEN * 0.147155) + (LOW * (1 - 0.147155))), 2) / ((OPEN * 0.147155) + (LOW * (1 - 0.147155)))) * -1), 3), 17)) * -1)

alpha074 = ((RANK(CORRELATION(CLOSE, SUM(ADV(30), 37), 15)) < RANK(CORRELATION(RANK(((HIGH * 0.0261661) + (VWAP * (1 - 0.0261661)))), RANK(VOLUME), 11))) * -1)

alpha075 = (RANK(CORRELATION(VWAP, VOLUME, 4)) < RANK(CORRELATION(RANK(LOW), RANK(ADV(50)), 12)))

# Modify TS_RANK(CORRELATION(INDUSTRY_NEUTRALIZE(LOW), ADV(81), 8), 19.569) to TS_RANK(CORRELATION(INDUSTRY_NEUTRALIZE(LOW), ADV(81), 8), 20)
alpha076 = (MAX(RANK(DECAY_LINEAR(DELTA(VWAP, 1), 12)), TS_RANK(DECAY_LINEAR(TS_RANK(CORRELATION(INDUSTRY_NEUTRALIZE(LOW), ADV(81), 8), 20), 17), 19)) * -1)

alpha077 = MIN(RANK(DECAY_LINEAR(((((HIGH + LOW) / 2) + HIGH) - (VWAP + HIGH)), 20)), RANK(DECAY_LINEAR(CORRELATION(((HIGH + LOW) / 2), ADV(40), 3), 6)))

alpha078 = (RANK(CORRELATION(SUM(((LOW * 0.352233) + (VWAP * (1 - 0.352233))), 20), SUM(ADV(40), 20), 7))**RANK(CORRELATION(RANK(VWAP), RANK(VOLUME), 6)))

alpha079 = (RANK(DELTA(INDUSTRY_NEUTRALIZE(((CLOSE * 0.60733) + (OPEN * (1 - 0.60733)))), 1)) < RANK(CORRELATION(TS_RANK(VWAP, 4), TS_RANK(ADV(150), 9), 15)))

alpha080 = ((RANK(SIGN(DELTA(INDUSTRY_NEUTRALIZE(((OPEN * 0.868128) + (HIGH * (1 - 0.868128)))), 4)))**TS_RANK(CORRELATION(HIGH, ADV(10), 5), 6)) * -1)

alpha081 = ((RANK(LOG(PRODUCT(RANK((RANK(CORRELATION(VWAP, SUM(ADV(10), 50), 8))**4)), 15))) < RANK(CORRELATION(RANK(VWAP), RANK(VOLUME), 5))) * -1)

alpha082 = (MIN(RANK(DECAY_LINEAR(DELTA(OPEN, 1), 15)), TS_RANK(DECAY_LINEAR(CORRELATION(INDUSTRY_NEUTRALIZE(VOLUME), ((OPEN * 0.634196) + (OPEN * (1 - 0.634196))), 17), 7), 13)) * -1)

alpha083 = ((RANK(DELAY(((HIGH - LOW) / (SUM(CLOSE, 5) / 5)), 2)) * RANK(RANK(VOLUME))) / (((HIGH - LOW) / (SUM(CLOSE, 5) / 5)) / (VWAP - CLOSE)))

alpha084 = SIGNEDPOWER(TS_RANK((VWAP - TS_MAX(VWAP, 15)), 21), DELTA(CLOSE, 5))

alpha085 = (RANK(CORRELATION(((HIGH * 0.876703) + (CLOSE * (1 - 0.876703))), ADV(30), 10))**RANK(CORRELATION(TS_RANK(((HIGH + LOW) / 2), 4), TS_RANK(VOLUME, 10), 7)))

alpha086 = ((TS_RANK(CORRELATION(CLOSE, SUM(ADV(20), 15), 6), 20) < RANK(((OPEN + CLOSE) - (VWAP + OPEN)))) * -1)

alpha087 = (MAX(RANK(DECAY_LINEAR(DELTA(((CLOSE * 0.369701) + (VWAP * (1 - 0.369701))), 2), 3)), TS_RANK(DECAY_LINEAR(ABS(CORRELATION(INDUSTRY_NEUTRALIZE(ADV(81)), CLOSE, 13)), 5), 14)) * -1)

# Modify TS_RANK(ADV(60), 20.6966) to TS_RANK(ADV(60), 21),
alpha088 = MIN(RANK(DECAY_LINEAR(((RANK(OPEN) + RANK(LOW)) - (RANK(HIGH) + RANK(CLOSE))), 8)), TS_RANK(DECAY_LINEAR(CORRELATION(TS_RANK(CLOSE, 8), TS_RANK(ADV(60), 21), 8), 7), 3))

alpha089 = (TS_RANK(DECAY_LINEAR(CORRELATION(((LOW * 0.967285) + (LOW * (1 - 0.967285))), ADV(10), 7), 6), 4) - TS_RANK(DECAY_LINEAR(DELTA(INDUSTRY_NEUTRALIZE(VWAP), 3), 10), 15))

alpha090 = ((RANK((CLOSE - TS_MAX(CLOSE, 5)))**TS_RANK(CORRELATION(INDUSTRY_NEUTRALIZE(ADV(40)), LOW, 5), 3)) * -1)

alpha091 = ((TS_RANK(DECAY_LINEAR(DECAY_LINEAR(CORRELATION(INDUSTRY_NEUTRALIZE(CLOSE), VOLUME, 10), 16), 4), 5) - RANK(DECAY_LINEAR(CORRELATION(VWAP, ADV(30), 4), 3))) * -1)

alpha092 = MIN(TS_RANK(DECAY_LINEAR(AS_FLOAT((((HIGH + LOW) / 2) + CLOSE) < (LOW + OPEN)), 15), 19), TS_RANK(DECAY_LINEAR(CORRELATION(RANK(LOW), RANK(ADV(30)), 8), 7), 7))

alpha093 = (TS_RANK(DECAY_LINEAR(CORRELATION(INDUSTRY_NEUTRALIZE(VWAP), ADV(81), 17), 20), 8) / RANK(DECAY_LINEAR(DELTA(((CLOSE * 0.524434) + (VWAP * (1 - 0.524434))), 3), 16)))

alpha094 = ((RANK((VWAP - TS_MIN(VWAP, 12)))**TS_RANK(CORRELATION(TS_RANK(VWAP, 20), TS_RANK(ADV(60), 4), 18), 3)) * -1)

alpha095 = (RANK((OPEN - TS_MIN(OPEN, 12))) < TS_RANK((RANK(CORRELATION(SUM(((HIGH + LOW) / 2), 19), SUM(ADV(40), 19), 13))**5), 12))

# Modify TS_RANK(ADV(60), 4.13242) to TS_RANK(ADV(60), 4)
alpha096 = MAX(TS_RANK(DECAY_LINEAR(CORRELATION(RANK(VWAP), RANK(VOLUME), 4), 4), 8), TS_RANK(DECAY_LINEAR(TS_ARGMAX(CORRELATION(TS_RANK(CLOSE, 7), TS_RANK(ADV(60), 4), 4), 13), 14), 13)) * -1

# Modify TS_RANK(LOW, 7.87871) to TS_RANK(LOW, 8)
alpha097 = ((RANK(DECAY_LINEAR(DELTA(INDUSTRY_NEUTRALIZE(((LOW * 0.721001) + (VWAP * (1 - 0.721001)))), 3), 20)) - TS_RANK(DECAY_LINEAR(TS_RANK(CORRELATION(TS_RANK(LOW, 8), TS_RANK(ADV(60), 17), 5), 19), 16), 7)) * -1)

alpha098 = (RANK(DECAY_LINEAR(CORRELATION(VWAP, SUM(ADV(5), 26), 6), 7)) - RANK(DECAY_LINEAR(TS_RANK(TS_ARGMIN(CORRELATION(RANK(OPEN), RANK(ADV(15)), 21), 9), 7), 8)))

alpha099 = ((RANK(CORRELATION(SUM(((HIGH + LOW) / 2), 20), SUM(ADV(60), 20), 9)) < RANK(CORRELATION(LOW, VOLUME, 6))) * -1)

alpha100 = (0 - (1 * (((1.5 * SCALE(INDUSTRY_NEUTRALIZE(INDUSTRY_NEUTRALIZE(RANK(((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME)))))) - SCALE(INDUSTRY_NEUTRALIZE((CORRELATION(CLOSE, RANK(ADV(20)), 5) - RANK(TS_ARGMIN(CLOSE, 30)))))) * (VOLUME / ADV(20)))))

alpha101 = ((CLOSE - OPEN) / ((HIGH - LOW) + .001))
